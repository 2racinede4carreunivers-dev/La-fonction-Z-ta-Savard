"""
Visualisations avancees pour Gabriel - Digamma et Rapport Spectral Asymetrique.

Deux graphiques principaux:
1. Digamma calcule pour n=1 a n=200
2. Rapport Spectral Asymetrique Ordonne (blocs A et B croissants)
"""
from __future__ import annotations

import logging
from typing import List, Dict, Any
from fractions import Fraction
from dataclasses import dataclass

from ._primes_data import PRIMES_RAW
from .spectral_models import get_model, Model_1_2

logger = logging.getLogger(__name__)

PRIMES: list[int] = list(PRIMES_RAW)


def nth_prime(n: int) -> int | None:
    """Retourne le n-ieme nombre premier (1-indexed)."""
    if n < 1 or n > len(PRIMES):
        return None
    return PRIMES[n - 1]


# =============================================================================
# GRAPHIQUE 1: DIGAMMA CALCULE (n=1 a n=200)
# =============================================================================

@dataclass
class DigammaDataPoint:
    """Point de donnees pour le graphique Digamma."""
    n: int              # Position
    p: int              # Nombre premier a cette position
    SA_value: float     # SA(n)
    SB_value: float     # SB(n)
    digamma: float      # digamma_calc(n, p) = SB(n) - 64*p
    
    def to_dict(self) -> dict:
        return {
            "n": self.n,
            "p": self.p,
            "SA": self.SA_value,
            "SB": self.SB_value,
            "digamma": self.digamma,
        }


def generate_digamma_curve_data(n_start: int = 1, n_end: int = 200) -> Dict[str, Any]:
    """
    Genere les donnees du graphique Digamma calcule.
    
    Criteres:
    - Valeurs du digamma calcule pour n=1 a n=200
    - Courbe donnant la valeur du Digamma calcule pour chaque n
    
    Formule: digamma_calc(n, p) = SB(n) - 64 * p
    """
    model = get_model("1/2")
    n_end = min(n_end, len(PRIMES))
    
    data_points: List[Dict] = []
    
    for n in range(n_start, n_end + 1):
        p = nth_prime(n)
        if p is None:
            continue
        
        SA_val = float(model.A(n))
        SB_val = float(model.B(n))
        digamma_val = float(model.digamma(n, p))
        
        data_points.append({
            "n": n,
            "p": p,
            "SA": SA_val,
            "SB": SB_val,
            "digamma": digamma_val,
        })
    
    # Statistiques
    digamma_values = [d["digamma"] for d in data_points]
    
    return {
        "type": "digamma_curve",
        "title": f"Digamma calcule pour n={n_start} a n={n_end}",
        "description": "Courbe du digamma_calc(n, p) = SB(n) - 64*p pour chaque position n",
        "formula": "digamma_calc(n, p) = SB(n) - 64 × p",
        "data": data_points,
        "stats": {
            "n_start": n_start,
            "n_end": n_end,
            "count": len(data_points),
            "digamma_min": min(digamma_values) if digamma_values else 0,
            "digamma_max": max(digamma_values) if digamma_values else 0,
        },
        "x_axis": "Position n",
        "y_axis": "Digamma calcule",
    }


# =============================================================================
# GRAPHIQUE 2: RAPPORT SPECTRAL ASYMETRIQUE ORDONNE
# =============================================================================

@dataclass 
class AsymmetricPair:
    """Paire de blocs A et B pour le rapport asymetrique."""
    pair_index: int           # Index de la paire (1, 2, 3, ...)
    block_A: List[int]        # Nombres premiers du bloc A
    block_B: List[int]        # Nombres premiers du bloc B
    size_A: int               # Taille du bloc A
    size_B: int               # Taille du bloc B (= size_A + 1)
    sum_SA_A: float           # Somme SA pour bloc A
    sum_SB_A: float           # Somme SB pour bloc A
    sum_SA_B: float           # Somme SA pour bloc B
    sum_SB_B: float           # Somme SB pour bloc B
    ratio: float              # Rapport spectral (sum_SA_A - sum_SA_B) / (sum_SB_A - sum_SB_B)
    expected_ratio: float     # Ratio attendu (1/2)
    
    def to_dict(self) -> dict:
        return {
            "pair_index": self.pair_index,
            "block_A": self.block_A,
            "block_B": self.block_B,
            "size_A": self.size_A,
            "size_B": self.size_B,
            "sum_SA_A": self.sum_SA_A,
            "sum_SB_A": self.sum_SB_A,
            "sum_SA_B": self.sum_SA_B,
            "sum_SB_B": self.sum_SB_B,
            "ratio": self.ratio,
            "expected_ratio": self.expected_ratio,
            "delta": abs(self.ratio - self.expected_ratio),
            "is_converged": abs(self.ratio - self.expected_ratio) < 0.001,
        }


def generate_asymmetric_ordered_data(num_pairs: int = 100) -> Dict[str, Any]:
    """
    Genere les donnees du graphique Rapport Spectral Asymetrique Ordonne.
    
    Criteres:
    - Blocs A et B en configuration asymetrique ordonnee
    - Bloc B = A + 1 terme
    - Ordre croissant chronologique des nombres premiers positifs
    
    Exemples:
    - Paire 1: A=[2], B=[3,5]
    - Paire 2: A=[2,3], B=[5,7,11]
    - Paire 3: A=[2,3,5], B=[7,11,13,17]
    - Paire 4: A=[2,3,5,7], B=[11,13,17,19,23]
    """
    model = get_model("1/2")
    
    # S'assurer qu'on a assez de premiers
    max_primes_needed = sum(range(1, num_pairs + 1)) + sum(range(2, num_pairs + 2))
    if max_primes_needed > len(PRIMES):
        num_pairs = min(num_pairs, 100)  # Limiter si necessaire
    
    pairs_data: List[Dict] = []
    current_prime_index = 0  # Index dans la liste PRIMES
    
    for pair_idx in range(1, num_pairs + 1):
        size_A = pair_idx
        size_B = pair_idx + 1
        
        # Verifier qu'on a assez de premiers
        total_needed = size_A + size_B
        if current_prime_index + total_needed > len(PRIMES):
            break
        
        # Construire bloc A (premiers nombres premiers consecutifs)
        block_A = PRIMES[current_prime_index:current_prime_index + size_A]
        positions_A = list(range(current_prime_index + 1, current_prime_index + size_A + 1))
        
        # Construire bloc B (nombres premiers suivants)
        block_B = PRIMES[current_prime_index + size_A:current_prime_index + size_A + size_B]
        positions_B = list(range(current_prime_index + size_A + 1, current_prime_index + size_A + size_B + 1))
        
        # Calculer les sommes spectrales
        sum_SA_A = sum(float(model.A(pos)) for pos in positions_A)
        sum_SB_A = sum(float(model.B(pos)) for pos in positions_A)
        sum_SA_B = sum(float(model.A(pos)) for pos in positions_B)
        sum_SB_B = sum(float(model.B(pos)) for pos in positions_B)
        
        # Calculer le rapport spectral
        numerator = sum_SA_A - sum_SA_B
        denominator = sum_SB_A - sum_SB_B
        
        if denominator != 0:
            ratio = numerator / denominator
        else:
            ratio = 0.0
        
        pair_data = {
            "pair_index": pair_idx,
            "block_A": block_A,
            "block_B": block_B,
            "block_A_str": "-".join(map(str, block_A)),
            "block_B_str": "-".join(map(str, block_B)),
            "size_A": size_A,
            "size_B": size_B,
            "positions_A": positions_A,
            "positions_B": positions_B,
            "sum_SA_A": sum_SA_A,
            "sum_SB_A": sum_SB_A,
            "sum_SA_B": sum_SA_B,
            "sum_SB_B": sum_SB_B,
            "ratio": ratio,
            "expected_ratio": 0.5,
            "delta": abs(ratio - 0.5),
            "is_converged": abs(ratio - 0.5) < 0.001,
        }
        
        pairs_data.append(pair_data)
        
        # Avancer au prochain groupe de premiers
        current_prime_index += size_A + size_B
    
    # Statistiques de convergence
    ratios = [p["ratio"] for p in pairs_data]
    deltas = [p["delta"] for p in pairs_data]
    converged_count = sum(1 for p in pairs_data if p["is_converged"])
    
    return {
        "type": "asymmetric_ordered",
        "title": f"Rapport Spectral Asymetrique Ordonne - {len(pairs_data)} paires",
        "description": "Blocs A et B en configuration asymetrique ordonnee (B = A + 1 terme)",
        "formula": "RsP = (sum_SA(A) - sum_SA(B)) / (sum_SB(A) - sum_SB(B))",
        "expected": "1/2 = 0.5",
        "data": pairs_data,
        "stats": {
            "num_pairs": len(pairs_data),
            "ratio_min": min(ratios) if ratios else 0,
            "ratio_max": max(ratios) if ratios else 0,
            "ratio_mean": sum(ratios) / len(ratios) if ratios else 0,
            "delta_min": min(deltas) if deltas else 0,
            "delta_max": max(deltas) if deltas else 0,
            "converged_count": converged_count,
            "convergence_rate": converged_count / len(pairs_data) if pairs_data else 0,
        },
        "x_axis": "Index de paire (k)",
        "y_axis_ratio": "Rapport spectral RsP",
        "y_axis_sums": "Sommes SA et SB",
    }


def generate_asymmetric_sums_data(num_pairs: int = 100) -> Dict[str, Any]:
    """
    Genere les donnees des sommes des blocs A et B pour visualisation.
    
    Retourne les courbes des valeurs des sommes SA et SB pour chaque bloc.
    """
    asymmetric_data = generate_asymmetric_ordered_data(num_pairs)
    
    # Extraire les donnees de sommes pour graphique
    sums_data = []
    for pair in asymmetric_data["data"]:
        sums_data.append({
            "k": pair["pair_index"],
            "sum_SA_A": pair["sum_SA_A"],
            "sum_SB_A": pair["sum_SB_A"],
            "sum_SA_B": pair["sum_SA_B"],
            "sum_SB_B": pair["sum_SB_B"],
            "ratio": pair["ratio"],
            "size_A": pair["size_A"],
            "size_B": pair["size_B"],
        })
    
    return {
        "type": "asymmetric_sums",
        "title": "Sommes spectrales des blocs A et B",
        "description": "Evolution des sommes SA et SB a mesure que les blocs grandissent",
        "data": sums_data,
        "pairs_details": asymmetric_data["data"][:10],  # 10 premieres paires en detail
        "stats": asymmetric_data["stats"],
    }


# =============================================================================
# FONCTION COMBINEE POUR API
# =============================================================================

def get_advanced_visualization_data(viz_type: str, **kwargs) -> Dict[str, Any]:
    """
    Point d'entree pour recuperer les donnees de visualisation avancee.
    
    Args:
        viz_type: "digamma" | "asymmetric_ordered" | "asymmetric_sums"
        **kwargs: Parametres additionnels (n_start, n_end, num_pairs)
    
    Returns:
        Donnees formatees pour le frontend
    """
    if viz_type == "digamma":
        n_start = kwargs.get("n_start", 1)
        n_end = kwargs.get("n_end", 200)
        return generate_digamma_curve_data(n_start, n_end)
    
    elif viz_type == "asymmetric_ordered":
        num_pairs = kwargs.get("num_pairs", 100)
        return generate_asymmetric_ordered_data(num_pairs)
    
    elif viz_type == "asymmetric_sums":
        num_pairs = kwargs.get("num_pairs", 100)
        return generate_asymmetric_sums_data(num_pairs)
    
    else:
        return {"error": f"Type de visualisation inconnu: {viz_type}"}
