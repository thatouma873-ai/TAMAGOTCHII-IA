from __future__ import annotations

import time
from typing import Optional

from core.models import Personality, Appearance
from core.needs import NeedsSystem
from core.moods import MoodEngine
from core.time_cycle import TimeCycle


class Pet:
    """
    Classe principale du Tamagotchi.
    Gère :
    - identité
    - besoins
    - humeur
    - santé
    - XP / niveau
    - pièces
    """

    def __init__(
        self,
        name: str,
        personality: Optional[Personality] = None,
        appearance: Optional[Appearance] = None,
        start_hour: int = 9,
    ) -> None:
        self.name = name

        # ===== PERSONNALITÉ & APPARENCE =====
        self.personality = personality if personality else Personality()
        self.personality.clamp()
        self.appearance = appearance if appearance else Appearance()

        # ===== STATS PRINCIPALES =====
        self.health = 100

        # 🔴 PIÈCES — DÉPART À 50 (OBLIGATOIRE)
        self.coins = 50

        self.level = 1
        self.xp = 0

        # ===== TEMPS & SYSTÈMES =====
        self.time_cycle = TimeCycle(start_hour=start_hour)
        self.needs_system = NeedsSystem(self.personality)
        self.mood_engine = MoodEngine()

        self.last_update_ts = time.time()
        self.mood = self.mood_engine.compute(
            self.needs_system.needs,
            self.health
        )

    # =======================
    # TEMPS / UPDATE
    # =======================
    def tick(self) -> None:
        now = time.time()
        elapsed = now - self.last_update_ts

        self.time_cycle.advance_seconds(elapsed)
        self.needs_system.tick(elapsed, self.time_cycle)

        delta_health, _ = self.needs_system.apply_critical_consequences()
        self.health = max(0, min(100, self.health + delta_health))

        self.mood = self.mood_engine.compute(
            self.needs_system.needs,
            self.health
        )
        self.last_update_ts = now

    # =======================
    # ACTIONS (LOGIQUE PURE)
    # ⚠️ LE COÛT EN PIÈCES
    # EST GÉRÉ DANS L'UI
    # =======================
    def eat(self) -> None:
        self.needs_system.apply_action("eat")
        self._update_mood()

    def sleep(self) -> None:
        self.needs_system.apply_action("sleep")
        self._update_mood()

    def wash(self) -> None:
        self.needs_system.apply_action("wash")
        self._update_mood()

    def play(self) -> None:
        self.needs_system.apply_action("play")
        self._update_mood()

    def _update_mood(self) -> None:
        self.mood = self.mood_engine.compute(
            self.needs_system.needs,
            self.health
        )

    # =======================
    # XP / NIVEAU
    # =======================
    def gain_xp(self, amount: int) -> None:
        amount = max(0, int(amount))
        self.xp += amount

        while self.xp >= self.level * 10:
            self.xp -= self.level * 10
            self.level += 1
            print(f"🎉 {self.name} passe niveau {self.level} !")

    # =======================
    # PIÈCES
    # =======================
    def add_coins(self, amount: int) -> None:
        """Ajoute des pièces (mini-jeux, récompenses…)"""
        self.coins += max(0, int(amount))

    def spend_coins(self, amount: int) -> bool:
        """Dépense des pièces si possible"""
        amount = max(0, int(amount))
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False

    # =======================
    # DEBUG / CONSOLE
    # =======================
    def print_status(self) -> None:
        n = self.needs_system.needs
        print(f"=== {self.name} ===")
        print(
            f"Heure: {self.time_cycle.hour:02d}:{self.time_cycle.minute:02d} "
            f"({self.time_cycle.get_period_label()})"
        )
        print(f"Santé: {self.health}/100")
        print(f"Niveau: {self.level} | XP: {self.xp} | Pièces: {self.coins}")
        print(
            f"Besoins: faim={n['hunger']} | énergie={n['energy']} "
            f"| hygiène={n['hygiene']} | social={n['social']}"
        )
        print(f"Apparence: {self.appearance.describe()}")
