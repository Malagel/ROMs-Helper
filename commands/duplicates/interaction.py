from core.duplicates.deletion import delete_game_paths
from core.helpers.cli import prompt_continue
from core.options import Options
from core.errors import AppError

from pathlib import Path

def confirm_delete(game_paths: list[Path], require_confirmation: bool, safe_deletion: bool) -> bool:
    if not require_confirmation: return True

    sentence = '• This game path' if len(game_paths) == 1 else '• These game paths'
    action = "moved to the 'DELETE' folder" if safe_deletion else "deleted permanently"
    print(f"\n{sentence} will be {action}:")

    for p in game_paths:
        print(f"▶ {p}") 

    while True:
        print("\nDo you confirm? [y/N]")
        answer = input("> ").lower().strip()
        if answer in ['y', 'n']:
            break
        print("[ERROR]: Invalid answer, try again.")
    
    return answer == 'y'

def select_game_paths(games_data: dict[int, dict], sorted_cluster: list[int], opts: Options) -> tuple[list[Path] | None, str]:
    print(
        f"\nSelect the games you wish to {'move to a folder' if opts.safe_deletion else 'eliminate'}" 
        ", separated with spaces (e.g.: 1 3 5).\n"
        "(Leave it blank to skip or type 'quit' to exit): "
        )
    
    max_index = len(sorted_cluster) - 1
    while True:
        selection = input("> ").strip().lower()
        if not selection or selection == 'quit':
            return None, selection
        
        try: 
            indices = {int(i.strip()) - 1 for i in selection.split() if i.isdigit()}
        except ValueError:
            print("[ERROR]: The value is invalid. Try again\n")
            continue
        if any(idx < 0 or idx > max_index for idx in indices):
            print("[ERROR]: That value does not belong to any game. Try again.\n")
            continue
        if not indices:
            print("[ERROR]: That's not a valid input. Try again.\n")
            continue

        break
    
    game_paths = [games_data[sorted_cluster[idx]]['path'] for idx in indices]

    return game_paths, selection


def handle_cluster(games_data: dict[int, dict], sorted_cluster: list[int], opts: Options) -> bool:
    while True:
        game_paths, selection = select_game_paths(games_data, sorted_cluster, opts)

        if not selection:
            return True
        if selection == 'quit':
            return False

        if game_paths and confirm_delete(game_paths, opts.require_confirmation, opts.safe_deletion):
            try:
                delete_game_paths(game_paths, opts.safe_deletion)
            except PermissionError as e:
                raise AppError(
                    "You do not have permission to modify this folder."
                ) from e

            print(
                f"• {'Moved' if opts.safe_deletion else 'Deleted'} " 
                f"{len(game_paths)} "
                f"{'game' if len(game_paths) == 1 else 'games'}"
                f"{' to the DELETE folder.' if opts.safe_deletion else '.'}"
            )

            if not prompt_continue(): 
                return False
            
            return True
        else:
            print("\n• Retrying...")
