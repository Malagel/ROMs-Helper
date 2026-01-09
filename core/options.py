from pathlib import Path
from core.helpers.cli import welcome_message, clear_console
from core.helpers.constants import THRESHOLD_DEFAULT, VALID_SUBFOLDERS_DEFAULT

class Options: 
    def __init__(self):
        self.path: Path | None = None
        self.rename_games: bool = False
        self.reverse_renaming: bool = False
        self.detect_duplicates: bool = False
        self.duplicates_custom_threshold: float = THRESHOLD_DEFAULT
        self.show_statistics: bool = False
        self.show_summary: bool = False
        self.logs: bool = False
        self.renames_backup: bool = True
        self.safe_deletion: bool = True
        self.require_confirmation: bool = True
        self.valid_subfolders: set[str] = VALID_SUBFOLDERS_DEFAULT

    def show_values(self) -> list[str]:
        return [f"{name}: {value}" for name, value in vars(self).items()]


def process_advanced_flags(choices: list[str], opt: Options) -> None:
    if '--dd-custom-threshold' in choices:
        idx = choices.index('--dd-custom-threshold')

        if idx + 1 >= len(choices):
            raise ValueError
        
        value = choices[idx + 1]

        threshold = float(value)

        if not (1 <= threshold <= 100):
            raise ValueError

        opt.duplicates_custom_threshold = threshold
        opt.detect_duplicates = True

    if '--custom-subfolders' in choices:
        idx = choices.index('--custom-subfolders')

        if idx + 1 >= len(choices):
            raise ValueError

        extracted = choices[idx + 1].split(',')
        custom_subfolders = {sub.replace('_', ' ').strip().lower() for sub in extracted}

        opt.valid_subfolders.update(custom_subfolders)
    
    opt.logs = '--logs' in choices
    opt.renames_backup = '--no-renames-backup' not in choices
    opt.require_confirmation = '--no-confirmation' not in choices   
    opt.safe_deletion = '--no-safe-deletion' not in choices 


def get_interactive_options() -> Options:
    opt = Options()
    welcome_message()

    while True:
        print("Enter the path to your ROMs folder to start:")
        folder = input("> ").strip()
        path = Path(folder)

        if path.is_dir() and folder:
            opt.path = path
            break
        print("[ERROR]: Not a valid directory, try again.\n")

    print("\nSelect the actions to perform, separated with spaces (e.g.: 1 3 5):")
    print("[1] Clean your game names (rename files).")
    print("[2] Reverse renaming using backup.")
    print("[3] Detect duplicated games.")
    print("[4] Generate statistics.")
    print("[5] Create a summary.")
    print("\n[INFO]: For advanced options and information of each feature, check the GitHub Page.")

    choices = input("\n> ").strip().split()
    opt.rename_games = '1' in choices
    opt.reverse_renaming = '2' in choices
    opt.detect_duplicates = '3' in choices
    opt.show_statistics = '4' in choices
    opt.show_summary = '5' in choices

    process_advanced_flags(choices, opt)

    clear_console()

    return opt