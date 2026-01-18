from pathlib import Path
from typing import Iterator
from core.helpers.filesystem import is_valid_subfolder

def iter_games(root: Path, valid_subfolders: set[str]) -> Iterator[tuple[Path, Path]]:
    for console in root.iterdir():
        if not console.is_dir():
            continue

        for entry in console.iterdir():
            if entry.is_dir() and is_valid_subfolder(entry.name, valid_subfolders):
                for game in entry.iterdir():
                    yield game, console
            else:
                yield entry, console
