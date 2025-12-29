import argparse
from pathlib import Path

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a summary of your ROMs collection with statistics and manage your files with useful tools."
    )
    
    parser.add_argument(
        "path",
        type=Path,
        help="Path to the root directory of your ROMs collection. You can drag a folder inside to get the path"
    )

    parser.add_argument(
        "--logs",
        action="store_true",
        help="Keeps track of all interactions with the program and saves them into a log file."
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Disables security confirmation for options that require it. Useful if you are sure of what you are doing."
    )
    
    parser.add_argument(
        "--summary",
        action="store_true",
        dest="summary",
        help="""Enables summary generation of your ROM/games collection, it will write all your games inside a organized
        text file."""
    )

    parser.add_argument(
        "--statistics",
        action="store_true",
        dest="statistics",
        help="Enables the statistics generation. This will create a text file with useful information."
    )

    parser.add_argument(
        "--detect-duplicates",
        nargs="?",
        choices=["identical", "similar"],
        const="identical",
        dest="detectDuplicates",
        help="""Enables the duplicates deletion system. It detects similar game-names within a threshold so you\n 
        can decide to keep them or not. By default they are moved to a 'DELETE' folder (You can change the default\n
        option with '--true-deletion').\n

        \nThe threshold options are added after, like this '--delete-similars [YOUR_OPTION]'. The options are:\n
            1) 'identical' : this will stage for deletion ONLY the game-files that are almost exactly equal, basically the same games\n
            2) 'similar' : games with similar names will be staged, useful if you want to check different versions of games or sagas\n
            
            \nLeaving it blank will use 'identical' as default."""
    )
    
    parser.add_argument(
        "--true-deletion",
        action="store_true",
        dest="trueDeletion",
        help="""Instead of moving files inside a folder for you to delete manually (like with the duplicaton system),\n
        delete them permanently."""
    )
    
    parser.add_argument(
        "--rename-games",
        action="store_true",
        dest="renameGames",
        help="""Renames each game in your collection by deleting specified tags (e.g., removing region tags like (USA), (EUR),\n
        version numbers such as v1.2, duplicate spaces, and formatting symbols like '_')."""
    )

    parser.add_argument(
        "--no-renames-backup",
        action="store_false",
        dest="renamesBackup",
        help="Desactivates the backup for renaming. No file for backup will be created."
    )

    parser.add_argument(
        "--reverse-renaming",
        action="store_true",
        dest="reverseRenaming",
        help="Reverses your last execution of the 'rename games' tool."
    )

    parser.add_argument(
        "--version",
        action="version",
        version="ROMs Helper 0.1.0"
    )

    return parser.parse_args()