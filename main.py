from core.data import get_roms_data
from core.statistics import create_statistics
from core.duplicates import delete_duplicates
from core.rename import rename_games
from core.summary import create_summary
from core.utils import log
from cli.parser import get_args

# Test path: "/mnt/d/ROM'S/ROM'S"

def main() -> None:
    args = get_args()

    path = args.path
    if not path.is_dir():
        print("The provided path is not a valid directory.")
        return

    data = get_roms_data(path, args.logs)
    if args.logs: log(f"\n===== BEGINNING OF LOGGING =====\n")

    if args.deleteDuplicates:
        delete_duplicates(path, data["games_and_consoles"], args.force, args.logs)

    if args.renameGames:
        rename_games(path, args.logs)

    if args.summary:
        create_summary(path, args.logs)

    if args.statistics:
        create_statistics(data, args.logs)


if __name__ == "__main__":
    main()
                        





