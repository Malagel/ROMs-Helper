from core.helpers.cli import clear_console, prompt_continue 
from core.errors import ClusterTooLargeError, AppError
from core.duplicates.deletion import delete_game_paths
from core.duplicates.similarity import get_clusters
from core.helpers.constants import THRESHOLD_DEFAULT
from core.options import Options
from core.logger import log
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


def detect_duplicates(games_data: dict[int, dict], opts: Options) -> None:
    threshold_string = 'default' if opts.duplicates_threshold == THRESHOLD_DEFAULT else str(opts.duplicates_threshold)
    print(f"• Building games with the threshold as {threshold_string}...", end="", flush=True)

    try:
        if opts.logs: log(f"\n▶ Building similarity graph with threshold {opts.duplicates_threshold}. This can be customized with --dd-custom-threshold.")
        clusters = get_clusters(games_data, opts.duplicates_threshold)
    except ClusterTooLargeError:
        raise("With the current threshold, the number of detected games exceeds 100.\n" 
             "Similarity was detected across too many entries of games, making it unfeasible for displaying.\n" 
             "Please try again with a higher threshold value."
        )
    
    print("DONE")

    if opts.logs:
        log("[DETECT DUPLICATES]: Showing clusters...")
        for cluster in clusters:
            for id in cluster:
                log(f"> {games_data[id]['original_name']} -- {games_data[id]['fuzzy_name']}")
            log("[DETECT DUPLICATES]: Next cluster.")

    for cluster in clusters:
        clear_console()
        sorted_cluster = sorted(cluster, key=lambda x: games_data[x]["original_name"])

        print(f"• Found {len(sorted_cluster)} games with the threshold as {threshold_string}:\n")
        for i, id in enumerate(sorted_cluster, start=1):
            print(f"[{i}] {games_data[id]['original_name']}  →  {games_data[id]['metadata']['console']}")
        
        while True:
            print(
                f"\nSelect the games you wish to {'move to a folder' if opts.safe_deletion else 'eliminate'}" 
                ", separated with spaces (e.g.: 1 3 5).\n"
                "(Leave it blank to skip or type 'quit' to exit): "
                )
            choice = input("> ").strip().lower()
            if not choice or choice == 'quit': break

            try: 
                indices = [int(i.strip()) - 1 for i in choice.split() if i.isdigit() and int(i) > 0]
                if not indices: 
                    raise ValueError
                
                game_paths = [games_data[sorted_cluster[idx]]['path'] for idx in indices]

            except ValueError:
                print(f"[ERROR]: The value is invalid, try again")
                continue

            if confirm_delete(game_paths, opts.require_confirmation, opts.safe_deletion):
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
        
                break
            else:
                print("\n• Retrying...")

        if not choice: continue
        elif choice == 'quit': break

        if not prompt_continue(): break

    clear_console()
    print("• Duplicates detection finalized.")