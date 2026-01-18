from datetime import datetime
from core.helpers.filesystem import create_app_timestamped_path

log_file = None

def start_logging():
    global log_file

    logs_path = create_app_timestamped_path("logs", None)

    log_file = logs_path.open("a", encoding="utf-8")


def log(msg: str) -> None:
    timestamp = datetime.now().isoformat(timespec="milliseconds")
    log_file.write(f"[{timestamp}]{msg}\n")
    log_file.flush()


def stop_logging():
    log_file.close()