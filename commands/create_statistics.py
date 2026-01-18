from core.helpers.filesystem import create_app_timestamped_path
from core.statistics.computing import compute_statistics
from core.statistics.render import generate_statistics_file
from core.options import Options
from datetime import datetime
from core.logger import log


def create_statistics(data: dict[str, dict], opts: Options) -> None:
    if opts.logs: log(f"\n▶ Starting creation of statistics...")
    print("• Creating statistics from your collection... ", end="", flush=True)

    current_time = datetime.now()

    statistics_path = create_app_timestamped_path("statistics", current_time)
    summary = compute_statistics(data)
    generate_statistics_file(summary, statistics_path, current_time)
    
    print("DONE")
    print("• The file was created inside the 'statistics' folder.")
    if opts.logs: log(f"Statistics created and saved on '{statistics_path}'.")
    