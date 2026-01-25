from core.options import Options
from core.summary.render import generate_summary_file
from core.logger import log
from datetime import datetime
from pathlib import Path

def create_summary(opts: Options) -> None:
    if opts.logs: log(f"\n▶ Starting creation of summary...")
    print("• Generating summary... ", end="", flush=True)

    current_time = datetime.now()

    generate_summary_file(opts.path, opts.valid_subfolders, current_time)

    print("DONE")
    print("• The file was created inside the 'summaries' folder.")

    if opts.logs: log(f"The text file 'summary_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.txt' was created.")