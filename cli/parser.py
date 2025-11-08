import argparse
from pathlib import Path

def get_args():
    parser = argparse.ArgumentParser(
        description="Create a summary of your ROMs collection with statistics and manage your files with useful tools."
    )
    
    parser.add_argument(
        "path",
        type=Path,
        help="Path to the root directory of your ROMs collection."
    )
    
    parser.add_argument(
        "--no-summary",
        action="store_false",
        dest="summary",
        help="Disables summary generation"
    )

    parser.add_argument(
        "--delete-duplicates",
        action="store_true",
        dest="deleteDuplicates",
        help="Enables the duplicate deletion system."
    )

    parser.add_argument(
        "--delete-tags",
        action="store_true",
        dest="deleteTags",
        help="Deletes specified tags from game filenames across the collection. (e.g., '(USA)', '(Europe)', ...)"
    )

    parser.add_argument(
        "--no-statistics",
        action="store_false",
        dest="statistics",
        help="Disables the statistics generation"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="ROMs Helper 1.0.0"
    )


    return parser.parse_args()