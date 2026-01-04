from pathlib import Path
import unicodedata
import ctypes
import sys
import re
import os

GENERIC_WORDS = [
        "the", "a", "an", "and", "of", "in", "on", "at", "for", "to", "from", "with", "by", "vs",
        "edition", "version", "remake", "re", "redux", "ultimate", "complete", "special", "collection",
        "deluxe", "international", "anniversary", "classic", "new", "super", "hd", "plus",
        "expanded", "enhanced", "revival", "legacy", "adventure", "adventures", "quest", "battle", "saga", "heroes", "rise",
        "fall", "origin", "3-d", "3d",
    ]


def roman_to_arabic(string: str) -> str:
    def is_roman(s):
        return re.fullmatch(r"M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})", s) is not None

    def roman_value(s):
        values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        total = 0
        prev = 0
        for ch in reversed(s):
            v = values[ch]
            if v < prev:
                total -= v
            else:
                total += v
            prev = v
        return total

    words = string.split()
    converted = []

    for w in words:
        if is_roman(w):
            converted.append(str(roman_value(w)))
        else:
            converted.append(w)

    return " ".join(converted)


def normalize(string: str, full_clean=False) -> str:
    string = re.sub(r"\s*\([^)]*\)", '', string)
    string = re.sub(r"[_]+", ' ', string)
    string = re.sub(r"\bv\d+(\.\d+)*\b", '', string)
    string = re.sub(r" +", ' ', string)

    if full_clean: 
        string = roman_to_arabic(string)
        string = string.lower()

        tokens = [t for t in string.split() if t not in GENERIC_WORDS]
        string = " ".join(tokens)

        string = re.sub(r"[^a-z0-9]+", " ", string)
        string = ''.join(c for c in unicodedata.normalize('NFKD', string) if not unicodedata.combining(c))
        

    return string.strip()


def clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def prompt_continue() -> bool:
    return input("\nPress enter to continue or type 'quit' to exit: ").strip().lower() != "quit"


def get_folder_byte_size(folder_path: Path) -> int:
    total_size = 0
    for element in folder_path.rglob('*'):
        if element.is_file():
            total_size += get_file_byte_size(element)

    return total_size


def get_file_byte_size(path: Path) -> int:
    return path.stat().st_size


def format_bytes(bytes: int) -> str:
    for unit in ("Bytes", "KB", "MB", "GB", "TB", "PB"):
        if bytes < 1024:
            if unit == "Bytes":
                return f"{bytes} {unit}"
            
            return f"{bytes:.2f} {unit}"
        bytes /= 1024


def is_valid_subfolder(name: str) -> bool:
    normalized = name.lower().replace("-", " ").strip()
    return normalized in ("single disk", "multi disk")


def get_app_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(sys.argv[0]).resolve().parent


def hide_folder_windows(path: Path):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ctypes.windll.kernel32.SetFileAttributesW(str(path), FILE_ATTRIBUTE_HIDDEN)


def welcome_message():
    print(r"""
╔════════════════════════════════════════════════════╗
║               Welcome to ROMsHelper!               ║
║                   Version 0.1.0                    ║
║====================================================║   
║                                                    ║      
║           A simple Command Line tool for           ║
║               organizing your ROMs.                ║
║                                                    ║
║====================================================║                      
║ > For more information consult the Github page:    ║
║ https://github.com/Malagel/ROMs-Helper             ║                                                          
╚════════════════════════════════════════════════════╝
""")