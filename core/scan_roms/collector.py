from core.helpers.filesystem import get_file_byte_size, get_folder_byte_size
from core.scan_roms.traversal import iter_games
from core.helpers.text import normalize
from collections import defaultdict
from pathlib import Path

def add_game_data(games_data: dict[int, dict], game: Path, console: Path, identifier: int) -> None:
        games_data[identifier] = {
            "original_name": game.stem,
            "fuzzy_name": normalize(game.stem, full_clean=True),
            "strict_name": normalize(game.stem, full_clean=False),
            "path": game,
            "metadata": {
                "console": console.name,
                "size": get_file_byte_size(game) if game.is_file() else get_folder_byte_size(game) 
            }
        }


def collect_roms_data(path: Path, valid_subfolders: set[str]) -> dict[str, dict]:
    bytes_per_console = {}
    games_per_console = defaultdict(int)
    games_data = {}

    for console in path.iterdir():
        if console.is_dir():
            bytes_per_console[console.name] = get_folder_byte_size(console)

    for identifier, (game, console) in enumerate(iter_games(path, valid_subfolders)):
        games_per_console[console.name] += 1
        add_game_data(games_data, game, console, identifier)

    return {
        "bytes_per_console": bytes_per_console,
        "games_per_console": games_per_console,
        "games_data": games_data,
    }