from pathlib import Path
from collections.abc import Iterator
from core.helpers.filesystem import is_valid_subfolder

def traverse_folder(path: Path, valid_subfolders: set[str]) -> Iterator[Path]:
    for console in path.iterdir(): 
        if not console.is_dir(): continue

        for game in list(console.iterdir()):
            if game.is_dir() and is_valid_subfolder(game.name, valid_subfolders):
                for sub_game in list(game.iterdir()):
                    yield sub_game
            else:
                yield game