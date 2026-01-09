from pathlib import Path
from core.helpers.text import normalize

def compute_new_path(old_path: Path) -> Path | None:
    new_path = old_path.with_name(f"{normalize(old_path.stem)}{old_path.suffix}")
    return None if new_path == old_path else new_path

def apply_rename(old_path: Path, new_path: Path) -> None:
    old_path.rename(new_path)

