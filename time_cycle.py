# core/time_cycle.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class TimeCycle:
    """
    Gère le temps du jeu (jour/nuit).
    """

    start_hour: int = 9
    hour: int = 9
    minute: int = 0
    minutes_per_real_second: float = 1.0

    def __post_init__(self) -> None:
        self.hour = int(self.start_hour) % 24
        self.minute = 0

    def advance_seconds(self, elapsed_seconds: float) -> None:
        if elapsed_seconds <= 0:
            return
        add_minutes = int(elapsed_seconds * self.minutes_per_real_second)
        total_minutes = (self.hour * 60 + self.minute + add_minutes) % (24 * 60)
        self.hour = total_minutes // 60
        self.minute = total_minutes % 60

    def is_night(self) -> bool:
        return self.hour >= 22 or self.hour < 6

    def get_period_label(self) -> str:
        return "Nuit" if self.is_night() else "Jour"

    def to_dict(self) -> Dict[str, object]:
        return {
            "hour": self.hour,
            "minute": self.minute,
            "minutes_per_real_second": self.minutes_per_real_second,
        }

    def load_from_dict(self, d: Dict[str, object]) -> None:
        self.hour = int(d.get("hour", self.hour)) % 24
        self.minute = int(d.get("minute", self.minute)) % 60
        self.minutes_per_real_second = float(
            d.get("minutes_per_real_second", self.minutes_per_real_second)
        )
