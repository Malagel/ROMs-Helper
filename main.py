from core.data import get_roms_data
from core.statistics import create_statistics
from core.duplicates import delete_duplicates
from core.summary import create_summary
from cli.parser import get_args


def main():
    args = get_args()

    path = args.path
    if not path.is_dir():
        print("The provided path is not a valid directory.")
        return

    if args.summary:
        create_summary(path)

    if args.statistics:
        data = get_roms_data(path, {"games_per_console", "gb_per_console", "game_and_console_names"})
        create_statistics(data["games_per_console"], data["gb_per_console"], data["game_and_console_names"])

    if args.delete:
        data = get_roms_data(path, {"game_and_console_names"})
        delete_duplicates(path, data["game_and_console_names"])

if __name__ == "__main__":
    main()
                        





