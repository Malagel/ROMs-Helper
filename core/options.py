from core.logger import log
from pathlib import Path
from core.utils import welcome_message, clear_console

THRESHOLD_SIMILAR = 76.0

class Options: 
    def __init__(self):
        self.path: Path | None = None
        self.renameGames: bool = False
        self.reverseRenaming: bool = False
        self.detectDuplicates: bool = False
        self.duplicatesCustomThreshold: float = THRESHOLD_SIMILAR
        self.statistics: bool = False
        self.summary: bool = False
        self.logs: bool = False
        self.renamesBackup: bool = True
        self.confirmation: bool = True
        self.safeDeletion: bool = True
        self.validSubfolders: set[str] = {"single disk", "multi disk", "single-disk", "multi-disk"}

    def show_values(self):
        values = []
        for name, value in vars(self).items():
            values.append(f"{name}: {value}")

        return values


def process_advanced_flags(choices: list[str], opt: Options) -> None:
    if '--dd-custom-threshold' in choices:
        idx = choices.index('--dd-custom-threshold')

        if idx + 1 >= len(choices):
            print("[ERROR]: The flag '--dd-custom-threshold' did not recieve anything.")
            raise ValueError
        
        value = choices[idx + 1]

        threshold = float(value)

        if not (1 <= threshold <= 100):
            print("[ERROR]: The flag '--dd-custom-threshold' recieved an invalid value.")
            raise ValueError

        opt.duplicatesCustomThreshold = threshold
        opt.detectDuplicates = True

    if '--custom-subfolders' in choices:
        idx = choices.index('--custom-subfolders')

        if idx + 1 >= len(choices):
            print("[ERROR]: The flag '--custom-subfolders' did not recieve anything.")
            raise ValueError

        extracted = choices[idx + 1].split(',')
        custom_subfolders = {sub.replace('_', ' ').strip().lower() for sub in extracted}

        opt.validSubfolders.update(custom_subfolders)
    
    opt.logs = '--logs' in choices
    opt.renamesBackup = '--no-renames-backup' not in choices
    opt.confirmation = '--no-confirmation' not in choices   
    opt.safeDeletion = '--no-safe-deletion' not in choices 


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
    opt.detectDuplicates = '3' in choices
    opt.statistics = '4' in choices
    opt.summary = '5' in choices

    process_advanced_flags(choices, opt)

    clear_console()

    return opt