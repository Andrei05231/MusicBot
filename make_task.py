import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BOT_SCRIPT = BASE_DIR / "bot.py"
PYTHON_EXE = Path(sys.executable)
TASK_NAME = "Audio Discord Bot"

# Run through pythonw.exe instead of python.exe.
# pythonw.exe does not open a console window.
pythonw_exe = PYTHON_EXE.with_name("pythonw.exe")

task_command = f'"{pythonw_exe}" "{BOT_SCRIPT}"'

subprocess.run(
    [
        "schtasks",
        "/Create",
        "/TN",
        TASK_NAME,
        "/TR",
        task_command,
        "/SC",
        "ONLOGON",
        "/F",
    ],
    check=True,
)

print("Background task created successfully.")
