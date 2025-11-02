import os
from collections import defaultdict

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_folder_size(folder_path):
    total_size = 0
    for element in folder_path.rglob('*'):
        if element.is_file():
            total_size += element.stat().st_size

    return round(total_size / (1024 ** 3), 2) 


def is_valid_subfolder(name):
    normalized = name.lower().replace("-", " ").strip()
    return normalized in ("single disk", "multi disk")


def get_games_per_console(path):
    games_per_console = {}
    for console in path.glob("*"):
        if console.is_dir():
            for sub in console.glob("*"):
                if sub.is_dir() and is_valid_subfolder(sub.name):
                    games_per_console[console.name] = sum(1 for _ in sub.glob("*"))
                else:
                    games_per_console[console.name] = games_per_console.get(console.name, 0) + 1

    return games_per_console


def gb_per_console(path):
    gb_per_console = {}
    for console in path.glob("*"):
        if console.is_dir():
            gb_per_console[console.name] = get_folder_size(console)

    return gb_per_console


def game_and_console_names(path):
    game_and_consoles_names = defaultdict(list)

    for console in path.glob("*"):
        if console.is_dir():
            for sub in console.glob("*"):
                if sub.is_dir() and is_valid_subfolder(sub.name):
                    for game in sub.glob("*"):
                        game_and_consoles_names[game.stem.lower().strip()].append(console.name)
                else:
                    game_and_consoles_names[sub.stem.lower().strip()].append(console.name)

    return game_and_consoles_names

# TODO: create a function that finds similar game names and presents them to the user to see if they are replicates or really
# different games. 