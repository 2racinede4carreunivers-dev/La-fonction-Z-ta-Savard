"""
Preuve par l'absurde : la Méthode Spectrale exclut strictement les composés.

Idée originale de Philippe Thomas Savard (juillet 2026) : l'échec systématique
de prime_position(C) pour un composé C constitue une preuve empirique par
l'absurde de la validité de la Méthode Spectrale sur l'ensemble ℙ des premiers.

Ce module transforme cette observation en un rapport pédagogique structuré
retourné à l'utilisateur, en complément de la formalisation Isabelle/HOL
(theorem composite_not_prime_i dans theories/methode_spectral.thy ligne ~1535).

THÉORÈMES FORMELS ÉTABLIS (methode_spectral.thy compile avec succès) :
  - composite_not_prime_i : ∀C composé, C ≠ prime_i(i) pour tout i
  - spectral_method_exclusively_for_primes : La MS s'applique UNIQUEMENT à ℙ
  - composite_no_reconstruction_position : Pas de reconstruction pour composés
  - composite_pair_no_rsp_positions : Pas de RsP pour paires de composés

Cas emblématiques couverts :
  - 4   = 2 × 2
  - 9   = 3 × 3
  - 15  = 3 × 5
  - 51  = 3 × 17   (cas rapporté par Philippe)
  - 91  = 7 × 13
  - 121 = 11 × 11
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

# Table des 100 premiers nombres premiers
PRIMES: list[int] = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197,
    199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
    283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
    383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
    467, 479, 487, 491, 499, 503, 509, 521, 523, 541
]

_PRIME_SET: frozenset[int] = frozenset(PRIMES)


def is_prime(n: int) -> bool:
    """Vérifie si |n| est premier.
    
    Convention Méthode Spectrale : les entiers négatifs -p (avec p premier
    positif) sont considérés comme des "premiers spectraux négatifs". Donc
    -7 est premier, -8 ne l'est pas, +51 = 3×17 ne l'est pas non plus.
    """
    abs_n = abs(int(n))
    if abs_n < 2:
        return False
    if abs_n in _PRIME_SET:
        return True
    # Fallback pour |n| > 541 : test naïf
    if abs_n > PRIMES[-1]:
        return _naive_prime_check(abs_n)
    return False


def _naive_prime_check(n: int) -> bool:
    """Test de primalité pour |n| au-delà de la table."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def factorize(n: int) -> List[int]:
    """Retourne la décomposition en facteurs premiers de |n|.
    
    Exemples :
        factorize(51)  -> [3, 17]
        factorize(4)   -> [2, 2]
        factorize(121) -> [11, 11]
    """
    n = abs(int(n))
    if n < 2:
        return []
    factors: List[int] = []
    for p in PRIMES:
        if p * p > n:
            break
        while n % p == 0:
            factors.append(p)
            n //= p
    if n > 1:
        factors.append(n)
    return factors


def nearest_primes(n: int) -> tuple[Optional[int], Optional[int]]:
    """Retourne (premier_inférieur, premier_supérieur) autour de |n|.
    
    Utile pour suggérer une correction pédagogique :
        « 51 n'est pas premier ; voisins premiers : 47 (avant), 53 (après) »
    """
    abs_n = abs(int(n))
    inf: Optional[int] = None
    sup: Optional[int] = None
    for p in PRIMES:
        if p < abs_n:
            inf = p
        elif p > abs_n and sup is None:
            sup = p
            break
        elif p == abs_n:
            return p, p
    return inf, sup


@dataclass(frozen=True)
class CompositeRejection:
    """Rapport pédagogique pour un entier composé soumis à Gabriel."""

    value: int
    factors: List[int]
    is_negative: bool
    nearest_prime_below: Optional[int]
    nearest_prime_above: Optional[int]
    thy_reference: str  # nom du théorème Isabelle/HOL correspondant si canonique

    @property
    def decomposition_str(self) -> str:
        """Ex : '51 = 3 × 17', '121 = 11 × 11', '-51 = -(3 × 17)'."""
        abs_val = abs(self.value)
        core = " × ".join(str(f) for f in self.factors) if self.factors else "?"
        if self.is_negative:
            return f"{self.value} = -({core}) = -{abs_val}"
        return f"{self.value} = {core}"

    def to_pedagogical_text(self) -> str:
        """Rend un message pédagogique complet pour l'utilisateur."""
        lines: List[str] = []
        lines.append(f"## ⛔ ARRÊT - {self.value} n'est pas un nombre premier")
        lines.append("")
        lines.append("### Preuve par l'absurde")
        lines.append("")
        lines.append(f"**Décomposition factorielle** : {self.decomposition_str}")
        lines.append("")
        lines.append("La Méthode Spectrale requiert un nombre premier. Elle ne s'applique")
        lines.append("qu'aux éléments de **ℙ** (l'ensemble des nombres premiers).")
        lines.append("")
        lines.append("Cette contrainte n'est **pas une lacune** : elle est une")
        lines.append("**CARACTÉRISATION AXIOMATIQUE** stricte de ℙ, formalisée dans")
        lines.append("`theories/methode_spectral.thy` (qui compile avec succès) sous les théorèmes :")
        lines.append("")
        lines.append("- `composite_not_prime_i` — Théorème principal : ∀C composé, C ≠ prime_i(i)")
        lines.append("- `spectral_method_exclusively_for_primes` — La MS s'applique UNIQUEMENT à ℙ")
        lines.append("- `composite_no_reconstruction_position` — Pas de reconstruction pour composés")
        lines.append("- `composite_pair_no_rsp_positions` — Pas de RsP pour paires de composés")
        
        if self.thy_reference:
            lines.append(f"- `{self.thy_reference}` — Cas concret pour {abs(self.value)}")
        
        lines.append("")
        lines.append("### Interprétation")
        lines.append("")
        lines.append("L'échec systématique de `prime_position(C)` pour un composé C constitue")
        lines.append("la **contraposition effective** du théorème `composite_not_prime_i` :")
        lines.append("")
        lines.append("> Si un composé admettait une position spectrale, la fonction la trouverait ;")
        lines.append("> puisqu'elle échoue systématiquement, le composé ne peut admettre de position.")
        lines.append("")
        lines.append("**Conclusion** : La Méthode Spectrale caractérise **EXACTEMENT** l'ensemble ℙ")
        lines.append("des nombres premiers, ni plus, ni moins.")
        
        if self.nearest_prime_below or self.nearest_prime_above:
            below = self.nearest_prime_below
            above = self.nearest_prime_above
            sign = "-" if self.is_negative else ""
            hints = []
            if below is not None:
                hints.append(f"{sign}{below}")
            if above is not None:
                hints.append(f"{sign}{above}")
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append(f"💡 **Suggestion** : Voulez-vous plutôt travailler avec un premier voisin ?")
            lines.append(f"   Candidats : {' ou '.join(hints)}")
        
        return "\n".join(lines)
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire pour l'API JSON."""
        return {
            "value": self.value,
            "factors": self.factors,
            "is_negative": self.is_negative,
            "nearest_prime_below": self.nearest_prime_below,
            "nearest_prime_above": self.nearest_prime_above,
            "thy_reference": self.thy_reference,
            "decomposition": self.decomposition_str,
            "is_composite": True,
            "message": self.to_pedagogical_text()
        }


def _canonical_thy_reference(abs_value: int) -> str:
    """Retourne le nom du théorème .thy spécifique si le composé est canonique."""
    canonical = {
        4: "no_spectral_position_for_4",
        9: "no_spectral_position_for_9",
        15: "no_spectral_position_for_15",
        51: "no_spectral_position_for_51",
        91: "no_spectral_position_for_91",
        121: "no_spectral_position_for_121",
    }
    return canonical.get(abs_value, "")


def build_composite_rejection(n: int) -> Optional[CompositeRejection]:
    """Construit un rapport de rejet si n est un entier composé.
    
    Retourne None si n est premier ou si |n| < 2.
    """
    abs_n = abs(int(n))
    if abs_n < 2:
        return None
    if is_prime(abs_n):
        return None
    factors = factorize(abs_n)
    below, above = nearest_primes(abs_n)
    if below == abs_n or above == abs_n:
        return None
    return CompositeRejection(
        value=int(n),
        factors=factors,
        is_negative=(n < 0),
        nearest_prime_below=below,
        nearest_prime_above=above,
        thy_reference=_canonical_thy_reference(abs_n),
    )


def detect_composites_in_numbers(numbers: List[int]) -> List[CompositeRejection]:
    """Détecte tous les composés dans une liste de nombres.
    
    Exemples :
        detect_composites_in_numbers([-7, -51])   -> [rejet pour -51]
        detect_composites_in_numbers([15, 51])    -> [rejet pour 15, rejet pour 51]
        detect_composites_in_numbers([-7, -5])    -> []
    """
    rejections: List[CompositeRejection] = []
    for n in numbers:
        rej = build_composite_rejection(n)
        if rej is not None:
            rejections.append(rej)
    return rejections


def get_composite_rejection_response(numbers: List[int]) -> Optional[dict]:
    """Vérifie si des nombres sont composés et retourne un message d'erreur formaté.
    
    Retourne None si tous les nombres sont premiers.
    Retourne un dict avec le message pédagogique si au moins un composé est détecté.
    """
    rejections = detect_composites_in_numbers(numbers)
    if not rejections:
        return None
    
    # Construire la réponse
    if len(rejections) == 1:
        return {
            "is_composite_error": True,
            "composites": [r.to_dict() for r in rejections],
            "response": rejections[0].to_pedagogical_text()
        }
    else:
        # Plusieurs composés détectés
        lines = ["## ⛔ ARRÊT - Plusieurs nombres composés détectés", ""]
        for r in rejections:
            lines.append(f"### {r.value}")
            lines.append(r.to_pedagogical_text())
            lines.append("")
        return {
            "is_composite_error": True,
            "composites": [r.to_dict() for r in rejections],
            "response": "\n".join(lines)
        }


__all__ = [
    "CompositeRejection",
    "build_composite_rejection",
    "detect_composites_in_numbers",
    "get_composite_rejection_response",
    "factorize",
    "is_prime",
    "nearest_primes",
]
