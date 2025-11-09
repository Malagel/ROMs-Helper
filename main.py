from core.data import get_roms_data
from core.statistics import create_statistics
from core.duplicates import delete_duplicates
from core.rename import rename_games
from core.summary import create_summary
from cli.parser import get_args


def main() -> None:
    args = get_args()

    path = args.path
    if not path.is_dir():
        print("The provided path is not a valid directory.")
        return

    data = get_roms_data(path)

    if args.deleteDuplicates:
        delete_duplicates(path, data["games_and_consoles"], args.force)

    if args.renameGames:
        rename_games(path)

    if args.summary:
        create_summary(path)

    if args.statistics:
        create_statistics(data)


if __name__ == "__main__":
    main()
                        





