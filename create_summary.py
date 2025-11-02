import os
import shutil
import argparse
from pathlib import Path
from collections import defaultdict

def get_folder_size(folder_path):
    total_size = 0
    for element in folder_path.rglob('*'):
        if element.is_file():
            total_size += element.stat().st_size

    return round(total_size / (1024 ** 3), 2) 


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def create_summary(path):
    games_per_console = {}
    gigabytes_per_console = {}
    game_names = defaultdict(list)
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
                            game_names[game.stem.lower().strip()].append(console.name)
                            games += 1
                    else:
                        f.write(f"{spaces}{sub.stem}\n")
                        game_names[sub.stem.lower().strip()].append(console.name)
                        games += 1

                gigabytes_per_console[f"{console.name}"] = get_folder_size(console)
                games_per_console[f"{console.name}"] = games
                games = 0
        print()

    return games_per_console, gigabytes_per_console, game_names


def create_statistics(games_per_console, gigabytes_per_console, game_names):
    with open("statistics.txt", "w") as f:
        duplicates = {game: consoles for game, consoles in game_names.items() if len(consoles) > 1}

        f.write("\n\n========== STATISTICS ==========\n\n")
        f.write(f"Total Games: {sum(games_per_console.values())}\n")
        f.write(f"Total Size: {sum(gigabytes_per_console.values())} GB\n")
        f.write(f"Consoles Analyzed: {len(games_per_console)}\n")

        if duplicates:
            f.write(f"Total Duplicates Found: {len(duplicates)}\n")
        else:
            f.write("No duplicates in your games found.\n")

        f.write(f"\nGames per console in descending order:\n\n")
        for i, (console, games) in enumerate(sorted(games_per_console.items(), key=lambda x: x[1], reverse=True), start=1):
            f.write(f"{i}) {console}: {games} games\n")

        f.write(f"\n\nStorage used per console in descending order:\n\n")
        for i, (console, size) in enumerate(sorted(gigabytes_per_console.items(), key=lambda x: x[1], reverse=True), start=1):
            f.write(f"{i}) {console}: {size} GB\n")

        if duplicates:
            f.write(f"\n\nDuplicates across consoles with identical name:\n\n")
            for game, consoles in duplicates.items():
                f.write(f"- {game.title()} -> {', '.join(sorted(consoles))}\n")
        
        return duplicates

def delete_duplicates(path, game_names, confirmation):
    duplicates = {game: consoles for game, consoles in game_names.items() if len(consoles) > 1}

    if not duplicates:
        return
    
    print("\nDuplicate games found across multiple consoles:")

    a = input("Proceed with deletion system? (yes / no)").strip().lower()
    if a != 'yes':
        print("No deletions were made")
        return
    
    for game, consoles in duplicates.items():
        clear()

        print(f"\nDuplicates found of {game.title()} in:\n")
        for i, console in enumerate(consoles, start=1):
            print(f"{i}) {console}")

        choice = input("\nFrom which consoles you wish to eliminate the game? (comma-separated, 'skip' if unsure): ").strip().lower()
        if choice == "skip":
            continue
        
        games_to_delete_paths = []
        try: 
            indices = [int(i) - 1 for i in choice.split(",")]
            for idx in indices:
                for game_file in (path / consoles[idx]).rglob("*"):
                    if game_file.stem.strip().lower() == game:
                        games_to_delete_paths.append(game_file)

        except Exception as e:
            print(f"Error: {e}. Skipping the duplicates in this console")
            input("Press enter to continue")
            continue
        
        if games_to_delete_paths and not confirmation:
#            for game_path in games_to_delete_paths:
#                if game_path.is_dir():
#                    shutil.rmtree(game_path)
#                else:
#                    game_path.unlink()
                
            continue
                
        if games_to_delete_paths and confirmation:
            print("These game paths will be deleted:")
            for game_path in games_to_delete_paths:
                print(game_path)
            
            answer = input("Do you confirm? (yes/no)").lower().strip()
            if answer != "yes":
                continue
            
            for game_path in games_to_delete_paths:
#                if game_path.is_dir():
#                    shutil.rmtree(game_path)
#                else:
#                    game_path.unlink()
                print(f"Deleted: {game_path}")

            print(f"Deleted {len(games_to_delete_paths)} instances of {game.title()}")
            input("Press enter to continue")
            continue

        
        print("No games to delete")
        input("Press enter to continue")
        

def main():

    parser = argparse.ArgumentParser(
        description="Create a summary of your ROMs collection with statistics and manage duplicates."
    )
    
    parser.add_argument(
        "path",
        type=Path,
        help="Path to the root directory of your ROMs collection."
    )

    parser.add_argument(
        "--no-delete",
        action="store_false",
        dest="delete",
        help="Disables the duplicate deletion system"
    )

    parser.add_argument(
        "--no-statistics",
        action="store_false",
        dest="statistics",
        help="Disables the statistics generation"
    )

    parser.add_argument(
        "--no-confirmation",
        action="store_false",
        dest="confirmation",
        help="Skips confirmation prompts during deletion"
    )
    args = parser.parse_args()

    path = args.path
    if not path.is_dir():
        print("The provided path is not a valid directory.")
        return

    games_per_console, gigabytes_per_console, game_names = create_summary(path)
    print("Summary generated successfully.")

    if args.statistics:
        create_statistics(games_per_console, gigabytes_per_console, game_names)
        print("Statistics generated successfully.")

    if args.delete:
        delete_duplicates(path, game_names, args.confirmation)
        print("Duplicates deleted successfully.")



if __name__ == "__main__":
    main()
                        





