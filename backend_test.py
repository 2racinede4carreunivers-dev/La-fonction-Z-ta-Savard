import requests
import sys
import json
from datetime import datetime

class UniversAuCarreAPITester:
    def __init__(self, base_url="https://intuitive-math-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.session_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        print(f"   Response: List with {len(response_data)} items")
                    elif isinstance(response_data, dict):
                        print(f"   Response keys: {list(response_data.keys())}")
                    return True, response_data
                except:
                    print(f"   Response: {response.text[:200]}...")
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout (30s)")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test health endpoint"""
        success, response = self.run_test(
            "Health Check",
            "GET",
            "api/health",
            200
        )
        return success

    def test_get_concepts(self):
        """Test getting all concepts"""
        success, response = self.run_test(
            "Get All Concepts",
            "GET", 
            "api/concepts",
            200
        )
        if success and isinstance(response, list):
            print(f"   Found {len(response)} concepts")
            if len(response) > 0:
                concept = response[0]
                required_fields = ['id', 'titre', 'description', 'categorie', 'mots_cles', 'contenu']
                missing_fields = [field for field in required_fields if field not in concept]
                if missing_fields:
                    print(f"   ⚠️  Missing fields in concept: {missing_fields}")
                else:
                    print(f"   ✅ Concept structure is valid")
                    return success, response[0]['id']  # Return first concept ID for later tests
        return success, None

    def test_get_concept_by_id(self, concept_id):
        """Test getting a specific concept"""
        if not concept_id:
            print("⚠️  Skipping concept by ID test - no concept ID available")
            return False
            
        success, response = self.run_test(
            "Get Concept by ID",
            "GET",
            f"api/concepts/{concept_id}",
            200
        )
        return success

    def test_get_categories(self):
        """Test getting categories"""
        success, response = self.run_test(
            "Get Categories",
            "GET",
            "api/categories", 
            200
        )
        if success and isinstance(response, list):
            print(f"   Found {len(response)} categories")
            for cat in response:
                if 'categorie' in cat and 'count' in cat:
                    print(f"   - {cat['categorie']}: {cat['count']} concepts")
        return success

    def test_search_concepts(self):
        """Test search functionality"""
        # Test search with query
        success1, response1 = self.run_test(
            "Search Concepts - 'géométrie'",
            "POST",
            "api/search",
            200,
            data={"query": "géométrie"}
        )
        
        # Test search with category filter
        success2, response2 = self.run_test(
            "Search Concepts - Category filter",
            "POST", 
            "api/search",
            200,
            data={"query": "nombres", "categorie": "Géométrie"}
        )
        
        return success1 and success2

    def test_chat_functionality(self):
        """Test AI chat functionality"""
        # Test basic chat
        success1, response1 = self.run_test(
            "Chat - Basic Question",
            "POST",
            "api/chat",
            200,
            data={"message": "Qu'est-ce que la théorie de l'univers au carré?"}
        )
        
        if success1 and isinstance(response1, dict):
            if 'session_id' in response1:
                self.session_id = response1['session_id']
                print(f"   Session ID: {self.session_id}")
            if 'response' in response1:
                print(f"   AI Response length: {len(response1['response'])} characters")
        
        # Test follow-up with session
        if self.session_id:
            success2, response2 = self.run_test(
                "Chat - Follow-up with Session",
                "POST",
                "api/chat", 
                200,
                data={"message": "Parlez-moi des nombres premiers", "session_id": self.session_id}
            )
            return success1 and success2
        
        return success1

    def test_chat_history(self):
        """Test chat history retrieval"""
        if not self.session_id:
            print("⚠️  Skipping chat history test - no session ID available")
            return False
            
        success, response = self.run_test(
            "Get Chat History",
            "GET",
            f"api/chat/history/{self.session_id}",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} messages in history")
            
        return success

    def test_collaboration_endpoints(self):
        """Test collaboration endpoints for AI document completion"""
        print("\n🤝 COLLABORATION FUNCTIONALITY TESTS")
        
        # Test data as suggested in the review request
        test_document = """## Réflexions sur la méthode Philippôt

La méthode de Philippe Thomas Savard pour déterminer la primalité des nombres premiers utilise une approche géométrique révolutionnaire basée sur les rapports triangulaires.

### Concepts fondamentaux
- Les 14 tableaux de Philippôt avec différents rapports base/hauteur
- Le calcul du Digamma à la 8ème position
- Les séquences de racines carrées

### Applications pratiques
Cette méthode permet de calculer directement des nombres premiers spécifiques selon leur position dans la suite."""

        collaboration_data = {
            "document": test_document,
            "request": "Complète cette section en développant les idées présentées sur les applications pratiques et les implications théoriques",
            "session_id": "test_collaboration_session_123",
            "document_title": "Test Collaboration IA - Méthode Philippôt"
        }
        
        # Test /api/collaborate endpoint
        success1, response1 = self.run_test(
            "AI Collaboration - Document Completion",
            "POST",
            "api/collaborate",
            200,
            data=collaboration_data
        )
        
        updated_document = None
        if success1 and isinstance(response1, dict):
            if 'updated_document' in response1:
                updated_document = response1['updated_document']
                print(f"   ✅ Document updated successfully")
                print(f"   Original length: {len(test_document)} chars")
                print(f"   Updated length: {len(updated_document)} chars")
                print(f"   Content added: {len(updated_document) - len(test_document)} chars")
            else:
                print(f"   ⚠️  No 'updated_document' in response")
        
        # Test /api/save-collaboration endpoint
        if updated_document:
            save_data = {
                "document": updated_document,
                "title": "Document Collaboratif - Méthode Philippôt Complété",
                "session_id": "test_collaboration_session_123"
            }
            
            success2, response2 = self.run_test(
                "Save Collaboration Document",
                "POST",
                "api/save-collaboration",
                200,
                data=save_data
            )
            
            if success2 and isinstance(response2, dict):
                if 'document_id' in response2:
                    doc_id = response2['document_id']
                    print(f"   ✅ Document saved with ID: {doc_id}")
                    
                    # Test retrieving the saved document
                    success3, response3 = self.run_test(
                        "Get Saved Collaboration Document",
                        "GET",
                        f"api/collaboration-document/{doc_id}",
                        200
                    )
                    
                    if success3 and isinstance(response3, dict):
                        if 'content' in response3 and 'title' in response3:
                            print(f"   ✅ Document retrieved successfully")
                            print(f"   Title: {response3['title']}")
                            print(f"   Content length: {len(response3['content'])} chars")
                        else:
                            print(f"   ⚠️  Missing content or title in retrieved document")
                    
                    return success1 and success2 and success3
                else:
                    print(f"   ⚠️  No 'document_id' in save response")
                    return success1 and success2
            else:
                return success1 and success2
        else:
            print("   ⚠️  Skipping save test - no updated document available")
            return success1
    
    def test_collaboration_session_management(self):
        """Test collaboration session and document management"""
        session_id = "test_session_documents_456"
        
        # Test getting documents for a session (should be empty initially)
        success1, response1 = self.run_test(
            "Get Collaboration Documents - Empty Session",
            "GET",
            f"api/collaboration-documents/{session_id}",
            200
        )
        
        if success1 and isinstance(response1, list):
            print(f"   ✅ Found {len(response1)} documents for new session")
        
        return success1

    def test_invalid_endpoints(self):
        """Test error handling for invalid endpoints"""
        # Test non-existent concept
        success1, _ = self.run_test(
            "Invalid Concept ID",
            "GET",
            "api/concepts/invalid-id-12345",
            404
        )
        
        # Test invalid chat history
        success2, _ = self.run_test(
            "Invalid Session ID",
            "GET", 
            "api/chat/history/invalid-session-12345",
            200  # This might return empty array
        )
        
        # Test invalid collaboration document
        success3, _ = self.run_test(
            "Invalid Collaboration Document ID",
            "GET",
            "api/collaboration-document/invalid-doc-id-12345",
            404
        )
        
        return success1 and success3

def main():
    print("🚀 Starting L'univers est au carré API Tests")
    print("=" * 60)
    
    tester = UniversAuCarreAPITester()
    concept_id = None
    
    # Run all tests
    print("\n📋 BASIC FUNCTIONALITY TESTS")
    tester.test_health_check()
    
    success, concept_id = tester.test_get_concepts()
    tester.test_get_concept_by_id(concept_id)
    tester.test_get_categories()
    
    print("\n🔍 SEARCH FUNCTIONALITY TESTS") 
    tester.test_search_concepts()
    
    print("\n🤖 AI CHAT FUNCTIONALITY TESTS")
    tester.test_chat_functionality()
    tester.test_chat_history()
    
    print("\n❌ ERROR HANDLING TESTS")
    tester.test_invalid_endpoints()
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS")
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {tester.tests_run - tester.tests_passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())