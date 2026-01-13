from core.helpers.filesystem import get_app_base_dir
from datetime import datetime
from pathlib import Path

def get_statistics_path(current_time: datetime) -> Path:
    base_dir = get_app_base_dir() / "statistics"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / f"statistics_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

