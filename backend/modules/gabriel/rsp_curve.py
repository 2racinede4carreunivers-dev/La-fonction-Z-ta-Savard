"""
rsp_curve.py - Calcul d'une courbe d'evolution du rapport spectral
pour k = 1, 2, ..., k_max, avec rendu ASCII en terminal.

Configurations supportees :
  - "1x1"   : pour chaque k, paire (prime_k, prime_(k+1)) -> attendu 1/2
  - "sym"   : pour chaque k, deux blocs symetriques de taille k -> attendu 1/2
  - "chaos" : pour chaque k, A de taille k et B de taille k+2 chaotique
  - "ord"   : pour chaque k, A=(p1..pk) B=(p(k+1)..p(2k+1)) ordonne ->
              proche de 1 pour petit k, tend vers 1/2 quand k grandit
"""
from __future__ import annotations

from typing import Any, Optional
from fractions import Fraction

from ._primes_data import PRIMES_RAW

PRIMES: list[int] = list(PRIMES_RAW)


def SA(n: int) -> Fraction:
    """SA(n) = (3.25 / 2) * 2^n - 2"""
    return Fraction(13, 8) * Fraction(2) ** n - Fraction(2)


def SB(n: int) -> Fraction:
    """SB(n) = (6.5 / 2) * 2^n - 66"""
    return Fraction(13, 4) * Fraction(2) ** n - Fraction(66)


def ratio_1x1(n1: int, n2: int) -> Fraction:
    """RsP(n1, n2) = (SA(n1) - SA(n2)) / (SB(n1) - SB(n2))"""
    diff_a = SA(n1) - SA(n2)
    diff_b = SB(n1) - SB(n2)
    if diff_b == 0:
        raise ValueError("Division par zero dans le rapport spectral")
    return diff_a / diff_b


def sum_SA(indices: list[int]) -> Fraction:
    return sum((SA(i) for i in indices), Fraction(0))


def sum_SB(indices: list[int]) -> Fraction:
    return sum((SB(i) for i in indices), Fraction(0))


def compute_rsp_curve(
    config: str,
    k_max: int = 50,
) -> list[dict[str, Any]]:
    """
    Calcule le RsP pour k de 1 a k_max.
    Retourne une liste de dicts : [{'k': 1, 'RsP_decimal': 0.5, 'RsP_fraction': '1/2', ...}, ...]
    """
    points = []
    for k in range(1, k_max + 1):
        try:
            A, B = _build_config(config, k)
            r = _analyze_spectral_ratio(A, B)
            points.append({
                "k": k,
                "A": A, "B": B,
                "configuration": r.get("configuration", "?"),
                "RsP_fraction": r.get("RsP_fraction", "n/a"),
                "RsP_decimal": r.get("RsP_decimal", float("nan")),
                "matches_half": r.get("matches_half", False),
                "near_half": r.get("near_half", False),
                "error": r.get("error"),
            })
        except (ValueError, IndexError) as exc:
            points.append({"k": k, "error": str(exc)})
    return points


def _build_config(config: str, k: int) -> tuple[list[int], list[int]]:
    """Construit deux blocs A, B pour une config et un k donnes."""
    primes = PRIMES
    if config == "1x1":
        # paire (prime_k, prime_(k+1))
        if k + 1 > len(primes):
            raise IndexError(f"k+1 > {len(primes)}")
        return [primes[k - 1]], [primes[k]]
    if config == "sym":
        # A = k premiers a partir de position 1, B = k premiers a partir de position k+1
        if 2 * k > len(primes):
            raise IndexError(f"2k > {len(primes)}")
        return primes[:k], primes[k:2 * k]
    if config == "chaos":
        # A = k premiers, B = k+2 premiers decales
        if k + (k + 2) > len(primes):
            raise IndexError(f"taille trop grande")
        # ordre "chaotique" : inverser les blocs
        return list(reversed(primes[:k])), list(reversed(primes[k:k + k + 2]))
    if config == "ord":
        # A = primes[0..k-1], B = primes[k..2k] (croissants, |B|=|A|+1)
        if 2 * k + 1 > len(primes):
            raise IndexError(f"2k+1 > {len(primes)}")
        return primes[:k], primes[k:2 * k + 1]
    raise ValueError(f"Config inconnue : {config}")


def _analyze_spectral_ratio(A: list[int], B: list[int]) -> dict:
    """Analyse le rapport spectral pour les blocs A et B."""
    # Convertir en indices (positions 1-indexed)
    A_indices = []
    B_indices = []
    for p in A:
        try:
            idx = PRIMES.index(p) + 1
            A_indices.append(idx)
        except ValueError:
            pass
    for p in B:
        try:
            idx = PRIMES.index(p) + 1
            B_indices.append(idx)
        except ValueError:
            pass
    
    if not A_indices or not B_indices:
        return {"error": "Indices non trouves"}
    
    # Calcul du rapport
    if len(A_indices) == 1 and len(B_indices) == 1:
        configuration = "1x1"
        ratio = ratio_1x1(A_indices[0], B_indices[0])
    else:
        if len(A_indices) == len(B_indices):
            configuration = "symmetric_nxn"
        elif len(B_indices) == len(A_indices) + 1:
            configuration = "asymmetric_ordered"
        else:
            configuration = "asymmetric_chaotic"
        
        sa = sum_SA(A_indices)
        sb = sum_SB(B_indices)
        if sb == 0:
            return {"error": "Division par zero"}
        ratio = sa / sb
    
    ratio_decimal = float(ratio)
    expected = Fraction(1, 2)
    
    return {
        "configuration": configuration,
        "RsP_fraction": str(ratio),
        "RsP_decimal": ratio_decimal,
        "matches_half": ratio == expected,
        "near_half": abs(ratio_decimal - 0.5) < 0.01,
    }


def render_ascii_curve(
    points: list[dict[str, Any]],
    width: int = 60,
    height: int = 18,
    target: float = 0.5,
) -> str:
    """
    Rendu ASCII de la courbe k -> RsP_decimal avec ligne de reference target=0.5.
    """
    # Filtre les points valides
    valid = [(p["k"], p["RsP_decimal"]) for p in points
             if "RsP_decimal" in p and p.get("RsP_decimal") is not None
             and not (isinstance(p["RsP_decimal"], float) and p["RsP_decimal"] != p["RsP_decimal"])]  # NaN check
    if not valid:
        return "(aucun point valide a tracer)"

    ks = [k for k, _ in valid]
    vals = [v for _, v in valid]

    vmin = min(min(vals), target) - 0.05
    vmax = max(max(vals), target) + 0.05
    if vmax - vmin < 0.01:
        vmax = vmin + 0.1

    def y_to_row(v: float) -> int:
        # 0 = top, height-1 = bottom
        ratio = (vmax - v) / (vmax - vmin) if vmax != vmin else 0.5
        return max(0, min(height - 1, int(round(ratio * (height - 1)))))

    target_row = y_to_row(target)

    grid = [[" "] * width for _ in range(height)]
    # Ligne de reference y = 0.5
    for x in range(width):
        grid[target_row][x] = "."

    # Trace les points
    k_min, k_max_val = min(ks), max(ks)
    span_k = max(1, k_max_val - k_min)
    for k, v in valid:
        x = int(round((k - k_min) / span_k * (width - 1)))
        y = y_to_row(v)
        grid[y][x] = "*"

    # Construire le rendu avec axes
    lines = [f"  RsP (cible 1/2 = {target:.2f})"]
    for i, row in enumerate(grid):
        # Affiche la valeur a gauche pour quelques lignes
        if i == 0:
            label = f"{vmax:>5.3f} |"
        elif i == height - 1:
            label = f"{vmin:>5.3f} |"
        elif i == target_row:
            label = f"{target:>5.3f} +"
        else:
            label = "      |"
        lines.append(label + "".join(row))
    lines.append("      +" + "-" * width)
    lines.append(f"        k={k_min}" + " " * (width - 10) + f"k={k_max_val}")
    return "\n".join(lines)


def summarize_curve(points: list[dict[str, Any]]) -> str:
    """Resume statistique de la courbe."""
    valid = [p for p in points if "RsP_decimal" in p and not p.get("error")]
    if not valid:
        return "(aucun point valide)"
    exact = sum(1 for p in valid if p["matches_half"])
    near = sum(1 for p in valid if p["near_half"] and not p["matches_half"])
    far = len(valid) - exact - near
    vals = [p["RsP_decimal"] for p in valid]
    avg = sum(vals) / len(vals)
    return (
        f"Points calcules : {len(valid)}/{len(points)}\n"
        f"  exact 1/2     : {exact} ({100*exact/len(valid):.1f}%)\n"
        f"  proche 1/2    : {near} ({100*near/len(valid):.1f}%)\n"
        f"  eloigne 1/2   : {far} ({100*far/len(valid):.1f}%)\n"
        f"  moyenne RsP   : {avg:.4f}\n"
        f"  k=1 -> RsP    : {valid[0]['RsP_decimal']:.4f}\n"
        f"  k={valid[-1]['k']} -> RsP   : {valid[-1]['RsP_decimal']:.4f}"
    )


def generate_rsp_viz_data(config: str = "1x1", k_max: int = 50) -> dict:
    """
    Genere les donnees de visualisation pour la courbe RSP.
    Retourne un dict compatible avec le frontend.
    """
    points = compute_rsp_curve(config, k_max)
    ascii_render = render_ascii_curve(points)
    summary = summarize_curve(points)
    
    # Preparer donnees pour graphique frontend
    chart_data = []
    for p in points:
        if "RsP_decimal" in p and not p.get("error"):
            chart_data.append({
                "k": p["k"],
                "rsp": p["RsP_decimal"],
                "expected": 0.5,
                "matches": p.get("matches_half", False),
            })
    
    return {
        "config": config,
        "k_max": k_max,
        "points": points,
        "chart_data": chart_data,
        "ascii_curve": ascii_render,
        "summary": summary,
    }
