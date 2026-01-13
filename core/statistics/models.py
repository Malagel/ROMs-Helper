from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class GameSize:
    name: str
    size: int

@dataclass(frozen=True)
class ConsoleStatistics:
    console: str
    games: int
    total_bytes: int
    biggest_game: Optional[GameSize]
    smallest_game: Optional[GameSize]


@dataclass(frozen=True)
class StatisticsSummary:
    total_games: int
    total_bytes: int
    total_consoles: int
    consoles_by_games: list[ConsoleStatistics]
    consoles_by_size: list[ConsoleStatistics]

