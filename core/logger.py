from datetime import datetime
from pathlib import Path
from core.utils import get_app_base_dir

log_file = None

def start_logging():
    global log_file
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    log_dir = get_app_base_dir() / "logs" 
    log_dir.mkdir(parents=True, exist_ok=True)

    log_path = log_dir / f"logs_{timestamp}.txt"

    log_file = log_path.open("a", encoding="utf-8")


def log(msg: str):
    log_file.write(f"{msg}\n")
    log_file.flush()


def stop_logging():
    log_file.close()