"""
GAP SOLVER CORRIGÉ - Formule EXACTE selon Philippe Thomas Savard.

=== FORMULE GÉNÉRALE ===
gap = (SA(n_suivant_min) - (SB(n_max) - Digamma(n_max)) - Digamma(n_min)) / 64

Où:
- n_min = position du PLUS PETIT premier (le plus négatif pour négatifs, le plus petit pour positifs)
- n_max = position du PLUS GRAND premier
- n_suivant_min = premier SUIVANT le plus petit:
    - Pour (+,+): vers +infini (7 -> suivant = 11)
    - Pour (-,-): vers zéro (-19 -> suivant = -17)
    - Pour (-,+): vers zéro (le négatif est le min)

=== EXEMPLES DE PHILIPPE ===

1. Écart entre 7 et 23 (cas +,+):
   - min=7 (pos 4), max=23 (pos 9), suivant_min=11 (pos 5)
   - SA(11) = 50
   - SB(23) = 1598, Digamma(23) = 126
   - SB(7) = -14, Digamma(7) = -462
   - gap = (50 - (1598 - 126) - (-462)) / 64 = (50 - 1472 + 462) / 64 = -960/64 = -15
   - Vérification: 8,9,10,11,12,13,14,15,16,17,18,19,20,21,22 = 15 nombres ✓

2. Écart entre -19 et -5 (cas -,-):
   - min=-19 (pos -8), max=-5 (pos -3), suivant_min=-17 (pos -7)
   - gap = -13
   - Vérification: -18,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6 = 13 nombres ✓

3. Écart entre -31 et 17 (cas -,+):
   - min=-31 (pos -11), max=17 (pos 7), suivant_min=-29 (pos -10)
   - gap = -47
   - Vérification: 30 (de -30 à -1) + 1 (zéro) + 16 (de 1 à 16) = 47 nombres ✓
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Optional
from fractions import Fraction

logger = logging.getLogger(__name__)

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


def nth_prime(n: int) -> int | None:
    """Retourne le n-ième nombre premier (1-indexed). 2 = 1er, 3 = 2e, etc."""
    if n < 1 or n > len(PRIMES):
        return None
    return PRIMES[n - 1]


def prime_position(p: int) -> int | None:
    """Retourne la position (1-indexed) du nombre premier p."""
    try:
        return PRIMES.index(p) + 1
    except ValueError:
        return None


def SA(n: int) -> Fraction:
    """
    Suite A pour la position n.
    SA(n) = (3.25/2) * 2^n - 2 = (13/8) * 2^n - 2
    
    Pour n négatif: SA(n) = 3.25 * 2^n - 2 (coefficient différent selon Philippe)
    """
    if n >= 0:
        return Fraction(13, 8) * Fraction(2 ** n) - Fraction(2)
    else:
        # Pour négatifs: 3.25 * 2^n - 2
        return Fraction(13, 4) * Fraction(2 ** n) - Fraction(2)


def SB(n: int) -> Fraction:
    """
    Suite B pour la position n.
    SB(n) = (6.5/2) * 2^n - 66 = (13/4) * 2^n - 66
    
    Pour n négatif: SB(n) = 6.5 * 2^n - 66
    """
    if n >= 0:
        return Fraction(13, 4) * Fraction(2 ** n) - Fraction(66)
    else:
        # Pour négatifs: 6.5 * 2^n - 66
        return Fraction(13, 2) * Fraction(2 ** n) - Fraction(66)


def digamma(n: int, p: int) -> Fraction:
    """
    Digamma calculé pour la position n et le premier p.
    digamma(n, p) = SB(n) - 64 * p
    """
    return SB(n) - Fraction(64) * Fraction(p)


@dataclass
class GapResult:
    """Resultat d'un calcul d'ecart."""
    p1: int
    p2: int
    gap_type: str
    
    pos_min: int
    pos_max: int
    pos_suivant_min: int
    
    p_min: int
    p_max: int
    p_suivant_min: int
    
    SA_suivant_min: float
    SB_max: float
    digamma_max: float
    SB_min: float
    digamma_min: float
    
    numerator: float
    gap_count: int
    gap_float: float
    arithmetic_gap: int
    
    formula_used: str
    explanation: str
    steps: list[str]
    
    def to_dict(self) -> dict:
        return {
            "p1": self.p1,
            "p2": self.p2,
            "gap_type": self.gap_type,
            # Clés attendues par gabriel_service.py
            "position_p1": self.pos_min if self.p1 == self.p_min else self.pos_max,
            "position_p2": self.pos_max if self.p2 == self.p_max else self.pos_min,
            "position_suivant_min": self.pos_suivant_min,
            # Anciennes clés conservées pour compatibilité
            "pos_min": self.pos_min,
            "pos_max": self.pos_max,
            "pos_suivant_min": self.pos_suivant_min,
            "p_min": self.p_min,
            "p_max": self.p_max,
            "p_suivant_min": self.p_suivant_min,
            "SA_suivant_min": self.SA_suivant_min,
            "SB_max": self.SB_max,
            "digamma_max": self.digamma_max,
            "SB_min": self.SB_min,
            "digamma_min": self.digamma_min,
            "numerator": self.numerator,
            "gap_count": self.gap_count,
            "gap_float": self.gap_float,
            "arithmetic_gap": self.arithmetic_gap,
            "formula_used": self.formula_used,
            "explanation": self.explanation,
            "steps": self.steps,
            # Sous-dictionnaire validation attendu par gabriel_service.py
            "validation": {
                "arithmetic_gap": self.arithmetic_gap,
                "spectral_gap": self.gap_count,
                "match": self.arithmetic_gap == self.gap_count
            }
        }


class GapSolver:
    """Résout les écarts avec la formule EXACTE de Philippe Thomas Savard."""
    
    def __init__(self):
        logger.info("GapSolver initialisé avec la formule corrigée de Philippe")
    
    def solve_gap(self, p1: int, p2: int) -> Optional[GapResult]:
        """
        Calcule l'écart entre deux nombres premiers.
        
        Formule: gap = (SA(suivant_min) - (SB(max) - Digamma(max)) - Digamma(min)) / 64
        """
        if p1 == p2:
            return None
        
        # Déterminer le type d'écart
        if p1 > 0 and p2 > 0:
            return self._solve_positive_positive(p1, p2)
        elif p1 < 0 and p2 < 0:
            return self._solve_negative_negative(p1, p2)
        else:
            return self._solve_mixed(p1, p2)
    
    def _solve_positive_positive(self, p1: int, p2: int) -> Optional[GapResult]:
        """Cas (+,+): Écart entre deux premiers positifs."""
        steps = []
        
        # Identifier min et max
        p_min = min(p1, p2)
        p_max = max(p1, p2)
        
        pos_min = prime_position(p_min)
        pos_max = prime_position(p_max)
        
        if pos_min is None or pos_max is None:
            return None
        
        steps.append(f"Plus petit premier: p_min = {p_min} (position n = {pos_min})")
        steps.append(f"Plus grand premier: p_max = {p_max} (position n = {pos_max})")
        
        # Premier SUIVANT le plus petit (vers +infini)
        pos_suivant_min = pos_min + 1
        p_suivant_min = nth_prime(pos_suivant_min)
        
        if p_suivant_min is None:
            return None
        
        steps.append(f"Premier suivant {p_min}: {p_suivant_min} (position n = {pos_suivant_min})")
        
        # Calculs
        sa_suivant = float(SA(pos_suivant_min))
        sb_max = float(SB(pos_max))
        dgm_max = float(digamma(pos_max, p_max))
        sb_min = float(SB(pos_min))
        dgm_min = float(digamma(pos_min, p_min))
        
        steps.append(f"")
        steps.append(f"=== CALCULS ===")
        steps.append(f"SA({pos_suivant_min}) = {sa_suivant}")
        steps.append(f"SB({pos_max}) = {sb_max}, Digamma({pos_max}, {p_max}) = {dgm_max}")
        steps.append(f"SB({pos_min}) = {sb_min}, Digamma({pos_min}, {p_min}) = {dgm_min}")
        
        # Formule: gap = (SA(suivant) - (SB(max) - Digamma(max)) - Digamma(min)) / 64
        terme1 = sa_suivant
        terme2 = sb_max - dgm_max
        terme3 = dgm_min
        
        numerator = terme1 - terme2 - terme3
        gap_float = numerator / 64
        gap_count = int(round(gap_float))
        
        steps.append(f"")
        steps.append(f"=== FORMULE ===")
        steps.append(f"gap = (SA(suivant) - (SB(max) - Digamma(max)) - Digamma(min)) / 64")
        steps.append(f"gap = ({sa_suivant} - ({sb_max} - {dgm_max}) - {dgm_min}) / 64")
        steps.append(f"gap = ({sa_suivant} - {terme2} - {dgm_min}) / 64")
        steps.append(f"gap = {numerator} / 64 = {gap_float}")
        
        arithmetic_gap = p_max - p_min - 1
        
        steps.append(f"")
        steps.append(f"=== RÉSULTAT ===")
        steps.append(f"Écart spectral: {abs(gap_count)} nombres entre {p_min} et {p_max}")
        steps.append(f"Écart arithmétique: {arithmetic_gap} nombres")
        
        return GapResult(
            p1=p1, p2=p2, gap_type="positive_positive",
            pos_min=pos_min, pos_max=pos_max, pos_suivant_min=pos_suivant_min,
            p_min=p_min, p_max=p_max, p_suivant_min=p_suivant_min,
            SA_suivant_min=sa_suivant, SB_max=sb_max, digamma_max=dgm_max,
            SB_min=sb_min, digamma_min=dgm_min,
            numerator=numerator, gap_count=abs(gap_count), gap_float=gap_float,
            arithmetic_gap=arithmetic_gap,
            formula_used="gap = (SA(n_suivant_min) - (SB(n_max) - Digamma(n_max)) - Digamma(n_min)) / 64",
            explanation=f"Écart entre {p_min} et {p_max}: {abs(gap_count)} nombres",
            steps=steps,
        )
    
    def _solve_negative_negative(self, p1: int, p2: int) -> Optional[GapResult]:
        """
        Cas (-,-): Écart entre deux premiers négatifs.
        
        IMPORTANT: Pour les négatifs, le "suivant" va vers ZÉRO!
        Exemple: suivant de -19 est -17 (pas -23)
        Séquence: ..., -19, -17, -13, -11, -7, -5, -3, -2 (vers zéro)
        """
        steps = []
        
        # Pour les négatifs: min = le PLUS négatif, max = le MOINS négatif
        # -19 < -5, donc min = -19, max = -5
        p_min = min(p1, p2)  # Le plus négatif (ex: -19)
        p_max = max(p1, p2)  # Le moins négatif (ex: -5)
        
        abs_min = abs(p_min)
        abs_max = abs(p_max)
        
        pos_min_abs = prime_position(abs_min)
        pos_max_abs = prime_position(abs_max)
        
        if pos_min_abs is None or pos_max_abs is None:
            return None
        
        # Positions négatives
        pos_min = -pos_min_abs  # ex: -8 pour -19
        pos_max = -pos_max_abs  # ex: -3 pour -5
        
        steps.append(f"Plus petit premier (plus négatif): p_min = {p_min} (position n = {pos_min})")
        steps.append(f"Plus grand premier (moins négatif): p_max = {p_max} (position n = {pos_max})")
        
        # Premier SUIVANT le plus petit (vers ZÉRO)
        # Si -19 est en position -8, le suivant est en position -7 (vers zéro)
        pos_suivant_min = pos_min + 1  # -8 + 1 = -7
        abs_suivant = pos_min_abs - 1  # Position absolue du suivant
        
        if abs_suivant < 1:
            return None
        
        p_suivant_min = -nth_prime(abs_suivant)  # ex: -17
        
        steps.append(f"Premier suivant {p_min} (vers zéro): {p_suivant_min} (position n = {pos_suivant_min})")
        
        # Calculs avec positions négatives
        sa_suivant = float(SA(pos_suivant_min))
        sb_max = float(SB(pos_max))
        dgm_max = float(digamma(pos_max, p_max))
        sb_min = float(SB(pos_min))
        dgm_min = float(digamma(pos_min, p_min))
        
        steps.append(f"")
        steps.append(f"=== CALCULS ===")
        steps.append(f"SA({pos_suivant_min}) = {sa_suivant}")
        steps.append(f"SB({pos_max}) = {sb_max}, Digamma({pos_max}, {p_max}) = {dgm_max}")
        steps.append(f"SB({pos_min}) = {sb_min}, Digamma({pos_min}, {p_min}) = {dgm_min}")
        
        # Formule identique
        terme1 = sa_suivant
        terme2 = sb_max - dgm_max
        terme3 = dgm_min
        
        numerator = terme1 - terme2 - terme3
        gap_float = numerator / 64
        gap_count = int(round(gap_float))
        
        steps.append(f"")
        steps.append(f"=== FORMULE ===")
        steps.append(f"gap = (SA(suivant) - (SB(max) - Digamma(max)) - Digamma(min)) / 64")
        steps.append(f"gap = ({sa_suivant} - ({sb_max} - {dgm_max}) - {dgm_min}) / 64")
        steps.append(f"gap = {numerator} / 64 = {gap_float}")
        
        # Pour négatifs: écart arithmétique = |p_max - p_min| - 1 = |-5 - (-19)| - 1 = 14 - 1 = 13
        arithmetic_gap = abs(p_max - p_min) - 1
        
        steps.append(f"")
        steps.append(f"=== RÉSULTAT ===")
        steps.append(f"Écart spectral: {abs(gap_count)} nombres entre {p_min} et {p_max}")
        steps.append(f"Écart arithmétique: {arithmetic_gap} nombres")
        
        return GapResult(
            p1=p1, p2=p2, gap_type="negative_negative",
            pos_min=pos_min, pos_max=pos_max, pos_suivant_min=pos_suivant_min,
            p_min=p_min, p_max=p_max, p_suivant_min=p_suivant_min,
            SA_suivant_min=sa_suivant, SB_max=sb_max, digamma_max=dgm_max,
            SB_min=sb_min, digamma_min=dgm_min,
            numerator=numerator, gap_count=abs(gap_count), gap_float=gap_float,
            arithmetic_gap=arithmetic_gap,
            formula_used="gap = (SA(n_suivant_min) - (SB(n_max) - Digamma(n_max)) - Digamma(n_min)) / 64",
            explanation=f"Écart entre {p_min} et {p_max}: {abs(gap_count)} nombres",
            steps=steps,
        )
    
    def _solve_mixed(self, p1: int, p2: int) -> Optional[GapResult]:
        """
        Cas (-,+): Écart entre un premier négatif et un positif.
        
        Le MINIMUM est toujours le négatif.
        Le SUIVANT du minimum va vers ZÉRO.
        """
        steps = []
        
        # Identifier négatif et positif
        if p1 < 0:
            p_neg, p_pos = p1, p2
        else:
            p_neg, p_pos = p2, p1
        
        # min = négatif, max = positif
        p_min = p_neg
        p_max = p_pos
        
        abs_min = abs(p_min)
        pos_min_abs = prime_position(abs_min)
        pos_max = prime_position(p_max)
        
        if pos_min_abs is None or pos_max is None:
            return None
        
        pos_min = -pos_min_abs
        
        steps.append(f"Premier négatif (minimum): p_min = {p_min} (position n = {pos_min})")
        steps.append(f"Premier positif (maximum): p_max = {p_max} (position n = {pos_max})")
        
        # Premier SUIVANT le négatif (vers ZÉRO)
        pos_suivant_min = pos_min + 1
        abs_suivant = pos_min_abs - 1
        
        if abs_suivant < 1:
            # Cas spécial: le suivant de -2 serait... on passe à 2
            p_suivant_min = 2
            pos_suivant_min = 1
        else:
            p_suivant_min = -nth_prime(abs_suivant)
        
        steps.append(f"Premier suivant {p_min} (vers zéro): {p_suivant_min} (position n = {pos_suivant_min})")
        
        # Calculs
        sa_suivant = float(SA(pos_suivant_min))
        sb_max = float(SB(pos_max))
        dgm_max = float(digamma(pos_max, p_max))
        sb_min = float(SB(pos_min))
        dgm_min = float(digamma(pos_min, p_min))
        
        steps.append(f"")
        steps.append(f"=== CALCULS ===")
        steps.append(f"SA({pos_suivant_min}) = {sa_suivant}")
        steps.append(f"SB({pos_max}) = {sb_max}, Digamma({pos_max}, {p_max}) = {dgm_max}")
        steps.append(f"SB({pos_min}) = {sb_min}, Digamma({pos_min}, {p_min}) = {dgm_min}")
        
        # Formule
        terme1 = sa_suivant
        terme2 = sb_max - dgm_max
        terme3 = dgm_min
        
        numerator = terme1 - terme2 - terme3
        gap_float = numerator / 64
        gap_count = int(round(gap_float))
        
        steps.append(f"")
        steps.append(f"=== FORMULE ===")
        steps.append(f"gap = (SA(suivant) - (SB(max) - Digamma(max)) - Digamma(min)) / 64")
        steps.append(f"gap = ({sa_suivant} - ({sb_max} - {dgm_max}) - {dgm_min}) / 64")
        steps.append(f"gap = {numerator} / 64 = {gap_float}")
        
        # Pour mixte: écart = |p_neg| + |p_pos| - 1 (en comptant le zéro)
        # Entre -31 et 17: 30 + 1 + 16 = 47
        arithmetic_gap = abs(p_neg) + p_pos - 1
        
        steps.append(f"")
        steps.append(f"=== RÉSULTAT ===")
        steps.append(f"Écart spectral: {abs(gap_count)} nombres entre {p_min} et {p_max}")
        steps.append(f"Écart arithmétique: {arithmetic_gap} nombres (incluant zéro)")
        
        return GapResult(
            p1=p1, p2=p2, gap_type="mixed",
            pos_min=pos_min, pos_max=pos_max, pos_suivant_min=pos_suivant_min,
            p_min=p_min, p_max=p_max, p_suivant_min=p_suivant_min,
            SA_suivant_min=sa_suivant, SB_max=sb_max, digamma_max=dgm_max,
            SB_min=sb_min, digamma_min=dgm_min,
            numerator=numerator, gap_count=abs(gap_count), gap_float=gap_float,
            arithmetic_gap=arithmetic_gap,
            formula_used="gap = (SA(n_suivant_min) - (SB(n_max) - Digamma(n_max)) - Digamma(n_min)) / 64",
            explanation=f"Écart mixte entre {p_min} et {p_max}: {abs(gap_count)} nombres",
            steps=steps,
        )


# Instance globale
_gap_solver_instance: Optional[GapSolver] = None


def get_gap_solver() -> GapSolver:
    """Récupère l'instance unique du GapSolver."""
    global _gap_solver_instance
    if _gap_solver_instance is None:
        _gap_solver_instance = GapSolver()
    return _gap_solver_instance


def compute_gap(p1: int, p2: int) -> Optional[dict]:
    """Fonction utilitaire pour calculer un écart."""
    solver = get_gap_solver()
    result = solver.solve_gap(p1, p2)
    if result:
        return result.to_dict()
    return None
