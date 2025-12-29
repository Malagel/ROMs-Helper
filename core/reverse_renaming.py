from core.utils import get_app_base_dir
from datetime import datetime
from core.logger import log
from pathlib import Path
import json

def reverse_renaming_with(backup: Path, logs: bool) -> None:
    with backup.open("r", encoding="utf-8") as f:
        pairs = json.load(f)

    for item in pairs:
        old = Path(item["old"])
        new = Path(item["new"])

        if not new.exists():
            if logs: log(f"[BACKUP RENAMING TOOL]: Skipping '{new.name}', file does not exist.")
            continue
        if old.exists():
            if logs: log(f"[BACKUP RENAMING TOOL]: Skipping '{old.name}', target already exists.")
            continue

        new.rename(old)
        if logs: log(f"[BACKUP RENAMING TOOL]: '{new.name}' renamed to '{old.name}'")

    print("Backup process finished.")
    answer = input(f"\nDo you want to remove the backup used? (y/n): ").strip().lower()
    if answer == "y":
        backup.unlink()
        print("\nBackup removed.")

def choose_backup(backups_available: list[Path]) -> int:
    print("More than one backup for renaming was found:\n")

    for i, backup in enumerate(backups_available, start=1):
        human_readable_timestamp = datetime.strptime(str(backup.stem), "%d%m%Y_%H%M%S").strftime("%d-%m-%Y at %H:%M:%S")
        print(f"{i}) Backup from {human_readable_timestamp}")

    while True:
        try:
            choice = input("\nChoose one number from the list or type 'quit' to exit: ")
            if choice == 'quit':
                print("Exiting. No changes were made.")
                return None
            
            choice = int(choice) - 1

            if choice > len(backups_available) - 1 or choice < 0:
                print("[ERROR]: invalid choice. Try again.\n")
                continue
        except ValueError:
            print("[ERROR]: invalid choice. Try again.\n")
            continue
        break
    
    return choice

def reverse_renaming(logs: bool) -> None:
    backup_dir = get_app_base_dir() / ".renaming_backups"

    if not backup_dir.exists():
        print("[ERROR]: There are no backups available.")
        return
    
    backups_available = [backup for backup in sorted(backup_dir.glob("*"), key=lambda b: b.stem, reverse=True)]

    if not backups_available:
        print("[ERROR]: There are no backups available.")
        return

    if len(backups_available) == 1:
        reverse_renaming_with(backups_available[0], logs)
        return

    chosen_backup = choose_backup(backups_available)
    if chosen_backup is None:
        return
    else:
        reverse_renaming_with(backups_available[chosen_backup], logs)
