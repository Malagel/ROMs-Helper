from pathlib import Path
from datetime import datetime
import ctypes
import sys

def create_app_timestamped_path(name: str, current_time: datetime | None) -> Path:
    if current_time is None: current_time = datetime.now()

    base_dir = get_app_base_dir() / name
    base_dir.mkdir(parents=True, exist_ok=True)

    return base_dir / f"{name}_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"


def get_folder_byte_size(folder_path: Path) -> int:
    total_size = 0
    for element in folder_path.rglob('*'):
        if element.is_file():
            total_size += get_file_byte_size(element)

    return total_size


def get_file_byte_size(path: Path) -> int:
    return path.stat().st_size


def format_bytes(bytes: int) -> str:
    for unit in ("Bytes", "KB", "MB", "GB", "TB", "PB"):
        if bytes < 1024:
            if unit == "Bytes":
                return f"{bytes} {unit}"
            
            return f"{bytes:.2f} {unit}"
        bytes /= 1024


def is_valid_subfolder(name: str, valid_subfolders: set[str]) -> bool:
    normalized = name.replace("_", " ").strip().lower()
    return normalized in valid_subfolders


def get_app_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(sys.argv[0]).resolve().parent


def hide_folder_windows(path: Path):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ctypes.windll.kernel32.SetFileAttributesW(str(path), FILE_ATTRIBUTE_HIDDEN)


