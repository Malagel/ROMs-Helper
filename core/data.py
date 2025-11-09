from core.utils import is_valid_subfolder, get_folder_size, log
from collections import defaultdict
from pathlib import Path


def get_roms_data(path: Path, logs: bool) -> dict[str, dict]:
    if logs: log(f"[DATA COLLECTOR]: Fetching and organizing data from {path}")

    gb_per_console = {}
    games_per_console = defaultdict(int)
    games_and_consoles = defaultdict(list)

    for console in path.glob("*"):
        if not console.is_dir(): 
            if logs: log(f"[DATA COLLECTOR]: Ignoring non-directory item {console.name}")
            continue

        if logs: log(f"[DATA COLLECTOR]: Scanning console {console.name}")

        gb_per_console[console.name] = get_folder_size(console)

        # Get through all files inside console folders
        for sub in console.glob("*"):
            if sub.is_dir() and is_valid_subfolder(sub.name):
                for game in sub.glob("*"):

                    games_per_console[console.name] += 1
                    games_and_consoles[(game.stem).lower().strip()].append(console.name)

            else:

                    games_per_console[console.name] += 1
                    games_and_consoles[(sub.stem).lower().strip()].append(console.name)
        if logs:
            log(f"[DATA COLLECTOR]: Folder size of {console.name} = {gb_per_console[console.name]}")
            log(f"[DATA COLLECTOR]: Found {games_per_console[console.name]} games in {console.name}") 
    
    if logs: log(f"[DATA COLLECTOR]: Collection of data finalized - {len(gb_per_console)} consoles processed")

    return {
            "gb_per_console": gb_per_console,
            "games_per_console": games_per_console,
            "games_and_consoles": games_and_consoles          
    }

