import re
import unicodedata

_SEQUEL_NUMBERS_RE = re.compile(r"\b\d{1,2}\b")

GENERIC_WORDS = [
        "the", "a", "an", "and", "of", "in", "on", "at", "for", "to", "from", "with", "by", "vs",
        "edition", "version", "remake", "re", "redux", "ultimate", "complete", "special", "collection",
        "deluxe", "international", "anniversary", "classic", "hd", "plus",
        "expanded", "enhanced", "revival", "legacy", "adventure", "adventures", "quest", "battle", "saga", "heroes", "rise",
        "fall", "origin", "3-d", "3d",
    ]

def extract_sequel_numbers(name: str) -> set[int]:
    return {int(n) for n in _SEQUEL_NUMBERS_RE.findall(name)}


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