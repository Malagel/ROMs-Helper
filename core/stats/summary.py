from core.utils import is_valid_subfolder, get_app_base_dir
from datetime import datetime
from core.logger import log
from pathlib import Path

# TODO: Prettify all this mess

def create_summary(path: Path, logs: bool) -> None:
    spaces = " " * 4

    print("Generating summary... ", end="", flush=True)
    if logs: log(f"[SUMMARY TOOL]: Generating summary from {path}")

    now = datetime.now()
    base = get_app_base_dir()
    summary_path = base / f"summary_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    with open(summary_path, "w") as f:
        f.write("===========================================================\n")
        f.write(f"Summary generated on: {now.strftime('%d/%m/%Y at %H:%M:%S')}\n")
        f.write("===========================================================\n\n")

        for console in path.glob("*"): 
            if not console.is_dir(): continue

            f.write(f"================= {console.name} =================\n")

            for sub in console.glob("*"):
                if sub.is_dir() and is_valid_subfolder(sub.name):
                    if logs: log(f"[SUMMARY TOOL]: Found subfolder {sub.name} inside {console.name}. Iterating over...")
                    f.write(f"{spaces}Subfolder: {sub.name}\n")
                    for game in sub.glob("*"):
                        f.write(f"{spaces * 2}{game.stem}\n")
                else:
                    f.write(f"{spaces}{sub.stem}\n")

            if logs: log(f"[SUMMARY TOOL]: Finished scanning and writing for {console.name}")
            f.write("\n")
            
    print("DONE")
    if logs: log(f"[SUMMARY TOOL]: The text file 'summary_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt' was created.")
