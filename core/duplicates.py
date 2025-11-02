from core.utils import clear
import shutil

def delete_duplicates(path, game_names):
    duplicates = {game: consoles for game, consoles in game_names.items() if len(consoles) > 1}

    if not duplicates: return

    for game, consoles in duplicates.items():
        clear()

        print(f"\nDuplicates found of {game.title()} in:\n")
        for i, console in enumerate(consoles, start=1):
            print(f"{i}) {console}")

        choice = input("\nFrom which consoles you wish to eliminate the game? (comma-separated, 'skip' if unsure): ").strip().lower()
        if choice == "skip": continue
        
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
        
        if games_to_delete_paths:
            print("These game paths will be deleted:")
            for game_path in games_to_delete_paths:
                print(game_path)
            
            answer = input("\nDo you confirm? (yes/no)").lower().strip()
            if answer == "yes":            
                for game_path in games_to_delete_paths:
    #                if game_path.is_dir():
    #                    shutil.rmtree(game_path)
    #                else:
    #                    game_path.unlink()
                    print(f"Deleted: {game_path}")

                print(f"\nDeleted {len(games_to_delete_paths)} instances of {game.title()}")
                input("Press enter to continue")
                continue

        print("No games to delete")
        input("Press enter to continue")
    
    print("Duplicate removal process completed.")