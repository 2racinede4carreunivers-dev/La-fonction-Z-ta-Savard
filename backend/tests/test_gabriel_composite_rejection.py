"""
Tests for the composite absurdity prover in Gabriel.

Feature under test: POST /api/gabriel/ask must detect composite integers in the
user's question and return a pedagogical rejection message (preuve par
l'absurde) instead of running the spectral engine.

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


# === Composite detection: canonical composites ===
class TestCompositeRejectionCanonical:
    """The 6 canonical composites (with dedicated .thy theorems) must all trigger rejection."""

    @pytest.mark.parametrize("n", CANONICAL_COMPOSITES)
    def test_canonical_composite_rejected(self, n):
        data = _post(f"Peux-tu calculer la position spectrale de {n} ?")
        assert data.get("is_composite_error") is True, f"n={n}: expected is_composite_error=True, got {data}"
        assert data.get("computation_type") == "composite_rejection", f"n={n}: {data.get('computation_type')}"
        assert data.get("computation") is None
        composites = data.get("composites") or []
        assert any(c["value"] == n for c in composites), f"n={n}: composites list = {composites}"

    def test_response_contains_factorization_51(self):
        data = _post("Reconstruis 51")
        resp = data["response"]
        assert "51" in resp
        assert "3" in resp and "17" in resp
        # Décomposition explicite
        assert "3 × 17" in resp or "3 x 17" in resp or "3×17" in resp

    def test_response_contains_hol_theorems(self):
        data = _post("Analyse le nombre 51")
        resp = data["response"]
        # Must cite the formal HOL theorems from methode_spectral.thy
        assert "composite_not_prime_i" in resp
        assert "spectral_method_exclusively_for_primes" in resp

    def test_response_cites_canonical_thy_for_51(self):
        data = _post("Que penses-tu de 51 ?")
        resp = data["response"]
        assert "no_spectral_position_for_51" in resp

    def test_composites_dict_has_required_fields(self):
        data = _post("Position de 51 ?")
        c = data["composites"][0]
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


# === Negative composites should also be caught ===
class TestNegativeComposites:
    def test_negative_composite_minus_51(self):
        data = _post("Analyse -51")
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
