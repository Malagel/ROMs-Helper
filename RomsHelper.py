from commands.statistics import create_statistics
from commands.duplicates import detect_duplicates
from commands.summary import create_summary
from commands.rename import rename_games
from commands.reverse_renaming import reverse_renaming
from core.logger import start_logging, stop_logging, log
from core.fetch_data import get_roms_data
from core.options import get_interactive_options

# Test path: /mnt/d/ROM'S/ROM'S

def main() -> None:
    try:
        opts = get_interactive_options()
    except ValueError:
        print("[ERROR]: Invalid value.")
        input("\nPress enter to exit. ")
        return
    
    path = opts.path
    data = None

    arg_options = [
        opts.rename_games,
        opts.detect_duplicates,
        opts.show_summary,
        opts.show_statistics,
        opts.reverse_renaming
    ]   

    if not any(arg_options):
        print("[ERROR]: There were no actions provided.")
        input("\nPress enter to exit. ")
        return
    
    if opts.logs: 
        start_logging()
        log("▶ Starting logging")
        log(f"Using this options: {opts.show_values()}")

    if opts.rename_games:
        if opts.reverse_renaming:
            print("[ERROR]: You can't rename your games and reverse it at the same time...")
            input("\nPress enter to exit. ")
            return
        rename_games(path, opts)

    if opts.reverse_renaming:
        reverse_renaming(opts)

    if opts.detect_duplicates:
        if not data:
            data = get_roms_data(path, opts)

        detect_duplicates(data["games_data"], opts)

    if opts.show_statistics:
        if not data or opts.detect_duplicates:
            data = get_roms_data(path, opts)

        create_statistics(data, opts)

    if opts.show_summary:
        create_summary(path, opts)

    if opts.logs: 
        log("Closing logging and saving...")
        stop_logging()
    
    input("\nPress enter to exit. ")

if __name__ == "__main__":
    main()