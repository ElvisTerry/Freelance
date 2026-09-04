

# src/generator/seed_generator.py

"""
INF232 - TP Statistiques
Génération déterministe d'une graine à partir
du nom du chef de groupe.

Conforme aux exigences de l'annexe.
"""

import unicodedata
class SeedGenerator:

    @staticmethod
    def normalize_name(full_name: str) -> str:
        """
        Transforme le nom :
        - suppression des accents
        - suppression des espaces
        - suppression des caractères spéciaux (ponctuation, symboles)
        - conservation des lettres ET des chiffres
        - passage en majuscules
        """
        text = unicodedata.normalize(
            "NFD",
            full_name
        )
        text = "".join(
            c
            for c in text
            if unicodedata.category(c) != "Mn"
        )
        text = "".join(
            c
            for c in text
            if c.isalnum()
        )
        return text.upper()

    @staticmethod
    def generate_seed(full_name: str) -> int:
        """
        Algorithme conçu par le groupe.

        seed =
        somme(
            position * ASCII²
        )

        puis réduction modulo 1 000 000.
        """

        normalized = SeedGenerator.normalize_name(
            full_name
        )

        seed = 0

        for i, char in enumerate(normalized):

            seed += (i + 1) * (ord(char) ** 2)

        return seed % 1_000_000


if __name__ == "__main__":

    chef = input(
        "Nom du chef : "
    )

    normalized = SeedGenerator.normalize_name(
        chef
    )

    seed = SeedGenerator.generate_seed(
        chef
    )

    print("\nChaîne normalisée :")
    print(normalized)

    print("\nSeed obtenue :")
    print(seed)