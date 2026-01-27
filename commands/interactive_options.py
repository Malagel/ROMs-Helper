from core.helpers.cli import welcome_message, clear_console
from core.options import Options
from core.errors import AppError

from pathlib import Path

def parse_advanced_flags(choices: list[str], opt: Options) -> None:
    if '--duplicates-threshold' in choices:
        idx = choices.index('--duplicates-threshold')

        if idx + 1 >= len(choices):
            raise AppError("No value entered for '--duplicates-threshold' flag.")
        
        value = choices[idx + 1]

        threshold = float(value)

        if not (1 <= threshold <= 100):
            raise AppError("Value for threshold is not valid. Make sure it's between 1 and 100 (included).")

        opt.duplicates_threshold = threshold

    if '--custom-subfolders' in choices:
        idx = choices.index('--custom-subfolders')

        if idx + 1 >= len(choices):
            raise AppError("No values entered for '--custom-subfolders' flag.") 

        extracted = choices[idx + 1].split(',')
        custom_subfolders = {sub.replace('-', ' ').strip().lower() for sub in extracted}

        opt.valid_subfolders.update(custom_subfolders)

    opt.reverse_renaming = '--reverse-renaming' in choices    
    opt.debug = '--debug' in choices
    opt.logs = '--logs' in choices
    opt.renames_backup = '--no-renames-backup' not in choices
    opt.require_confirmation = '--no-confirmation' not in choices   
    opt.safe_deletion = '--no-safe-deletion' not in choices 


def get_interactive_options() -> Options:
    opt = Options()
    welcome_message()

    while True:
        print("Drag and Drop your ROMs Folder, or paste it's path to start:")
        folder = input("> ").strip()
        path = Path(folder)

        if path.is_dir() and folder:
            opt.path = path
            break
        print("[ERROR]: Not a valid directory. Try again.\n")

    print("\nSelect the actions to perform, separated with spaces (e.g.: 1 3 5):")
    print("[1] Detect duplicated games.")
    print("[2] Clean your game names (rename files).")
    print("[3] Generate statistics.")
    print("[4] Create a summary.")
    print("\n[INFO]: For advanced options and information of each feature, check the GitHub Page.")

    choices = input("\n> ").strip().split()

    opt.detect_duplicates = '1' in choices
    opt.rename_games = '2' in choices
    opt.create_statistics = '3' in choices
    opt.create_summary = '4' in choices

    parse_advanced_flags(choices, opt)

    clear_console()

    return opt