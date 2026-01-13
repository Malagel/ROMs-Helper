from core.statistics.models import ConsoleStatistics, GameSize, StatisticsSummary

def compute_statistics(data: dict[str, dict]) -> StatisticsSummary:
    games_per_console = data["games_per_console"]
    bytes_per_console = data["bytes_per_console"]
    games_data = data["games_data"]

    consoles: list[ConsoleStatistics] = []

    for console, game_count in games_per_console.items():
        console_games = [
            game for game in games_data.values()
            if game["metadata"]["console"] == console
        ]

        biggest = None
        smallest = None

        if console_games:
            biggest_game = max(console_games, key=lambda g: g["metadata"]["size"])
            smallest_game = min(console_games, key=lambda g: g["metadata"]["size"])

            biggest = GameSize(
                name=biggest_game["original_name"],
                size=biggest_game["metadata"]["size"],
            )

            smallest = GameSize(
                name=smallest_game["original_name"],
                size=smallest_game["metadata"]["size"],
            )

        consoles.append(
            ConsoleStatistics(
                console=console,
                games=game_count,
                total_bytes=bytes_per_console.get(console, 0),
                biggest_game=biggest,
                smallest_game=smallest,
            )
        )

    consoles_by_games = sorted(consoles, key=lambda c: c.games, reverse=True)
    consoles_by_size = sorted(consoles, key=lambda c: c.total_bytes, reverse=True)

    return StatisticsSummary(
        total_games=sum(games_per_console.values()),
        total_bytes=sum(bytes_per_console.values()),
        total_consoles=len(games_per_console),
        consoles_by_games=consoles_by_games,
        consoles_by_size=consoles_by_size
    )