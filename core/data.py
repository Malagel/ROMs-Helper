from core.utils import get_games_per_console, gb_per_console, game_and_console_names

def get_roms_data(path, options):
    VALID_OPTIONS = {
        "games_per_console",
        "gb_per_console", 
        "game_and_console_names"}
    
    invalid = options - VALID_OPTIONS
    if invalid:
        raise ValueError(f"Invalid options: {', '.join(invalid)}")
    
    data = {}

    if "games_per_console" in options:
        data["games_per_console"] = get_games_per_console(path)

    if "gb_per_console" in options:
        data["gb_per_console"] = gb_per_console(path)

    if "game_and_console_names" in options:
        data["game_and_console_names"] = game_and_console_names(path)

    return data