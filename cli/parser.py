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
        help="""Enables summary generation of your ROM/Games collection, it will write all your games inside a organized
        text file."""
    )

    parser.add_argument(
        "--statistics",
        action="store_true",
        dest="statistics",
        help="Enables the statistics generation. This will create a text file with useful information."
    )

    parser.add_argument(
        "--delete-duplicates",
        nargs="?",
        choices=["identical", "similar"],
        const="identical",
        dest="delete",
        help="""Enables the similar deletion system. It detects similar game-names within a threshold so you\n 
        can decide to keep them or not.\n

        \nThe threshold options are added after, like this '--delete-similars [YOUR_OPTION]'. The options are:\n
            1) 'identical' : this will stage for deletion ONLY the game-files that are almost exactly equal, basically the same games\n
            2) 'similar' : games with similar names will be staged, useful if you want to check different versions of games or sagas\n
            
            \nLeaving it blank will use 'identical' as default."""
    )
    
    parser.add_argument(
        "--rename-games",
        action="store_true",
        dest="renameGames",
        help="""Renames each game in your collection by deleting specified tags (e.g., '(USA)', '(Europe)', ...) and
        cleans the filename"""
    )

    parser.add_argument(
        "--version",
        action="version",
        version="ROMs Helper 0.1.0"
    )

    return parser.parse_args()