from core.utils import is_valid_subfolder, log
from pathlib import Path
import re


def clean_string(string: str) -> str:
    string = re.sub(r"\s*\([^)]*\)", '', string)
    string = re.sub(r"[_]+", ' ', string)
    string = re.sub(r"v\d+(\.\d+)*", '', string)

    return string.strip()


def rename_file(file: Path, logs: bool) -> None:
    old_name = file.name
    new_name = file.with_name(clean_string(file.name))

    if old_name != new_name.name:
        try:
            file.rename(new_name)
            if logs: log(f"[RENAMING TOOL]: Renamed {old_name} -> {new_name.name}")
        except FileExistsError:
            print(f"ERROR: Renaming caused a file to have the same name as other in the same folder. Skipping {old_name} from {file.parent}")
            if logs: log(f"[RENAMING TOOL]: Skipped {old_name}: {new_name.name} already exists in {file.parent}")


def rename_games(path: Path, logs: bool) -> None:
    print("Renaming all your gamefiles... ", end="")
    for console in path.glob("*"): 
        if not console.is_dir(): continue

        for sub in console.glob("*"):
            if sub.is_dir() and is_valid_subfolder(sub.name):
                for game in sub.glob("*"):
                    rename_file(game, logs)
            else:
                rename_file(sub, logs)
                
    print("DONE")
                