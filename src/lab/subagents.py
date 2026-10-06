"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": "Use when a task requires reading instructions, documentation, code, or sample data before making changes. Report findings and relevant edge cases without editing files.",
            "system_prompt": "Inspect the assigned files and requirements. Report concrete findings, constraints, and edge cases. Do not modify files. Use only the task details and paths supplied in the delegation.",
        },
        {
            "name": "implementer",
            "description": "Use when a task requires changing workspace files, running tests or scripts, and reporting what was changed and verified.",
            "system_prompt": "Implement the delegated task in the workspace. Read the relevant specification first, make focused changes, run the available checks, and report the files changed and test results. Follow all rules supplied in the delegation.",
        },
        {
            "name": "reviewer",
            "description": "Use when a completed change or data output needs an independent check against the task instructions and edge cases.",
            "system_prompt": "Review the delegated result against the supplied instructions. Inspect files and run checks where useful. Report specific defects and evidence. Do not modify files.",
        },
    ]
