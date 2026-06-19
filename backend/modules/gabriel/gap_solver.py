"""
GAP SOLVER CORRECT FINAL - Formule EXACTE selon les calculs de Philippe Thomas Savard.

LA VRAIE FORMULE (issue des calculs pour -41 et -5) :

Ecart = (SA(n_suivant_du_PLUS_PETIT) - (SB(n_plus_petit) - dgm(n_plus_petit)) - (SB(n_plus_grand) - dgm(n_plus_grand))) / 64

Pour (-41, -5) :
  Plus petit = -41 (position -13)
  Plus grand = -5 (position -3)
  Premier SUIVANT -41 (vers zero) = -37 (position -12)
  
  Terme A = SA(-12) - (SB(-3) - dgm(-3))
           = -32755/16384 - (-320)
           = 5210125/16384
  
  Terme B = dgm(-13)
           = 41909773/16384
  
  Ecart = (5210125/16384 - 41909773/16384) / 64
        = -36699648/1048576
        ~ -35
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Optional
from fractions import Fraction

from ._primes_data import PRIMES_RAW

logger = logging.getLogger(__name__)

PRIMES: list[int] = list(PRIMES_RAW)


def nth_prime(n: int) -> int | None:
    if n < 1 or n > len(PRIMES):
        return None
    return PRIMES[n - 1]


def prime_position(p: int) -> int | None:
    try:
        return PRIMES.index(p) + 1
    except ValueError:
        return None


def max_position() -> int:
    return len(PRIMES)


@dataclass
class GapResult:
    """Resultat d'un calcul d'ecart."""
    p1: int
    p2: int
    gap_type: str
    
    position_p1: int
    position_p2: int
    position_suivant_min: int
    
    SA_suivant_min: float
    SB_min: float
    digamma_min: float
    SB_max: float
    digamma_max: float
    
    gap_count: int
    gap_float: float
    
    formula_used: str
    explanation: str
    validation: dict[str, Any]
    
    def to_dict(self) -> dict:
        return {
            "p1": self.p1,
            "p2": self.p2,
            "gap_type": self.gap_type,
            "position_p1": self.position_p1,
            "position_p2": self.position_p2,
            "position_suivant_min": self.position_suivant_min,
            "SA_suivant_min": self.SA_suivant_min,
            "SB_min": self.SB_min,
            "digamma_min": self.digamma_min,
            "SB_max": self.SB_max,
            "digamma_max": self.digamma_max,
            "gap_count": self.gap_count,
            "gap_float": self.gap_float,
            "formula_used": self.formula_used,
            "explanation": self.explanation,
            "validation": self.validation,
        }


class GapSolver:
    """Resout les ecarts avec la VRAIE formule spectrale."""
    
    def __init__(self):
        logger.info("GapSolver initialized with FINAL CORRECT formula")
    
    def solve_gap(self, p1: int, p2: int) -> Optional[GapResult]:
        """
        FORMULE FINALE :
        
        gap = (SA(n_suivant_min) - (SB(n_min) - dgm(n_min)) - (SB(n_max) - dgm(n_max))) / 64
        
        Ou :
          - n_min : position du nombre PLUS PETIT (en valeur absolue pour negatifs)
          - n_max : position du nombre PLUS GRAND
          - n_suivant_min : position du premier SUIVANT le minimum (vers +inf ou vers 0 si negatif)
        """
        if p1 > 0 and p2 > 0:
            return self._solve_positive_positive(p1, p2)
        elif p1 < 0 and p2 < 0:
            return self._solve_negative_negative(p1, p2)
        elif (p1 < 0 and p2 > 0) or (p1 > 0 and p2 < 0):
            return self._solve_mixed(p1, p2)
        else:
            return None
    
    def _solve_positive_positive(self, p1: int, p2: int) -> Optional[GapResult]:
        """CAS (+,+) : Entre deux premiers positifs."""
        logger.info(f"Solving gap (+,+) : p1={p1}, p2={p2}")
        
        # Identifier min et max
        p_min = min(p1, p2)
        p_max = max(p1, p2)
        
        pos_min = prime_position(p_min)
        pos_max = prime_position(p_max)
        
        if pos_min is None or pos_max is None:
            return None
        
        # Premier SUIVANT le plus petit (vers +inf) : position + 1
        pos_suivant_min = pos_min + 1
        
        sa_suivant_min = self._compute_SA(pos_suivant_min)
        sb_min = self._compute_SB(pos_min)
        digamma_min = self._compute_digamma_int(pos_min, p_min)
        
        sb_max = self._compute_SB(pos_max)
        digamma_max = self._compute_digamma_int(pos_max, p_max)
        
        # VRAIE FORMULE
        term_a = sa_suivant_min - (sb_min - digamma_min)
        term_b = sb_max - digamma_max
        gap_float = (term_a - term_b) / 64
        gap_count = int(round(gap_float))
        
        # Ecart arithmetique reel pour comparaison
        arithmetic_gap = p_max - p_min
        
        logger.info(f"(+,+) : ({term_a:.2f} - {term_b:.2f}) / 64 = {gap_float:.2f} -> {gap_count}")
        
        return GapResult(
            p1=p_min, p2=p_max, gap_type="positive_positive",
            position_p1=pos_min, position_p2=pos_max,
            position_suivant_min=pos_suivant_min,
            SA_suivant_min=sa_suivant_min, SB_min=sb_min, digamma_min=digamma_min,
            SB_max=sb_max, digamma_max=digamma_max,
            gap_count=gap_count, gap_float=gap_float,
            formula_used="gap = (SA(n_next_min) - (SB(n_min) - dgm(n_min)) - (SB(n_max) - dgm(n_max))) / 64",
            explanation=f"Entre {p_min} et {p_max} : ecart arithmetique = {arithmetic_gap}, calcul spectral = {gap_count}",
            validation={"source": "methode_spectral.thy::gap_positive_positive", "arithmetic_gap": arithmetic_gap},
        )
    
    def _solve_negative_negative(self, p1: int, p2: int) -> Optional[GapResult]:
        """CAS (-,-) : Entre deux premiers negatifs."""
        logger.info(f"Solving gap (-,-) : p1={p1}, p2={p2}")
        
        # Identifier min et max EN VALEUR
        # -41 < -5, donc min=-41, max=-5
        p_min = min(p1, p2)  # Le PLUS negatif
        p_max = max(p1, p2)  # Le MOINS negatif
        
        abs_min = abs(p_min)
        abs_max = abs(p_max)
        
        pos_min_abs = prime_position(abs_min)
        pos_max_abs = prime_position(abs_max)
        
        if pos_min_abs is None or pos_max_abs is None:
            logger.error(f"Cannot find positions for {abs_min} or {abs_max}")
            return None
        
        pos_min = -pos_min_abs
        pos_max = -pos_max_abs
        
        # Premier SUIVANT le plus petit (vers zero) : position + 1
        # Ex: -41 (pos -13) -> -37 (pos -12)
        pos_suivant_min = pos_min + 1
        
        sa_suivant_min = self._compute_SA_negative(pos_suivant_min)
        sb_min = self._compute_SB_negative(pos_min)
        digamma_min = self._compute_digamma_int_negative(pos_min, p_min)
        
        sb_max = self._compute_SB_negative(pos_max)
        digamma_max = self._compute_digamma_int_negative(pos_max, p_max)
        
        # VRAIE FORMULE (meme structure)
        term_a = sa_suivant_min - (sb_min - digamma_min)
        term_b = sb_max - digamma_max
        gap_float = (term_a - term_b) / 64
        gap_count = int(round(gap_float))
        
        # Ecart arithmetique reel
        arithmetic_gap = p_max - p_min
        
        logger.info(f"(-,-) : ({term_a:.6f} - {term_b:.6f}) / 64 = {gap_float:.2f} -> {gap_count}")
        
        return GapResult(
            p1=p_min, p2=p_max, gap_type="negative_negative",
            position_p1=pos_min, position_p2=pos_max,
            position_suivant_min=pos_suivant_min,
            SA_suivant_min=sa_suivant_min, SB_min=sb_min, digamma_min=digamma_min,
            SB_max=sb_max, digamma_max=digamma_max,
            gap_count=gap_count, gap_float=gap_float,
            formula_used="gap = (SA(n_next_min) - (SB(n_min) - dgm(n_min)) - (SB(n_max) - dgm(n_max))) / 64",
            explanation=f"Entre {p_min} et {p_max} : ecart arithmetique = {arithmetic_gap}, calcul spectral = {gap_count}",
            validation={"source": "methode_spectral.thy::gap_negative_negative", "arithmetic_gap": arithmetic_gap},
        )
    
    def _solve_mixed(self, p1: int, p2: int) -> Optional[GapResult]:
        """CAS (-,+) : Entre premier negatif et positif."""
        logger.info(f"Solving gap (-,+) MIXED : p1={p1}, p2={p2}")
        
        # Normaliser : p_min = negatif, p_max = positif
        if p1 < p2:
            p_min, p_max = p1, p2
        else:
            p_min, p_max = p2, p1
        
        abs_min = abs(p_min)
        pos_min_abs = prime_position(abs_min)
        pos_max = prime_position(p_max)
        
        if pos_min_abs is None or pos_max is None:
            return None
        
        pos_min = -pos_min_abs
        
        # Premier SUIVANT le plus petit (vers zero) : position + 1
        pos_suivant_min = pos_min + 1
        
        sa_suivant_min = self._compute_SA_negative(pos_suivant_min)
        sb_min = self._compute_SB_negative(pos_min)
        digamma_min = self._compute_digamma_int_negative(pos_min, p_min)
        
        sb_max = self._compute_SB(pos_max)
        digamma_max = self._compute_digamma_int(pos_max, p_max)
        
        # VRAIE FORMULE
        term_a = sa_suivant_min - (sb_min - digamma_min)
        term_b = sb_max - digamma_max
        gap_float = (term_a - term_b) / 64
        gap_count = int(round(gap_float))
        
        # Ecart arithmetique (passage par zero special)
        arithmetic_gap = p_max - p_min
        
        return GapResult(
            p1=p_min, p2=p_max, gap_type="mixed",
            position_p1=pos_min, position_p2=pos_max,
            position_suivant_min=pos_suivant_min,
            SA_suivant_min=sa_suivant_min, SB_min=sb_min, digamma_min=digamma_min,
            SB_max=sb_max, digamma_max=digamma_max,
            gap_count=gap_count, gap_float=gap_float,
            formula_used="gap = (SA(n_next_min) - (SB(n_min) - dgm(n_min)) - (SB(n_max) - dgm(n_max))) / 64 [MIXTE]",
            explanation=f"Entre {p_min} et {p_max} : ecart arithmetique = {arithmetic_gap}, calcul spectral = {gap_count} (ZERO SPECIAL)",
            validation={"source": "methode_spectral.thy::gap_mixed", "zero_special": True, "arithmetic_gap": arithmetic_gap},
        )
    
    # ========================================================================
    # HELPERS - Calculs spectraux
    # ========================================================================
    
    def _compute_SA(self, n: int) -> float:
        """SA(n) pour n positif : (3.25 / 2) * 2^n - 2"""
        return (3.25 / 2) * (2 ** n) - 2
    
    def _compute_SB(self, n: int) -> float:
        """SB(n) pour n positif : (6.5 / 2) * 2^n - 66"""
        return (6.5 / 2) * (2 ** n) - 66
    
    def _compute_SA_negative(self, n: int) -> float:
        """SA(n) pour n negatif : (3.25 / 2) * 2^n - 2"""
        return (3.25 / 2) * (2 ** n) - 2
    
    def _compute_SB_negative(self, n: int) -> float:
        """SB(n) pour n negatif : (6.5 / 2) * 2^n - 66"""
        return (6.5 / 2) * (2 ** n) - 66
    
    def _compute_digamma_int(self, n: int, p: int) -> float:
        """digamma_int(n, p) = SB(n) - 64*p"""
        sb = self._compute_SB(n)
        return sb - 64 * p
    
    def _compute_digamma_int_negative(self, n: int, p: int) -> float:
        """digamma_int(n, p) pour negatifs."""
        sb = self._compute_SB_negative(n)
        return sb - 64 * p


# Instance globale
_gap_solver_instance: Optional[GapSolver] = None


def get_gap_solver() -> GapSolver:
    """Recupere l'instance unique du GapSolver."""
    global _gap_solver_instance
    if _gap_solver_instance is None:
        _gap_solver_instance = GapSolver()
    return _gap_solver_instance


def compute_gap(p1: int, p2: int) -> Optional[dict]:
    """Fonction utilitaire pour calculer un ecart."""
    solver = get_gap_solver()
    result = solver.solve_gap(p1, p2)
    if result:
        return result.to_dict()
    return None
