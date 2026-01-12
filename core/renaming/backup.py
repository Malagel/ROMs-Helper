from core.helpers.filesystem import get_app_base_dir, hide_folder_windows
from pathlib import Path
from datetime import datetime
import json
import sys

def create_backup_path() -> Path:
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")

    backup_dir = get_app_base_dir() / ".renaming_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    if sys.platform.startswith("win"):
        hide_folder_windows(backup_dir)

    return backup_dir / f"{timestamp}.json" 

    
def create_renaming_backup(backup_data: list[dict[str, str]]) -> None:

    backup_path = create_backup_path()
    
    with backup_path.open("w", encoding="utf-8") as f:
        json.dump(backup_data, f, indent=2)


def get_available_backups(backup_dir: Path) -> list[Path]:
    return [backup for backup in sorted(backup_dir.iterdir(), key=lambda b: b.stem, reverse=True)]
