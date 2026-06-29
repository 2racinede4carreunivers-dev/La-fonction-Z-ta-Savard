"""
Test suite for Gabriel V2 - New endpoints for gap (corrected formula),
RSP curve, visualize and ask detection (gap_v2, reconstruct_neg).
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')


# === /api/gabriel/gap ===
class TestGabrielGapEndpoint:
    """Tests for POST /api/gabriel/gap (V2 corrected formula)"""

    def test_gap_positive_positive_7_43(self):
        """Gap between two positive primes (7, 43)"""
        r = requests.post(f"{BASE_URL}/api/gabriel/gap",
                          json={"p1": 7, "p2": 43}, timeout=15)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["gap_type"] == "positive_positive"
        assert d["p1"] == 7 and d["p2"] == 43
        assert d["position_p1"] == 4 and d["position_p2"] == 14
        assert d["position_suivant_min"] == 5
        assert "SA_suivant_min" in d and "SB_min" in d and "digamma_min" in d
        assert "SB_max" in d and "digamma_max" in d
        assert "gap_count" in d and "gap_float" in d
        # Updated: French formula key uses 'n_suivant_min'
        assert "n_suivant_min" in d["formula_used"]
        # Arithmetic gap: 43 - 7 - 1 = 35 entiers entre 7 et 43
        assert d["validation"]["arithmetic_gap"] == 35

    def test_gap_negative_negative_minus41_minus5(self):
        """Gap between two negative primes (-41, -5)"""
        r = requests.post(f"{BASE_URL}/api/gabriel/gap",
                          json={"p1": -41, "p2": -5}, timeout=15)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["gap_type"] == "negative_negative"
        assert d["p1"] == -41 and d["p2"] == -5
        assert d["position_p1"] == -13 and d["position_p2"] == -3
        assert d["position_suivant_min"] == -12
        # Corrected: |-5 - (-41)| - 1 = 36 - 1 = 35 entiers entre -41 et -5
        assert d["validation"]["arithmetic_gap"] == 35
        assert isinstance(d["gap_count"], int)
        assert isinstance(d["gap_float"], float)

    def test_gap_mixed_negative_positive(self):
        """Mixed gap (-5, 7)"""
        r = requests.post(f"{BASE_URL}/api/gabriel/gap",
                          json={"p1": -5, "p2": 7}, timeout=15)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["gap_type"] == "mixed"
        assert d["p1"] == -5 and d["p2"] == 7
        # Corrected: arithmetic_gap for mixed = |p_neg| + p_pos - 1 = 5 + 7 - 1 = 11
        assert d["validation"]["arithmetic_gap"] == 11
        assert "match" in d["validation"]

    def test_gap_missing_params(self):
        """Missing p1 or p2 should return error"""
        r = requests.post(f"{BASE_URL}/api/gabriel/gap",
                          json={"p1": 7}, timeout=10)
        assert r.status_code == 200
        assert "error" in r.json()


# === /api/gabriel/rsp-curve ===
class TestGabrielRSPCurve:
    """Tests for GET /api/gabriel/rsp-curve"""

    def test_rsp_curve_default_1x1(self):
        r = requests.get(f"{BASE_URL}/api/gabriel/rsp-curve",
                         params={"config": "1x1", "k_max": 20}, timeout=20)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["config"] == "1x1"
        assert d["k_max"] == 20
        assert isinstance(d["points"], list) and len(d["points"]) == 20
        assert isinstance(d["chart_data"], list) and len(d["chart_data"]) > 0
        # 1x1 must converge to 1/2
        first = d["chart_data"][0]
        assert "k" in first and "rsp" in first and "expected" in first
        assert abs(first["rsp"] - 0.5) < 1e-9
        assert "ascii_curve" in d and "summary" in d

    def test_rsp_curve_sym_config(self):
        r = requests.get(f"{BASE_URL}/api/gabriel/rsp-curve",
                         params={"config": "sym", "k_max": 10}, timeout=20)
        assert r.status_code == 200
        d = r.json()
        assert d["config"] == "sym"
        assert len(d["points"]) == 10

    def test_rsp_curve_clamped_k_max(self):
        r = requests.get(f"{BASE_URL}/api/gabriel/rsp-curve",
                         params={"config": "1x1", "k_max": 500}, timeout=30)
        assert r.status_code == 200
        # k_max should be clamped to 200
        assert r.json()["k_max"] == 200


# === /api/gabriel/visualize ===
class TestGabrielVisualize:
    """Tests for GET /api/gabriel/visualize"""

    def test_visualize_default_range(self):
        r = requests.get(f"{BASE_URL}/api/gabriel/visualize",
                         params={"start": 1, "end": 50}, timeout=15)
        assert r.status_code == 200, r.text
        d = r.json()
        assert "suites" in d
        suites = d["suites"]
        assert isinstance(suites, list) and len(suites) > 0
        first = suites[0]
        for f in ("n", "p", "SA", "SB"):
            assert f in first
        assert first["n"] == 1 and first["p"] == 2


# === /api/gabriel/ask (detection only) ===
class TestGabrielAskDetection:
    """Tests for detection logic in /api/gabriel/ask (LLM may fail, fallback OK)"""

    def test_ask_detects_gap_v2(self):
        """Asking for ecart should set computation_type=gap_v2"""
        r = requests.post(f"{BASE_URL}/api/gabriel/ask", json={
            "question": "Quel est l'ecart entre 7 et 43?",
            "session_id": "test-gap-detect-1"
        }, timeout=45)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d.get("computation_type") == "gap_v2"
        comp = d.get("computation") or ""
        assert "ECART SPECTRAL V2" in comp
        assert "Type d'ecart: positive_positive" in comp

    def test_ask_detects_reconstruct_neg(self):
        """Asking reconstruction of negative prime should detect reconstruct_neg"""
        r = requests.post(f"{BASE_URL}/api/gabriel/ask", json={
            "question": "Reconstruis le premier negatif a la position 3",
            "session_id": "test-recon-neg-1"
        }, timeout=45)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d.get("computation_type") == "reconstruct_neg"
        comp = d.get("computation") or ""
        assert "NEGATIF" in comp.upper() or "negatif" in comp


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
