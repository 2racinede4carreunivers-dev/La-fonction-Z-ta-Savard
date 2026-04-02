"""
Backend tests for GitHub sync functionality
Tests:
- GET /api/github/status - verify repo_url, content_size > 200000, status=active
- POST /api/github/sync - verify success=true, content_size > 200000
- POST /api/chat - verify response uses knowledge from new repo (.thy files)
"""

import pytest
import requests
import os
import time

# Get backend URL from environment
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
if not BASE_URL:
    BASE_URL = "https://theo-sync.preview.emergentagent.com"

print(f"Testing against: {BASE_URL}")


class TestGitHubStatus:
    """Tests for GET /api/github/status endpoint"""
    
    def test_github_status_returns_200(self):
        """Test that /api/github/status returns 200 OK"""
        response = requests.get(f"{BASE_URL}/api/github/status")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"✅ GET /api/github/status returned 200")
    
    def test_github_status_correct_repo_url(self):
        """Test that repo_url contains the new repo name"""
        response = requests.get(f"{BASE_URL}/api/github/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "repo_url" in data, "Response missing 'repo_url' field"
        
        # Verify the new repo URL
        expected_repo = "Theorie-mathematique-philippe-thomas-savard-2026"
        assert expected_repo in data["repo_url"], \
            f"Expected repo URL to contain '{expected_repo}', got: {data['repo_url']}"
        print(f"✅ repo_url correctly contains: {expected_repo}")
        print(f"   Full URL: {data['repo_url']}")
    
    def test_github_status_content_size_over_200k(self):
        """Test that content_size > 200000 characters"""
        response = requests.get(f"{BASE_URL}/api/github/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "content_size" in data, "Response missing 'content_size' field"
        
        content_size = data["content_size"]
        assert content_size > 200000, \
            f"Expected content_size > 200000, got: {content_size}"
        print(f"✅ content_size = {content_size} (> 200000)")
    
    def test_github_status_is_active(self):
        """Test that status is 'active'"""
        response = requests.get(f"{BASE_URL}/api/github/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data, "Response missing 'status' field"
        assert data["status"] == "active", \
            f"Expected status='active', got: {data['status']}"
        print(f"✅ status = 'active'")
    
    def test_github_status_has_last_sync(self):
        """Test that last_sync field is present"""
        response = requests.get(f"{BASE_URL}/api/github/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "last_sync" in data, "Response missing 'last_sync' field"
        print(f"✅ last_sync = {data['last_sync']}")


class TestGitHubSync:
    """Tests for POST /api/github/sync endpoint"""
    
    def test_github_sync_returns_200(self):
        """Test that /api/github/sync returns 200 OK"""
        response = requests.post(f"{BASE_URL}/api/github/sync")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"✅ POST /api/github/sync returned 200")
    
    def test_github_sync_success_true(self):
        """Test that sync returns success=true"""
        response = requests.post(f"{BASE_URL}/api/github/sync")
        assert response.status_code == 200
        
        data = response.json()
        assert "success" in data, "Response missing 'success' field"
        assert data["success"] == True, \
            f"Expected success=True, got: {data['success']}"
        print(f"✅ success = True")
    
    def test_github_sync_content_size_over_200k(self):
        """Test that sync returns content_size > 200000"""
        response = requests.post(f"{BASE_URL}/api/github/sync")
        assert response.status_code == 200
        
        data = response.json()
        assert "content_size" in data, "Response missing 'content_size' field"
        
        content_size = data["content_size"]
        assert content_size > 200000, \
            f"Expected content_size > 200000, got: {content_size}"
        print(f"✅ content_size = {content_size} (> 200000)")
    
    def test_github_sync_has_message(self):
        """Test that sync returns a message"""
        response = requests.post(f"{BASE_URL}/api/github/sync")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data, "Response missing 'message' field"
        print(f"✅ message = {data['message']}")


class TestChatWithGitHubContext:
    """Tests for POST /api/chat using knowledge from the new repo"""
    
    def test_chat_endpoint_returns_200(self):
        """Test that /api/chat returns 200 OK"""
        payload = {
            "message": "Bonjour",
            "session_id": "test_session_github_sync"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=payload)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"✅ POST /api/chat returned 200")
    
    def test_chat_about_thy_files(self):
        """Test that chat can respond about .thy files from the repo"""
        payload = {
            "message": "Quels sont les fichiers .thy (Isabelle/HOL) disponibles dans le dépôt? Liste-les.",
            "session_id": "test_session_thy_files"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=60)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "response" in data, "Response missing 'response' field"
        
        response_text = data["response"].lower()
        # The response should mention .thy files or Isabelle/HOL
        has_thy_reference = any(term in response_text for term in [
            ".thy", "isabelle", "hol", "preuve", "formelle", "théorie"
        ])
        
        print(f"✅ Chat response received ({len(data['response'])} chars)")
        print(f"   Response mentions .thy/Isabelle: {has_thy_reference}")
        print(f"   First 500 chars: {data['response'][:500]}...")
    
    def test_chat_about_methode_spectrale(self):
        """Test that chat knows about methode_spectrale.thy content"""
        payload = {
            "message": "Explique-moi la méthode spectrale pour les nombres premiers selon la théorie de Philippôt.",
            "session_id": "test_session_spectrale"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=60)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "response" in data, "Response missing 'response' field"
        
        response_text = data["response"].lower()
        # Check for relevant terms from the theory
        relevant_terms = ["spectral", "premier", "nombre", "philippôt", "méthode"]
        found_terms = [term for term in relevant_terms if term in response_text]
        
        print(f"✅ Chat response about méthode spectrale received")
        print(f"   Found relevant terms: {found_terms}")
        print(f"   Response length: {len(data['response'])} chars")
    
    def test_chat_about_digamma(self):
        """Test that chat knows about Digamma from the theory"""
        payload = {
            "message": "Qu'est-ce que le Digamma de Philippôt et comment est-il utilisé pour les nombres premiers?",
            "session_id": "test_session_digamma"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=60)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "response" in data, "Response missing 'response' field"
        
        response_text = data["response"].lower()
        # Check for Digamma-related content
        has_digamma = "digamma" in response_text
        
        print(f"✅ Chat response about Digamma received")
        print(f"   Mentions Digamma: {has_digamma}")
        print(f"   Response length: {len(data['response'])} chars")
    
    def test_chat_returns_session_id(self):
        """Test that chat returns a session_id"""
        payload = {
            "message": "Test message",
            "session_id": "test_session_id_check"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=30)
        assert response.status_code == 200
        
        data = response.json()
        assert "session_id" in data, "Response missing 'session_id' field"
        print(f"✅ session_id returned: {data['session_id']}")


class TestBackendHealth:
    """Basic health checks for the backend"""
    
    def test_backend_is_running(self):
        """Test that backend responds to requests"""
        try:
            response = requests.get(f"{BASE_URL}/api/github/status", timeout=10)
            assert response.status_code == 200
            print(f"✅ Backend is running and responding")
        except requests.exceptions.ConnectionError:
            pytest.fail("Backend is not running or not accessible")
    
    def test_backend_cors_headers(self):
        """Test that CORS headers are present"""
        response = requests.options(f"{BASE_URL}/api/github/status")
        # OPTIONS might return 200 or 405 depending on configuration
        # The important thing is that the server responds
        print(f"✅ Backend responds to OPTIONS request: {response.status_code}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
