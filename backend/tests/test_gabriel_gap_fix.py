"""
Tests pour le correctif du bug KeyError 'position_p1' dans gap_solver.py.

Bug RCA: gap_solver.GapResult.to_dict() retournait pos_min/pos_max mais
gabriel_service.run_computation (cas gap_v2) attendait position_p1, position_p2
et position_suivant_min, ce qui causait KeyError -> 500.

Le correctif (lignes 137-170) ajoute les clés mappées dans to_dict().
"""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL").rstrip("/")
GAP_URL = f"{BASE_URL}/api/gabriel/gap"
ASK_URL = f"{BASE_URL}/api/gabriel/ask"


# === Fixtures ===
@pytest.fixture(scope="module")
def api_client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# === Tests directs sur /api/gabriel/gap ===
class TestGapEndpointDirect:
    """Vérifie que /api/gabriel/gap retourne les bons gap_count et les clés requises."""

    @pytest.mark.parametrize(
        "p1,p2,expected_gap,expected_type",
        [
            (23, 7, 15, "positive_positive"),     # (+,+) entre 8..22 => 15 nombres
            (-19, -5, 13, "negative_negative"),    # (-,-) entre -18..-6 => 13 nombres
            (-31, 17, 47, "mixed"),                # (-,+) 30 + 1 (zero) + 16 = 47
            (-7, 29, 35, "mixed"),                 # cas utilisateur initial du bug
        ],
    )
    def test_gap_count(self, api_client, p1, p2, expected_gap, expected_type):
        r = api_client.post(GAP_URL, json={"p1": p1, "p2": p2}, timeout=20)
        assert r.status_code == 200, f"HTTP {r.status_code}: {r.text}"
        data = r.json()
        assert "error" not in data, f"Erreur: {data.get('error')}"

        # Assertions principales du bug
        assert data["gap_count"] == expected_gap, (
            f"gap({p1},{p2}): attendu {expected_gap}, obtenu {data['gap_count']}"
        )
        assert data["gap_type"] == expected_type

        # Clés ajoutées par le correctif (root cause du KeyError)
        for k in ("position_p1", "position_p2", "position_suivant_min"):
            assert k in data, f"Clé manquante '{k}' dans la réponse"

        # Validation du sous-dictionnaire
        assert "validation" in data
        assert "arithmetic_gap" in data["validation"]
        assert "spectral_gap" in data["validation"]
        assert data["validation"]["spectral_gap"] == expected_gap


class TestGapPositionsMapping:
    """Vérifie le mapping correct position_p1 <-> p1, position_p2 <-> p2."""

    def test_positions_match_inputs_positive(self, api_client):
        # p1=23 (pos 9), p2=7 (pos 4)
        r = api_client.post(GAP_URL, json={"p1": 23, "p2": 7}, timeout=20)
        data = r.json()
        assert data["position_p1"] == 9, f"position_p1 attendu 9, obtenu {data['position_p1']}"
        assert data["position_p2"] == 4, f"position_p2 attendu 4, obtenu {data['position_p2']}"

    def test_positions_match_inputs_mixed(self, api_client):
        # p1=-7 (pos -4), p2=29 (pos 10)
        r = api_client.post(GAP_URL, json={"p1": -7, "p2": 29}, timeout=20)
        data = r.json()
        assert data["position_p1"] == -4
        assert data["position_p2"] == 10


# === Test que /api/gabriel/ask ne retourne plus 500 sur les écarts ===
class TestGabrielAskNoError500:
    """Vérifie que l'endpoint /ask n'erreure plus sur les questions d'écart (le bug d'origine)."""

    @pytest.mark.parametrize(
        "question",
        [
            "Quel est l'écart entre -7 et 29 ?",  # cas utilisateur du bug
            "écart entre 23 et 7",
            "écart entre -19 et -5",
            "écart entre -31 et 17",
        ],
    )
    def test_ask_gap_no_500(self, api_client, question):
        r = api_client.post(
            ASK_URL,
            json={"question": question, "session_id": "TEST_gap_fix"},
            timeout=60,
        )
        assert r.status_code == 200, f"HTTP {r.status_code}: {r.text[:500]}"
        data = r.json()
        # La détection doit être gap_v2
        assert data.get("computation_type") == "gap_v2", (
            f"computation_type attendu 'gap_v2', obtenu {data.get('computation_type')}"
        )
        # La computation doit contenir les calculs (pas vide ni erreur)
        comp = data.get("computation") or ""
        assert "ECART SPECTRAL V2" in comp or "Ecart" in comp, (
            f"Computation manquante/incorrecte: {comp[:300]}"
        )
        # Aucun KeyError ne doit apparaître
        assert "KeyError" not in comp
        assert "position_p1" not in comp or "n=" in comp  # clé utilisée correctement
