"""Regression tests for Gabriel Section XIII (Pont Savard) update - iteration 9."""
import os
import re
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/")
if not BASE_URL:
    # Fallback to reading frontend/.env directly
    with open("/app/frontend/.env") as f:
        for line in f:
            if line.startswith("REACT_APP_BACKEND_URL="):
                BASE_URL = line.split("=", 1)[1].strip().rstrip("/")
                break

ASK = f"{BASE_URL}/api/gabriel/ask"
COMPUTE = f"{BASE_URL}/api/gabriel/compute"
GAP = f"{BASE_URL}/api/gabriel/gap"

TIMEOUT = 90


def _ask(question, sid):
    r = requests.post(ASK, json={"question": question, "session_id": sid}, timeout=TIMEOUT)
    assert r.status_code == 200, f"HTTP {r.status_code}: {r.text[:400]}"
    body = r.json()
    assert "response" in body and isinstance(body["response"], str) and len(body["response"]) > 30
    return body["response"].lower()


# --- SYSTEM_PROMPT / static file content checks -------------------------------

def test_system_prompt_contains_section_xiii():
    from modules.gabriel.gabriel_service import SPECTRAL_SYSTEM_PROMPT as sp
    assert "SECTION XIII" in sp
    assert "PONT SAVARD" in sp
    assert "psi_savard" in sp


def test_system_prompt_contains_canonical_validations():
    from modules.gabriel.gabriel_service import SPECTRAL_SYSTEM_PROMPT as sp
    assert "28.888" in sp
    assert "96.894" in sp
    assert "226.894" in sp or "228" in sp


def test_system_prompt_contains_ensemble_structure():
    from modules.gabriel.gabriel_service import SPECTRAL_SYSTEM_PROMPT as sp
    assert "1/x" in sp and "1/t" in sp and "1/ms" in sp
    assert "ENSEMBLE" in sp.upper()


def test_system_prompt_contains_three_concordances():
    from modules.gabriel.gabriel_service import SPECTRAL_SYSTEM_PROMPT as sp
    assert "C1" in sp and "C2" in sp and "C3" in sp


def test_methode_spectral_thy_line_count():
    path = "/app/backend/modules/gabriel/theories/methode_spectral.thy"
    assert os.path.exists(path)
    with open(path) as f:
        lines = f.readlines()
    # File should be substantial (~3180 lines per review)
    assert len(lines) >= 3000, f"Only {len(lines)} lines, expected ~3180"


def test_section_xiii_module_present():
    assert os.path.exists("/app/backend/modules/gabriel/section_XIII.py")


# --- Spectral engine (deterministic) ------------------------------------------

def test_reconstruction_33rd_prime_is_137():
    r = requests.post(COMPUTE, json={"action": "nth_prime", "params": {"n": 33}}, timeout=TIMEOUT)
    assert r.status_code == 200, r.text[:300]
    data = r.json()
    # Endpoint returns something like {"n":33,"prime":137,...}
    val = data.get("prime") or data.get("result") or data.get("p")
    assert val == 137, f"Expected 137, got {data}"


def test_gap_between_5_and_47_is_minus_41():
    r = requests.post(GAP, json={"p1": 5, "p2": 47}, timeout=TIMEOUT)
    assert r.status_code == 200, r.text[:300]
    data = r.json()
    gap = data.get("gap_float") if data.get("gap_float") is not None else (data.get("gap") or data.get("result") or data.get("ecart"))
    assert gap == -41 or gap == -41.0, f"Expected -41, got gap={gap}"


# --- LLM behavior: Gabriel can talk about Section XIII ------------------------

def test_gabriel_explains_section_xiii_and_pont_savard():
    txt = _ask(
        "Explique-moi en 5 lignes la Section XIII et le Pont Savard, "
        "en mentionnant psi_savard et Re(rho) = 1/2.",
        "sxiii-1",
    )
    assert "savard" in txt
    assert "psi" in txt or "ψ" in txt
    # Must mention link to Riemann critical line / RsP
    assert "1/2" in txt or "0.5" in txt


def test_gabriel_mentions_three_concordances():
    txt = _ask(
        "Enumere les trois concordances C1, C2, C3 du Pont Savard.",
        "sxiii-2",
    )
    assert "c1" in txt and "c2" in txt and "c3" in txt


def test_gabriel_knows_psi_savard_canonical_value_30_10():
    txt = _ask(
        "Quelle est la valeur de psi_savard(30, 10) donnee dans la Section XIII ?",
        "sxiii-3",
    )
    # Accept the canonical value or its rounded forms
    assert re.search(r"28[.,]888", txt) is not None, f"Missing 28.888 in: {txt[:400]}"
