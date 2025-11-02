from core.utils import get_folder_size

from collections import defaultdict


def create_summary(path):
    games_per_console = {}
    gb_per_console = {}
    game_and_consoles_names = defaultdict(list)
    games = 0
    spaces = " " * 4

    print("Generating summary...\n")

    with open("summary.txt", "w") as f:

        for console in path.glob("*"): 
            print(f"Processing: {console.name}", end="\r", flush=True)

            if console.is_dir():
                f.write(f"======== {console.name} ========\n")

                for sub in console.glob("*"):

                    if sub.is_dir() and (sub.name == "Single-Disk" or sub.name == "Multi-Disk"):
                        f.write(f"{spaces}Subfolder: {sub.name}\n")
                        for game in sub.glob("*"):
                            f.write(f"{spaces * 2}{game.stem}\n")
                            game_and_consoles_names[game.stem.lower().strip()].append(console.name)
                            games += 1
                    else:
                        f.write(f"{spaces}{sub.stem}\n")
                        game_and_consoles_names[sub.stem.lower().strip()].append(console.name)
                        games += 1

                gb_per_console[f"{console.name}"] = get_folder_size(console)
                games_per_console[f"{console.name}"] = games
                games = 0
        print()

    return games_per_console, gb_per_console, game_and_consoles_names

