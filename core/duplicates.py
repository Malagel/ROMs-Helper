from pathlib import Path
from core.utils import clear, prompt_continue, log
import shutil


def get_games_to_delete(path: Path, consoles: list[str], game: str, logs: bool) -> list[Path]:
    paths = []
    for console in consoles:
        console_path = path / console
        if not console_path.exists():
            if logs: log(f"[DELETE TOOL]: {console_path} does not exist.") 
            continue

        for file in console_path.rglob("*"):
            if file.stem.strip().lower() == game.lower():
                paths.append(file)
    return paths


def delete_game_paths(game_paths: list[Path], game_name: str, logs: bool) -> None:
    for game_path in game_paths:
        if game_path.is_dir():
            shutil.rmtree(game_path)
        else:
            game_path.unlink()
        
        if logs: log(f"[DELETE TOOL]: Deleted {'folder' if game_path.is_dir else 'file'} {game_path}.")


    print(f"\nDeleted {len(game_paths)} instances of {game_name.title()}")



def confirm_delete(games_to_delete_paths: list[Path], force: bool) -> bool:
    if not force:
        print("\nThese game paths will be deleted:")
        for p in games_to_delete_paths:
            print(p)
    answer = "yes" if force else input("\nDo you confirm? (yes/no) ").lower().strip()
    return answer == "yes"



def delete_duplicates(path: Path, games_and_consoles: dict[str, list[str]], force: bool, logs: bool) -> None:
    duplicates = {game: consoles for game, consoles in games_and_consoles.items() if len(consoles) > 1}
    if not duplicates: 
        print("No duplicates found.")
        return

    for game, consoles in duplicates.items():
        clear()

        print(f"\nDuplicates found of {game.title()} in:\n")
        for i, console in enumerate(consoles, start=1):
            print(f"{i}) {console}")

        choice = input(
            "\nFrom which consoles you wish to eliminate the game? "
            "(comma-separated, 'skip' if unsure): "
            ).strip().lower()
        
        if choice == "skip":
            if logs: log(f"[DELETE TOOL]: Skipping {game} by user.")
            print("Skipping...")

            if not prompt_continue():
                break
            continue
                
        try:
            indices = [int(i.strip()) - 1 for i in choice.split(",")]
            selected_consoles = [consoles[idx] for idx in indices]
        except (ValueError, IndexError) as e:
            print(f"Invalid selection: {e}. Skipping this game.")
            if logs: log(f"[DELETE TOOL]: Invalid selection: {e}. Skipping game {game}.")

            if not prompt_continue():
                break
            continue

        games_to_delete_paths = get_games_to_delete(path, selected_consoles, game, logs)
        if not games_to_delete_paths:
            print("No matching game files found for deletion.")
            if logs: log(f"[DELETE TOOL]: No matching games to delete. Maybe they are deleted already.")
            if not prompt_continue():
                break
            continue

        if confirm_delete(games_to_delete_paths, force):            
            delete_game_paths(games_to_delete_paths, game, logs)
        else:
            if logs: log(f"[DELETE TOOL]: Deletion of game {game} in {', '.join(selected_consoles)} not confirmed by user.")
            print("No games were deleted.")

        if not prompt_continue():
            break
        
    print("\nDuplicate removal process completed.")