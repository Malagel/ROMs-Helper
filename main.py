from core.statistics import create_statistics
from core.duplicates import delete_duplicates
from core.summary import create_summary
from core.utils import get_folder_size, clear
from cli.parser import get_args


def main():
    args = get_args()

    path = args.path
    if not path.is_dir():
        print("The provided path is not a valid directory.")
        return

    games_per_console, gb_per_console, game_and_console_names = create_summary(path)
    print("Summary generated successfully.")

    if args.statistics:
        create_statistics(games_per_console, gb_per_console, game_and_console_names)
        print("Statistics generated successfully.")

    if args.delete:
        delete_duplicates(path, game_and_console_names)
        print("Duplicates removed successfully.")


if __name__ == "__main__":
    main()
                        





