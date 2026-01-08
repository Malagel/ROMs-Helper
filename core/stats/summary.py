from core.helpers.filesystem import is_valid_subfolder, get_app_base_dir
from core.helpers.text import normalize
from datetime import datetime
from core.logger import log
from pathlib import Path

TITLE_LINE = "=" * 75
SECTION_LINE = "-" * 75
INDENT = " " * 4
SUB = "▶"
ITEM = "•"

def create_summary(path: Path, logs: bool, validSubfolders: set[str]) -> None:
    print("• Generating summary... ", end="", flush=True)
    if logs: log(f"[SUMMARY TOOL]: Generating summary from {path}")

    now = datetime.now()

    base_dir = get_app_base_dir() / "summaries"
    base_dir.mkdir(parents=True, exist_ok=True)

    summary_path = base_dir / f"summary_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    
    with open(summary_path, "w") as f:
        f.write(f"{TITLE_LINE}\n")
        f.write("                               ROMS SUMMARY\n")
        f.write(f"{TITLE_LINE}\n\n") 

        f.write(f"Summary generated on: {now.strftime('%d/%m/%Y at %H:%M:%S')}\n\n")

        for console in sorted(p for p in path.iterdir() if p.is_dir()): 

            f.write(f"[ {console.name} ]\n")
            f.write(f"{SECTION_LINE}\n")

            for sub in sorted(console.iterdir()):
                if sub.is_dir() and is_valid_subfolder(sub.name, validSubfolders):
                    if logs: log(f"[SUMMARY TOOL]: Found subfolder {sub.name} inside {console.name}. Iterating over...")

                    f.write(f"{SUB} Subfolder : {sub.name}\n")

                    for game in sorted(sub.iterdir()):
                        f.write(f"{INDENT}{ITEM} {normalize(game.stem)}\n")
                else:
                    f.write(f"{ITEM} {normalize(sub.stem)}\n")

            if logs: log(f"[SUMMARY TOOL]: Finished scanning and writing for {console.name}")
            f.write("\n")
            
    print("DONE")
    print("• The file was created inside the 'summaries' folder.")

    if logs: log(f"[SUMMARY TOOL]: The text file 'summary_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt' was created.")
