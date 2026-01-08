from core.helpers.filesystem import get_app_base_dir, format_bytes
from datetime import datetime
from core.logger import log

TITLE_LINE = "=" * 90
SECTION_LINE = "-" * 90

def create_statistics(data: dict[str, dict], logs: bool) -> None:
    games_per_console = data["games_per_console"]
    bytes_per_console = data["bytes_per_console"]
    games_data = data["games_data"]

    if logs: log(f"[STATISTICS TOOL]: Starting computation of data.")

    base_dir = get_app_base_dir() / "statistics"
    base_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    statistics_path = base_dir / f"statistics_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    total_games = sum(games_per_console.values())
    total_size_formatted = format_bytes(sum(bytes_per_console.values()))
    total_consoles = len(games_per_console)

    print("• Creating statistics from your collection... ", end="", flush=True)
    with open(statistics_path, "w") as f:

        f.write(f"{TITLE_LINE}\n")
        f.write("                                      ROMS STATISTICS\n")
        f.write(f"{TITLE_LINE}\n\n")

        f.write(f"Generated on : {now.strftime('%d/%m/%Y at %H:%M:%S')}\n\n")

        f.write("SUMMARY\n")
        f.write(f"{SECTION_LINE}\n")
        f.write(f"{'Total Games':<20} : {total_games}\n")
        f.write(f"{'Total Size':<20} : {total_size_formatted}\n")
        f.write(f"{'Consoles Analyzed':<20} : {total_consoles}\n\n")

        f.write(f"GAMES PER CONSOLE\n")
        f.write(f"{SECTION_LINE}\n")
        for i, (console, games) in enumerate(sorted(games_per_console.items(), key=lambda x: x[1], reverse=True), start=1):
            f.write(f"[{i:02}] {console:<35} : {games:>5} games\n")

        f.write(f"\nSTORAGE PER CONSOLE\n")
        f.write(f"{SECTION_LINE}\n")

        for i, (console, size) in enumerate(sorted(bytes_per_console.items(), key=lambda x: x[1], reverse=True), start=1):
            f.write(f"[{i:02}] {console:<65} : {format_bytes(size):>10}\n")

            console_games = [game for _, game in games_data.items() if game["metadata"]["console"] == console]

            if not console_games: 
                continue
            
            biggest = max(console_games, key=lambda x: x["metadata"]["size"])
            smallest = min(console_games, key=lambda x: x["metadata"]["size"])

            f.write(
                f"      Biggest game  : {biggest['original_name']:<55} "
                f"→ {format_bytes(biggest['metadata']['size']):>10}\n"
            )
            f.write(
                f"      Smallest game : {smallest['original_name']:<55} "
                f"→ {format_bytes(smallest['metadata']['size']):>10}\n\n"
            )

    print("DONE")
    print("• The file was created inside the 'statistics' folder.")
    if logs: log(f"[STATISTICS TOOL]: Statistics created and saved on 'statistics_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt'.")
    