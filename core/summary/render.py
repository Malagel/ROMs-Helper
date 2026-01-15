from core.helpers.filesystem import create_app_timestamped_path
from core.helpers.filesystem import is_valid_subfolder
from core.helpers.text import normalize
from datetime import datetime
from pathlib import Path

TITLE_LINE = "=" * 75
SECTION_LINE = "-" * 75
INDENT = " " * 4
SUB = "▶"
ITEM = "•"

def generate_summary_file(path: Path, valid_subfolders: set[str], current_time: datetime) -> None:
    summary_path = create_app_timestamped_path("summary", current_time)
    
    with summary_path.open("w", encoding="utf-8") as f:
        f.write(f"{TITLE_LINE}\n")
        f.write("                               ROMS SUMMARY\n")
        f.write(f"{TITLE_LINE}\n\n") 

        f.write(f"Summary generated on: {current_time.strftime('%d/%m/%Y at %H:%M:%S')}\n\n")

        for console in sorted(p for p in path.iterdir() if p.is_dir()): 

            f.write(f"[ {console.name} ]\n")
            f.write(f"{SECTION_LINE}\n")

            for sub in sorted(console.iterdir()):
                if sub.is_dir() and is_valid_subfolder(sub.name, valid_subfolders):
                    f.write(f"{SUB} Subfolder : {sub.name}\n")

                    for game in sorted(sub.iterdir()):
                        f.write(f"{INDENT}{ITEM} {normalize(game.stem)}\n")
                else:
                    f.write(f"{ITEM} {normalize(sub.stem)}\n")

            f.write("\n")