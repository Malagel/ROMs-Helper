from core.statistics.paths import get_statistics_path
from core.statistics.computing import compute_statistics
from core.statistics.render import generate_statistics_file
from core.options import Options
from datetime import datetime
from core.logger import log


def create_statistics(data: dict[str, dict], opts: Options) -> None:
    if opts.logs: log(f"\n▶ Starting creation of statistics...")

    current_time = datetime.now()
    print("• Creating statistics from your collection... ", end="", flush=True)

    try:
        statistics_path = get_statistics_path(current_time)
        summary = compute_statistics(data)
        generate_statistics_file(summary, statistics_path, current_time)
    except Exception as e:
        print(f"\n[ERROR]: A problem occured creating statistics. {e}") 
        if opts.logs: log(f"[ERROR]: A problem occured creating statistics. {e}")
        return
    
    print("DONE")
    print("• The file was created inside the 'statistics' folder.")
    if opts.logs: log(f"Statistics created and saved on '{statistics_path}'.")
    