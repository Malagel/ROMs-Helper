from core.utils import is_valid_subfolder, clean_string

def rename_games(path):
    print("Renaming all your gamefiles...")
    for console in path.glob("*"): 
        if not console.is_dir(): continue

        for sub in console.glob("*"):
            if sub.is_dir() and is_valid_subfolder(sub.name):
                for game in sub.glob("*"):
                    game.rename(game.with_name(clean_string(game.name)))
            else:
                sub.rename(sub.with_name(clean_string(sub.name)))
                
    print("All your games have been renamed and cleaned.")
                