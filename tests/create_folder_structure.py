from pathlib import Path
from utils_tests import create_structure

structure = {
    "Roms-collection": {
        "Playstation 1": {"files": 134},
        "Playstation 2": {
            "single-disk": {"files": 82},
            "multi-disk": {"files": 43},
            },
        "Nintendo DS": {"files": 102},
        "Nintendo Switch": {"files": 34},
        "PC games": {
            "pc-game1": {"files": 12},
            "pc-game2": {"files": 23},
            "pc-game3": {"files": 4}
            },
        "Super Nintendo": {"files": 212},
        "Sega Dreamcast": {
            "Single disk": {"files": 32},
            "Multi Disk": {
                "dreamcast-game1": {"files": 4},
                "dreamcast-game2": {"files": 2}
            }
        }
    }
}

def main():
    create_structure("/home/nick/projects/ROMs-Helper/tests", structure)


if __name__ == "__main__":
    main()
