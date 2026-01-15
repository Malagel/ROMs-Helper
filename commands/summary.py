from core.options import Options
from core.summary.render import generate_summary_file
from datetime import datetime
from core.logger import log
from pathlib import Path


def create_summary(path: Path, opts: Options) -> None:
    if opts.logs: log(f"\n▶ Starting creation of summary...")
    print("• Generating summary... ", end="", flush=True)

    current_time = datetime.now()

    try:
        generate_summary_file(path, opts.valid_subfolders, current_time)
    except Exception as e:
        print(f"\n[ERROR]: A problem occured creating the summary. {e}") 
        if opts.logs: log(f"[ERROR]: A problem occured creating the summary. \n{repr(e)}")
        return
        
    print("DONE")
    print("• The file was created inside the 'summaries' folder.")

    if opts.logs: log(f"The text file 'summary_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.txt' was created.")

    
    