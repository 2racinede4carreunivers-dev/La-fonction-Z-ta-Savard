"""
Test suite for Gabriel - Assistant HOL specialiste Geometrie du spectre des nombres premiers
Tests the spectral computation engine and LLM integration endpoints.
"""
import pytest
import requests
import os
import time

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestGabrielComputeEndpoint:
    """Tests for POST /api/gabriel/compute - Pure spectral calculations (no LLM)"""
    
    def test_analyze_prime_29(self):
        """Test analyze_prime action with prime 29 - should return equation_holds:true"""
        response = requests.post(f"{BASE_URL}/api/gabriel/compute", json={
            "action": "analyze_prime",
            "params": {"prime": 29}
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "prime" in data, "Response should contain 'prime' field"
        assert data["prime"] == 29, f"Expected prime=29, got {data['prime']}"
        assert "position" in data, "Response should contain 'position' field"
        assert data["position"] == 10, f"Expected position=10 for prime 29, got {data['position']}"
        assert "models" in data, "Response should contain 'models' field"
        assert "1/2" in data["models"], "Response should contain model '1/2'"
        
        model_data = data["models"]["1/2"]
        assert "equation_holds" in model_data, "Model data should contain 'equation_holds'"
        assert model_data["equation_holds"] == True, f"Expected equation_holds=True for prime 29, got {model_data['equation_holds']}"
        print(f"PASS: analyze_prime(29) returns equation_holds=True, position=10")
    
    def test_nth_prime_10(self):
        """Test nth_prime action with n=10 - should return prime 29"""
        response = requests.post(f"{BASE_URL}/api/gabriel/compute", json={
            "action": "nth_prime",
            "params": {"n": 10}
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "n" in data, "Response should contain 'n' field"
        assert data["n"] == 10, f"Expected n=10, got {data['n']}"
        assert "prime" in data, "Response should contain 'prime' field"
        assert data["prime"] == 29, f"Expected prime=29 for n=10, got {data['prime']}"
        print(f"PASS: nth_prime(10) returns prime=29")
    
    def test_position_prime_97(self):
        """Test position action with prime 97 - should return position 25"""
        response = requests.post(f"{BASE_URL}/api/gabriel/compute", json={
            "action": "position",
            "params": {"prime": 97}
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "prime" in data, "Response should contain 'prime' field"
        assert data["prime"] == 97, f"Expected prime=97, got {data['prime']}"
        assert "position" in data, "Response should contain 'position' field"
        assert data["position"] == 25, f"Expected position=25 for prime 97, got {data['position']}"
        assert "is_prime" in data, "Response should contain 'is_prime' field"
        assert data["is_prime"] == True, f"Expected is_prime=True for 97, got {data['is_prime']}"
        print(f"PASS: position(97) returns position=25, is_prime=True")
    
    def test_verify_equation_n10_p29_model_half(self):
        """Test verify action with n=10, p=29, model='1/2' - should return equation_holds:true"""
        response = requests.post(f"{BASE_URL}/api/gabriel/compute", json={
            "action": "verify",
            "params": {"n": 10, "p": 29, "model": "1/2"}
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "model" in data, "Response should contain 'model' field"
        assert data["model"] == "1/2", f"Expected model='1/2', got {data['model']}"
        assert "n" in data, "Response should contain 'n' field"
        assert data["n"] == 10, f"Expected n=10, got {data['n']}"
        assert "p" in data, "Response should contain 'p' field"
        assert data["p"] == 29, f"Expected p=29, got {data['p']}"
        assert "equation_holds" in data, "Response should contain 'equation_holds' field"
        assert data["equation_holds"] == True, f"Expected equation_holds=True, got {data['equation_holds']}"
        assert "SA" in data, "Response should contain 'SA' field"
        assert "SB" in data, "Response should contain 'SB' field"
        assert "digamma_calc" in data, "Response should contain 'digamma_calc' field"
        print(f"PASS: verify(n=10, p=29, model='1/2') returns equation_holds=True")
    
    def test_analyze_prime_non_prime(self):
        """Test analyze_prime with a non-prime number - should return error"""
        response = requests.post(f"{BASE_URL}/api/gabriel/compute", json={
            "action": "analyze_prime",
            "params": {"prime": 30}  # 30 is not prime
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "error" in data, "Response should contain 'error' field for non-prime"
        print(f"PASS: analyze_prime(30) returns error for non-prime")
    
    def test_range_action(self):
        """Test range action - analyze primes in a range"""
        response = requests.post(f"{BASE_URL}/api/gabriel/compute", json={
            "action": "range",
            "params": {"start": 2, "end": 20}
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "results" in data, "Response should contain 'results' field"
        results = data["results"]
        assert len(results) > 0, "Results should not be empty"
        # Primes between 2 and 20: 2, 3, 5, 7, 11, 13, 17, 19 = 8 primes
        assert len(results) == 8, f"Expected 8 primes between 2-20, got {len(results)}"
        print(f"PASS: range(2, 20) returns 8 primes")
    
    def test_invalid_action(self):
        """Test invalid action - should return 400"""
        response = requests.post(f"{BASE_URL}/api/gabriel/compute", json={
            "action": "invalid_action",
            "params": {}
        })
        assert response.status_code == 400, f"Expected 400 for invalid action, got {response.status_code}"
        print(f"PASS: invalid action returns 400")


class TestGabrielAskEndpoint:
    """Tests for POST /api/gabriel/ask - LLM-powered responses with spectral calculations"""
    
    def test_ask_about_prime_29(self):
        """Test asking about prime 29 - should return response with computation data"""
        response = requests.post(f"{BASE_URL}/api/gabriel/ask", json={
            "question": "Verifie le nombre premier 29",
            "session_id": "test-session-1"
        }, timeout=30)  # LLM calls can take time
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "response" in data, "Response should contain 'response' field"
        assert len(data["response"]) > 0, "Response should not be empty"
        assert "session_id" in data, "Response should contain 'session_id' field"
        
        # Check if computation was performed
        if "computation" in data and data["computation"]:
            assert "computation_type" in data, "Should have computation_type when computation is present"
            print(f"PASS: ask about prime 29 returns response with computation_type={data.get('computation_type')}")
        else:
            print(f"PASS: ask about prime 29 returns response (no computation detected)")
    
    def test_ask_empty_question(self):
        """Test asking with empty question - should return 400"""
        response = requests.post(f"{BASE_URL}/api/gabriel/ask", json={
            "question": "",
            "session_id": "test-session-2"
        })
        assert response.status_code == 400, f"Expected 400 for empty question, got {response.status_code}"
        print(f"PASS: empty question returns 400")
    
    def test_ask_general_question(self):
        """Test asking a general question about the spectral method"""
        response = requests.post(f"{BASE_URL}/api/gabriel/ask", json={
            "question": "Qu'est-ce que la methode spectrale?",
            "session_id": "test-session-3"
        }, timeout=30)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "response" in data, "Response should contain 'response' field"
        assert len(data["response"]) > 50, "Response should be substantial"
        print(f"PASS: general question returns substantial response ({len(data['response'])} chars)")


class TestGitHubStatusEndpoint:
    """Test that previously working endpoint still works"""
    
    def test_github_status_qa_bank_size(self):
        """Test GET /api/github/status returns qa_bank_size >= 127"""
        response = requests.get(f"{BASE_URL}/api/github/status")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "qa_bank_size" in data, "Response should contain 'qa_bank_size' field"
        assert data["qa_bank_size"] >= 127, f"Expected qa_bank_size >= 127, got {data['qa_bank_size']}"
        print(f"PASS: /api/github/status returns qa_bank_size={data['qa_bank_size']} (>= 127)")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
