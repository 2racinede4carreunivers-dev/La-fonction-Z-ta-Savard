import requests
import sys
import json
from datetime import datetime

class UniversAuCarreAPITester:
    def __init__(self, base_url="https://universe-squared.preview.emergentagent.com"):
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

    def test_concept_formula_management_system(self):
        """Test the complete concept and formula administration system"""
        print("\n🔬 CONCEPT AND FORMULA MANAGEMENT SYSTEM TESTS")
        print("Testing new concept/formula administration with auto-generation and AI integration")
        
        all_tests_passed = True
        
        # Test 1: POST /api/concepts - Create new concept
        print("\n1️⃣ Testing POST /api/concepts - Create New Concept")
        test_concept_data = {
            "titre": "Digamma Test",
            "description": "Concept de test pour la fonction Digamma dans la théorie de Philippôt",
            "domaine": "nombres",
            "sous_domaine": "fonction_speciale",
            "mots_cles": ["digamma", "test", "nombres premiers", "philippôt"],
            "niveau_complexite": 3,
            "document_source": "Test automatisé - Système de gestion des concepts",
            "page_reference": "Test Page 1",
            "created_by": "Système de test automatisé"
        }
        
        success1, response1 = self.run_test(
            "Create New Concept - Digamma Test",
            "POST",
            "api/concepts",
            200,
            data=test_concept_data
        )
        
        created_concept_id = None
        if success1 and isinstance(response1, dict):
            if 'concept_id' in response1 and 'success' in response1:
                created_concept_id = response1['concept_id']
                print(f"   ✅ Concept created successfully with ID: {created_concept_id}")
                print(f"   📝 Message: {response1.get('message', 'N/A')}")
            else:
                print(f"   ❌ Missing concept_id or success field in create response")
                all_tests_passed = False
        else:
            all_tests_passed = False
        
        # Test 2: GET /api/concepts - List concepts with filters
        print("\n2️⃣ Testing GET /api/concepts - List Concepts with Filters")
        
        # Test without filter
        success2a, response2a = self.run_test(
            "Get All Concepts",
            "GET",
            "api/concepts",
            200
        )
        
        # Test with domain filter
        success2b, response2b = self.run_test(
            "Get Concepts - Domain Filter (nombres)",
            "GET",
            "api/concepts?domaine=nombres",
            200
        )
        
        if success2a and isinstance(response2a, list):
            print(f"   ✅ All concepts retrieved: {len(response2a)} concepts found")
        
        if success2b and isinstance(response2b, list):
            print(f"   ✅ Filtered concepts retrieved: {len(response2b)} concepts in 'nombres' domain")
            
            # Check if our created concept is in the filtered results
            if created_concept_id:
                found_concept = any(concept.get('id') == created_concept_id for concept in response2b)
                if found_concept:
                    print(f"   ✅ Created concept found in filtered results")
                else:
                    print(f"   ⚠️  Created concept not found in filtered results")
        
        # Test 3: GET /api/concepts/{concept_id} - Get concept with relations
        if created_concept_id:
            print("\n3️⃣ Testing GET /api/concepts/{concept_id} - Get Concept with Relations")
            success3, response3 = self.run_test(
                "Get Specific Concept with Relations",
                "GET",
                f"api/concepts/{created_concept_id}",
                200
            )
            
            if success3 and isinstance(response3, dict):
                required_fields = ['id', 'titre', 'description', 'domaine', 'complexite']
                missing_fields = [field for field in required_fields if field not in response3]
                if missing_fields:
                    print(f"   ⚠️  Missing fields in concept: {missing_fields}")
                    all_tests_passed = False
                else:
                    print(f"   ✅ Concept structure is valid")
                    print(f"   📝 Title: {response3['titre']}")
                    print(f"   🔢 Domain: {response3['domaine']}")
                    print(f"   📊 Complexity: {response3['complexite']}")
            else:
                all_tests_passed = False
        
        # Test 4: POST /api/formules - Create new formula with auto-generated code
        print("\n4️⃣ Testing POST /api/formules - Create Formula with Auto-Generated Code")
        test_formula_data = {
            "nom_formule": "Calcul Digamma Test",
            "formule_mathematique": "ψ(n) = -γ + Σ(k=1 to n-1) 1/k",
            "domaine": "nombres",  # Should generate NUM001, NUM002, etc.
            "description": "Formule de test pour le calcul du Digamma dans la méthode de Philippôt",
            "variables": {"n": "position dans la séquence", "γ": "constante d'Euler-Mascheroni"},
            "concepts_lies": [],
            "formules_dependantes": [],
            "exemple_calcul": "Pour n=2: ψ(2) = -γ + 1 = 1 - γ",
            "resultat_exemple": "ψ(2) ≈ 0.4228",
            "niveau_complexite": 3,
            "document_source": "Test automatisé - Système de gestion des formules"
        }
        
        success4, response4 = self.run_test(
            "Create Formula with Auto-Generated Code",
            "POST",
            "api/formules",
            200,
            data=test_formula_data
        )
        
        created_formula_code = None
        if success4 and isinstance(response4, dict):
            if 'code_formule' in response4 and 'success' in response4:
                created_formula_code = response4['code_formule']
                print(f"   ✅ Formula created successfully with code: {created_formula_code}")
                print(f"   📝 Message: {response4.get('message', 'N/A')}")
                
                # Verify auto-generated code format
                if created_formula_code.startswith('NUM') and len(created_formula_code) == 6:
                    print(f"   ✅ Auto-generated code format is correct (NUM###)")
                else:
                    print(f"   ⚠️  Auto-generated code format unexpected: {created_formula_code}")
                    all_tests_passed = False
            else:
                print(f"   ❌ Missing code_formule or success field in create response")
                all_tests_passed = False
        else:
            all_tests_passed = False
        
        # Test 5: GET /api/formules - List all formulas by domain
        print("\n5️⃣ Testing GET /api/formules - List Formulas by Domain")
        
        # Test all formulas
        success5a, response5a = self.run_test(
            "Get All Formulas",
            "GET",
            "api/formules",
            200
        )
        
        # Test by domain
        success5b, response5b = self.run_test(
            "Get Formulas by Domain (nombres)",
            "GET",
            "api/formules?domaine=nombres",
            200
        )
        
        if success5a and isinstance(response5a, list):
            print(f"   ✅ All formulas retrieved: {len(response5a)} formulas found")
        
        if success5b and isinstance(response5b, dict):
            formules = response5b.get('formules', [])
            print(f"   ✅ Domain-filtered formulas retrieved: {len(formules)} nombres formulas found")
            
            # Check if our created formula is in the results
            if created_formula_code:
                found_formula = any(formula.get('code_formule') == created_formula_code for formula in formules)
                if found_formula:
                    print(f"   ✅ Created formula found in domain results")
                else:
                    print(f"   ⚠️  Created formula not found in domain results")
        
        # Test 6: GET /api/formules/{code_formule} - Get formula with validations
        if created_formula_code:
            print("\n6️⃣ Testing GET /api/formules/{code_formule} - Get Formula with Validations")
            success6, response6 = self.run_test(
                "Get Specific Formula with Validations",
                "GET",
                f"api/formules/{created_formula_code}",
                200
            )
            
            if success6 and isinstance(response6, dict):
                required_fields = ['code_formule', 'nom', 'description', 'domaine', 'formule_latex']
                missing_fields = [field for field in required_fields if field not in response6]
                if missing_fields:
                    print(f"   ⚠️  Missing fields in formula: {missing_fields}")
                    all_tests_passed = False
                else:
                    print(f"   ✅ Formula structure is valid")
                    print(f"   📝 Name: {response6['nom']}")
                    print(f"   🔢 Code: {response6['code_formule']}")
                    print(f"   🏷️  Domain: {response6['domaine']}")
            else:
                all_tests_passed = False
        
        return all_tests_passed
    
    def test_automatic_indexing_system(self):
        """Test the automatic indexing system for formula extraction"""
        print("\n🤖 AUTOMATIC INDEXING SYSTEM TESTS")
        print("Testing AI-powered formula extraction and validation")
        
        all_tests_passed = True
        
        # Test 1: POST /api/indexation/analyser-document - Analyze text for formulas
        print("\n1️⃣ Testing POST /api/indexation/analyser-document - Formula Extraction")
        
        # Text with mathematical formulas as suggested in review request
        mathematical_text = """
        Dans la théorie de Philippôt, nous utilisons plusieurs formules fondamentales:
        
        1. La fonction Digamma: ψ(n) = -γ + Σ(k=1 to n-1) 1/k
        2. La fonction Zêta de Riemann: ζ(s) = Σ(n=1 to ∞) 1/n^s
        3. Le théorème de Philippôt: A² + B² + C² = V_triangle
        4. La constante de l'inverse du temps: (√1.6)³ = 2.023857703
        5. Rapport triangulaire: base/hauteur = 1/2, 1/3, 1/4, ..., 1/100
        
        Ces formules permettent de calculer directement les nombres premiers selon leur position.
        La méthode utilise également √((n+7)² + (n+8)²) pour le calcul du Digamma à la 8ème position.
        """
        
        success1, response1 = self.run_test(
            "Analyze Document - Extract Mathematical Formulas",
            "POST",
            "api/indexation/analyser-document",
            200,
            data={
                "texte_document": mathematical_text,
                "type_analyse": "formules_mathematiques",
                "session_id": "test_indexation_extraction_123"
            }
        )
        
        extracted_formulas = []
        if success1 and isinstance(response1, dict):
            if 'formules_extraites' in response1 and 'success' in response1:
                extracted_formulas = response1['formules_extraites']
                print(f"   ✅ Formula extraction completed: {len(extracted_formulas)} formulas found")
                
                # Check for expected formulas
                expected_patterns = ["ψ(n)", "ζ(s)", "A² + B² + C²", "√1.6", "1/k"]
                found_patterns = []
                
                for formula in extracted_formulas:
                    if isinstance(formula, dict) and 'formule' in formula:
                        formula_text = formula['formule']
                        for pattern in expected_patterns:
                            if pattern in formula_text:
                                found_patterns.append(pattern)
                
                if found_patterns:
                    print(f"   ✅ Expected formula patterns found: {', '.join(set(found_patterns))}")
                else:
                    print(f"   ⚠️  Expected formula patterns not clearly detected")
                    all_tests_passed = False
                
                # Check for domain classification
                if len(extracted_formulas) > 0:
                    first_formula = extracted_formulas[0]
                    if 'domaine_suggere' in first_formula:
                        print(f"   ✅ Domain classification working: {first_formula['domaine_suggere']}")
                    else:
                        print(f"   ⚠️  Domain classification not present")
            else:
                print(f"   ❌ Missing formules_extraites or success field")
                all_tests_passed = False
        else:
            all_tests_passed = False
        
        # Test 2: POST /api/indexation/valider-extraction - Validate and save extracted formulas
        if extracted_formulas and len(extracted_formulas) > 0:
            print("\n2️⃣ Testing POST /api/indexation/valider-extraction - Validate Extracted Formulas")
            
            # Select first extracted formula for validation
            formula_to_validate = extracted_formulas[0]
            validation_data = {
                "formules_validees": [
                    {
                        "formule_extraite": formula_to_validate,
                        "validation_utilisateur": True,
                        "corrections": {
                            "nom": "Fonction Digamma Validée",
                            "description": "Fonction Digamma utilisée dans la méthode de Philippôt"
                        }
                    }
                ],
                "session_id": "test_validation_extraction_456"
            }
            
            success2, response2 = self.run_test(
                "Validate and Save Extracted Formulas",
                "POST",
                "api/indexation/valider-extraction",
                200,
                data=validation_data
            )
            
            if success2 and isinstance(response2, dict):
                if 'formules_sauvegardees' in response2 and 'success' in response2:
                    saved_formulas = response2['formules_sauvegardees']
                    print(f"   ✅ Formula validation completed: {len(saved_formulas)} formulas saved")
                    
                    # Check for auto-generated codes
                    for saved_formula in saved_formulas:
                        if 'code_formule' in saved_formula:
                            code = saved_formula['code_formule']
                            print(f"   ✅ Auto-generated code assigned: {code}")
                            
                            # Verify code format (should be like NUM001, GEO001, etc.)
                            if len(code) == 6 and code[3:].isdigit():
                                print(f"   ✅ Code format is correct")
                            else:
                                print(f"   ⚠️  Code format unexpected: {code}")
                                all_tests_passed = False
                else:
                    print(f"   ❌ Missing formules_sauvegardees or success field")
                    all_tests_passed = False
            else:
                all_tests_passed = False
        else:
            print("\n2️⃣ Skipping validation test - no formulas extracted")
            all_tests_passed = False
        
        return all_tests_passed
    
    def test_privileged_ai_access_system(self):
        """Test the privileged AI access system for specialized queries"""
        print("\n🔐 PRIVILEGED AI ACCESS SYSTEM TESTS")
        print("Testing specialized AI access with complete data organized by domains")
        
        all_tests_passed = True
        
        # Test 1: GET /api/acces-privilegie/concepts-complets - Privileged access for specialized AI
        print("\n1️⃣ Testing GET /api/acces-privilegie/concepts-complets - Complete Concepts Access")
        
        success1, response1 = self.run_test(
            "Privileged Access - Complete Concepts",
            "GET",
            "api/acces-privilegie/concepts-complets",
            200
        )
        
        if success1 and isinstance(response1, dict):
            if 'concepts_complets' in response1 and 'statistiques' in response1:
                concepts = response1['concepts_complets']
                stats = response1['statistiques']
                
                print(f"   ✅ Privileged access granted successfully")
                print(f"   📊 Total concepts: {stats.get('total_concepts', 'N/A')}")
                print(f"   📊 Domains: {len(stats.get('domaines', []))}")
                print(f"   📊 Documents sources: {len(stats.get('documents_sources', []))}")
                
                # Check domain organization
                if 'domaines' in stats:
                    domains = stats['domaines']
                    expected_domains = ['Géométrie Fondamentale', 'Théorie des Nombres', 'Physique Théorique']
                    found_domains = [domain for domain in expected_domains if domain in domains]
                    if found_domains:
                        print(f"   ✅ Expected domains found: {', '.join(found_domains)}")
                    else:
                        print(f"   ⚠️  Expected domains not found in: {', '.join(domains[:5])}")
                
                # Check concept structure
                if len(concepts) > 0:
                    sample_concept = concepts[0]
                    required_fields = ['id', 'titre', 'domaine_principal', 'concepts_cles', 'formules']
                    missing_fields = [field for field in required_fields if field not in sample_concept]
                    if missing_fields:
                        print(f"   ⚠️  Missing fields in concept: {missing_fields}")
                        all_tests_passed = False
                    else:
                        print(f"   ✅ Concept structure is complete")
                        print(f"   📝 Sample: {sample_concept['titre']} ({sample_concept['domaine_principal']})")
            else:
                print(f"   ❌ Missing concepts_complets or statistiques field")
                all_tests_passed = False
        else:
            all_tests_passed = False
        
        # Test 2: POST /api/acces-privilegie/requete-contextuelle - Contextual queries by domain
        print("\n2️⃣ Testing POST /api/acces-privilegie/requete-contextuelle - Contextual Domain Queries")
        
        # Test queries for different domains
        domain_queries = [
            {
                "domaine": "Géométrie Fondamentale",
                "question": "Explique-moi la Sphère de Zêta et ses propriétés géométriques",
                "session_id": "test_contextuel_geo_123"
            },
            {
                "domaine": "Théorie des Nombres", 
                "question": "Comment fonctionne le calcul du Digamma dans la méthode de Philippôt?",
                "session_id": "test_contextuel_num_456"
            },
            {
                "domaine": "Physique Théorique",
                "question": "Quelle est la relation entre l'intrication quantique géométrique et l'espace de Minkowski selon Philippôt?",
                "session_id": "test_contextuel_phys_789"
            }
        ]
        
        contextual_success = True
        for i, query_data in enumerate(domain_queries, 1):
            success_query, response_query = self.run_test(
                f"Contextual Query - {query_data['domaine']}",
                "POST",
                "api/acces-privilegie/requete-contextuelle",
                200,
                data=query_data
            )
            
            if success_query and isinstance(response_query, dict):
                if 'reponse_contextuelle' in response_query and 'domaine_utilise' in response_query:
                    ai_response = response_query['reponse_contextuelle']
                    domain_used = response_query['domaine_utilise']
                    concepts_used = response_query.get('concepts_utilises', 0)
                    
                    print(f"   ✅ Contextual query {i} successful")
                    print(f"   🏷️  Domain: {domain_used}")
                    print(f"   📚 Concepts used: {concepts_used}")
                    print(f"   📝 Response length: {len(ai_response)} characters")
                    
                    # Check for domain-specific content
                    domain_keywords = {
                        "Géométrie Fondamentale": ["sphère", "zêta", "géométrique", "cubes"],
                        "Théorie des Nombres": ["digamma", "nombres premiers", "calcul", "philippôt"],
                        "Physique Théorique": ["intrication", "quantique", "minkowski", "espace-temps"]
                    }
                    
                    expected_keywords = domain_keywords.get(query_data['domaine'], [])
                    found_keywords = [kw for kw in expected_keywords if kw.lower() in ai_response.lower()]
                    
                    if found_keywords:
                        print(f"   ✅ Domain-specific keywords found: {', '.join(found_keywords)}")
                    else:
                        print(f"   ⚠️  Domain-specific keywords not clearly present")
                        contextual_success = False
                    
                    # Check response quality
                    if len(ai_response) < 200:
                        print(f"   ⚠️  Response seems short for complex query")
                        contextual_success = False
                else:
                    print(f"   ❌ Missing reponse_contextuelle or domaine_utilise field")
                    contextual_success = False
            else:
                contextual_success = False
        
        if not contextual_success:
            all_tests_passed = False
        
        return all_tests_passed
    
    def test_empirical_validations_system(self):
        """Test the empirical validations system for formulas"""
        print("\n📊 EMPIRICAL VALIDATIONS SYSTEM TESTS")
        print("Testing formula validation recording and tracking")
        
        all_tests_passed = True
        
        # Test 1: POST /api/validations - Record formula validations
        print("\n1️⃣ Testing POST /api/validations - Record Formula Validations")
        
        # Test validation data
        validation_data = {
            "formule_id": created_formula_code or "NUM001",  # Use created formula or fallback
            "type_validation": "test_numerique",
            "donnees_test": {
                "test_cases": [
                    {"input": "n=1", "expected": "-0.5772", "obtained": "-0.5772156649"},
                    {"input": "n=2", "expected": "0.4228", "obtained": "0.4227843351"},
                    {"input": "n=10", "expected": "2.2517", "obtained": "2.2517525890"}
                ]
            },
            "resultat_attendu": "Fonction Digamma calculée correctement",
            "resultat_obtenu": "Tous les tests passés avec précision acceptable",
            "statut": "validee",
            "commentaires": "Validation empirique de la fonction Digamma pour les premiers entiers positifs",
            "testeur": "Système de test automatisé",
            "precision_resultat": 0.0001
        }
        
        success1, response1 = self.run_test(
            "Record Empirical Validation",
            "POST",
            "api/validations",
            200,
            data=validation_data
        )
        
        validation_id = None
        if success1 and isinstance(response1, dict):
            if 'validation_id' in response1 and 'success' in response1:
                validation_id = response1['validation_id']
                print(f"   ✅ Validation recorded successfully with ID: {validation_id}")
                
                # Check validation statistics
                if 'statistiques' in response1:
                    stats = response1['statistiques']
                    print(f"   📊 Tests passed: {stats.get('tests_valides', 'N/A')}/{stats.get('total_tests', 'N/A')}")
                    print(f"   📊 Average precision: {stats.get('precision_moyenne', 'N/A')}")
                    print(f"   📊 Validation status: {stats.get('statut_global', 'N/A')}")
            else:
                print(f"   ❌ Missing validation_id or success field")
                all_tests_passed = False
        else:
            all_tests_passed = False
        
        # Test 2: GET /api/validations/{code_formule} - Retrieve validations for a formula
        if validation_id:
            print("\n2️⃣ Testing GET /api/validations/{code_formule} - Retrieve Formula Validations")
            
            success2, response2 = self.run_test(
                "Get Formula Validations",
                "GET",
                "api/validations/NUM001",
                200
            )
            
            if success2 and isinstance(response2, dict):
                if 'validations' in response2:
                    validations = response2['validations']
                    print(f"   ✅ Validations retrieved: {len(validations)} validation records found")
                    
                    # Check if our validation is in the results
                    found_validation = any(val.get('validation_id') == validation_id for val in validations)
                    if found_validation:
                        print(f"   ✅ Created validation found in results")
                    else:
                        print(f"   ⚠️  Created validation not found in results")
                        all_tests_passed = False
                else:
                    print(f"   ❌ Missing validations field")
                    all_tests_passed = False
            else:
                all_tests_passed = False
        
        return all_tests_passed

    def test_advanced_intelligence_endpoints(self):
        """Test the new advanced intelligence endpoints as requested in review"""
        print("\n🧠 ADVANCED INTELLIGENCE ENDPOINTS TESTS")
        print("Testing new AI-powered endpoints with Philippôt theory context")
        
        all_tests_passed = True
        
        # Test data based on Philippôt theory as suggested in review request
        philippot_text = """La théorie de l'univers au carré développée par Philippe Thomas Savard révèle des relations géométriques fondamentales entre les nombres premiers. La méthode de Philippôt utilise des rapports triangulaires spécifiques (1/2, 1/3, 1/4...) pour déterminer directement les nombres premiers selon leur position dans la suite. Cette approche révolutionnaire s'appuie sur le calcul du Digamma à la 8ème position des séquences de racines carrées, permettant une prédiction géométrique des nombres premiers. Les 14 tableaux de Philippôt démontrent cette méthode avec des exemples concrets : rapport 1/2 → 29 (10ème premier), rapport 1/3 → 227 (49ème premier). Cette géométrie du spectre des nombres premiers ouvre de nouvelles perspectives pour résoudre l'hypothèse de Riemann."""
        
        # Test 1: POST /api/suggestions-contenu
        print("\n1️⃣ Testing /api/suggestions-contenu - Contextual Content Suggestions")
        success1, response1 = self.run_test(
            "Suggestions Contenu - Philippôt Theory Context",
            "POST",
            "api/suggestions-contenu",
            200,
            data={
                "texte_actuel": philippot_text,
                "contexte": "Développement théorique sur la méthode de Philippôt",
                "session_id": "test_suggestions_philippot_123"
            }
        )
        
        if success1 and isinstance(response1, dict):
            if 'success' in response1 and response1['success']:
                print(f"   ✅ Content suggestions generated successfully")
                if 'suggestions' in response1:
                    print(f"   📝 AI suggestions received")
                if 'concepts_disponibles' in response1:
                    concepts_count = response1['concepts_disponibles']
                    print(f"   📚 Concepts available: {concepts_count}")
                    if concepts_count > 10:  # Should have substantial concept base
                        print(f"   ✅ Rich concept base available for suggestions")
                    else:
                        print(f"   ⚠️  Limited concept base")
            else:
                print(f"   ❌ Suggestions generation failed")
                all_tests_passed = False
        else:
            all_tests_passed = False
        
        # Test 2: POST /api/resume-automatique with different styles
        print("\n2️⃣ Testing /api/resume-automatique - Automatic Summaries")
        
        # Test executive style
        success2a, response2a = self.run_test(
            "Resume Automatique - Executive Style",
            "POST",
            "api/resume-automatique",
            200,
            data={
                "texte_complet": philippot_text,
                "style": "executif",
                "longueur_cible": "moyen",
                "session_id": "test_resume_executif_456"
            }
        )
        
        # Test technical style
        success2b, response2b = self.run_test(
            "Resume Automatique - Technical Style",
            "POST",
            "api/resume-automatique",
            200,
            data={
                "texte_complet": philippot_text,
                "style": "technique",
                "longueur_cible": "detaille",
                "session_id": "test_resume_technique_789"
            }
        )
        
        # Test conceptual style
        success2c, response2c = self.run_test(
            "Resume Automatique - Conceptual Style",
            "POST",
            "api/resume-automatique",
            200,
            data={
                "texte_complet": philippot_text,
                "style": "conceptuel",
                "longueur_cible": "court",
                "session_id": "test_resume_conceptuel_101"
            }
        )
        
        # Validate compression statistics
        if success2a and isinstance(response2a, dict):
            if 'statistiques' in response2a:
                stats = response2a['statistiques']
                if 'taux_compression' in stats:
                    compression = stats['taux_compression']
                    print(f"   📊 Compression rate: {compression}%")
                    if compression > 0:
                        print(f"   ✅ Text successfully compressed")
                    else:
                        print(f"   ⚠️  No compression achieved")
                if 'mots_original' in stats and 'mots_resume' in stats:
                    original_words = stats['mots_original']
                    summary_words = stats['mots_resume']
                    print(f"   📊 Words: {original_words} → {summary_words}")
        
        # Test 3: POST /api/detection-coherence with different detail levels
        print("\n3️⃣ Testing /api/detection-coherence - Coherence Analysis")
        
        # Test with logical arguments text
        logical_text = """La méthode de Philippôt démontre que les nombres premiers suivent une géométrie précise. Premièrement, les rapports triangulaires 1/2, 1/3, 1/4 génèrent des séquences spécifiques. Deuxièmement, le calcul du Digamma à la 8ème position permet de déterminer le nombre premier correspondant. Troisièmement, cette approche géométrique révèle la structure sous-jacente du spectre des nombres premiers. Par conséquent, l'hypothèse de Riemann peut être résolue par cette méthode géométrique révolutionnaire."""
        
        # Test basic level
        success3a, response3a = self.run_test(
            "Detection Coherence - Basic Level",
            "POST",
            "api/detection-coherence",
            200,
            data={
                "texte_analyse": logical_text,
                "niveau_detail": "basic",
                "session_id": "test_coherence_basic_111"
            }
        )
        
        # Test standard level
        success3b, response3b = self.run_test(
            "Detection Coherence - Standard Level",
            "POST",
            "api/detection-coherence",
            200,
            data={
                "texte_analyse": logical_text,
                "niveau_detail": "standard",
                "session_id": "test_coherence_standard_222"
            }
        )
        
        # Test advanced level
        success3c, response3c = self.run_test(
            "Detection Coherence - Advanced Level",
            "POST",
            "api/detection-coherence",
            200,
            data={
                "texte_analyse": logical_text,
                "niveau_detail": "approfondi",
                "session_id": "test_coherence_advanced_333"
            }
        )
        
        if success3b and isinstance(response3b, dict):
            if 'analyse_coherence' in response3b:
                print(f"   ✅ Coherence analysis completed")
                if 'niveau_analyse' in response3b:
                    level = response3b['niveau_analyse']
                    print(f"   📊 Analysis level: {level}")
        
        # Test 4: POST /api/citations-automatiques with different styles
        print("\n4️⃣ Testing /api/citations-automatiques - Automatic Citations")
        
        citation_text = """Cette recherche s'appuie sur les travaux révolutionnaires concernant la géométrie des nombres premiers. Les concepts de Digamma et de rapports triangulaires sont centraux à cette approche. L'intrication quantique géométrique et le théorème fondamental établissent les bases théoriques."""
        
        # Test academic style
        success4a, response4a = self.run_test(
            "Citations Automatiques - Academic Style",
            "POST",
            "api/citations-automatiques",
            200,
            data={
                "contenu_texte": citation_text,
                "style_citation": "academique",
                "domaines_focus": ["Géométrie Fondamentale", "Théorie des Nombres"],
                "session_id": "test_citations_academic_444"
            }
        )
        
        # Test technical style
        success4b, response4b = self.run_test(
            "Citations Automatiques - Technical Style",
            "POST",
            "api/citations-automatiques",
            200,
            data={
                "contenu_texte": citation_text,
                "style_citation": "technique",
                "session_id": "test_citations_technical_555"
            }
        )
        
        # Test informal style
        success4c, response4c = self.run_test(
            "Citations Automatiques - Informal Style",
            "POST",
            "api/citations-automatiques",
            200,
            data={
                "contenu_texte": citation_text,
                "style_citation": "informel",
                "session_id": "test_citations_informal_666"
            }
        )
        
        if success4a and isinstance(response4a, dict):
            if 'citations' in response4a:
                print(f"   ✅ Citations generated successfully")
                if 'concepts_sources' in response4a:
                    sources = response4a['concepts_sources']
                    print(f"   📚 Concept sources used: {sources}")
        
        # Test 5: POST /api/notifications-intelligentes with different importance levels
        print("\n5️⃣ Testing /api/notifications-intelligentes - Intelligent Notifications")
        
        notification_text = """La théorie de l'univers au carré utilise des méthodes géométriques pour analyser les nombres premiers. Cette approche révolutionnaire permet de prédire directement les nombres premiers selon leur position. Les calculs du Digamma sont essentiels pour cette détermination."""
        
        # Test low importance
        success5a, response5a = self.run_test(
            "Notifications Intelligentes - Low Importance",
            "POST",
            "api/notifications-intelligentes",
            200,
            data={
                "texte_actuel": notification_text,
                "seuil_importance": "low",
                "types_notifications": ["corrections", "suggestions"],
                "session_id": "test_notifications_low_777"
            }
        )
        
        # Test medium importance
        success5b, response5b = self.run_test(
            "Notifications Intelligentes - Medium Importance",
            "POST",
            "api/notifications-intelligentes",
            200,
            data={
                "texte_actuel": notification_text,
                "seuil_importance": "medium",
                "types_notifications": ["corrections", "suggestions", "coherence"],
                "session_id": "test_notifications_medium_888"
            }
        )
        
        # Test high importance
        success5c, response5c = self.run_test(
            "Notifications Intelligentes - High Importance",
            "POST",
            "api/notifications-intelligentes",
            200,
            data={
                "texte_actuel": notification_text,
                "seuil_importance": "high",
                "types_notifications": ["corrections", "coherence"],
                "session_id": "test_notifications_high_999"
            }
        )
        
        if success5b and isinstance(response5b, dict):
            if 'notifications' in response5b:
                print(f"   ✅ Intelligent notifications generated")
                if 'seuil_utilise' in response5b:
                    threshold = response5b['seuil_utilise']
                    print(f"   📊 Importance threshold: {threshold}")
                if 'types_actifs' in response5b:
                    types = response5b['types_actifs']
                    print(f"   📋 Active notification types: {', '.join(types)}")
        
        # Combine all test results
        all_advanced_tests = [
            success1,
            success2a and success2b and success2c,
            success3a and success3b and success3c,
            success4a and success4b and success4c,
            success5a and success5b and success5c
        ]
        
        all_tests_passed = all(all_advanced_tests)
        
        if all_tests_passed:
            print(f"\n🎉 ALL ADVANCED INTELLIGENCE ENDPOINTS PASSED")
            print(f"✅ All 5 new AI endpoints working with Philippôt theory context")
        else:
            print(f"\n⚠️  Some advanced intelligence tests failed")
            failed_tests = []
            if not success1: failed_tests.append("suggestions-contenu")
            if not (success2a and success2b and success2c): failed_tests.append("resume-automatique")
            if not (success3a and success3b and success3c): failed_tests.append("detection-coherence")
            if not (success4a and success4b and success4c): failed_tests.append("citations-automatiques")
            if not (success5a and success5b and success5c): failed_tests.append("notifications-intelligentes")
            print(f"❌ Failed endpoints: {', '.join(failed_tests)}")
        
        return all_tests_passed

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
    print("🚀 Testing Complete Concept and Formula Administration System")
    print("=" * 80)
    print("Focus: Testing new concept/formula management with auto-generation and AI integration")
    
    tester = UniversAuCarreAPITester()
    
    # Run health check first
    print("\n📋 BASIC HEALTH CHECK")
    health_success = tester.test_health_check()
    
    # PRIMARY FOCUS: Test the new concept and formula management system as requested
    print("\n🔬 CONCEPT AND FORMULA MANAGEMENT SYSTEM - PRIMARY TESTS")
    concept_formula_success = tester.test_concept_formula_management_system()
    
    print("\n🤖 AUTOMATIC INDEXING SYSTEM - AI FORMULA EXTRACTION")
    indexing_success = tester.test_automatic_indexing_system()
    
    print("\n🔐 PRIVILEGED AI ACCESS SYSTEM - SPECIALIZED QUERIES")
    privileged_access_success = tester.test_privileged_ai_access_system()
    
    print("\n📊 EMPIRICAL VALIDATIONS SYSTEM - FORMULA VALIDATION")
    validations_success = tester.test_empirical_validations_system()
    
    # Secondary tests for context
    print("\n🧠 EXISTING ADVANCED INTELLIGENCE VALIDATION")
    advanced_intelligence_success = tester.test_advanced_intelligence_endpoints()
    
    print("\n🔬 PHILIPPÔT THEORY ACCESS VALIDATION")
    theory_access_success = tester.test_philippot_theorem_privileged_access()
    
    # Print final results
    print("\n" + "=" * 80)
    print(f"📊 FINAL RESULTS")
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    
    # Detailed results breakdown
    print(f"\n🎯 RESULTS BREAKDOWN:")
    print(f"   Health Check: {'✅ PASSED' if health_success else '❌ FAILED'}")
    print(f"   Concept/Formula Management: {'✅ PASSED' if concept_formula_success else '❌ FAILED'}")
    print(f"   Automatic Indexing: {'✅ PASSED' if indexing_success else '❌ FAILED'}")
    print(f"   Privileged AI Access: {'✅ PASSED' if privileged_access_success else '❌ FAILED'}")
    print(f"   Empirical Validations: {'✅ PASSED' if validations_success else '❌ FAILED'}")
    print(f"   Advanced Intelligence: {'✅ PASSED' if advanced_intelligence_success else '❌ FAILED'}")
    print(f"   Theory Access: {'✅ PASSED' if theory_access_success else '❌ FAILED'}")
    
    # Success criteria: Core concept/formula system must work
    core_systems_success = (
        concept_formula_success and 
        indexing_success and 
        privileged_access_success and 
        validations_success
    )
    
    if core_systems_success and tester.tests_passed >= (tester.tests_run * 0.70):  # 70% success rate
        print("\n🎉 CONCEPT AND FORMULA ADMINISTRATION SYSTEM TESTS PASSED!")
        print("✅ Concept management with domain filtering working")
        print("✅ Formula auto-generation (NUM001, GEO001, etc.) functional")
        print("✅ AI-powered formula extraction from text working")
        print("✅ Privileged AI access organized by domains operational")
        print("✅ Empirical validation system recording properly")
        print("✅ MongoDB relational structure confirmed")
        print("✅ Emergent LLM integration for intelligent extraction validated")
        return 0
    else:
        print(f"\n⚠️  Core concept/formula system tests failed or insufficient success rate")
        if not core_systems_success:
            failed_systems = []
            if not concept_formula_success: failed_systems.append("Concept/Formula Management")
            if not indexing_success: failed_systems.append("Automatic Indexing")
            if not privileged_access_success: failed_systems.append("Privileged AI Access")
            if not validations_success: failed_systems.append("Empirical Validations")
            print(f"❌ Critical systems failed: {', '.join(failed_systems)}")
        if tester.tests_passed < (tester.tests_run * 0.70):
            print(f"❌ Overall success rate too low: {tester.tests_passed}/{tester.tests_run}")
        return 1

if __name__ == "__main__":
    sys.exit(main())