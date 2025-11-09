from core.utils import log


def create_statistics(data: dict[str, dict], logs: bool) -> None:
    games_per_console = data["games_per_console"]
    gb_per_console = data["gb_per_console"]
    games_and_consoles = data["games_and_consoles"]

    if logs: log(f"[STATISTICS TOOL]: Starting computation of data.")

    print("Creating statistics from your collection... ", end="")
    with open("statistics.txt", "w") as f:
        duplicates = {game: consoles for game, consoles in games_and_consoles.items() if len(consoles) > 1}

        f.write("========== STATISTICS ==========\n\n")
        f.write(f"Total Games: {sum(games_per_console.values())}\n")
        f.write(f"Total Size: {sum(gb_per_console.values())} GB\n")
        f.write(f"Consoles Analyzed: {len(games_per_console)}\n")

        if duplicates:
            f.write(f"Total Duplicates Found: {len(duplicates)}\n")
        else:
            f.write("No duplicates in your games found.\n")

        f.write(f"\nGames per console in descending order:\n\n")
        for i, (console, games) in enumerate(sorted(games_per_console.items(), key=lambda x: x[1], reverse=True), start=1):
            f.write(f"{i}) {console}: {games} games\n")

        f.write(f"\n\nStorage used per console in descending order:\n\n")
        for i, (console, size) in enumerate(sorted(gb_per_console.items(), key=lambda x: x[1], reverse=True), start=1):
            f.write(f"{i}) {console}: {size} GB\n")

        if duplicates:
            f.write(f"\n\nDuplicates across consoles with identical name:\n\n")
            for game, consoles in duplicates.items():
                f.write(f"- {game.title()} -> {', '.join(sorted(consoles))}\n")
    
    print("DONE")
    if logs: log(f"[STATISTICS TOOL]: Statistics created and saved on 'statistics.txt'.")
    