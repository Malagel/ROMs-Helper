from pathlib import Path
from core.utils import welcome_message, clear_console

THRESHOLD_SIMILAR = 76.0

class Options: 
    def __init__(self):
        self.path: Path | None = None
        self.renameGames: bool = False
        self.reverseRenaming: bool = False
        self.detectDuplicates: float | None = None
        self.statistics: bool = False
        self.summary: bool = False
        self.logs: bool = False
        self.renamesBackup: bool = True
        self.force: bool = False
        self.trueDeletion: bool = False


def process_advanced_flags(choices: list[str], opt: Options) -> None:
    if '--dd-custom-threshold' in choices:
        print("\nCustom Threshold flag detected, please input a number between 1 and 100 (included): ")
        while True:
            choice = input("> ")
            try:
                threshold = float(choice)
                if 1 <= threshold <= 100:
                    break
                else:
                    print("[ERROR]: The value is not between the bounds, try again.")
            except ValueError:
                print("[ERROR]: The value is not a number, try again.")

        opt.detectDuplicates = threshold

    opt.logs = '--logs' in choices
    opt.renamesBackup = '--no-renames-backup' not in choices
    opt.force = '--force' in choices
    opt.trueDeletion = '--true-deletion' in choices 


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
    opt.renameGames = '1' in choices
    opt.reverseRenaming = '2' in choices
    opt.detectDuplicates = THRESHOLD_SIMILAR if '3' in choices else None
    opt.statistics = '4' in choices
    opt.summary = '5' in choices

    process_advanced_flags(choices, opt)

    clear_console()

    return opt