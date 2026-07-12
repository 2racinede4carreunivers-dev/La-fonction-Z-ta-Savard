"""Tests for gap_solver formula corrections (5-47, 7-23, -7/29, -19/-5)."""
import os
import sys
import pytest
import requests

sys.path.insert(0, "/app/backend")

from modules.gabriel.gap_solver import compute_gap, SA, SB, digamma

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "http://localhost:8001").rstrip("/")


# --- Intermediate value checks (Philippe's exact numbers) ---
class TestIntermediateValues:
    def test_SA_4(self):
        assert float(SA(4)) == 24.0

    def test_SB_15(self):
        assert float(SB(15)) == 106430.0

    def test_digamma_15_47(self):
        assert float(digamma(15, 47)) == 103422.0

    def test_SB_3(self):
        assert float(SB(3)) == -40.0

    def test_digamma_3_5(self):
        assert float(digamma(3, 5)) == -360.0


# --- End-to-end gap computations ---
class TestGapComputations:
    def test_gap_5_47(self):
        r = compute_gap(5, 47)
        assert r is not None
        assert r["gap_float"] == -41.0
        assert r["gap_count"] == 41
        assert r["gap_type"] == "positive_positive"
        assert r["SA_suivant_min"] == 24.0
        assert r["SB_max"] == 106430.0
        assert r["digamma_max"] == 103422.0
        assert r["SB_min"] == -40.0
        assert r["digamma_min"] == -360.0

    def test_gap_7_23(self):
        r = compute_gap(7, 23)
        assert r is not None
        assert r["gap_float"] == -15.0
        assert r["gap_count"] == 15
        assert r["gap_type"] == "positive_positive"

    def test_gap_neg7_29(self):
        r = compute_gap(-7, 29)
        assert r is not None
        assert r["gap_float"] == -35.0
        assert r["gap_count"] == 35
        assert r["gap_type"] == "mixed"

    def test_gap_neg19_neg5(self):
        r = compute_gap(-19, -5)
        assert r is not None
        assert r["gap_float"] == -13.0
        assert r["gap_count"] == 13
        assert r["gap_type"] == "negative_negative"


# --- API endpoint /api/gabriel/ask ---
class TestGabrielAskAPI:
    def test_ask_gap_5_47(self):
        resp = requests.post(
            f"{BASE_URL}/api/gabriel/ask",
            json={"question": "Quel est l'ecart entre 5 et 47 ?", "session_id": "test_gap_5_47"},
            timeout=30,
        )
        assert resp.status_code == 200, resp.text
        data = resp.json()
        # Look for computation_type or nested result
        comp_type = data.get("computation_type") or data.get("type")
        # Support both flat and nested response shapes
        text = str(data)
        assert "41" in text, f"Expected 41 in response: {text[:500]}"
        # Try to locate structured field
        if "computation" in data and isinstance(data["computation"], dict):
            c = data["computation"]
            assert c.get("gap_count") == 41 or c.get("gap_float") == -41.0

    def test_ask_gap_7_23(self):
        resp = requests.post(
            f"{BASE_URL}/api/gabriel/ask",
            json={"question": "ecart entre 7 et 23", "session_id": "test_gap_7_23"},
            timeout=30,
        )
        assert resp.status_code == 200, resp.text
        assert "15" in str(resp.json())
