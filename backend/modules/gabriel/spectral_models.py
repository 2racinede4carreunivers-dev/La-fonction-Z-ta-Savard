"""
Trois modeles spectraux de Philippe Thomas Savard : 1/2, 1/3, 1/4.

Conformes a `theories/methode_spectral.thy` (verite officielle).

Chaque modele implemente :
  - A(n), B(n)               : les 2 suites alternees
  - digamma(n, p)            : B(n) - factor*p
  - reconstruct(n, digamma)  : (B(n) - digamma) / factor = p
  - RsP(n1, n2)              : (A(n1) - A(n2)) / (B(n1) - B(n2)) = ratio
  - n_factor                 : (1/2 -> 2, 1/3 -> 3, 1/4 -> 4)
  - reconstruction_factor    : (1/2 -> 64, 1/3 -> 729, 1/4 -> 4096)
  - ratio                    : Fraction(1, 2) | Fraction(1, 3) | Fraction(1, 4)

Toute la mathematique utilise `fractions.Fraction` pour exactitude infinie.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence, Optional


# --------------------------------------------------------------------------
# Resultats unifies
# --------------------------------------------------------------------------
@dataclass
class RatioResult:
    """Resultat d'un calcul de rapport spectral pour un modele."""
    model_name: str          # "1/2" | "1/3" | "1/4"
    case: str                # "1x1" | "nxn_symetrique" | "asym_chaotique" | "asym_ordonnee"
    A_positions: list[int]
    B_positions: list[int]
    numerator: Fraction      # A(n1) - A(n2) ou somme des differences
    denominator: Fraction
    ratio: Fraction          # numerator / denominator
    expected: Fraction       # 1/2, 1/3 ou 1/4
    is_exact: bool           # ratio == expected
    formula: str             # description textuelle

    @property
    def convergence_delta(self) -> Fraction:
        """Ecart entre le ratio calcule et le ratio attendu."""
        return self.ratio - self.expected

    @property
    def convergence_delta_float(self) -> float:
        """Idem en float pour comparaisons numeriques."""
        return float(self.convergence_delta)

    @property
    def is_close(self) -> bool:
        """True si |ratio - expected| < 1e-3."""
        return abs(self.convergence_delta_float) < 1e-3
    
    def to_dict(self) -> dict:
        return {
            "model_name": self.model_name,
            "case": self.case,
            "A_positions": self.A_positions,
            "B_positions": self.B_positions,
            "numerator": float(self.numerator),
            "denominator": float(self.denominator),
            "ratio": float(self.ratio),
            "expected": float(self.expected),
            "is_exact": self.is_exact,
            "formula": self.formula,
            "convergence_delta": float(self.convergence_delta),
            "is_close": self.is_close,
        }


@dataclass
class ReconstructionResult:
    """Resultat de la reconstruction du n-ieme nombre premier."""
    model_name: str
    n: int
    A_value: Fraction
    B_value: Fraction
    digamma: Fraction
    reconstructed_prime: Fraction
    actual_prime: int        # depuis prime_table
    is_exact: bool           # reconstructed == actual
    formula: str
    
    def to_dict(self) -> dict:
        return {
            "model_name": self.model_name,
            "n": self.n,
            "position": self.n,
            "num_terms": self.n,
            "A_value": float(self.A_value),
            "B_value": float(self.B_value),
            "SA_float": float(self.A_value),
            "SB_float": float(self.B_value),
            "digamma": float(self.digamma),
            "digamma_calc_float": float(self.digamma),
            "reconstructed_prime": int(self.reconstructed_prime),
            "p": int(self.reconstructed_prime),
            "prime": int(self.reconstructed_prime),
            "actual_prime": self.actual_prime,
            "is_exact": self.is_exact,
            "equation_holds": self.is_exact,
            "formula": self.formula,
            "model": self.model_name,
        }


@dataclass
class GapResult:
    """Resultat d'un calcul de gap entre 2 nombres premiers."""
    model_name: str
    case: str                # "++", "--", "-+"
    p1: int
    p2: int
    gap_count: int           # |p1 - p2| - 1 (entiers strictement entre)
    formula: str
    
    def to_dict(self) -> dict:
        return {
            "model_name": self.model_name,
            "case": self.case,
            "p1": self.p1,
            "p2": self.p2,
            "gap_count": self.gap_count,
            "formula": self.formula,
        }


# --------------------------------------------------------------------------
# Classe abstraite
# --------------------------------------------------------------------------
class SpectralModel(ABC):
    """Interface commune aux 3 modeles spectraux."""

    name: str                      # "1/2" | "1/3" | "1/4"
    n_factor: int                  # 2 | 3 | 4 (puissance dans A/B(n))
    reconstruction_factor: int     # 64 | 729 | 4096

    @property
    def ratio(self) -> Fraction:
        """Le rapport spectral attendu (1/2, 1/3 ou 1/4)."""
        return Fraction(1, self.n_factor)

    @abstractmethod
    def A(self, n: int) -> Fraction:
        """Suite alternee A(n) en exact (Fraction)."""

    @abstractmethod
    def B(self, n: int) -> Fraction:
        """Suite alternee B(n) en exact (Fraction)."""

    def digamma(self, n: int, p: int) -> Fraction:
        """digamma(n, p) = B(n) - factor*p (formule officielle .thy)."""
        return self.B(n) - self.reconstruction_factor * p

    def reconstruct(self, n: int, digamma: Fraction) -> Fraction:
        """Reconstruit p depuis (n, digamma) : p = (B(n) - digamma) / factor."""
        return (self.B(n) - digamma) / self.reconstruction_factor

    def RsP_1x1(self, n1: int, n2: int) -> RatioResult:
        """Cas 1x1 : RsP = (A(n1) - A(n2)) / (B(n1) - B(n2)) = 1/{n_factor}."""
        if n1 == n2:
            raise ValueError(f"n1 et n2 doivent etre differents (recu {n1}, {n2})")
        num = self.A(n1) - self.A(n2)
        den = self.B(n1) - self.B(n2)
        ratio = num / den
        return RatioResult(
            model_name=self.name, case="1x1",
            A_positions=[n1], B_positions=[n2],
            numerator=num, denominator=den, ratio=ratio,
            expected=self.ratio, is_exact=(ratio == self.ratio),
            formula=f"RsP({n1},{n2}) = (A({n1}) - A({n2})) / (B({n1}) - B({n2}))",
        )

    def RsP_nxn(
        self,
        A_positions: Sequence[int],
        B_positions: Sequence[int],
        case: str = "nxn_symetrique",
    ) -> RatioResult:
        """Cas n×n (symetrique, asymetrique chaotique ou ordonnee)."""
        if not A_positions or not B_positions:
            raise ValueError("A_positions et B_positions doivent etre non vides")
        if list(A_positions) == list(B_positions):
            raise ValueError("A_positions et B_positions doivent differer")

        sum_A_a = sum(self.A(n) for n in A_positions)
        sum_A_b = sum(self.A(n) for n in B_positions)
        sum_B_a = sum(self.B(n) for n in A_positions)
        sum_B_b = sum(self.B(n) for n in B_positions)

        num = sum_A_a - sum_A_b
        den = sum_B_a - sum_B_b
        if den == 0:
            raise ZeroDivisionError(
                f"Denominateur nul pour A={list(A_positions)} B={list(B_positions)}"
            )
        ratio = num / den
        return RatioResult(
            model_name=self.name, case=case,
            A_positions=list(A_positions), B_positions=list(B_positions),
            numerator=num, denominator=den, ratio=ratio,
            expected=self.ratio, is_exact=(ratio == self.ratio),
            formula=(
                f"RsP({case}) = (sum_A(A_pos) - sum_A(B_pos)) "
                f"/ (sum_B(A_pos) - sum_B(B_pos))"
            ),
        )

    def reconstruct_nth_prime(
        self,
        n: int,
        actual_prime: int,
    ) -> ReconstructionResult:
        """Reconstruit le n-ieme nombre premier via le modele."""
        a_val = self.A(n)
        b_val = self.B(n)
        digamma_val = self.digamma(n, actual_prime)
        reconstructed = self.reconstruct(n, digamma_val)
        return ReconstructionResult(
            model_name=self.name, n=n,
            A_value=a_val, B_value=b_val, digamma=digamma_val,
            reconstructed_prime=reconstructed,
            actual_prime=actual_prime,
            is_exact=(reconstructed == actual_prime),
            formula=(
                f"p = (B({n}) - digamma({n},p)) / {self.reconstruction_factor} = "
                f"({float(b_val):.1f} - {float(digamma_val):.1f}) / {self.reconstruction_factor}"
            ),
        )

    def gap(self, p1: int, p2: int) -> GapResult:
        """Calcule le gap |p1 - p2| - 1."""
        if p1 == p2:
            return GapResult(
                model_name=self.name, case="++", p1=p1, p2=p2,
                gap_count=0, formula="gap(p,p) = 0 (memes nombres)",
            )
        if p1 >= 0 and p2 >= 0:
            case = "++"
        elif p1 < 0 and p2 < 0:
            case = "--"
        else:
            case = "-+"
        gap_count = abs(p1 - p2) - 1
        return GapResult(
            model_name=self.name, case=case, p1=p1, p2=p2,
            gap_count=gap_count,
            formula=f"gap({p1}, {p2}) = |{p1} - {p2}| - 1 = {gap_count}  (cas {case})",
        )


# --------------------------------------------------------------------------
# Modele 1/2 (Section I de methode_spectral.thy)
# --------------------------------------------------------------------------
class Model_1_2(SpectralModel):
    """Modele spectral 1/2 (rapport 1/2 attendu).

    SA(n) = (3.25 / 2) * 2^n - 2  =  (13/8) * 2^n - 2
    SB(n) = (6.5 / 2)  * 2^n - 66 =  (13/4) * 2^n - 66
    digamma_calc n p = SB n - 64 * real p
    """

    name = "1/2"
    n_factor = 2
    reconstruction_factor = 64

    def A(self, n: int) -> Fraction:
        return Fraction(13, 8) * (2 ** n) - 2

    def B(self, n: int) -> Fraction:
        return Fraction(13, 4) * (2 ** n) - 66


# --------------------------------------------------------------------------
# Modele 1/3 (Section III de methode_spectral.thy)
# --------------------------------------------------------------------------
class Model_1_3(SpectralModel):
    """Modele spectral 1/3 (rapport 1/3 attendu).

    A_1_3 n = (73/108) * 3^n - 3/2
    B_1_3 n = (219/108) * 3^n - 1461/2
    factor = 729
    """

    name = "1/3"
    n_factor = 3
    reconstruction_factor = 729

    def A(self, n: int) -> Fraction:
        return Fraction(73, 108) * (3 ** n) - Fraction(3, 2)

    def B(self, n: int) -> Fraction:
        return Fraction(219, 108) * (3 ** n) - Fraction(1461, 2)


# --------------------------------------------------------------------------
# Modele 1/4 (Section II de methode_spectral.thy)
# --------------------------------------------------------------------------
class Model_1_4(SpectralModel):
    """Modele spectral 1/4 (rapport 1/4 attendu).

    A_1_4 n = (241/192) * 4^n - 4/3
    B_1_4 n = (964/192) * 4^n - 12292/3
    factor = 4096
    """

    name = "1/4"
    n_factor = 4
    reconstruction_factor = 4096

    def A(self, n: int) -> Fraction:
        return Fraction(241, 192) * (4 ** n) - Fraction(4, 3)

    def B(self, n: int) -> Fraction:
        return Fraction(964, 192) * (4 ** n) - Fraction(12292, 3)


# --------------------------------------------------------------------------
# Registry & helpers
# --------------------------------------------------------------------------
_REGISTRY: dict[str, SpectralModel] = {
    "1/2": Model_1_2(),
    "1/3": Model_1_3(),
    "1/4": Model_1_4(),
}


def get_model(name: str) -> SpectralModel:
    """Recupere un modele par son nom : '1/2', '1/3' ou '1/4'."""
    if name not in _REGISTRY:
        raise ValueError(
            f"Modele inconnu : '{name}'. Disponibles : {list(_REGISTRY)}"
        )
    return _REGISTRY[name]


def list_models() -> list[str]:
    """Liste des modeles disponibles."""
    return list(_REGISTRY.keys())


def all_models() -> list[SpectralModel]:
    """Renvoie tous les modeles instancies."""
    return list(_REGISTRY.values())
