from core.data import get_roms_data
from core.statistics import create_statistics
from core.similar import delete_similar
from core.rename import rename_games
from core.summary import create_summary
from core.utils import log
from cli.parser import get_args

# Test path: "/mnt/d/ROM'S/ROM'S"

def main() -> None:
    args = get_args()

    path = args.path
    if not path.is_dir():
        print("ERROR: The provided path is not a valid directory.")
        return

    if args.logs: log(f"===== BEGINNING OF LOGGING =====\n")

    if args.renameGames:
        rename_games(path, args.logs)

    if args.delete:
        data = get_roms_data(path, args.logs)
        delete_similar(path, data["games_and_consoles"], args.force, args.logs, args.delete)

    if args.summary:
        create_summary(path, args.logs)

    if args.statistics:
        data = get_roms_data(path, args.logs)
        create_statistics(data, args.logs)


if __name__ == "__main__":
    main()
                        





