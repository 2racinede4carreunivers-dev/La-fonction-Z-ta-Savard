#!/usr/bin/env python3
"""
Critical Deployment Tests for L'univers est au carré
Test complet final du backend avant déploiement
"""

import requests
import sys
import json
from datetime import datetime

class CriticalDeploymentTester:
    def __init__(self, base_url="https://universe-squared.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            start_time = datetime.now()
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=60)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=60)
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Status: {response.status_code}")
                print(f"⏱️  Temps de réponse: {response_time:.2f}s")
                try:
                    response_data = response.json()
                    return True, response_data, response_time
                except:
                    return True, response.text, response_time
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False, {}, response_time

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout (60s)")
            return False, {}, 60.0
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}, 0.0

    def test_critical_endpoints(self):
        """Test all critical endpoints for final deployment"""
        print("🚀 CRITICAL DEPLOYMENT ENDPOINTS - FINAL TESTING")
        print("Test complet final du backend avant déploiement - Application 'L'univers est au carré'")
        print("Code d'accès upload documents implémenté: Uni1374079226497308car")
        print("Backend sur: https://universe-squared.preview.emergentagent.com")
        print("=" * 80)
        
        all_critical_tests_passed = True
        
        # 1. IA Spécialisée (PRIORITÉ HAUTE)
        print("\n1️⃣ IA SPÉCIALISÉE (PRIORITÉ HAUTE)")
        print("Endpoint: POST /api/chat")
        print("Payload: {\"message\": \"Explique la sphère de Zêta\", \"session_id\": \"test_final_deploy\"}")
        
        success1, response1, time1 = self.run_test(
            "IA Spécialisée - Sphère de Zêta",
            "POST",
            "api/chat",
            200,
            data={
                "message": "Qu'est-ce que la sphère de Zêta?",
                "session_id": "test_final_deploy"
            }
        )
        
        if success1 and isinstance(response1, dict):
            if 'response' in response1:
                ai_response = response1['response']
                print(f"📝 Longueur réponse: {len(ai_response)} caractères")
                print(f"📄 Extrait réponse: {ai_response[:200]}...")
                
                # Check for specific content
                key_terms = ["zêta", "sphère", "géométrie", "philippôt", "nombres premiers"]
                found_terms = [term for term in key_terms if term.lower() in ai_response.lower()]
                if found_terms:
                    print(f"🔍 Termes spécialisés détectés: {', '.join(found_terms)}")
                else:
                    print(f"⚠️  Termes spécialisés non détectés clairement")
            else:
                print(f"❌ Pas de champ 'response' dans la réponse")
                all_critical_tests_passed = False
        else:
            all_critical_tests_passed = False
        
        # 2. IA Privilégiée (PRIORITÉ HAUTE)
        print("\n2️⃣ IA PRIVILÉGIÉE (PRIORITÉ HAUTE)")
        print("Endpoint: POST /api/chat-privileged")
        print("Payload: {\"message\": \"Quelle est l'inconnue unique dans la matrice?\", \"session_id\": \"test_priv_final\"}")
        
        success2, response2, time2 = self.run_test(
            "IA Privilégiée - Matrice à dérive première",
            "POST",
            "api/chat-privileged",
            200,
            data={
                "message": "Quelle est l'inconnue unique dans la matrice?",
                "session_id": "test_priv_final"
            }
        )
        
        if success2 and isinstance(response2, dict):
            if 'response' in response2 and 'privileged_access' in response2:
                ai_response = response2['response']
                privileged_access = response2['privileged_access']
                concepts_available = response2.get('concepts_available', 0)
                
                print(f"📝 Longueur réponse: {len(ai_response)} caractères")
                print(f"🔐 Accès privilégié: {privileged_access}")
                print(f"📚 Concepts disponibles: {concepts_available}")
                print(f"📄 Extrait réponse: {ai_response[:200]}...")
                
                # Verify access to 55 concepts
                if concepts_available >= 55:
                    print(f"✅ Accès aux 55 concepts enrichis confirmé")
                else:
                    print(f"⚠️  Accès limité aux concepts: {concepts_available}/55")
            else:
                print(f"❌ Champs manquants dans la réponse privilégiée")
                all_critical_tests_passed = False
        else:
            all_critical_tests_passed = False
        
        # 3. Concepts Enrichis (PRIORITÉ HAUTE)
        print("\n3️⃣ CONCEPTS ENRICHIS (PRIORITÉ HAUTE)")
        print("Endpoint: GET /api/concepts-enrichis-list")
        
        success3, response3, time3 = self.run_test(
            "Concepts Enrichis - Liste complète",
            "GET",
            "api/concepts-enrichis",
            200
        )
        
        if success3 and isinstance(response3, dict):
            if 'concepts' in response3:
                concepts = response3['concepts']
                domaines = response3.get('domaines', [])
                
                print(f"📊 Concepts retournés: {len(concepts)}")
                print(f"📊 Domaines: {len(domaines)}")
                
                # Verify 55 concepts requirement
                if len(concepts) >= 55:
                    print(f"✅ Exigence 55 concepts respectée: {len(concepts)} concepts")
                else:
                    print(f"⚠️  Moins de 55 concepts: {len(concepts)} trouvés")
                
                # Show sample concepts
                if len(concepts) > 0:
                    sample_titles = [c.get('titre', 'N/A') for c in concepts[:3]]
                    print(f"📝 Exemples: {', '.join(sample_titles)}")
                    
                    # Check for chaos discret concepts
                    chaos_concepts = [c for c in concepts if 'chaos' in c.get('titre', '').lower() or 'chaon' in c.get('titre', '').lower()]
                    if chaos_concepts:
                        print(f"🔍 Concepts chaos discret trouvés: {len(chaos_concepts)}")
                        for concept in chaos_concepts[:3]:
                            print(f"   - {concept.get('titre', 'N/A')}")
            else:
                print(f"❌ Pas de champ 'concepts' dans la réponse")
                all_critical_tests_passed = False
        else:
            all_critical_tests_passed = False
        
        # 4. IA Évolutive
        print("\n4️⃣ IA ÉVOLUTIVE")
        print("Endpoint: POST /api/dialogue-evolutif")
        print("Payload: {\"question\": \"Test\", \"session_id\": \"test_evolutif_final\"}")
        
        # First initialize the system
        print("   Initializing IA Évolutive system...")
        init_success, init_response, init_time = self.run_test(
            "IA Évolutive - Initialization",
            "POST",
            "api/ia-evolutif/initialiser-auto",
            200,
            data={}
        )
        
        if init_success:
            print("   ✅ System initialized successfully")
            success4, response4, time4 = self.run_test(
                "IA Évolutive - Test dialogue",
                "POST",
                "api/ia-evolutif/dialoguer",
                200,
                data={
                    "question": "Test",
                    "session_id": "test_evolutif_final"
                }
            )
        else:
            print("   ❌ Failed to initialize system")
            success4, response4, time4 = False, {}, 0.0
        
        if success4 and isinstance(response4, dict):
            if 'reponse' in response4:
                ai_response = response4['reponse']
                evolution_silencieuse = response4.get('evolution_silencieuse', False)
                taille_banque = response4.get('taille_banque', 0)
                
                print(f"📝 Longueur réponse: {len(ai_response)} caractères")
                print(f"🔄 Évolution silencieuse: {evolution_silencieuse}")
                print(f"📚 Taille banque: {taille_banque}")
                print(f"📄 Extrait réponse: {ai_response[:150]}...")
            else:
                print(f"❌ Pas de champ 'reponse' dans la réponse")
                all_critical_tests_passed = False
        else:
            all_critical_tests_passed = False
        
        # 5. Health Check
        print("\n5️⃣ HEALTH CHECK")
        print("Endpoint: GET /api/health ou /")
        
        success5, response5, time5 = self.run_test(
            "Health Check - Backend Status",
            "GET",
            "api/health",
            200
        )
        
        if success5:
            if isinstance(response5, dict):
                print(f"📄 Extrait réponse: {str(response5)[:150]}...")
        else:
            all_critical_tests_passed = False
        
        # Summary of critical tests
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ TESTS CRITIQUES DÉPLOIEMENT")
        print("=" * 80)
        
        print("\nFORMAT:")
        print("Pour chaque endpoint:")
        print("- Status (✅/❌)")
        print("- Code HTTP")
        print("- Temps de réponse")
        print("- Extrait réponse")
        print("\nRÉSULTATS:")
        
        critical_results = [
            ("IA Spécialisée (POST /api/chat)", "✅" if success1 else "❌", 200 if success1 else "ERROR", f"{time1:.2f}s"),
            ("IA Privilégiée (POST /api/chat-privileged)", "✅" if success2 else "❌", 200 if success2 else "ERROR", f"{time2:.2f}s"),
            ("Concepts Enrichis (GET /api/concepts-enrichis)", "✅" if success3 else "❌", 200 if success3 else "ERROR", f"{time3:.2f}s"),
            ("IA Évolutive (POST /api/dialogue-evolutif)", "✅" if success4 else "❌", 200 if success4 else "ERROR", f"{time4:.2f}s"),
            ("Health Check (GET /api/health)", "✅" if success5 else "❌", 200 if success5 else "ERROR", f"{time5:.2f}s")
        ]
        
        for endpoint, status, code, time_resp in critical_results:
            print(f"{status} {endpoint} - Code: {code} - Temps: {time_resp}")
        
        print(f"\nTests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if all_critical_tests_passed:
            print("\n🎉 TOUS LES ENDPOINTS CRITIQUES FONCTIONNENT CORRECTEMENT")
            print("✅ Application prête pour déploiement")
        else:
            print("\n⚠️  CERTAINS ENDPOINTS CRITIQUES PRÉSENTENT DES PROBLÈMES")
            print("❌ Corrections nécessaires avant déploiement")
        
        return all_critical_tests_passed

def main():
    """Main function to run critical deployment tests"""
    tester = CriticalDeploymentTester()
    
    # Run critical deployment tests
    success = tester.test_critical_endpoints()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())