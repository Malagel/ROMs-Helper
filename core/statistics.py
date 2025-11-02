def create_statistics(games_per_console, gigabytes_per_console, game_names):
    with open("statistics.txt", "w") as f:
        duplicates = {game: consoles for game, consoles in game_names.items() if len(consoles) > 1}

        f.write("\n\n========== STATISTICS ==========\n\n")
        f.write(f"Total Games: {sum(games_per_console.values())}\n")
        f.write(f"Total Size: {sum(gigabytes_per_console.values())} GB\n")
        f.write(f"Consoles Analyzed: {len(games_per_console)}\n")

        if duplicates:
            f.write(f"Total Duplicates Found: {len(duplicates)}\n")
        else:
            f.write("No duplicates in your games found.\n")

        f.write(f"\nGames per console in descending order:\n\n")
        for i, (console, games) in enumerate(sorted(games_per_console.items(), key=lambda x: x[1], reverse=True), start=1):
            f.write(f"{i}) {console}: {games} games\n")

        f.write(f"\n\nStorage used per console in descending order:\n\n")
        for i, (console, size) in enumerate(sorted(gigabytes_per_console.items(), key=lambda x: x[1], reverse=True), start=1):
            f.write(f"{i}) {console}: {size} GB\n")

        if duplicates:
            f.write(f"\n\nDuplicates across consoles with identical name:\n\n")
            for game, consoles in duplicates.items():
                f.write(f"- {game.title()} -> {', '.join(sorted(consoles))}\n")
        