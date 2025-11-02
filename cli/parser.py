import argparse
from pathlib import Path

def get_args():
    parser = argparse.ArgumentParser(
        description="Create a summary of your ROMs collection with statistics and manage duplicates."
    )
    
    parser.add_argument(
        "path",
        type=Path,
        help="Path to the root directory of your ROMs collection."
    )

    parser.add_argument(
        "--no-delete",
        action="store_false",
        dest="delete",
        help="Disables the duplicate deletion system"
    )

    parser.add_argument(
        "--no-statistics",
        action="store_false",
        dest="statistics",
        help="Disables the statistics generation"
    )

    return parser.parse_args()