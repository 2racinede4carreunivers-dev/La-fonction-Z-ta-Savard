"""Regression tests for health, public content, OAuth session validation, Gabriel, and chat APIs."""

import os
import uuid
from datetime import datetime, timedelta, timezone

import pytest
import requests
from dotenv import dotenv_values
from pymongo import MongoClient


frontend_env = dotenv_values("/app/frontend/.env")
backend_env = dotenv_values("/app/backend/.env")
base_url = os.environ.get("REACT_APP_BACKEND_URL") or frontend_env.get("REACT_APP_BACKEND_URL")
if not base_url:
    raise RuntimeError("REACT_APP_BACKEND_URL is missing")
BASE_URL = base_url.rstrip("/")


@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()


@pytest.fixture(scope="session")
def seeded_auth_session():
    mongo_url = os.environ.get("MONGO_URL") or backend_env.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME") or backend_env.get("DB_NAME")
    if not mongo_url or not db_name:
        pytest.fail("MONGO_URL or DB_NAME missing; cannot seed OAuth-compatible test session")

    mongo = MongoClient(mongo_url)
    db = mongo[db_name]
    suffix = uuid.uuid4().hex
    user_id = f"test-user-{suffix}"
    token = f"test_session_{suffix}"
    email = f"test.user.{suffix}@example.com"
    now = datetime.now(timezone.utc)
    db.users.insert_one({
        "user_id": user_id,
        "email": email,
        "name": "TEST_OAuth User",
        "picture": None,
        "is_admin": False,
        "created_at": now,
        "last_login": now,
    })
    db.user_sessions.insert_one({
        "user_id": user_id,
        "session_token": token,
        "expires_at": now + timedelta(days=1),
        "created_at": now,
    })
    yield {"user_id": user_id, "token": token, "email": email}
    db.user_sessions.delete_many({"session_token": token})
    db.users.delete_many({"user_id": user_id})
    mongo.close()


# Core health and homepage content endpoints.
class TestCoreContent:
    def test_health(self, api_client):
        response = api_client.get(f"{BASE_URL}/api/health", timeout=20)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "L'univers est au carré" in data["message"]

    def test_concepts(self, api_client):
        response = api_client.get(f"{BASE_URL}/api/concepts", timeout=30)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list) and len(data) > 0
        assert all(isinstance(item.get("id"), str) and item.get("titre") for item in data)

    def test_categories(self, api_client):
        response = api_client.get(f"{BASE_URL}/api/categories", timeout=30)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list) and len(data) > 0
        assert all(item.get("categorie") and isinstance(item.get("count"), int) and item["count"] > 0 for item in data)

    def test_tableaux(self, api_client):
        response = api_client.get(f"{BASE_URL}/api/tableaux-philippot", timeout=30)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list) and len(data) == 14
        assert all(item.get("id") and item.get("rapport") and isinstance(item.get("calcul_detaille"), dict) for item in data)


# OAuth session authentication and error handling.
class TestAuthentication:
    def test_me_rejects_unauthenticated_user(self, api_client):
        response = api_client.get(f"{BASE_URL}/api/auth/me", timeout=20)
        assert response.status_code == 401
        assert response.json()["detail"] == "Non authentifié"

    def test_session_exchange_rejects_invalid_session_id(self, api_client):
        response = api_client.post(
            f"{BASE_URL}/api/auth/session",
            json={"session_id": f"invalid-{uuid.uuid4().hex}"},
            timeout=30,
        )
        assert response.status_code == 401
        assert "invalide" in response.json()["detail"].lower()

    def test_me_accepts_valid_seeded_bearer_session(self, api_client, seeded_auth_session):
        response = api_client.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {seeded_auth_session['token']}"},
            timeout=20,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == seeded_auth_session["user_id"]
        assert data["email"] == seeded_auth_session["email"]
        assert data["name"] == "TEST_OAuth User"
        assert data["is_admin"] is False
        assert "_id" not in data


# AI module smoke tests; allow extra time for provider responses.
class TestAIModules:
    def test_gabriel_simple_prime_query(self, api_client):
        response = api_client.post(
            f"{BASE_URL}/api/gabriel/ask",
            json={"question": "Quel est le 10e nombre premier ?", "session_id": f"TEST_{uuid.uuid4().hex}"},
            timeout=120,
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("response"), str) and len(data["response"]) > 20
        assert "29" in data["response"] or "29" in str(data.get("computation", ""))

    def test_chat_simple_question(self, api_client):
        response = api_client.post(
            f"{BASE_URL}/api/chat",
            json={"message": "Qu'est-ce que le Digamma de Philippôt ?", "session_id": f"TEST_{uuid.uuid4().hex}"},
            timeout=120,
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("response"), str) and len(data["response"]) > 20
        assert isinstance(data.get("session_id"), str) and data["session_id"].startswith("TEST_")
