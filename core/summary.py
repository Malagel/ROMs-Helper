from core.utils import is_valid_subfolder
from pathlib import Path

def create_summary(path: Path) -> None:
    spaces = " " * 4

    print("Generating summary...\n")

    with open("summary.txt", "w") as f:
        for console in path.glob("*"): 
            if not console.is_dir(): continue

            f.write(f"================= {console.name} =================\n")

            for sub in console.glob("*"):
                if sub.is_dir() and is_valid_subfolder(sub.name):
                    f.write(f"{spaces}Subfolder: {sub.name}\n")
                    for game in sub.glob("*"):
                        f.write(f"{spaces * 2}{game.stem}\n")
                else:
                    f.write(f"{spaces}{sub.stem}\n")

    print("Summary file 'summary.txt' created successfully.")

