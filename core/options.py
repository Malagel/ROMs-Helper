from pathlib import Path
from core.helpers.constants import THRESHOLD_DEFAULT, VALID_SUBFOLDERS_DEFAULT

class Options: 
    def __init__(self):
        self.path: Path | None = None
        
        self.rename_games: bool = False
        self.reverse_renaming: bool = False
        self.detect_duplicates: bool = False
        self.create_statistics: bool = False
        self.create_summary: bool = False
        self.logs: bool = False
        self.debug: bool = False

        self.renames_backup: bool = True
        self.safe_deletion: bool = True
        self.require_confirmation: bool = True

        self.valid_subfolders: set[str] = VALID_SUBFOLDERS_DEFAULT
        self.duplicates_threshold: float = THRESHOLD_DEFAULT

    def show_values(self) -> list[str]:
        return [f"{name}: {value}" for name, value in vars(self).items()]