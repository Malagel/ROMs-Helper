from core.renaming.backup import get_available_backups
from core.helpers.filesystem import get_app_base_dir
from core.renaming.operations import apply_rename
from core.renaming.traversal import traverse_json
from core.errors import AppError
from core.options import Options
from datetime import datetime
from core.logger import log
from pathlib import Path


def choose_backup_index(backups_available: list[Path]) -> int | None:
    print("More than one backup for renaming was found (Day/Month/Year):\n")
    for i, backup in enumerate(backups_available, start=1):
        human_readable_timestamp = datetime.strptime(str(backup.stem), "%d%m%Y_%H%M%S").strftime("%d/%m/%Y at %H:%M:%S")
        print(f"[{i}] Backup from {human_readable_timestamp}")

    while True:
        try:
            print("\nChoose one number from the list or type 'quit' to exit:")
            choice = input("> ")
            if choice == 'quit':
                print("\n• No changes were made.")
                return None
            
            if int(choice) > len(backups_available) or int(choice) < 1:
                print("[ERROR]: Invalid choice, try again.")
                continue
        except ValueError:
            print("[ERROR]: Please use a number, try again.")
            continue
        break
    
    return int(choice) - 1


def reverse_renaming(opts: Options) -> None:
    backup_dir = get_app_base_dir() / ".renaming_backups"
    if opts.logs: log(f"\n▶ Starting the renaming of gamefiles from backup now...")

    if not backup_dir.exists():
        print("[ERROR]: There is no backup folder available.")
        if opts.logs: log("No backup folder available. It was deleted, moved, or never created")
        return
    
    available_backups = get_available_backups(backup_dir)

    if not available_backups:
        print("[ERROR]: There are no backup files available.")
        if opts.logs: log("No backup file available. It was deleted, moved, or never created")
        return

 
    if len(available_backups) == 1:
        chosen_index = 0
    else:
        chosen_index = choose_backup_index(available_backups)
        if chosen_index is None: 
            return
            
    print("• Renaming your gamefiles from backup... ", end="", flush=True)
    for old_path, new_path in traverse_json(available_backups[chosen_index]):
        try:
            apply_rename(new_path, old_path)
            if opts.logs: log(f"Renamed correctly {new_path.name} to {old_path.name}")
        except (FileExistsError, FileNotFoundError) as e:
            if opts.logs: log(f"[ERROR]: Failed to rename {new_path}. {e}")
        except PermissionError as e:
            raise AppError("You do not have permission to modify this files.") from e
        except OSError as e:
            raise AppError("Failed to rename the file due to a filesystem error.") from e
    print("DONE")

    print("\nDo you want to remove the backup used? [y/N]:")
    answer = input("> ").strip().lower()
    if answer == "y":
        available_backups[chosen_index].unlink()
        print("• Backup removed.")

