"""
Iteration 8: Regression tests after LLM model rename
'claude-sonnet-4-20250514' -> 'claude-sonnet-4-5-20250929'
Verifies that all AI endpoints depending on Anthropic Claude via emergentintegrations
return valid 200 responses (i.e. the previously invalid model name is fixed).
"""
import os
import pytest
import requests

def _load_backend_url():
    v = os.environ.get("REACT_APP_BACKEND_URL")
    if v:
        return v.rstrip("/")
    # fallback: read /app/frontend/.env
    try:
        with open("/app/frontend/.env") as f:
            for line in f:
                if line.startswith("REACT_APP_BACKEND_URL="):
                    return line.split("=", 1)[1].strip().rstrip("/")
    except Exception:
        pass
    raise RuntimeError("REACT_APP_BACKEND_URL not set")


BASE_URL = _load_backend_url()
API = f"{BASE_URL}/api"

# Longer timeout: Anthropic LLM calls can take 30-60s
TIMEOUT = 120


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# ---------- Gabriel (baseline, should always work) ----------
def test_gabriel_ask(session):
    r = session.post(
        f"{API}/gabriel/ask",
        json={"question": "Quel est le 10e nombre premier ?", "session_id": "TEST_iter8"},
        timeout=TIMEOUT,
    )
    assert r.status_code == 200, f"Gabriel ask failed: {r.status_code} {r.text[:400]}"
    data = r.json()
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0


# ---------- IA Spécialisée /api/chat ----------
def test_chat_specialisee(session):
    r = session.post(
        f"{API}/chat",
        json={"message": "Explique-moi brièvement la fonction Digamma de Philippôt.",
              "session_id": "TEST_iter8_chat"},
        timeout=TIMEOUT,
    )
    assert r.status_code == 200, f"/api/chat failed: {r.status_code} {r.text[:500]}"
    data = r.json()
    assert "response" in data and isinstance(data["response"], str)
    assert len(data["response"]) > 20, "Empty/too-short LLM response"
    assert "session_id" in data


# ---------- IA Évolutive: init + dialoguer ----------
def test_ia_evolutif_initialiser_auto(session):
    r = session.post(f"{API}/ia-evolutif/initialiser-auto", timeout=TIMEOUT)
    assert r.status_code == 200, f"initialiser-auto failed: {r.status_code} {r.text[:400]}"
    data = r.json()
    assert data.get("success") is True
    assert data.get("nombre_questions", 0) > 0


def test_ia_evolutif_dialoguer(session):
    # Ensure system is initialized (idempotent-ish)
    session.post(f"{API}/ia-evolutif/initialiser-auto", timeout=TIMEOUT)

    r = session.post(
        f"{API}/ia-evolutif/dialoguer",
        json={"question": "Qu'est-ce que la géométrie de Philippôt ?"},
        timeout=TIMEOUT,
    )
    assert r.status_code == 200, f"dialoguer failed: {r.status_code} {r.text[:500]}"
    data = r.json()
    assert "reponse" in data and isinstance(data["reponse"], str)
    assert len(data["reponse"]) > 20
    assert "concepts_utilises" in data
    assert "evolution_silencieuse" in data


# ---------- IA Socratique /api/ia-socratique/challenger ----------
def test_ia_socratique_challenger(session):
    r = session.post(
        f"{API}/ia-socratique/challenger",
        json={
            "reflexion_utilisateur": (
                "Je pense que la fonction Digamma révèle la structure des nombres premiers "
                "car elle relie les rapports fractionnaires à des invariants géométriques."
            )
        },
        timeout=TIMEOUT,
    )
    assert r.status_code == 200, f"socratique challenger failed: {r.status_code} {r.text[:500]}"
    data = r.json()
    assert "reponse_socratique" in data and isinstance(data["reponse_socratique"], str)
    assert len(data["reponse_socratique"]) > 10
    assert "questions_challengeantes" in data and isinstance(data["questions_challengeantes"], list)
    assert "niveau_challenge" in data
