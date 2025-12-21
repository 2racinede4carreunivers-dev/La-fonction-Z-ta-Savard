#!/usr/bin/env python3

import requests
import json
import sys

def test_concept_formula_system():
    """Test the concept and formula management system specifically"""
    base_url = "https://universe-squared.preview.emergentagent.com"
    
    print("🔬 FOCUSED TEST: Concept and Formula Management System")
    print("=" * 60)
    
    # Test 1: Create a concept
    print("\n1️⃣ Testing POST /api/concepts")
    concept_data = {
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
    
    try:
        response = requests.post(f"{base_url}/api/concepts", json=concept_data, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            concept_id = result.get('concept_id')
            print(f"✅ Concept created with ID: {concept_id}")
        else:
            print(f"❌ Failed to create concept")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Create a formula
    print("\n2️⃣ Testing POST /api/formules")
    formula_data = {
        "code_formule": "",  # Should be auto-generated
        "nom_formule": "Calcul Digamma Test",
        "formule_mathematique": "ψ(n) = -γ + Σ(k=1 to n-1) 1/k",
        "domaine": "nombres",
        "description": "Formule de test pour le calcul du Digamma dans la méthode de Philippôt",
        "variables": {"n": "position dans la séquence", "γ": "constante d'Euler-Mascheroni"},
        "concepts_lies": [],
        "formules_dependantes": [],
        "exemple_calcul": "Pour n=2: ψ(2) = -γ + 1 = 1 - γ",
        "resultat_exemple": "ψ(2) ≈ 0.4228",
        "niveau_complexite": 3,
        "document_source": "Test automatisé - Système de gestion des formules"
    }
    
    try:
        response = requests.post(f"{base_url}/api/formules", json=formula_data, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            formula_code = result.get('code_formule')
            print(f"✅ Formula created with code: {formula_code}")
        else:
            print(f"❌ Failed to create formula")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 3: List formulas
    print("\n3️⃣ Testing GET /api/formules")
    try:
        response = requests.get(f"{base_url}/api/formules", timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            formulas = result.get('formules', [])
            print(f"✅ Retrieved {len(formulas)} formulas")
        else:
            print(f"❌ Failed to list formulas: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Test indexation system
    print("\n4️⃣ Testing POST /api/indexation/analyser-document")
    indexation_data = {
        "texte_document": """
        Dans la théorie de Philippôt, nous utilisons plusieurs formules fondamentales:
        1. La fonction Digamma: ψ(n) = -γ + Σ(k=1 to n-1) 1/k
        2. La fonction Zêta de Riemann: ζ(s) = Σ(n=1 to ∞) 1/n^s
        3. Le théorème de Philippôt: A² + B² + C² = V_triangle
        """,
        "type_analyse": "formules_mathematiques",
        "session_id": "test_indexation_123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/indexation/analyser-document", json=indexation_data, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Document analysis completed")
        else:
            print(f"❌ Failed document analysis")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Test privileged access
    print("\n5️⃣ Testing GET /api/acces-privilegie/concepts-complets")
    try:
        response = requests.get(f"{base_url}/api/acces-privilegie/concepts-complets", timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Privileged access working")
            print(f"Response keys: {list(result.keys())}")
        else:
            print(f"❌ Failed privileged access: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 FOCUSED TEST COMPLETED")
    return True

if __name__ == "__main__":
    test_concept_formula_system()