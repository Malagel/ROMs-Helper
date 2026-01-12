from core.renaming.traversal import traverse_folder
from core.renaming.operations import compute_new_path, apply_rename
from core.renaming.backup import create_renaming_backup
from core.options import Options
from core.logger import log
from pathlib import Path

def rename_games(path: Path, opts: Options) -> None:
    backup_data: list[dict[str, str]] = []
    files_renamed_count = 0

    print("• Renaming all your gamefiles... ", end="", flush=True)
    if opts.logs: log(f"\n▶ Starting the renaming of gamefiles now...")
    
    for game_path in traverse_folder(path, opts.valid_subfolders):
        new_path = compute_new_path(game_path)
        if new_path is None: 
            continue

        try: 
            apply_rename(game_path, new_path)

            if opts.renames_backup: backup_data.append({"old": str(game_path), "new": str(new_path)})
            if opts.logs: log(f"[INFO]: Renamed '{game_path.name}' -> '{new_path.name}'")
            
            files_renamed_count += 1
        except (FileExistsError, FileNotFoundError, PermissionError, OSError) as e:
            if opts.logs: log(f"[ERROR]: Skipping '{new_path.name}'. {e}.")
        
    if opts.renames_backup and backup_data:
        create_renaming_backup(backup_data)
        if opts.logs: log("[INFO]: Created filenames backup for restoration.")

    print("DONE")

    if files_renamed_count:
        print(f"• The tool renamed {files_renamed_count} file{'s' if files_renamed_count > 1 else ''}.")
        print("[INFO]: If you want to reverse the effects, use the 'reverse renaming' option.")
        if opts.logs: log(f"[INFO]: Finished renaming gamefiles. Files renamed: {files_renamed_count}.")
        
    else:
        print("No renames were made. Your files are clean already.")
        if opts.logs: log("[INFO]: Finished renaming. No files were renamed.")
