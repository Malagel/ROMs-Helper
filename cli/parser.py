import argparse
from pathlib import Path

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a summary of your ROMs collection with statistics and manage your files with useful tools."
    )
    
    parser.add_argument(
        "path",
        type=Path,
        help="Path to the root directory of your ROMs collection."
    )

    parser.add_argument(
        "--logs",
        action="store_true",
        help="Keeps track of all interactions with the program and saves it to a log file."
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
        help="Enables summary generation"
    )

    parser.add_argument(
        "--statistics",
        action="store_true",
        dest="statistics",
        help="Enables the statistics generation"
    )

    parser.add_argument(
        "--delete-duplicates",
        nargs="?",
        choices=["identical", "similar"],
        const="identical",
        dest="delete",
        help="""Enables the similar deletion system. It detects similar game-names within a threshold so you\n 
        can decide to keep them or not.
        The threshold options are added after '--delete-similars', and are: \n
            1) 'identical' : this will stage for deletion ONLY the game-files that are almost exactly equal, basically the same games\n
            2) 'similar' : games with similar names will be staged, useful if you want to check different versions of games or sagas\n"""
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
        version="ROMs Helper 1.0.0"
    )

    return parser.parse_args()