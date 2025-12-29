from core.utils import get_app_base_dir
from core.logger import log
from pathlib import Path
import sys


def create_statistics(data: dict[str, dict], logs: bool) -> None:
    games_per_console = data["games_per_console"]
    gb_per_console = data["gb_per_console"]
    games_data = data["games_data"]

    if logs: log(f"[STATISTICS TOOL]: Starting computation of data.")

    base = get_app_base_dir()
    statistics_path = base / "statistics.txt"

    print("Creating statistics from your collection... ", end="", flush=True)
    with open(statistics_path, "w") as f:

        f.write("============== STATISTICS ==============\n\n")
        f.write(f"Total Games: {sum(games_per_console.values())}\n")
        f.write(f"Total Size: {sum(gb_per_console.values())} GB\n")
        f.write(f"Consoles Analyzed: {len(games_per_console)}\n")

        f.write(f"\nGames per console in descending order:\n\n")
        for i, (console, games) in enumerate(sorted(games_per_console.items(), key=lambda x: x[1], reverse=True), start=1):
            f.write(f"{i}) {console}: {games} games\n")

        f.write(f"\n\nStorage used per console in descending order:\n\n")
        for i, (console, size) in enumerate(sorted(gb_per_console.items(), key=lambda x: x[1], reverse=True), start=1):
            f.write(f"{i}) {console}: {size} GB\n")

            console_games = [game for _, game in games_data.items() if game["metadata"]["console"] == console]

            if not console_games: 
                continue
            
            biggest = max(console_games, key=lambda x: x["metadata"]["size"])
            smallest = min(console_games, key=lambda x: x["metadata"]["size"])

            f.write(f"  Biggest game: {biggest['original_name']} -> {biggest['metadata']['size']} MB\n")
            f.write(f"  Smallest game: {smallest['original_name']} -> {smallest['metadata']['size']} MB\n\n")

    
    print("DONE")
    if logs: log(f"[STATISTICS TOOL]: Statistics created and saved on 'statistics.txt'.")
    