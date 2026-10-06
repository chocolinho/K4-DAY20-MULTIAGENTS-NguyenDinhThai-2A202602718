### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool call: ls
{"path": "workspace/bookings"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Tool call: ls
{"path": "workspace/tests"}

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

### Tool call: execute
{"command": "pytest workspace/tests"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\lab-task-upckkkk8
plugins: anyio-4.15.1, langsmith-0.14.4
collected 0 items / 1 error

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\lab-task-upckkkk8\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.18s ===============================

Exit code: 2
[Command failed with exit code 2]

### Tool call: execute
{"command": "python -m pytest workspace/tests"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\lab-task-upckkkk8
plugins: anyio-4.15.1, langsmith-0.14.4
collected 0 items / 1 error

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\lab-task-upckkkk8\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.18s ===============================

Exit code: 2
[Command failed with exit code 2]

### Tool call: execute
{"command": "python -m pytest workspace"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\lab-task-upckkkk8
plugins: anyio-4.15.1, langsmith-0.14.4
collected 0 items / 1 error

=================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py ______________
ImportError while importing test module '~\AppData\Local\Temp\lab-task-upckkkk8\workspace\tests\test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
..\..\Programs\Python\Python311\Lib\importlib\__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace\tests\test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ===========================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.17s ===============================

Exit code: 2
[Command failed with exit code 2]

### Tool call: execute
{"command": "python -m pytest -o pythonpath=workspace workspace/tests"}

### Tool result
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: ~\AppData\Local\Temp\lab-task-upckkkk8
plugins: anyio-4.15.1, langsmith-0.14.4
collected 3 items

workspace\tests\test_bookings.py FF.                                     [100%]

================================== FAILURES ===================================
______________________ test_total_minutes_mixed_formats _______________________

    def test_total_minutes_mixed_formats():
>       assert total_minutes(["1h30m", "2h"]) == 210
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

workspace\tests\test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
workspace\bookings\schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace\bookings\schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

text = '2h'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45    # a bare number means minutes
        Surrounding whitespace is ignored.
        """
        m = re.fullmatch(r"(\d+)h(

### Tool call: read_file
{"limit": 1000, "file_path": "workspace/tests/test_bookings.py", "offset": 0}

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: read_file
{"offset": 0, "limit": 1000, "file_path": "workspace/bookings/__init__.py"}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool call: read_file
{"limit": 1000, "offset": 0, "file_path": "workspace/bookings/billing.py"}

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)