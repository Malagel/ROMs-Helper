from core.statistics.models import StatisticsSummary 
from datetime import datetime
from pathlib import Path
from core.helpers.filesystem import format_bytes
TITLE_LINE = "=" * 90
SECTION_LINE = "-" * 90

def generate_statistics_file(summary: StatisticsSummary, statistics_path: Path,  generated_at: datetime) -> None:
    with statistics_path.open("w", encoding="utf-8") as f:
        f.write(f"{TITLE_LINE}\n")
        f.write("                                      ROMS STATISTICS\n")
        f.write(f"{TITLE_LINE}\n\n")

        f.write(f"Generated on : {generated_at.strftime('%d/%m/%Y at %H:%M:%S')}\n\n")

        f.write("SUMMARY\n")
        f.write(f"{SECTION_LINE}\n")
        f.write(f"{'Total Games':<20} : {summary.total_games}\n")
        f.write(f"{'Total Size':<20} : {format_bytes(summary.total_bytes)}\n")
        f.write(f"{'Consoles Analyzed':<20} : {summary.total_consoles}\n\n")

        f.write("GAMES PER CONSOLE\n")
        f.write(f"{SECTION_LINE}\n")
        for i, console in enumerate(summary.consoles_by_games, start=1):
            f.write(
                f"[{i:02}] {console.console:<35} : {console.games:>5} games\n"
            )

        f.write("\nSTORAGE PER CONSOLE\n")
        f.write(f"{SECTION_LINE}\n")
        for i, console in enumerate(summary.consoles_by_size, start=1):
            f.write(
                f"[{i:02}] {console.console:<65} : "
                f"{format_bytes(console.total_bytes):>10}\n"
            )

            if console.biggest_game:
                f.write(
                    f"      Biggest game  : {console.biggest_game.name:<55} "
                    f"→ {format_bytes(console.biggest_game.size):>10}\n"
                )

            if console.smallest_game:
                f.write(
                    f"      Smallest game : {console.smallest_game.name:<55} "
                    f"→ {format_bytes(console.smallest_game.size):>10}\n"
                )

            f.write("\n")