from commands.create_statistics import create_statistics
from commands.duplicates import detect_duplicates
from commands.create_summary import create_summary
from commands.rename import rename_games
from commands.scan_roms import scan_roms
from commands.reverse_renaming import reverse_renaming
from commands.interactive_options import get_interactive_options

from core.logger import start_logging, stop_logging, log
from core.options import Options
from core.errors import AppError

# Test path: /mnt/d/ROM'S/ROM'S

def main() -> None:
    opts: Options | None = None

    try:
        opts = get_interactive_options()
        _run(opts)
    except AppError as e:
        print(f"[ERROR]: {e}")
        if opts and opts.logs:
            log(f"[ERROR]: {e}")

        if opts and opts.debug:
            raise
    except Exception as e:
        print(f"[FATAL]: A fatal error ocurred. Please reach out through the GitHub page:")
        print("https://github.com/Malagel/ROMs-Helper\n")
        if opts and opts.logs:
            log(f"[FATAL]: A fatal error ocurred. \n{repr(e)}")
    finally:
        if opts and opts.logs:
            stop_logging()  

    input("\nPress enter to exit. ")   


def _run(opts: Options) -> None:
    path = opts.path
    if opts and opts.logs: 
        start_logging()
        log("▶ Starting logging")
        log(f"Using this options: {opts.show_values()}")

    arg_options = [
        opts.rename_games,
        opts.detect_duplicates,
        opts.show_summary,
        opts.show_statistics,
        opts.reverse_renaming
    ]   

    if not any(arg_options):
        raise AppError("There were no actions provided.")
    
    if opts.rename_games:
        if opts.reverse_renaming:
            raise AppError("You can't rename your games and reverse it at the same time...")
        rename_games(path, opts)

    if opts.reverse_renaming:
        reverse_renaming(opts)

    if opts.detect_duplicates:
        data = scan_roms(path, opts)
        detect_duplicates(data["games_data"], opts)

    if opts.show_statistics:
        data = scan_roms(path, opts)
        create_statistics(data, opts)

    if opts.show_summary:
        create_summary(path, opts)

    if opts.logs: 
        log("Closing logging and saving...")
        stop_logging()


if __name__ == "__main__":
    main()