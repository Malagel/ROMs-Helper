from pathlib import Path
import unicodedata
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


def log(msg: str) -> None:
    with open("logs.txt", "a") as f:
        f.write(f"{msg}\n") 


def prompt_continue() -> bool:
    return input("\nPress enter to continue or type 'quit' to exit: ").strip().lower() != "quit"


def get_folder_size_gb(folder_path: Path) -> float:
    total_size = 0
    for element in folder_path.rglob('*'):
        if element.is_file():
            total_size += element.stat().st_size

    return round(total_size / (1024 ** 3), 2) 


def get_file_size_mb(path: Path) -> float:
    if path.is_file():
        return  round(path.stat().st_size / (1024 ** 2), 2)
    else:
        return get_folder_size_gb(path) * 1024
    

def is_valid_subfolder(name: str) -> bool:
    normalized = name.lower().replace("-", " ").strip()
    return normalized in ("single disk", "multi disk")
