import os
import re
from collections import defaultdict

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def prompt_continue():
    return input("Press enter to continue or 'quit' to exit").strip().lower() != "quit"


def get_folder_size(folder_path):
    total_size = 0
    for element in folder_path.rglob('*'):
        if element.is_file():
            total_size += element.stat().st_size

    return round(total_size / (1024 ** 3), 2) 


def is_valid_subfolder(name):
    normalized = name.lower().replace("-", " ").strip()
    return normalized in ("single disk", "multi disk")


def clean_string(string):
    string = re.sub(r"\s*\([^)]*\)", '', string)
    string = re.sub(r"[-_]+", ' ', string)
    string = re.sub(r"v\d+(\.\d+)*", '', string)

    return string.strip()



# TODO: create a function that finds similar game names and presents them to the user to see if they are replicates or really
# different games. 