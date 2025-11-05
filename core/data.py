from core.utils import is_valid_subfolder, get_folder_size
from collections import defaultdict

def get_roms_data(path):
    gb_per_console = {}
    games_per_console = defaultdict(int)
    games_and_consoles = defaultdict(list)

    for console in path.glob("*"):
        if not console.is_dir(): continue

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

    return {
            "gb_per_console": gb_per_console,
            "games_per_console": games_per_console,
            "games_and_consoles": games_and_consoles          
    }

