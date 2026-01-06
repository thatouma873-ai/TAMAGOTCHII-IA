# core/models.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


# =========================
# PERSONNALITÉ
# =========================
@dataclass
class Personality:
    """Traits de personnalité (0..100)."""
    playfulness: int = 50
    appetite: int = 50
    cleanliness: int = 50
    sociability: int = 50

    def clamp(self) -> None:
        """Empêche les valeurs de sortir de 0..100"""
        self.playfulness = max(0, min(100, self.playfulness))
        self.appetite = max(0, min(100, self.appetite))
        self.cleanliness = max(0, min(100, self.cleanliness))
        self.sociability = max(0, min(100, self.sociability))


# =========================
# APPARENCE
# =========================
@dataclass
class Appearance:
    species: str = "blob"
    color: str = "yellow"   # yellow / blue / pink

    size: str = "medium"    # small / medium / large
    weight: str = "normal"  # slim / normal / chubby

    outfit: str = "none"
    accessories: List[str] = field(default_factory=list)

    def describe(self) -> str:
        acc = ", ".join(self.accessories) if self.accessories else "aucun"
        return (
            f"{self.species} | couleur: {self.color} | "
            f"taille: {self.size} | poids: {self.weight} | "
            f"tenue: {self.outfit} | accessoires: {acc}"
        )
