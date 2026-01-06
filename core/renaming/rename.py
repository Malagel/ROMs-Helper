from core.utils import is_valid_subfolder, normalize, get_app_base_dir, hide_folder_windows
from datetime import datetime
from core.logger import log
from pathlib import Path
import json
import sys

def create_renaming_backup(backup_data: list[dict[str, str]]) -> None:
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")

    backup_dir = get_app_base_dir() / ".renaming_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    if sys.platform.startswith("win"):
        hide_folder_windows(backup_dir)

    backup_file = backup_dir / f"{timestamp}.json" 

    with backup_file.open("w", encoding="utf-8") as f:
        json.dump(backup_data, f, indent=2)

 
def rename_file(file: Path, logs: bool, renamesBackup: bool, backup: list[dict[str, str]]) -> bool:
    old_path = file
    new_path = file.with_name(f"{normalize(file.stem)}{old_path.suffix}")

    if old_path.name == new_path.name:
        return False
    
    try:
        old_path.rename(new_path)

        if renamesBackup:
            backup.append({"old": str(old_path), "new": str(new_path)})
        if logs: log(f"[RENAMING TOOL]: Renamed {old_path.name} -> {new_path.name}")

    except FileExistsError:
        if logs: log(f"[RENAMING TOOL]: Skipped {old_path.name}: '{new_path.name}' already exists in '{old_path.parent}'")
        return False
    
    return True


def rename_games(path: Path, logs: bool, renamesBackup: bool, validSubfolders: set[str]) -> None:
    backup_data = list()
    total_files_renamed = 0
    print("• Renaming all your gamefiles... ", end="", flush=True)

    for console in path.glob("*"): 
        if not console.is_dir(): continue

        for sub in list(console.glob("*")):
            if sub.is_dir() and is_valid_subfolder(sub.name, validSubfolders):
                for game in list(sub.glob("*")):
                    if rename_file(game, logs, renamesBackup, backup_data): total_files_renamed += 1
            else:
                if rename_file(sub, logs, renamesBackup, backup_data): total_files_renamed += 1

    if renamesBackup and backup_data:
        create_renaming_backup(backup_data)

    print("DONE")
    if total_files_renamed:
        fileS = 'file' if total_files_renamed == 1 else 'files'
        print(f"• The tool renamed {total_files_renamed} {fileS}.")

        print("If you want to reverse the effects, use the 'reverse renaming' option.")
    else:
        print("No renamed were made since your files already have clean names.")
        
                