from core.stats.statistics import create_statistics
from core.duplicates import detect_duplicates
from core.stats.summary import create_summary
from core.renaming.rename import rename_games
from core.renaming.reverse_renaming import reverse_renaming
from core.logger import start_logging, stop_logging
from core.fetch_data import get_roms_data
from core.options import get_interactive_options

# Test path: /mnt/d/ROM'S/ROM'S

def main() -> None:
    opts = get_interactive_options()
    path = opts.path
    data = None

    arg_options = [
        opts.renameGames,
        opts.detectDuplicates,
        opts.summary,
        opts.statistics,
        opts.reverseRenaming
    ]   

    if not any(arg_options):
        print("[ERROR]: There were no actions provided.")
        input("Press enter to exit. ")
        return
    
    if opts.logs: start_logging()

    if opts.renameGames:
        rename_games(path, opts.logs, opts.renamesBackup)

    if opts.reverseRenaming:
        if opts.renameGames:
            print("[ERROR]: You can't rename your games and reverse it at the same time...")
            input("Press enter to exit. ")
            return
        
        reverse_renaming(opts.logs)

    if opts.detectDuplicates:
        if not data:
            data = get_roms_data(path, opts.logs)

        detect_duplicates(data["games_data"], opts.force, opts.logs, opts.detectDuplicates, opts.trueDeletion)

    if opts.statistics:
        if not data or opts.detectDuplicates:
            data = get_roms_data(path, opts.logs)

        create_statistics(data, opts.logs)

    if opts.summary:
        create_summary(path, opts.logs)

    if opts.logs: stop_logging()
    
    input("\nPress enter to exit. ")

if __name__ == "__main__":
    main()
                        





