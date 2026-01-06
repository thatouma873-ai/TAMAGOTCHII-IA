 # core/needs.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Tuple

from core.time_cycle import TimeCycle
from core.models import Personality


class NeedStatus(Enum):
    OK = auto()
    LOW = auto()
    CRITICAL = auto()


def clamp_0_100(x: int) -> int:
    return max(0, min(100, int(x)))


@dataclass
class NeedThresholds:
    low: int = 35
    critical: int = 15


class NeedsSystem:
    """
    Gère les besoins du Tamagotchi.
    """

    def __init__(self, personality: Personality) -> None:
        self.personality = personality
        self.needs: Dict[str, int] = {
            "hunger": 80,
            "energy": 80,
            "hygiene": 80,
            "social": 80,
        }
        self.thresholds = NeedThresholds()
        self._critical_ticks: Dict[str, int] = {k: 0 for k in self.needs}

    def tick(self, elapsed_seconds: float, time_cycle: TimeCycle) -> None:
        minutes = elapsed_seconds / 60.0
        if minutes <= 0:
            return

        hunger_rate = 2.0 * (0.8 + self.personality.appetite / 100)
        energy_rate = 2.2
        hygiene_rate = 1.6 * (0.8 + self.personality.cleanliness / 100)
        social_rate = 1.8 * (0.8 + self.personality.sociability / 100)

        if time_cycle.is_night():
            energy_rate *= 0.6
            social_rate *= 0.8

        deltas = {
            "hunger": int(hunger_rate * minutes),
            "energy": int(energy_rate * minutes),
            "hygiene": int(hygiene_rate * minutes),
            "social": int(social_rate * minutes),
        }

        for k, d in deltas.items():
            self.needs[k] = clamp_0_100(self.needs[k] - d)

    def apply_action(self, action: str, strength: int = 20) -> None:
        s = max(1, strength)

        if action == "eat":
            self.needs["hunger"] = clamp_0_100(self.needs["hunger"] + s)
        elif action == "sleep":
            self.needs["energy"] = clamp_0_100(self.needs["energy"] + s)
        elif action == "wash":
            self.needs["hygiene"] = clamp_0_100(self.needs["hygiene"] + s)
        elif action == "play":
            self.needs["social"] = clamp_0_100(self.needs["social"] + s)
            self.needs["energy"] = clamp_0_100(self.needs["energy"] - s // 3)

    def get_need_statuses(self) -> Dict[str, NeedStatus]:
        out = {}
        for k, v in self.needs.items():
            if v <= self.thresholds.critical:
                out[k] = NeedStatus.CRITICAL
            elif v <= self.thresholds.low:
                out[k] = NeedStatus.LOW
            else:
                out[k] = NeedStatus.OK
        return out

    def apply_critical_consequences(self) -> Tuple[int, List[str]]:
        delta_health = 0
        alerts: List[str] = []

        for k, status in self.get_need_statuses().items():
            if status == NeedStatus.CRITICAL:
                self._critical_ticks[k] += 1
                penalty = 1 + self._critical_ticks[k] // 3
                delta_health -= penalty
                alerts.append(f"Besoin critique: {k}")

        return delta_health, alerts
