from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from core.time_cycle import TimeCycle


@dataclass
class Suggestion:
    title: str
    reason: str
    priority: int


class AIMoodEngine:
    """
    IA simple qui suggère des actions au joueur
    en fonction des besoins du Tamagotchi.
    """

    def suggest(
        self,
        needs: Dict[str, int],
        health: int,
        time_cycle: TimeCycle
    ) -> List[Suggestion]:

        suggestions: List[Suggestion] = []

        if needs.get("hunger", 50) <= 20:
            suggestions.append(
                Suggestion("Manger", "La faim est très basse", 100)
            )

        if needs.get("energy", 50) <= 20:
            suggestions.append(
                Suggestion("Dormir", "Manque d'énergie", 90)
            )

        if needs.get("hygiene", 50) <= 20:
            suggestions.append(
                Suggestion("Se laver", "Hygiène insuffisante", 80)
            )

        if needs.get("social", 50) <= 20:
            suggestions.append(
                Suggestion("Socialiser", "Besoin social faible", 70)
            )

        if health <= 30:
            suggestions.append(
                Suggestion("Se reposer", "Santé faible", 110)
            )

        if time_cycle.is_night():
            suggestions.append(
                Suggestion("Dormir", "Il fait nuit", 60)
            )

        # Trier par priorité décroissante
        suggestions.sort(key=lambda s: s.priority, reverse=True)

        return suggestions
