from core.utils import is_valid_subfolder, get_file_byte_size, get_folder_byte_size, normalize
from collections import defaultdict
from core.logger import log
from pathlib import Path

def add_game_data(games_data: dict[int, dict], game: Path, console: Path, logs: bool, identifier: int) -> None:
        games_data[identifier] = {
            "original_name": game.stem,
            "path": game,
            "normalized_name": normalize(game.stem, full_clean=True),
            "metadata": {
                "console": console.name,
                "size": get_file_byte_size(game) if game.is_file() else get_folder_byte_size(game) 
            }
        }

        if logs:
            log(f"[DATA COLLECTOR]: {games_data[identifier]} ")


def get_roms_data(path: Path, logs: bool) -> dict[str, dict]:
    if logs: log(f"[DATA COLLECTOR]: Fetching and organizing data from {path}")

    bytes_per_console = {}
    games_per_console = defaultdict(int)
    games_data = {}
    identifier = 0

    print(f"Getting your ROMs data from {path}... ", end="", flush=True)
    for console in path.glob("*"):
        if not console.is_dir(): 
            if logs: log(f"[DATA COLLECTOR]: Ignoring non-directory item {console.name}")
            continue

        if logs: log(f"[DATA COLLECTOR]: Scanning console {console.name}")

        bytes_per_console[console.name] = get_folder_byte_size(console)

        # Get through all files inside console folders
        for sub in console.glob("*"):
            if sub.is_dir() and is_valid_subfolder(sub.name):
                for game in sub.glob("*"):

                    # Inside single or multidisk
                    games_per_console[console.name] += 1
                    add_game_data(games_data, game, console, logs, identifier)
                    identifier += 1

            else:
        
                # Inside the original folders
                games_per_console[console.name] += 1
                add_game_data(games_data, sub, console, logs, identifier)
                identifier += 1


        if logs:
            log(f"[DATA COLLECTOR]: The folder '{console.name}' has a size of {bytes_per_console[console.name]} GB.")
            log(f"[DATA COLLECTOR]: Found {games_per_console[console.name]} games in '{console.name}'.") 
    
    if logs: log(f"[DATA COLLECTOR]: Collection of data finalized - {len(bytes_per_console)} consoles processed.")

    print("DONE")
    return {
            "bytes_per_console": bytes_per_console,
            "games_per_console": games_per_console,
            "games_data": games_data          
    }

