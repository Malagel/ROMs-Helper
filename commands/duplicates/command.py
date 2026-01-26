from core.duplicates.similarity import get_clusters
from core.logger import log
from core.options import Options
from core.helpers.constants import THRESHOLD_DEFAULT
from core.helpers.cli import clear_console

from commands.duplicates.display import sort_and_print_cluster
from commands.duplicates.interaction import handle_cluster
from commands.duplicates.logging import log_found_clusters

def detect_duplicates(games_data: dict[int, dict], opts: Options) -> None:
    threshold_string = 'default' if opts.duplicates_threshold == THRESHOLD_DEFAULT else str(opts.duplicates_threshold)

    if opts.logs: log(f"▶ Building similarity graph with threshold {opts.duplicates_threshold}.", True)
    print(f"• Building games with the threshold as {threshold_string}... ", end="", flush=True)
    clusters = get_clusters(games_data, opts.duplicates_threshold)
    print("DONE")

    if opts.logs: 
        log_found_clusters(clusters, games_data)

    for cluster in clusters:
        clear_console()
        sorted_cluster = sort_and_print_cluster(cluster, games_data, threshold_string)
        
        should_continue = handle_cluster(games_data, sorted_cluster, opts)
        if not should_continue: 
            break
    
    clear_console()
    print("• Duplicates detection finalized.")