from core.statistics import create_statistics
from core.duplicates import detect_duplicates
from core.summary import create_summary
from core.rename import rename_games
from core.reverse_renaming import reverse_renaming
from core.logger import start_logging, stop_logging
from core.fetch_data import get_roms_data
from cli.parser import get_args
from datetime import datetime

# Test path: "/mnt/d/ROM'S/ROM'S"

def main() -> None:
    args = get_args()
    path = args.path
    data = None

    arg_options = [
        args.renameGames,
        args.detectDuplicates,
        args.summary,
        args.statistics,
        args.reverseRenaming
    ]   

    if not any(arg_options):
        print("[ERROR]: There were no tool flags provided")
        return
    
    if not path.is_dir():   
        print("[ERROR]: The provided path is not a valid directory.")
        return

    if args.logs: start_logging()

    if args.renameGames:
        rename_games(path, args.logs, args.renamesBackup)

    if args.reverseRenaming:
        if args.renameGames:
            print("[ERROR]: You can't rename your games and reverse it at the same time...")
            return
        
        reverse_renaming(args.logs)

    if args.detectDuplicates:
        if not data:
            data = get_roms_data(path, args.logs)

        detect_duplicates(data["games_data"], args.force, args.logs, args.detectDuplicates, args.trueDeletion)

    if args.statistics:
        if not data or args.detectDuplicates:
            data = get_roms_data(path, args.logs)

        create_statistics(data, args.logs)

    if args.summary:
        create_summary(path, args.logs)


    if args.logs: stop_logging()

if __name__ == "__main__":
    main()
                        





