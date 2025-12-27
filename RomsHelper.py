from core.statistics import create_statistics
from core.duplicates import delete_similar
from core.summary import create_summary
from core.rename import rename_games
from core.data import get_roms_data
from cli.parser import get_args
from core.utils import log

# Test path: "/mnt/d/ROM'S/ROM'S"

def main() -> None:
    args = get_args()
    path = args.path
    data = None

    arg_options = [
        args.renameGames,
        args.delete,
        args.summary,
        args.statistics,
    ]   

    if not any(arg_options):
        print("ERROR: There were no flags provided")
        return
    
    if not path.is_dir():   
        print("ERROR: The provided path is not a valid directory.")
        return

    if args.logs: log(f"\n===== BEGINNING OF LOGGING =====\n")

    if args.renameGames:
        rename_games(path, args.logs)

    if args.delete:
        if not data:
            data = get_roms_data(path, args.logs)

        delete_similar(data["games_data"], args.force, args.logs, args.delete)

    if args.summary:
        create_summary(path, args.logs)

    if args.statistics:
        if not data:
            data = get_roms_data(path, args.logs)

        create_statistics(data, args.logs)


if __name__ == "__main__":
    main()
                        





