from core.utils import is_valid_subfolder, log
from pathlib import Path


def create_summary(path: Path, logs: bool) -> None:
    spaces = " " * 4

    print("Generating summary...\n")
    if logs: log(f"SUMMARY TOOL: Generating summary from {path}")

    with open("summary.txt", "w") as f:
        for console in path.glob("*"): 
            if not console.is_dir(): continue

            f.write(f"================= {console.name} =================\n")

            for sub in console.glob("*"):
                if sub.is_dir() and is_valid_subfolder(sub.name):
                    if logs: log(f"SUMMARY TOOL: Found subfolder {sub.name} inside {console.name}. Iterating over...")
                    f.write(f"{spaces}Subfolder: {sub.name}\n")
                    for game in sub.glob("*"):
                        f.write(f"{spaces * 2}{game.stem}\n")
                else:
                    f.write(f"{spaces}{sub.stem}\n")

            if logs: log(f"SUMMARY TOOL: Finished scanning and writing for {console.name}")
            f.write("\n")
            
    print("Summary file 'summary.txt' created successfully.")
    if logs: log(f"SUMMARY TOOL: The text file 'summary.txt' was created.")
