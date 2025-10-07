import requests
import sys
import json
from datetime import datetime

class UniversAuCarreAPITester:
    def __init__(self, base_url="https://square-universe.preview.emergentagent.com"):
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

    def test_privileged_access_system(self):
        """Test the privileged access system for specialized AI"""
        print("\n🔐 PRIVILEGED ACCESS SYSTEM TESTS")
        
        # Test 1: /api/test-privileged-access endpoint
        success1, response1 = self.run_test(
            "Test Privileged Access - Statistics and Enrichment",
            "GET",
            "api/test-privileged-access",
            200
        )
        
        if success1 and isinstance(response1, dict):
            # Validate response structure
            required_fields = ['success', 'message', 'statistics', 'privileged_system_length', 'sample_enrichment']
            missing_fields = [field for field in required_fields if field not in response1]
            if missing_fields:
                print(f"   ⚠️  Missing fields in privileged access response: {missing_fields}")
            else:
                print(f"   ✅ Privileged access response structure is valid")
                
                # Check statistics
                stats = response1.get('statistics', {})
                if 'total_concepts' in stats:
                    print(f"   📊 Total concepts: {stats['total_concepts']}")
                if 'domaines' in stats:
                    print(f"   📊 Domaines: {len(stats['domaines'])} ({', '.join(stats['domaines'][:3])}...)")
                if 'documents_sources' in stats:
                    print(f"   📊 Documents sources: {len(stats['documents_sources'])}")
                
                # Check enrichment content
                enrichment_length = response1.get('privileged_system_length', 0)
                print(f"   📊 Privileged system content length: {enrichment_length} characters")
                
                if enrichment_length > 10000:  # Should be substantial content
                    print(f"   ✅ Enrichment content is substantial")
                else:
                    print(f"   ⚠️  Enrichment content seems short")
        
        # Test 2: /api/concepts-enrichis endpoint
        success2, response2 = self.run_test(
            "Get All Enriched Concepts",
            "GET",
            "api/concepts-enrichis",
            200
        )
        
        if success2 and isinstance(response2, dict):
            concepts = response2.get('concepts', [])
            domaines = response2.get('domaines', [])
            print(f"   📊 Found {len(concepts)} enriched concepts")
            print(f"   📊 Found {len(domaines)} domains: {', '.join(domaines[:5])}")
            
            # Validate concept structure
            if concepts and len(concepts) > 0:
                concept = concepts[0]
                required_concept_fields = ['id', 'titre', 'description', 'domaine_principal', 'concepts_cles', 'formules', 'definitions', 'relations']
                missing_concept_fields = [field for field in required_concept_fields if field not in concept]
                if missing_concept_fields:
                    print(f"   ⚠️  Missing fields in enriched concept: {missing_concept_fields}")
                else:
                    print(f"   ✅ Enriched concept structure is valid")
                    print(f"   📝 Sample concept: {concept['titre']} ({concept['domaine_principal']})")
        
        # Test 3: /api/chat-privileged endpoint with Philippôt theory question
        test_questions = [
            "Peux-tu m'expliquer la Sphère de Zêta selon Philippôt?",
            "Quelle est la relation entre le spectre des nombres premiers et l'hypothèse de Riemann dans la théorie?"
        ]
        
        privileged_chat_success = True
        for i, question in enumerate(test_questions, 1):
            success3, response3 = self.run_test(
                f"Privileged Chat - Question {i} (Philippôt Theory)",
                "POST",
                "api/chat-privileged",
                200,
                data={"message": question, "session_id": f"test_privileged_session_{i}"}
            )
            
            if success3 and isinstance(response3, dict):
                if 'response' in response3 and 'privileged_access' in response3:
                    ai_response = response3['response']
                    privileged_access = response3['privileged_access']
                    concepts_available = response3.get('concepts_available', 0)
                    
                    print(f"   ✅ Privileged chat response received")
                    print(f"   📊 Response length: {len(ai_response)} characters")
                    print(f"   🔐 Privileged access: {privileged_access}")
                    print(f"   📚 Concepts available: {concepts_available}")
                    
                    # Check for bi-partite structure
                    if "🔵" in ai_response and "⚪" in ai_response:
                        print(f"   ✅ Bi-partite response structure detected")
                    else:
                        print(f"   ⚠️  Bi-partite structure not clearly detected")
                    
                    # Check for specific concepts mentioned
                    key_concepts = ["Sphère de Zêta", "Philippôt", "nombres premiers", "Riemann"]
                    mentioned_concepts = [concept for concept in key_concepts if concept.lower() in ai_response.lower()]
                    if mentioned_concepts:
                        print(f"   ✅ Key concepts mentioned: {', '.join(mentioned_concepts)}")
                    else:
                        print(f"   ⚠️  Key concepts not clearly mentioned")
                else:
                    print(f"   ⚠️  Missing response or privileged_access field")
                    privileged_chat_success = False
            else:
                privileged_chat_success = False
        
        # Test 4: Test specific domain access
        success4, response4 = self.run_test(
            "Get Concepts by Domain - Géométrie Fondamentale",
            "GET",
            "api/concepts-enrichis/Géométrie Fondamentale",
            200
        )
        
        if success4 and isinstance(response4, dict):
            domain_concepts = response4.get('concepts', [])
            domain_name = response4.get('domaine', '')
            concept_count = response4.get('count', 0)
            
            print(f"   ✅ Domain-specific concepts retrieved")
            print(f"   📊 Domain: {domain_name}")
            print(f"   📊 Concepts in domain: {concept_count}")
            
            if domain_concepts and len(domain_concepts) > 0:
                sample_concept = domain_concepts[0]
                print(f"   📝 Sample concept: {sample_concept.get('titre', 'N/A')}")
        
        return success1 and success2 and privileged_chat_success and success4

    def test_philippot_theorem_privileged_access(self):
        """Test specific question about Philippôt theorem from second part"""
        print("\n🔬 THÉORÈME DE PHILIPPÔT - DEUXIÈME PARTIE TEST")
        
        # Test the specific question requested in the review
        test_question = "Explique-moi le théorème de Philippôt de la deuxième partie"
        
        success, response = self.run_test(
            "Privileged Chat - Théorème de Philippôt (Deuxième Partie)",
            "POST",
            "api/chat-privileged",
            200,
            data={"message": test_question, "session_id": "test_philippot_theorem_session"}
        )
        
        if success and isinstance(response, dict):
            # Validate response structure
            required_fields = ['response', 'privileged_access', 'concepts_available']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                print(f"   ⚠️  Missing fields in response: {missing_fields}")
                return False
            
            ai_response = response['response']
            privileged_access = response['privileged_access']
            concepts_available = response['concepts_available']
            
            print(f"   ✅ Response received successfully")
            print(f"   📊 Response length: {len(ai_response)} characters")
            print(f"   🔐 Privileged access: {privileged_access}")
            print(f"   📚 Concepts available: {concepts_available}")
            
            # Check for privileged access confirmation
            if not privileged_access:
                print(f"   ❌ Privileged access not confirmed")
                return False
            
            # Check for bi-partite structure (🔵 and ⚪)
            has_bipartite = "🔵" in ai_response and "⚪" in ai_response
            if has_bipartite:
                print(f"   ✅ Bi-partite response structure detected")
            else:
                print(f"   ⚠️  Bi-partite structure (🔵/⚪) not detected")
            
            # Check for specific content from second part
            key_concepts_second_part = [
                "trois carrés égalent à un triangle",
                "trois carrés égalent un triangle", 
                "intrication quantique",
                "géométrie de philippôt",
                "théorème de philippôt"
            ]
            
            mentioned_concepts = []
            for concept in key_concepts_second_part:
                if concept.lower() in ai_response.lower():
                    mentioned_concepts.append(concept)
            
            if mentioned_concepts:
                print(f"   ✅ Key concepts from second part mentioned: {', '.join(mentioned_concepts)}")
            else:
                print(f"   ❌ Key concepts from second part NOT mentioned")
                print(f"   Expected concepts: {', '.join(key_concepts_second_part)}")
                return False
            
            # Check for specific theorem content
            theorem_indicators = [
                "trois carrés",
                "triangle",
                "intrication",
                "géométrique"
            ]
            
            found_indicators = [indicator for indicator in theorem_indicators if indicator.lower() in ai_response.lower()]
            if len(found_indicators) >= 2:
                print(f"   ✅ Theorem content indicators found: {', '.join(found_indicators)}")
            else:
                print(f"   ⚠️  Limited theorem content indicators: {', '.join(found_indicators)}")
            
            # Check response quality (should be substantial for this complex topic)
            if len(ai_response) < 500:
                print(f"   ⚠️  Response seems short for such a complex topic ({len(ai_response)} chars)")
            else:
                print(f"   ✅ Response has substantial content ({len(ai_response)} chars)")
            
            # Final validation
            validation_passed = (
                privileged_access and
                len(mentioned_concepts) > 0 and
                len(found_indicators) >= 2 and
                len(ai_response) >= 300
            )
            
            if validation_passed:
                print(f"   🎉 Théorème de Philippôt test PASSED - AI has access to second part content")
                return True
            else:
                print(f"   ❌ Théorème de Philippôt test FAILED - Missing expected content")
                return False
        else:
            print(f"   ❌ Failed to get valid response")
            return False

    def test_analyse_texte_endpoint(self):
        """Test the new /api/analyse-texte endpoint with intelligent correction system"""
        print("\n📝 SYSTÈME DE CORRECTION INTELLIGENTE TESTS")
        
        # Test text with intentional errors as specified in the review request
        test_text = """Bonjour, je vais tester le systeme de corection intelligent. Il y a plusieurs erreur dans ce texte que l'IA doit detecter et proposer des ameliorations. Par exemple, les mots sans accent comme "systeme" ou "erreur" au pluriel mal accordé. Aussi des phrase mal structuré comme celle-ci qui pourrait etre ameliorer pour la clartés."""
        
        # Test payload as specified in the review request
        test_payload = {
            "texte": test_text,
            "options": {
                "orthographe": True,
                "grammaire": True,
                "semantique": True
            },
            "session_id": "test_correction_123"
        }
        
        # Test 1: Basic functionality with intentional errors
        success1, response1 = self.run_test(
            "Analyse Texte - Correction Intelligente",
            "POST",
            "api/analyse-texte",
            200,
            data=test_payload
        )
        
        if success1 and isinstance(response1, dict):
            # Validate response structure
            required_fields = ['success', 'analyse', 'options_utilisees', 'session_id', 'longueur_texte']
            missing_fields = [field for field in required_fields if field not in response1]
            if missing_fields:
                print(f"   ⚠️  Missing fields in response: {missing_fields}")
            else:
                print(f"   ✅ Response structure is valid")
                
                # Check analysis content
                analyse = response1.get('analyse', {})
                if 'analyse_orthographe' in analyse:
                    orthographe_errors = analyse['analyse_orthographe']
                    print(f"   📊 Orthographe errors detected: {len(orthographe_errors) if isinstance(orthographe_errors, list) else 'N/A'}")
                    
                    # Check for specific expected corrections
                    expected_corrections = ["système", "correction", "erreurs", "détecter", "améliorations"]
                    if isinstance(orthographe_errors, list):
                        found_corrections = []
                        for error in orthographe_errors:
                            if isinstance(error, dict) and 'suggestion' in error:
                                suggestion = error['suggestion'].lower()
                                for expected in expected_corrections:
                                    if expected.lower() in suggestion:
                                        found_corrections.append(expected)
                        
                        if found_corrections:
                            print(f"   ✅ Expected corrections found: {', '.join(found_corrections)}")
                        else:
                            print(f"   ⚠️  Expected corrections not clearly detected")
                
                if 'analyse_grammaire' in analyse:
                    grammaire_errors = analyse['analyse_grammaire']
                    print(f"   📊 Grammaire errors detected: {len(grammaire_errors) if isinstance(grammaire_errors, list) else 'N/A'}")
                
                # Check options used
                options_used = response1.get('options_utilisees', {})
                expected_options = ['orthographe', 'grammaire', 'semantique']
                for option in expected_options:
                    if options_used.get(option):
                        print(f"   ✅ Option '{option}' was processed")
                    else:
                        print(f"   ⚠️  Option '{option}' was not processed")
                
                # Check text length
                text_length = response1.get('longueur_texte', 0)
                expected_length = len(test_text)
                if text_length == expected_length:
                    print(f"   ✅ Text length correctly calculated: {text_length} characters")
                else:
                    print(f"   ⚠️  Text length mismatch: expected {expected_length}, got {text_length}")
                
                # Check session ID
                session_id = response1.get('session_id', '')
                if session_id == "test_correction_123":
                    print(f"   ✅ Session ID correctly preserved: {session_id}")
                else:
                    print(f"   ⚠️  Session ID mismatch: expected 'test_correction_123', got '{session_id}'")
        
        # Test 2: Edge case - empty text
        success2, response2 = self.run_test(
            "Analyse Texte - Empty Text (Error Case)",
            "POST",
            "api/analyse-texte",
            400,  # Should return 400 for empty text
            data={"texte": "", "options": {"orthographe": True}, "session_id": "test_empty"}
        )
        
        # Test 3: Different options configuration
        test_payload_minimal = {
            "texte": "Texte simple pour test minimal.",
            "options": {
                "orthographe": True,
                "grammaire": False,
                "semantique": False
            },
            "session_id": "test_minimal_options"
        }
        
        success3, response3 = self.run_test(
            "Analyse Texte - Minimal Options",
            "POST",
            "api/analyse-texte",
            200,
            data=test_payload_minimal
        )
        
        if success3 and isinstance(response3, dict):
            options_used = response3.get('options_utilisees', {})
            if options_used.get('orthographe') and not options_used.get('grammaire') and not options_used.get('semantique'):
                print(f"   ✅ Options correctly filtered: only orthographe enabled")
            else:
                print(f"   ⚠️  Options filtering not working as expected")
        
        # Test 4: French text with mathematical/scientific terms
        scientific_text = """La fonction Zêta de Riemann ζ(s) est définie par la série ζ(s) = Σ(1/n^s). Cette fonction joue un rôle crucial dans la théorie des nombres premiers selon l'hypothèse de Riemann."""
        
        test_payload_scientific = {
            "texte": scientific_text,
            "options": {
                "orthographe": True,
                "grammaire": True,
                "semantique": True
            },
            "session_id": "test_scientific_text"
        }
        
        success4, response4 = self.run_test(
            "Analyse Texte - Scientific/Mathematical Text",
            "POST",
            "api/analyse-texte",
            200,
            data=test_payload_scientific
        )
        
        if success4 and isinstance(response4, dict):
            print(f"   ✅ Scientific text processed successfully")
            analyse = response4.get('analyse', {})
            if 'score_global' in analyse:
                scores = analyse['score_global']
                print(f"   📊 Global scores: {scores}")
        
        return success1 and success2 and success3 and success4

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

    def test_collaboration_page_restructured_endpoints(self):
        """Test the specific endpoints for CollaborationPage after 4-quadrant restructuring"""
        print("\n🎯 COLLABORATION PAGE - RESTRUCTURED 4-QUADRANTS TESTS")
        print("Testing endpoints after interface restructuring to 4-quadrants layout")
        
        all_tests_passed = True
        
        # Test 1: /api/chat-extended - for specialized AI chat with privileged access
        print("\n1️⃣ Testing /api/chat-extended - Specialized AI Chat")
        test_question = "Explique-moi le théorème de Philippôt et ses applications dans la géométrie des nombres premiers"
        
        success1, response1 = self.run_test(
            "Chat Extended - Specialized AI with Privileged Access",
            "POST",
            "api/chat-extended",
            200,
            data={
                "message": test_question,
                "session_id": "test_collaboration_restructured_123",
                "context_mode": "extended"
            }
        )
        
        if success1 and isinstance(response1, dict):
            if 'response' in response1:
                ai_response = response1['response']
                print(f"   ✅ AI response received: {len(ai_response)} characters")
                
                # Check for theoretical content access
                theoretical_terms = ["philippôt", "théorème", "géométrie", "nombres premiers"]
                found_terms = [term for term in theoretical_terms if term.lower() in ai_response.lower()]
                if found_terms:
                    print(f"   ✅ Theoretical content detected: {', '.join(found_terms)}")
                else:
                    print(f"   ⚠️  Limited theoretical content in response")
                    all_tests_passed = False
            else:
                print(f"   ❌ No response field in chat-extended response")
                all_tests_passed = False
        else:
            all_tests_passed = False
        
        # Test 2: /api/analyse-texte - for intelligent corrections
        print("\n2️⃣ Testing /api/analyse-texte - Intelligent Corrections System")
        test_text_with_errors = """Voici un texte avec des erreur d'orthographe et de grammaire pour tester le systeme de corection intelligent. Il y a plusieurs faute que l'IA doit detecter et corriger automatiquement. Par exemple, les mot sans accent comme "systeme" ou les accord mal fait."""
        
        success2, response2 = self.run_test(
            "Analyse Texte - French Text with Intentional Errors",
            "POST",
            "api/analyse-texte",
            200,
            data={
                "texte": test_text_with_errors,
                "options": {
                    "orthographe": True,
                    "grammaire": True,
                    "semantique": True
                },
                "session_id": "test_correction_restructured_456"
            }
        )
        
        if success2 and isinstance(response2, dict):
            if 'analyse' in response2:
                analyse = response2['analyse']
                print(f"   ✅ Text analysis completed")
                
                # Check for orthographic corrections
                if 'analyse_orthographe' in analyse:
                    ortho_errors = analyse['analyse_orthographe']
                    if isinstance(ortho_errors, list) and len(ortho_errors) > 0:
                        print(f"   ✅ Orthographic errors detected: {len(ortho_errors)}")
                        
                        # Check for specific expected corrections
                        expected_corrections = ["système", "correction", "erreurs", "détecter", "mots"]
                        corrections_found = []
                        for error in ortho_errors:
                            if isinstance(error, dict) and 'suggestion' in error:
                                suggestion = error['suggestion'].lower()
                                for expected in expected_corrections:
                                    if expected.lower() in suggestion:
                                        corrections_found.append(expected)
                        
                        if corrections_found:
                            print(f"   ✅ Expected corrections found: {', '.join(set(corrections_found))}")
                        else:
                            print(f"   ⚠️  Expected corrections not clearly detected")
                    else:
                        print(f"   ⚠️  No orthographic errors detected in text with intentional errors")
                        all_tests_passed = False
                
                # Check for grammar analysis
                if 'analyse_grammaire' in analyse:
                    grammar_errors = analyse['analyse_grammaire']
                    if isinstance(grammar_errors, list):
                        print(f"   ✅ Grammar analysis completed: {len(grammar_errors)} issues detected")
                    else:
                        print(f"   ⚠️  Grammar analysis format unexpected")
            else:
                print(f"   ❌ No analysis field in response")
                all_tests_passed = False
        else:
            all_tests_passed = False
        
        # Test 3: /api/save-collaboration - for saving documents
        print("\n3️⃣ Testing /api/save-collaboration - Document Saving")
        test_document = """# Document Collaboratif - Théorie de Philippôt

## Introduction
Ce document explore les concepts fondamentaux de la théorie "L'univers est au carré" développée par Philippe Thomas Savard.

## Méthode de Philippôt
La méthode utilise des rapports triangulaires spécifiques pour déterminer les nombres premiers:
- Rapport 1/2 → 29 (10ème premier)
- Rapport 1/3 → 227 (49ème premier)
- Rapport 1/4 → 947 (163ème premier)

## Applications
Les applications de cette méthode révolutionnaire incluent:
1. Prédiction directe des nombres premiers
2. Analyse géométrique du spectre des nombres premiers
3. Résolution potentielle de l'hypothèse de Riemann

## Conclusion
Cette approche géométrique ouvre de nouvelles perspectives dans la théorie des nombres."""
        
        success3, response3 = self.run_test(
            "Save Collaboration - Document with Session ID",
            "POST",
            "api/save-collaboration",
            200,
            data={
                "document": test_document,
                "title": "Document Collaboratif - Théorie Philippôt Restructurée",
                "session_id": "test_collaboration_restructured_789"
            }
        )
        
        saved_doc_id = None
        if success3 and isinstance(response3, dict):
            if 'document_id' in response3 and 'success' in response3:
                saved_doc_id = response3['document_id']
                print(f"   ✅ Document saved successfully with ID: {saved_doc_id}")
            else:
                print(f"   ❌ Missing document_id or success field in save response")
                all_tests_passed = False
        else:
            all_tests_passed = False
        
        # Test 4: /api/collaboration-documents/{session_id} - for loading documents
        print("\n4️⃣ Testing /api/collaboration-documents/{session_id} - Document Loading")
        success4, response4 = self.run_test(
            "Get Collaboration Documents by Session",
            "GET",
            "api/collaboration-documents/test_collaboration_restructured_789",
            200
        )
        
        if success4 and isinstance(response4, list):
            print(f"   ✅ Documents retrieved for session: {len(response4)} documents found")
            
            if len(response4) > 0:
                doc = response4[0]
                required_fields = ['id', 'title', 'updated_at', 'word_count', 'char_count']
                missing_fields = [field for field in required_fields if field not in doc]
                if missing_fields:
                    print(f"   ⚠️  Missing fields in document: {missing_fields}")
                    all_tests_passed = False
                else:
                    print(f"   ✅ Document structure is valid")
                    print(f"   📄 Title: {doc['title']}")
                    print(f"   📊 Word count: {doc['word_count']}, Char count: {doc['char_count']}")
            else:
                print(f"   ⚠️  No documents found for session (expected at least 1)")
        else:
            all_tests_passed = False
        
        # Test 5: Retrieve specific saved document
        if saved_doc_id:
            print("\n5️⃣ Testing document retrieval by ID")
            success5, response5 = self.run_test(
                "Get Specific Collaboration Document",
                "GET",
                f"api/collaboration-document/{saved_doc_id}",
                200
            )
            
            if success5 and isinstance(response5, dict):
                if 'content' in response5 and 'title' in response5:
                    print(f"   ✅ Document retrieved successfully")
                    print(f"   📄 Title: {response5['title']}")
                    print(f"   📝 Content length: {len(response5['content'])} characters")
                    
                    # Verify content matches what we saved
                    if response5['content'] == test_document:
                        print(f"   ✅ Document content matches saved content")
                    else:
                        print(f"   ⚠️  Document content differs from saved content")
                        all_tests_passed = False
                else:
                    print(f"   ❌ Missing content or title in retrieved document")
                    all_tests_passed = False
            else:
                all_tests_passed = False
        
        # Test 6: Test content quality and theoretical access for chat-extended
        print("\n6️⃣ Testing theoretical content access in chat-extended")
        philippot_question = "Explique-moi le théorème de Philippôt de la deuxième partie avec les trois carrés qui égalent un triangle"
        
        success6, response6 = self.run_test(
            "Chat Extended - Theoretical Content Access",
            "POST",
            "api/chat-extended",
            200,
            data={
                "message": philippot_question,
                "session_id": "test_theoretical_content_999",
                "context_mode": "extended"
            }
        )
        
        if success6 and isinstance(response6, dict):
            if 'response' in response6:
                ai_response = response6['response']
                
                # Check for specific content from second part
                key_concepts = ["trois carrés", "triangle", "philippôt", "théorème"]
                found_concepts = [concept for concept in key_concepts if concept.lower() in ai_response.lower()]
                
                if len(found_concepts) >= 3:
                    print(f"   ✅ Key concepts from second part mentioned: {', '.join(found_concepts)}")
                    
                    # Check response quality
                    if len(ai_response) > 1000:
                        print(f"   ✅ Substantial response provided: {len(ai_response)} characters")
                        
                        # Check for structured content (even without bi-partite symbols)
                        has_structure = any(marker in ai_response for marker in ["PARTIE", "VISION", "CONTEXTE", "1)", "2)", "**"])
                        if has_structure:
                            print(f"   ✅ Response has structured content")
                        else:
                            print(f"   ⚠️  Response lacks clear structure")
                    else:
                        print(f"   ⚠️  Response seems short: {len(ai_response)} characters")
                        all_tests_passed = False
                else:
                    print(f"   ❌ Key concepts not adequately mentioned: {', '.join(found_concepts)}")
                    all_tests_passed = False
            else:
                print(f"   ❌ No response field in chat-extended response")
                all_tests_passed = False
        else:
            all_tests_passed = False
        
        return all_tests_passed

def main():
    print("🚀 Testing CollaborationPage after 4-Quadrant Restructuring")
    print("=" * 70)
    print("Focus: Testing collaboration endpoints after interface restructuring")
    
    tester = UniversAuCarreAPITester()
    
    # Run health check first
    print("\n📋 BASIC HEALTH CHECK")
    tester.test_health_check()
    
    # Focus on collaboration functionality as requested
    print("\n🎯 COLLABORATION PAGE - RESTRUCTURED ENDPOINTS TESTS")
    collaboration_success = tester.test_collaboration_page_restructured_endpoints()
    
    # Run additional relevant tests
    print("\n🔬 ADDITIONAL PHILIPPÔT THEORY TESTS")
    tester.test_philippot_theorem_privileged_access()
    
    print("\n📝 INTELLIGENT CORRECTION SYSTEM TESTS")
    tester.test_analyse_texte_endpoint()
    
    # Print final results
    print("\n" + "=" * 70)
    print(f"📊 FINAL RESULTS")
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    
    if collaboration_success and tester.tests_passed >= (tester.tests_run * 0.8):  # 80% success rate
        print("🎉 Collaboration functionality tests PASSED!")
        print("✅ CollaborationPage endpoints working after 4-quadrant restructuring")
        return 0
    else:
        print(f"⚠️  Some collaboration tests failed")
        print(f"❌ Issues detected in CollaborationPage after restructuring")
        return 1

if __name__ == "__main__":
    sys.exit(main())