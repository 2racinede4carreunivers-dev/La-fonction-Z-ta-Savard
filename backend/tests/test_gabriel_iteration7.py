"""Tests for iteration 7 - Gabriel service alignment with methode_spectral.thy.

Covers:
- Reconstruction du 33e premier -> p=137
- Ecarts: 5/47=-41, -19/-5=-13, -31/17=-47
- Rejet compose 51 (preuve par l'absurde)
- SYSTEM_PROMPT contient les references au fichier .thy
"""
import os
import sys
import pytest
import requests

sys.path.insert(0, "/app/backend")

from modules.gabriel.gap_solver import compute_gap
from modules.gabriel.gabriel_service import SPECTRAL_SYSTEM_PROMPT, detect_computation_request, run_computation
from modules.gabriel.composite_absurdity_prover import get_composite_rejection_response

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "http://localhost:8001").rstrip("/")


# --- SYSTEM_PROMPT references to .thy ---
class TestSystemPromptReferences:
    def test_prompt_mentions_thy_file(self):
        assert "methode_spectral.thy" in SPECTRAL_SYSTEM_PROMPT

    def test_prompt_mentions_2957_lines(self):
        assert "2957" in SPECTRAL_SYSTEM_PROMPT

    def test_prompt_rsp_un_demi_general_line_ref(self):
        assert "RsP_un_demi_general" in SPECTRAL_SYSTEM_PROMPT
        assert "133-163" in SPECTRAL_SYSTEM_PROMPT

    def test_prompt_gap_m19_m5_ref(self):
        assert "gap_m19_m5" in SPECTRAL_SYSTEM_PROMPT

    def test_prompt_gap_m31_17_ref(self):
        assert "gap_m31_17" in SPECTRAL_SYSTEM_PROMPT

    def test_prompt_composite_not_prime_i_ref(self):
        assert "composite_not_prime_i" in SPECTRAL_SYSTEM_PROMPT

    def test_prompt_position_33_137(self):
        assert "n=33->p=137" in SPECTRAL_SYSTEM_PROMPT


# --- Gap computations ---
class TestGapComputations:
    def test_gap_5_47(self):
        r = compute_gap(5, 47)
        assert r["gap_float"] == -41.0
        assert r["gap_type"] == "positive_positive"

    def test_gap_neg19_neg5(self):
        r = compute_gap(-19, -5)
        assert r["gap_float"] == -13.0
        assert r["gap_type"] == "negative_negative"

    def test_gap_neg31_17(self):
        r = compute_gap(-31, 17)
        assert r["gap_float"] == -47.0
        assert r["gap_type"] == "mixed"


# --- Reconstruction 33e -> p=137 ---
class TestReconstruction33:
    def test_detect_and_run_reconstruction_33(self):
        det = detect_computation_request("reconstruis le 33e nombre premier")
        assert det["needs_computation"] is True
        assert det["type"] == "reconstruct"
        assert 33 in det["params"]["numbers"]
        output = run_computation(det)
        # p=137, SA(33)=(13/8)*2^33-2, SB(33)=(13/4)*2^33-66
        SA_33 = (13/8) * (2**33) - 2
        SB_33 = (13/4) * (2**33) - 66
        digamma_33 = SB_33 - 64 * 137
        assert "137" in output
        assert "n = 33" in output
        assert str(SA_33) in output or f"{SA_33}" in output
        assert str(SB_33) in output or f"{SB_33}" in output
        assert str(digamma_33) in output or f"{digamma_33}" in output


# --- Composite rejection (51) ---
class TestCompositeRejection51:
    def test_51_detected_as_composite(self):
        resp = get_composite_rejection_response([51])
        assert resp is not None
        assert resp["is_composite_error"] is True
        assert any(c.get("value") == 51 for c in resp["composites"])

    def test_51_rejection_contains_absurdite_proof(self):
        resp = get_composite_rejection_response([51])
        text = resp["response"]
        # Should mention: composite, prime, absurdite / contradiction
        assert "51" in text
        assert "composite_not_prime_i" in text or "compose" in text.lower() or "composé" in text.lower()


# --- API endpoint tests ---
class TestGabrielAskAPI:
    def test_api_reconstruction_33(self):
        resp = requests.post(
            f"{BASE_URL}/api/gabriel/ask",
            json={"question": "reconstruis le 33e nombre premier", "session_id": "test_33"},
            timeout=60,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert data.get("computation_type") == "reconstruct"
        assert "137" in (data.get("computation") or "")

    def test_api_gap_5_47(self):
        resp = requests.post(
            f"{BASE_URL}/api/gabriel/ask",
            json={"question": "ecart entre 5 et 47", "session_id": "test_5_47"},
            timeout=60,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("computation_type") == "gap_v2"
        assert "-41" in (data.get("computation") or "") or "41" in (data.get("computation") or "")

    def test_api_gap_neg19_neg5(self):
        resp = requests.post(
            f"{BASE_URL}/api/gabriel/ask",
            json={"question": "ecart entre -19 et -5", "session_id": "test_m19_m5"},
            timeout=60,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("computation_type") == "gap_v2"
        assert "13" in (data.get("computation") or "")

    def test_api_gap_neg31_17(self):
        resp = requests.post(
            f"{BASE_URL}/api/gabriel/ask",
            json={"question": "ecart entre -31 et 17", "session_id": "test_m31_17"},
            timeout=60,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("computation_type") == "gap_v2"
        assert "47" in (data.get("computation") or "")

    def test_api_composite_51_rejection(self):
        resp = requests.post(
            f"{BASE_URL}/api/gabriel/ask",
            json={"question": "analyse le premier 51", "session_id": "test_c51"},
            timeout=60,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("is_composite_error") is True
        assert data.get("computation_type") == "composite_rejection"
