"""GUIDE Phần 1 - Dựng tác tử (agent) bằng Deep Agents.   >>> SINH VIÊN CÀI ĐẶT make_backend VÀ build_agent <<<

Pseudo-code: guides/pseudocode/01_agent.md
Kiểm tra:    pytest tests/test_02_agent.py
"""
import os
import sys
import tempfile
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import LocalShellBackend
from httpx import RemoteProtocolError
from langchain.agents.middleware import ModelRetryMiddleware
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_google_genai import ChatGoogleGenerativeAI

from .model import make_model
from .subagents import get_subagents

# ---- CÓ SẴN, KHÔNG SỬA: system prompt dùng chung cho mọi sinh viên (để đường cơ sở so sánh được) ----
PATHS_NOTE = (
    "PATHS: every path is relative to the sandbox root and never starts with '/'. "
    "The task files are in the folder workspace/ (for example workspace/app.log). "
    "Use exactly this relative form both in the file tools and in the shell (execute); "
    "the shell starts in the sandbox root. "
)
BASE_PROMPT = (
    "You are an engineering assistant working in a sandbox. "
    + PATHS_NOTE
    + "Use the shell to run Python and tests. "
    "When you are done, reply with a short summary that mentions only files you really created or changed."
)
SKILLS_NOTE = (
    " Skills are in the folder skills/ (one sub-folder per skill with a SKILL.md). "
    "As your FIRST action, read the SKILL.md of every skill whose description could apply to the task, "
    "then follow them. Never modify skills/."
)
SUBAGENTS_NOTE = (
    " You have specialised subagents (see the description of the task tool). "
    "For anything beyond a trivial step, delegate to a suitable subagent and put ALL the task rules and file paths "
    "in the delegation message, because a subagent sees only what you send. "
    "Check what a subagent returns before you rely on it."
)
# --------------------------------------------------------------------------------------------------


def make_backend(sandbox: Path):
    """Tạo backend (môi trường thực thi) cho tác tử.

    Yêu cầu:
      - Thư mục gốc (root_dir) là `sandbox`; đường dẫn tương đối `workspace/...` và `skills/...`
        phải dùng được ở CẢ công cụ tệp lẫn shell (shell chạy với thư mục làm việc = `sandbox`).
      - Tác tử chạy được lệnh shell và gọi được `python` (cần đặt PATH).
      - KHÔNG chuyển biến môi trường của bạn vào shell của tác tử (khóa API không được lộ).
    """
    paths = [str(Path(sys.executable).parent)]
    env = {"HOME": str(sandbox), "PYTHONDONTWRITEBYTECODE": "1"}
    if os.name == "nt":
        git_tools = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git" / "usr" / "bin"
        system_root = Path(os.environ.get("SystemRoot", "C:/Windows"))
        paths.extend([str(git_tools), str(system_root / "System32"), str(system_root)])
        env["SystemRoot"] = str(system_root)
    else:
        paths.extend(["/usr/local/bin", "/usr/bin", "/bin"])
    env["PATH"] = os.pathsep.join(paths)
    backend_type = LocalShellBackend
    if os.name == "nt":
        bash = git_tools / "bash.exe"
        if not bash.is_file():
            raise RuntimeError("Git for Windows Bash is required for the lab shell.")

        class BashLocalShellBackend(LocalShellBackend):
            """Run POSIX commands with Git Bash, including quoted multiline Python."""

            def execute(self, command: str, *, timeout: int | None = None):
                if not command or not isinstance(command, str):
                    return super().execute(command, timeout=timeout)
                with tempfile.TemporaryDirectory(prefix="lab-shell-") as shell_directory:
                    script = Path(shell_directory) / "command.sh"
                    script.write_text(
                        'python3() { python "$@"; }\n' + command,
                        encoding="utf-8", newline="\n",
                    )
                    return super().execute(
                        f'"{bash}" --noprofile --norc "{script.as_posix()}"', timeout=timeout,
                    )

        backend_type = BashLocalShellBackend
    return backend_type(
        root_dir=sandbox, virtual_mode=True, inherit_env=False, env=env, timeout=120,
    )


def build_agent(sandbox: Path, mode: str = "single", use_skills: bool = False, model=None):
    """Tạo tác tử Deep Agents.

    Tham số:
      sandbox:    thư mục chứa `workspace/` (và `skills/` nếu có).
      mode:       "single"    -> tác tử mặc định (có subagent `general-purpose` sẵn của Deep Agents)
                  "subagents" -> thêm các subagent từ `get_subagents()` (nối PATHS_NOTE vào `system_prompt` của MỖI subagent,
                                 vì subagent không nhận BASE_PROMPT) và thêm SUBAGENTS_NOTE vào prompt chính
      use_skills: True -> nạp thư mục "/skills/" qua tham số `skills=` của create_deep_agent
                  và thêm SKILLS_NOTE vào prompt.
      model:      mô hình ngôn ngữ; None -> dùng `make_model()`.
    mode không hợp lệ -> ném ValueError.
    Trả về: đồ thị (graph) đã biên dịch, gọi bằng `.invoke({"messages": [...]})`.
    """
    if mode not in {"single", "subagents"}:
        raise ValueError(f"unknown agent mode: {mode}")

    kwargs = {}
    prompt = BASE_PROMPT
    if mode == "subagents":
        kwargs["subagents"] = [
            {**sub, "system_prompt": sub["system_prompt"] + " " + PATHS_NOTE}
            for sub in get_subagents()
        ]
        prompt += SUBAGENTS_NOTE
    if use_skills:
        kwargs["skills"] = ["/skills/"]
        prompt += SKILLS_NOTE

    selected_model = model if model is not None else make_model()
    if model is None and isinstance(selected_model, ChatGoogleGenerativeAI):
        selected_model.timeout = 60
        selected_model.max_retries = 1
        selected_model.rate_limiter = InMemoryRateLimiter(
            requests_per_second=0.2, check_every_n_seconds=0.1, max_bucket_size=1,
        )
        kwargs["middleware"] = [ModelRetryMiddleware(
            max_retries=2, retry_on=(RemoteProtocolError,),
            initial_delay=2, on_failure="error",
        )]
    return create_deep_agent(
        model=selected_model, system_prompt=prompt, backend=make_backend(sandbox), **kwargs,
    )
