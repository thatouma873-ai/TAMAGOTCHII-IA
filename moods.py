from dataclasses import dataclass
from typing import Dict


@dataclass
class MoodResult:
    label: str        # ex: "Heureux", "Triste"
    value: int        # 0–100
    message: str      # phrase affichable


def clamp_0_100(x: int) -> int:
    return max(0, min(100, int(x)))


class MoodEngine:
    """
    Calcule l'humeur globale du Tamagotchi
    à partir de ses besoins et de sa santé.
    """

    def compute(self, needs: Dict[str, int], health: int) -> MoodResult:
        # Moyenne des besoins
        avg_needs = sum(needs.values()) / len(needs)

        # Calcul pondéré (besoins + santé)
        mood_value = clamp_0_100(0.7 * avg_needs + 0.3 * health)

        # États critiques
        if health <= 20:
            return MoodResult(
                label="Malade",
                value=mood_value,
                message="Je ne me sens vraiment pas bien..."
            )

        # États normaux
        if mood_value >= 80:
            return MoodResult(
                label="Heureux",
                value=mood_value,
                message="Je suis trop content 😄"
            )
        elif mood_value >= 60:
            return MoodResult(
                label="Content",
                value=mood_value,
                message="Ça va plutôt bien 🙂"
            )
        elif mood_value >= 40:
            return MoodResult(
                label="Bof",
                value=mood_value,
                message="J'ai connu mieux..."
            )
        else:
            return MoodResult(
                label="Triste",
                value=mood_value,
                message="Je ne me sens pas bien 😢"
            )
