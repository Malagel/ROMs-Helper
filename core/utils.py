from pathlib import Path
import re
import os


def normalize(string: str, lower=False) -> str:
    string = re.sub(r"\s*\([^)]*\)", '', string)
    string = re.sub(r"[_]+", ' ', string)
    string = re.sub(r"v\d+(\.\d+)*", '', string)

    if lower: return string.strip().lower()
    
    return string.strip()

def clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def log(msg: str) -> None:
    with open("logs.txt", "a") as f:
        f.write(f"{msg}\n") 


def prompt_continue() -> bool:
    return input("\nPress enter to continue or type 'quit' to exit: ").strip().lower() != "quit"


def get_folder_size(folder_path: Path) -> float:
    total_size = 0
    for element in folder_path.rglob('*'):
        if element.is_file():
            total_size += element.stat().st_size

    return round(total_size / (1024 ** 3), 2) 


def is_valid_subfolder(name: str) -> bool:
    normalized = name.lower().replace("-", " ").strip()
    return normalized in ("single disk", "multi disk")





# TODO: create a function that finds similar game names and presents them to the user to see if they are replicates or really
# different games. 