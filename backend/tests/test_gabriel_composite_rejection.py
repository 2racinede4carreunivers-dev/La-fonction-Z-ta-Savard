"""
Tests for the composite absurdity prover in Gabriel.

Feature under test: POST /api/gabriel/ask must detect composite integers when
they are used as PRIME NUMBERS to analyze (in gaps, prime analysis, etc.), NOT
when they are used as positions/indices (reconstruction of the n-th prime).

The composite rejection only applies to:
- gap_v2: "Écart entre 7 et 51" (51 is composite, rejected)
- analyze_prime: "Analyse le premier 51" (51 is composite, rejected)

The composite rejection does NOT apply to:
- reconstruct: "Reconstruis le 51ième premier" (51 is a position, allowed)

Reference module: /app/backend/modules/gabriel/composite_absurdity_prover.py
Reference service: /app/backend/modules/gabriel/gabriel_service.py (gabriel_ask)
"""
import os
import uuid
import pytest
import requests

def _load_backend_url():
    v = os.environ.get("REACT_APP_BACKEND_URL")
    if not v:
        env_path = "/app/frontend/.env"
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("REACT_APP_BACKEND_URL="):
                        v = line.split("=", 1)[1].strip()
                        break
    return v.rstrip("/") if v else ""

BASE_URL = _load_backend_url()
ASK_URL = f"{BASE_URL}/api/gabriel/ask"

CANONICAL_COMPOSITES = [4, 9, 15, 51, 91, 121]


def _post(question: str) -> dict:
    sid = f"TEST_composite_{uuid.uuid4().hex[:8]}"
    r = requests.post(ASK_URL, json={"question": question, "session_id": sid}, timeout=60)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text[:300]}"
    return r.json()


# === Composite detection via GAP queries (the correct context) ===
class TestCompositeRejectionViaGap:
    """Composites used in gap calculations must trigger rejection."""

    @pytest.mark.parametrize("n", [51, 91, 121])
    def test_composite_in_gap_rejected(self, n):
        """Écart entre un premier et un composé doit être rejeté."""
        data = _post(f"Quel est l'écart entre 7 et {n} ?")
        assert data.get("is_composite_error") is True, f"n={n}: expected is_composite_error=True"
        assert data.get("computation_type") == "composite_rejection"
        assert data.get("computation") is None
        composites = data.get("composites") or []
        assert any(c["value"] == n for c in composites), f"n={n}: composites = {composites}"

    def test_gap_51_factorization_in_response(self):
        """La réponse doit contenir la factorisation de 51."""
        data = _post("Écart entre 7 et 51")
        resp = data.get("response", "")
        assert "51" in resp
        assert ("3 × 17" in resp or "3 x 17" in resp or "3×17" in resp)

    def test_gap_cites_hol_theorems(self):
        """La réponse doit citer les théorèmes HOL."""
        data = _post("Écart entre 7 et 51")
        resp = data.get("response", "")
        assert "composite_not_prime_i" in resp
        assert "spectral_method_exclusively_for_primes" in resp

    def test_gap_51_cites_canonical_theorem(self):
        """La réponse doit citer le théorème spécifique pour 51."""
        data = _post("Écart entre 7 et 51")
        resp = data.get("response", "")
        assert "no_spectral_position_for_51" in resp

    def test_composites_dict_structure(self):
        """Le dictionnaire composites doit avoir les champs requis."""
        data = _post("Écart entre 7 et 51")
        composites = data.get("composites", [])
        assert len(composites) >= 1
        c = composites[0]
        assert c["value"] == 51
        assert c["factors"] == [3, 17]
        assert c["is_composite"] is True
        assert c["is_negative"] is False
        assert c["thy_reference"] == "no_spectral_position_for_51"
        assert "decomposition" in c
        assert "message" in c


# === Primes must still work normally (no composite rejection) ===
class TestPrimesStillWork:
    """Verify primes pass through and do NOT trigger composite_rejection."""

    def test_reconstruction_17th_prime_returns_59(self):
        data = _post("Reconstruis le 17ieme nombre premier")
        # Should NOT be rejected
        assert not data.get("is_composite_error"), f"17 should not be flagged as composite: {data}"
        assert data.get("computation_type") != "composite_rejection"
        # Computation should have been run
        comp = data.get("computation") or ""
        resp = data.get("response") or ""
        # The 17th prime is 59
        assert "59" in comp or "59" in resp, f"Expected 59 in response/computation. resp={resp[:400]} comp={comp[:400]}"

    def test_gap_between_minus7_and_29_returns_35(self):
        data = _post("Quel est l'ecart entre -7 et 29 ?")
        assert not data.get("is_composite_error"), f"-7 and 29 are prime, should not trigger: {data}"
        assert data.get("computation_type") != "composite_rejection"
        comp = data.get("computation") or ""
        resp = data.get("response") or ""
        assert "35" in comp or "35" in resp, f"Expected 35. resp={resp[:400]} comp={comp[:400]}"

    def test_plain_prime_question_not_rejected(self):
        # Ask about 7 (prime) - should not be flagged
        data = _post("Parle-moi du nombre 7")
        assert not data.get("is_composite_error"), f"7 is prime: {data}"


# === Negative composites via gap should also be caught ===
class TestNegativeComposites:
    def test_negative_composite_in_gap(self):
        """Un composé négatif dans un écart doit être rejeté."""
        data = _post("Écart entre -7 et -51")
        assert data.get("is_composite_error") is True
        composites = data.get("composites") or []
        assert any(c["value"] == -51 and c["is_negative"] is True for c in composites), composites


# === Unit-level checks (importing the module directly) ===
class TestCompositeProverUnit:
    def test_build_rejection_for_prime_returns_none(self):
        from modules.gabriel.composite_absurdity_prover import build_composite_rejection
        assert build_composite_rejection(7) is None
        assert build_composite_rejection(-7) is None
        assert build_composite_rejection(59) is None

    def test_build_rejection_for_composite(self):
        from modules.gabriel.composite_absurdity_prover import build_composite_rejection
        r = build_composite_rejection(51)
        assert r is not None
        assert r.factors == [3, 17]
        assert r.thy_reference == "no_spectral_position_for_51"

    def test_factorize_121(self):
        from modules.gabriel.composite_absurdity_prover import factorize
        assert factorize(121) == [11, 11]

    def test_factorize_91(self):
        from modules.gabriel.composite_absurdity_prover import factorize
        assert factorize(91) == [7, 13]
