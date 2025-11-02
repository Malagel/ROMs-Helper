import os

def get_folder_size(folder_path):
    total_size = 0
    for element in folder_path.rglob('*'):
        if element.is_file():
            total_size += element.stat().st_size

    return round(total_size / (1024 ** 3), 2) 

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
