#!/usr/bin/env python3
"""
Edge case testing for collaboration endpoints
"""
import requests
import json

def test_collaboration_edge_cases():
    base_url = "https://universe-squared.preview.emergentagent.com"
    
    print("🧪 Testing Collaboration Edge Cases")
    print("=" * 50)
    
    # Test 1: Empty document
    print("\n1. Testing empty document collaboration...")
    empty_doc_data = {
        "document": "",
        "request": "Ajoute du contenu sur la théorie de l'univers au carré",
        "session_id": "edge_test_empty",
        "document_title": "Document Vide"
    }
    
    try:
        response = requests.post(f"{base_url}/api/collaborate", json=empty_doc_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get('updated_document'):
                print(f"   ✅ Empty document handled - Added {len(result['updated_document'])} chars")
            else:
                print("   ❌ No updated document returned")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 2: Very long document
    print("\n2. Testing very long document...")
    long_doc = "La théorie de l'univers au carré. " * 100  # ~3500 chars
    long_doc_data = {
        "document": long_doc,
        "request": "Résume les points clés",
        "session_id": "edge_test_long",
        "document_title": "Document Long"
    }
    
    try:
        response = requests.post(f"{base_url}/api/collaborate", json=long_doc_data, timeout=45)
        if response.status_code == 200:
            result = response.json()
            if result.get('updated_document'):
                print(f"   ✅ Long document handled - Result: {len(result['updated_document'])} chars")
            else:
                print("   ❌ No updated document returned")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 3: Special characters and accents
    print("\n3. Testing special characters...")
    special_doc = """## Théorie révolutionnaire de Philippe Thomas Savard

    Concepts mathématiques avec caractères spéciaux:
    - Géométrie → triangles rectangles
    - Séquences √((n+7)² + (n+8)²)
    - Rapports 1/2, 1/3, 1/4... 1/100
    - Digamma ψ à la 8ème position
    - Zêta ζ de Philippôt
    
    Émojis: 🔢 📐 ∞ ∑ ∏ ∫"""
    
    special_data = {
        "document": special_doc,
        "request": "Développe les aspects techniques avec précision mathématique",
        "session_id": "edge_test_special",
        "document_title": "Document avec Caractères Spéciaux"
    }
    
    try:
        response = requests.post(f"{base_url}/api/collaborate", json=special_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get('updated_document'):
                print(f"   ✅ Special characters handled - Result: {len(result['updated_document'])} chars")
                # Check if special characters are preserved
                updated = result['updated_document']
                if '√' in updated and 'ψ' in updated and 'ζ' in updated:
                    print("   ✅ Mathematical symbols preserved")
                else:
                    print("   ⚠️  Some mathematical symbols may be missing")
            else:
                print("   ❌ No updated document returned")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 4: Missing required fields
    print("\n4. Testing missing required fields...")
    incomplete_data = {
        "document": "Test document",
        "request": "Complete this"
        # Missing session_id and document_title
    }
    
    try:
        response = requests.post(f"{base_url}/api/collaborate", json=incomplete_data, timeout=30)
        if response.status_code == 422:  # Validation error expected
            print("   ✅ Validation error correctly returned for missing fields")
        elif response.status_code == 200:
            print("   ⚠️  Request succeeded despite missing fields")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🏁 Edge case testing completed")

if __name__ == "__main__":
    test_collaboration_edge_cases()