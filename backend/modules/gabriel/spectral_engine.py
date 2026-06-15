"""
Moteur de calcul spectral - adapte de l'agent Gabriel (Philippe Thomas Savard).
Contient: suites SA/SB, digamma, verification premiers, ecarts, rapports spectraux.
Table des 1000 premiers nombres premiers (2 a 7919).
"""
from __future__ import annotations
from fractions import Fraction
from enum import Enum
from ._primes_data import PRIMES_RAW

# ===================== Table des nombres premiers =====================

PRIMES: list[int] = list(PRIMES_RAW)


def nth_prime(n: int):
    if n < 1 or n > len(PRIMES):
        return None
    return PRIMES[n - 1]


def prime_position(p: int):
    try:
        return PRIMES.index(p) + 1
    except ValueError:
        return None


def is_known_prime(p: int) -> bool:
    return p in PRIMES


def max_position() -> int:
    return len(PRIMES)


# ===================== Enums =====================

class GapKind(str, Enum):
    POS_POS = "++"
    NEG_NEG = "--"
    NEG_POS = "-+"


class AsymmetryKind(str, Enum):
    SYM_1x1 = "symmetric_1x1"
    SYM_NxN = "symmetric_nxn"
    ASYM_ORDERED = "asymmetric_ordered"
    ASYM_CHAOTIC = "asymmetric_chaotic"


# ===================== Suites spectrales =====================

def SA(n: int) -> Fraction:
    return Fraction(13, 8) * Fraction(2) ** n - Fraction(2)

def SB(n: int) -> Fraction:
    return Fraction(13, 4) * Fraction(2) ** n - Fraction(66)


# ===================== Suites spectrales NEGATIVES (n <= -1) =====================

def SA_neg(n: int) -> Fraction:
    """SA pour positions negatives: 3.25 * 2^n - 2 (n <= -1)"""
    return Fraction(13, 4) * Fraction(2) ** n - Fraction(2)

def SB_neg(n: int) -> Fraction:
    """SB pour positions negatives: 6.5 * 2^n - 66 (n <= -1)"""
    return Fraction(13, 2) * Fraction(2) ** n - Fraction(66)

def neg_nth_prime(n: int):
    """Retourne le n-ieme nombre premier negatif. n doit etre negatif (ex: -7 -> -17)."""
    pos = abs(n)
    p = nth_prime(pos)
    return -p if p is not None else None

def verify_neg_prime_equation(n: int, p: int) -> dict:
    """Verifie l'equation spectrale pour un premier negatif (n <= -1)."""
    sa_val = SA_neg(n)
    sb_val = SB_neg(n)
    dgm = sb_val - Fraction(64) * Fraction(p)
    reconstructed = (sb_val - dgm) / Fraction(64)
    return {
        "model": "1/2 (negatif)",
        "n": n, "p": p,
        "SA_neg": float(sa_val),
        "SB_neg": float(sb_val),
        "digamma_calc": float(dgm),
        "reconstructed_p": float(reconstructed),
        "equation_holds": reconstructed == Fraction(p),
    }

def analyze_neg_prime(n: int) -> dict:
    """Analyse spectrale complete d'un nombre premier negatif."""
    pos = abs(n)
    p_pos = nth_prime(pos)
    if p_pos is None:
        return {"error": f"Position {n} hors table (max: {max_position()})"}
    p_neg = -p_pos
    v = verify_neg_prime_equation(n, p_neg)
    neighbors = {}
    if pos > 1:
        neighbors["precedent"] = {"prime": -nth_prime(pos - 1), "position": -(pos - 1)}
    if pos < max_position():
        neighbors["suivant"] = {"prime": -nth_prime(pos + 1), "position": -(pos + 1)}
    return {"prime": p_neg, "position": n, "models": {"neg_1/2": v}, "neighbors": neighbors}

def A_1_3(n: int) -> Fraction:
    return Fraction(73, 9 * 12) * Fraction(3) ** n - Fraction(3, 2)

def B_1_3(n: int) -> Fraction:
    return Fraction(219, 9 * 12) * Fraction(3) ** n - Fraction(487 * 3, 2)

def A_1_4(n: int) -> Fraction:
    return Fraction(241, 16 * 12) * Fraction(4) ** n - Fraction(4, 3)

def B_1_4(n: int) -> Fraction:
    return Fraction(964, 16 * 12) * Fraction(4) ** n - Fraction(3073 * 4, 3)

def SA_mix(n: int) -> Fraction:
    return Fraction(48) + Fraction(13, 2 ** (n + 2))

def SB_mix(n: int) -> Fraction:
    return Fraction(-28) + Fraction(13, 2 ** (n + 1))

def sum_SA(indices):
    return sum((SA(i) for i in indices), Fraction(0))

def sum_SB(indices):
    return sum((SB(i) for i in indices), Fraction(0))

SUITES_BY_MODEL = {
    "1/2": {"A": SA, "B": SB, "sumA": sum_SA, "sumB": sum_SB, "base": 2, "factor": 64},
    "1/3": {"A": A_1_3, "B": B_1_3, "sumA": lambda i: sum((A_1_3(x) for x in i), Fraction(0)), "sumB": lambda i: sum((B_1_3(x) for x in i), Fraction(0)), "base": 3, "factor": 729},
    "1/4": {"A": A_1_4, "B": B_1_4, "sumA": lambda i: sum((A_1_4(x) for x in i), Fraction(0)), "sumB": lambda i: sum((B_1_4(x) for x in i), Fraction(0)), "base": 4, "factor": 4096},
}

def get_suite_functions(model: str) -> dict:
    if model not in SUITES_BY_MODEL:
        raise ValueError(f"Modele spectral inconnu : {model}. Choix : {list(SUITES_BY_MODEL)}")
    return SUITES_BY_MODEL[model]


# ===================== Digamma et equation du premier =====================

def digamma_calc(n: int, p: int, model: str = "1/2") -> Fraction:
    fns = get_suite_functions(model)
    return fns["B"](n) - fns["factor"] * p

def prime_equation(n: int, p: int, model: str = "1/2") -> Fraction:
    fns = get_suite_functions(model)
    return (fns["B"](n) - digamma_calc(n, p, model)) / fns["factor"]

def verify_prime_equation(n: int, p: int, model: str = "1/2") -> dict:
    fns = get_suite_functions(model)
    A_val = fns["A"](n)
    B_val = fns["B"](n)
    dgm = digamma_calc(n, p, model)
    reconstructed = prime_equation(n, p, model)
    return {
        "model": model, "n": n, "p": p,
        "base": fns["base"], "factor": fns["factor"],
        "SA": float(A_val), "SB": float(B_val),
        "digamma_calc": float(dgm),
        "reconstructed_p": float(reconstructed),
        "equation_holds": reconstructed == Fraction(p),
    }


# ===================== Rapport spectral (4 configurations) =====================

def ratio_1x1(n1: int, n2: int, model: str = "1/2") -> Fraction:
    fns = get_suite_functions(model)
    return (fns["A"](n1) - fns["A"](n2)) / (fns["B"](n1) - fns["B"](n2))

def ratio_nxn(A_indices, B_indices, model: str = "1/2") -> Fraction:
    fns = get_suite_functions(model)
    sum_a = fns["sumA"](A_indices)
    sum_b = fns["sumB"](B_indices)
    if sum_b == 0:
        raise ValueError("Somme des B nulle : division impossible.")
    return sum_a / sum_b

def detect_configuration(A_indices, B_indices) -> AsymmetryKind:
    if len(A_indices) == 1 and len(B_indices) == 1:
        return AsymmetryKind.SYM_1x1
    if len(A_indices) == len(B_indices):
        return AsymmetryKind.SYM_NxN
    if (len(B_indices) == len(A_indices) + 1 and
        A_indices == sorted(set(A_indices)) and
        B_indices == sorted(set(B_indices)) and
        all(i > 0 for i in A_indices + B_indices) and
        A_indices[-1] < B_indices[0]):
        return AsymmetryKind.ASYM_ORDERED
    return AsymmetryKind.ASYM_CHAOTIC

def compute_spectral_ratio(A_indices, B_indices, model: str = "1/2") -> dict:
    config = detect_configuration(A_indices, B_indices)
    fns = get_suite_functions(model)
    if config == AsymmetryKind.SYM_1x1:
        ratio = ratio_1x1(A_indices[0], B_indices[0], model)
    else:
        ratio = ratio_nxn(A_indices, B_indices, model)
    k = int(model.split("/")[1])
    expected = Fraction(1, k)
    return {
        "model": model, "configuration": config.value,
        "A_indices": A_indices, "B_indices": B_indices,
        "ratio": float(ratio), "expected": float(expected),
        "matches_expected": ratio == expected,
    }


# ===================== Ecarts entre premiers =====================

def gap_equation(A_next, B_high, D_high, D_low, model: str = "1/3") -> Fraction:
    fns = get_suite_functions(model)
    return (Fraction(A_next) - (Fraction(B_high) - Fraction(D_high)) - Fraction(D_low)) / fns["factor"]

def compute_gap(p_high: int, p_low: int, A_next, B_high, D_high, D_low, model: str = "1/3") -> dict:
    kind = GapKind.POS_POS if p_high >= 0 and p_low >= 0 else (GapKind.NEG_NEG if p_high <= 0 and p_low <= 0 else GapKind.NEG_POS)
    gap = gap_equation(A_next, B_high, D_high, D_low, model)
    return {
        "kind": kind.value, "model": model,
        "p_high": p_high, "p_low": p_low,
        "gap": float(gap), "expected_gap": p_low - p_high,
    }


# ===================== Analyse automatique d'un nombre premier =====================

def analyze_prime(p: int) -> dict:
    """Analyse spectrale complete d'un nombre premier."""
    pos = prime_position(p)
    if pos is None:
        return {"error": f"{p} n'est pas un nombre premier connu (table: 2-7919)"}

    result = {"prime": p, "position": pos, "models": {}}

    # Rapport 1/2 (modele principal)
    v = verify_prime_equation(pos, p, "1/2")
    result["models"]["1/2"] = v

    # Table: premiers voisins
    neighbors = {}
    if pos > 1:
        neighbors["precedent"] = {"prime": nth_prime(pos - 1), "position": pos - 1}
    if pos < max_position():
        neighbors["suivant"] = {"prime": nth_prime(pos + 1), "position": pos + 1}
    result["neighbors"] = neighbors

    return result


def analyze_range(start: int, end: int) -> list[dict]:
    """Analyse spectrale pour tous les premiers dans une plage."""
    results = []
    for p in PRIMES:
        if p < start:
            continue
        if p > end:
            break
        results.append(analyze_prime(p))
    return results


# ===================== Donnees de visualisation =====================

def generate_viz_data(start_pos: int = 1, end_pos: int = 50) -> dict:
    """Genere les series de donnees pour les 4 graphiques spectraux."""
    end_pos = min(end_pos, max_position())
    start_pos = max(1, start_pos)

    suites_data = []
    digamma_data = []
    rsp_data = []
    gaps_data = []

    prev_prime = None
    for n in range(start_pos, end_pos + 1):
        p = nth_prime(n)
        if p is None:
            continue

        sa_val = float(SA(n))
        sb_val = float(SB(n))
        dgm = float(digamma_calc(n, p))

        suites_data.append({"n": n, "p": p, "SA": sa_val, "SB": sb_val})
        digamma_data.append({"n": n, "p": p, "digamma": dgm})

        # RSP: ratio 1x1 entre positions consecutives
        if n > start_pos:
            try:
                r = float(ratio_1x1(n - 1, n))
                rsp_data.append({"n": n, "p": p, "ratio": r, "expected": 0.5})
            except Exception:
                pass

        # Ecarts entre premiers consecutifs
        if prev_prime is not None:
            gaps_data.append({
                "n": n, "p": p,
                "gap": p - prev_prime,
                "prev_p": prev_prime
            })
        prev_prime = p

    return {
        "suites": suites_data,
        "digamma": digamma_data,
        "rsp": rsp_data,
        "gaps": gaps_data,
        "range": {"start": start_pos, "end": end_pos}
    }
