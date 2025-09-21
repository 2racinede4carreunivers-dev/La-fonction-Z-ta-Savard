from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timezone
import uuid
from emergentintegrations.llm.chat import LlmChat, UserMessage
import math

# Charger les variables d'environnement
load_dotenv()

app = FastAPI(title="L'univers est au carré - API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration MongoDB
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "univers_au_carre")
EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")

# Client MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Modèles Pydantic
class ConceptModel(BaseModel):
    id: str
    titre: str
    description: str
    categorie: str
    mots_cles: List[str]
    contenu: str
    document_source: str
    created_at: str

class TableauPhilippotModel(BaseModel):
    id: str
    rapport: str
    rapport_fraction: str
    description: str
    digamma_position: int
    digamma_valeur: str
    nombre_premier_resultat: int
    position_nombre_premier: int
    calcul_detaille: Dict[str, Any]
    suite_1: List[str]
    suite_2: List[str]
    created_at: str

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

class SearchQuery(BaseModel):
    query: str
    categorie: Optional[str] = None

class CalculateurRequest(BaseModel):
    rapport_base: int
    rapport_hauteur: int

# Base de connaissances enrichie de la théorie
CONCEPTS_BASE = [
    {
        "id": str(uuid.uuid4()),
        "titre": "Géométrie du spectre des nombres premiers",
        "description": "Approche géométrique originale utilisant des triangles rectangles avec différents rapports base/hauteur",
        "categorie": "Géométrie",
        "mots_cles": ["nombres premiers", "géométrie", "spectre", "triangles", "rapports"],
        "contenu": "La théorie développe une approche géométrique unique basée sur 14 rapports base/hauteur différents (1/2, 1/3, 1/4... jusqu'à 1/100). Chaque rapport génère des séquences de racines carrées permettant de calculer des nombres premiers spécifiques.",
        "document_source": "univers_au_carre_partie1.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Les 14 Tableaux de Philippôt",
        "description": "Système complet de 14 tableaux utilisant différents rapports triangulaires pour générer les nombres premiers",
        "categorie": "Méthode",
        "mots_cles": ["tableaux", "philippôt", "rapports", "triangles", "calculs"],
        "contenu": "Chaque tableau correspond à un rapport base/hauteur spécifique et suit 10 étapes de calcul : construction de deux suites, calcul du Digamma à la 8ème position, et formule finale pour obtenir un nombre premier précis.",
        "document_source": "deuxieme_pdf_emergent_methode_philippot.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Le Digamma de Philippôt",
        "description": "Concept central : valeur calculée à la 8ème position des séquences pour déterminer les nombres premiers",
        "categorie": "Innovation",
        "mots_cles": ["digamma", "8ème position", "innovation", "calcul", "séquences"],
        "contenu": "Le Digamma est toujours calculé à la 8ème position selon la formule √((n+7)² + (n+8)²). Il peut être soustrait ou ajouté selon le tableau, et permet de déterminer précisément un nombre premier.",
        "document_source": "Pdf_emergent_methode_philippot.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Séquences de racines carrées",
        "description": "Construction mathématique des deux suites fondamentales pour chaque rapport triangulaire",
        "categorie": "Calculs",
        "mots_cles": ["séquences", "racines", "suites", "construction", "mathématiques"],
        "contenu": "Suite 1 : commence par √(1² + (n+1)²) et ajoute successivement les termes. Suite 2 : utilise les mêmes valeurs au carré. Ces suites génèrent les données nécessaires au calcul final.",
        "document_source": "deuxieme_pdf_emergent_methode_philippot.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Exemples concrets de calculs",
        "description": "Calculs détaillés pour les nombres premiers 29, 227, et 947 avec leurs méthodes exactes",
        "categorie": "Exemples",
        "mots_cles": ["exemples", "29", "227", "947", "calculs", "concrets"],
        "contenu": "Rapport 1/2 → 29 (10ème premier), Rapport 1/3 → 227 (49ème premier), Rapport 1/4 → 947 (163ème premier). Chaque exemple montre le calcul complet du Digamma et la formule finale.",
        "document_source": "deuxieme_pdf_emergent_methode_philippot.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Distance entre les nombres premiers",
        "description": "Méthode pour calculer la distance et les relations entre nombres premiers consécutifs",
        "categorie": "Relations",
        "mots_cles": ["distance", "relations", "consécutifs", "espacement", "patterns"],
        "contenu": "La théorie permet de calculer non seulement les nombres premiers mais aussi leurs distances relatives. Le Digamma joue un rôle clé dans cette détermination des espacements.",
        "document_source": "algotithme_manus_methode_philippot.docx",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Validation par Intelligence Artificielle",
        "description": "Une IA a testé la méthode et trouvé les 18ème et 29ème nombres premiers de manière autonome",
        "categorie": "Validation",
        "mots_cles": ["IA", "validation", "test", "18ème", "29ème", "autonome"],
        "contenu": "La méthode a été validée par une IA qui a réussi à trouver intuitivement les 18ème et 29ème nombres premiers en appliquant la logique de la théorie, prouvant sa robustesse algorithmique.",
        "document_source": "Pdf_emergent_methode_philippot.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
]

# Données des 14 tableaux de Philippôt
TABLEAUX_PHILIPPOT = [
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/2",
        "rapport_fraction": "1:2",
        "description": "Premier tableau - Rapport base/hauteur 1/2",
        "digamma_position": 8,
        "digamma_valeur": "√81920",
        "nombre_premier_resultat": 29,
        "position_nombre_premier": 10,
        "calcul_detaille": {
            "somme_suite_1": "√3452805",
            "somme_suite_2": "√13300805",
            "operation_digamma": "soustraction",
            "formule": "(√3452805 − √81920) / √5120 = 29"
        },
        "suite_1": ["√5", "√13", "√25", "√41", "√61", "√85", "√113", "√145", "√181", "√221"],
        "suite_2": ["5", "13", "25", "41", "61", "85", "113", "145", "181", "221"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/3",
        "rapport_fraction": "1:3",
        "description": "Deuxième tableau - Rapport base/hauteur 1/3",
        "digamma_position": 8,
        "digamma_valeur": "√281300",
        "nombre_premier_resultat": 227,
        "position_nombre_premier": 49,
        "calcul_detaille": {
            "somme_suite_1": "√7079856640",
            "somme_suite_2": "√6.333294724 × 10¹⁰",
            "operation_digamma": "soustraction",
            "formule": "Calcul complexe aboutissant à 227"
        },
        "suite_1": ["√10", "√25", "√41", "√61", "√85", "√113", "√145", "√181", "√221", "√265"],
        "suite_2": ["10", "25", "41", "61", "85", "113", "145", "181", "221", "265"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/4",
        "rapport_fraction": "1:4",
        "description": "Troisième tableau - Rapport base/hauteur 1/4",
        "digamma_position": 8,
        "digamma_valeur": "√451700",
        "nombre_premier_resultat": 947,
        "position_nombre_premier": 163,
        "calcul_detaille": {
            "somme_suite_1": "√1.840600404 × 10¹²",
            "somme_suite_2": "√2.940384489 × 10¹³",
            "operation_digamma": "addition",
            "formule": "Addition du Digamma cette fois, résultat = 947"
        },
        "suite_1": ["√17", "√41", "√61", "√85", "√113", "√145", "√181", "√221", "√265", "√313"],
        "suite_2": ["17", "41", "61", "85", "113", "145", "181", "221", "265", "313"],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
]

# Initialisation de la base de données
@app.on_event("startup")
async def startup_event():
    # Vérifier si les collections existent et les initialiser si nécessaire
    concepts_count = await db.concepts.count_documents({})
    if concepts_count == 0:
        await db.concepts.insert_many(CONCEPTS_BASE)
        print("Base de connaissances initialisée avec succès")
    
    tableaux_count = await db.tableaux_philippot.count_documents({})
    if tableaux_count == 0:
        await db.tableaux_philippot.insert_many(TABLEAUX_PHILIPPOT)
        print("Tableaux de Philippôt initialisés avec succès")

# Routes API existantes
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "L'univers est au carré API - Version enrichie"}

@app.get("/api/concepts", response_model=List[ConceptModel])
async def get_concepts(categorie: Optional[str] = None):
    """Récupère tous les concepts ou filtrés par catégorie"""
    filter_query = {}
    if categorie:
        filter_query["categorie"] = categorie
    
    concepts = await db.concepts.find(filter_query).to_list(length=None)
    return [ConceptModel(**concept) for concept in concepts]

@app.get("/api/concepts/{concept_id}", response_model=ConceptModel)
async def get_concept(concept_id: str):
    """Récupère un concept spécifique"""
    concept = await db.concepts.find_one({"id": concept_id})
    if not concept:
        raise HTTPException(status_code=404, detail="Concept non trouvé")
    return ConceptModel(**concept)

@app.get("/api/categories")
async def get_categories():
    """Récupère toutes les catégories disponibles"""
    pipeline = [
        {"$group": {"_id": "$categorie", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    categories = await db.concepts.aggregate(pipeline).to_list(length=None)
    return [{"categorie": cat["_id"], "count": cat["count"]} for cat in categories]

@app.post("/api/search")
async def search_concepts(query: SearchQuery):
    """Recherche dans les concepts par mots-clés"""
    search_filter = {
        "$or": [
            {"titre": {"$regex": query.query, "$options": "i"}},
            {"description": {"$regex": query.query, "$options": "i"}},
            {"contenu": {"$regex": query.query, "$options": "i"}},
            {"mots_cles": {"$regex": query.query, "$options": "i"}}
        ]
    }
    
    if query.categorie:
        search_filter["categorie"] = query.categorie
    
    concepts = await db.concepts.find(search_filter).to_list(length=None)
    return [ConceptModel(**concept) for concept in concepts]

# Nouvelles routes pour les tableaux de Philippôt
@app.get("/api/tableaux-philippot", response_model=List[TableauPhilippotModel])
async def get_tableaux_philippot():
    """Récupère tous les tableaux de la méthode de Philippôt"""
    tableaux = await db.tableaux_philippot.find().to_list(length=None)
    return [TableauPhilippotModel(**tableau) for tableau in tableaux]

@app.get("/api/tableaux-philippot/{tableau_id}", response_model=TableauPhilippotModel)
async def get_tableau_philippot(tableau_id: str):
    """Récupère un tableau spécifique"""
    tableau = await db.tableaux_philippot.find_one({"id": tableau_id})
    if not tableau:
        raise HTTPException(status_code=404, detail="Tableau non trouvé")
    return TableauPhilippotModel(**tableau)

@app.get("/api/tableaux-philippot/rapport/{rapport}")
async def get_tableau_by_rapport(rapport: str):
    """Récupère un tableau par son rapport (ex: 1/2)"""
    tableau = await db.tableaux_philippot.find_one({"rapport": rapport})
    if not tableau:
        raise HTTPException(status_code=404, detail="Tableau non trouvé pour ce rapport")
    return TableauPhilippotModel(**tableau)

@app.post("/api/calculateur-philippot")
async def calculateur_philippot(request: CalculateurRequest):
    """Calcule une séquence selon la méthode de Philippôt"""
    try:
        base = request.rapport_base
        hauteur = request.rapport_hauteur
        
        # Construction des suites selon la méthode
        suite_1 = []
        suite_2 = []
        
        for i in range(10):
            # Suite 1: √((base+i)² + (hauteur+i+1)²)
            valeur = math.sqrt((base + i)**2 + (hauteur + i + 1)**2)
            suite_1.append(round(valeur, 6))
            
            # Suite 2: même valeur au carré
            suite_2.append(round(valeur**2, 6))
        
        # Calcul du Digamma à la 8ème position
        digamma_index = 7  # 8ème position (index 7)
        digamma_valeur = suite_1[digamma_index]
        
        # Sommes des suites
        somme_suite_1 = sum(suite_1)
        somme_suite_2 = sum(suite_2)
        
        return {
            "rapport": f"{base}/{hauteur}",
            "suite_1": suite_1,
            "suite_2": suite_2,
            "digamma_position": 8,
            "digamma_valeur": digamma_valeur,
            "somme_suite_1": somme_suite_1,
            "somme_suite_2": somme_suite_2,
            "calcul_reussi": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de calcul: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(chat_message: ChatMessage):
    """Chat avec l'IA spécialisée dans la théorie 'L'univers est au carré'"""
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    # Générer un session_id si non fourni
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    # Contexte enrichi avec les détails de la méthode de Philippôt
    system_message = """Tu es un expert spécialisé dans la théorie 'L'univers est au carré' développée par Philippe Thomas Savard. 
    Tu ne réponds QU'AUX QUESTIONS liées à cette théorie spécifique.
    
    La théorie comprend notamment :
    
    **LA MÉTHODE DE PHILIPPÔT :**
    - 14 tableaux utilisant différents rapports base/hauteur (1/2, 1/3, 1/4... jusqu'à 1/100)
    - Chaque tableau suit 10 étapes de calcul précises
    - Construction de deux suites de racines carrées
    - Calcul du "Digamma" toujours à la 8ème position selon √((n+7)² + (n+8)²)
    - Le Digamma peut être soustrait ou ajouté selon le tableau
    - Formule finale donnant un nombre premier précis
    
    **EXEMPLES CONCRETS :**
    - Rapport 1/2 : Digamma = √81920, résultat = 29 (10ème nombre premier)
    - Rapport 1/3 : Digamma = √281300, résultat = 227 (49ème nombre premier)  
    - Rapport 1/4 : Digamma = √451700, résultat = 947 (163ème nombre premier)
    
    **CONCEPTS CLÉS :**
    1. Approche géométrique des nombres premiers (triangles, rapports)
    2. Séquences de racines carrées construites systématiquement
    3. Le "Digamma de Philippôt" (différent du digamma mathématique classique)
    4. Relations entre géométrie et nombres premiers
    5. Calcul des distances entre nombres premiers
    6. Validation par IA (qui a trouvé les 18ème et 29ème nombres premiers)
    
    Si on te pose une question non liée à cette théorie, réponds poliment que tu es spécialisé uniquement dans 'L'univers est au carré' et invite à poser des questions sur cette théorie.
    
    Réponds en français, de manière pédagogique et accessible, en donnant des exemples concrets avec les vrais chiffres de la méthode."""
    
    try:
        # Initialiser le chat Claude
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=system_message
        ).with_model("anthropic", "claude-3-5-sonnet-20241022")
        
        # Créer le message utilisateur
        user_message = UserMessage(text=chat_message.message)
        
        # Envoyer le message et obtenir la réponse
        response = await chat.send_message(user_message)
        
        # Sauvegarder la conversation
        conversation = {
            "session_id": session_id,
            "user_message": chat_message.message,
            "ai_response": response,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.conversations.insert_one(conversation)
        
        return ChatResponse(response=response, session_id=session_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chat: {str(e)}")

@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Récupère l'historique d'une session de chat"""
    history = await db.conversations.find(
        {"session_id": session_id}
    ).sort("timestamp", 1).to_list(length=None)
    
    return [
        {
            "user_message": conv["user_message"],
            "ai_response": conv["ai_response"],
            "timestamp": conv["timestamp"]
        }
        for conv in history
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)