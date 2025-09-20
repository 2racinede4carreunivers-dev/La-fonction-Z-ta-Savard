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

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

class SearchQuery(BaseModel):
    query: str
    categorie: Optional[str] = None

# Base de connaissances de la théorie
CONCEPTS_BASE = [
    {
        "id": str(uuid.uuid4()),
        "titre": "Géométrie du spectre des nombres premiers",
        "description": "Approche géométrique originale pour analyser la distribution des nombres premiers",
        "categorie": "Géométrie",
        "mots_cles": ["nombres premiers", "géométrie", "spectre", "tesseract", "spirales"],
        "contenu": "La théorie développe une approche géométrique unique pour comprendre la distribution des nombres premiers en utilisant des formes géométriques comme les tesseracts et les spirales.",
        "document_source": "univers_au_carre_partie1.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Analyse numérique métrique",
        "description": "Méthode originale d'analyse développée par Philippe Thomas Savard",
        "categorie": "Méthodologie",
        "mots_cles": ["analyse", "numérique", "métrique", "granulométrie", "méthodologie"],
        "contenu": "L'analyse numérique métrique est une méthode unique qui applique des concepts de granulométrie à l'étude des nombres premiers.",
        "document_source": "univers_au_carre_partie1.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Fonction digamma",
        "description": "Rôle de la fonction digamma dans les calculs de la théorie",
        "categorie": "Mathématiques",
        "mots_cles": ["digamma", "fonction", "calculs", "séquence", "nombres premiers"],
        "contenu": "La fonction digamma joue un rôle central dans les calculs liés à la séquence des nombres premiers et leur représentation géométrique.",
        "document_source": "univers_au_carre_partie1.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Théorème de Philippôt",
        "description": "Théorème sur l'intrication quantique et l'équivalence géométrique",
        "categorie": "Théorèmes",
        "mots_cles": ["philippôt", "théorème", "intrication", "quantique", "carrés", "triangle"],
        "contenu": "Le théorème de Philippôt démontre l'équivalence entre trois carrés et un triangle, explorant cette relation à travers diverses manipulations géométriques.",
        "document_source": "univers_au_carre_partie2.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Méthode de Philippôt",
        "description": "Algorithme pour la détermination des nombres premiers",
        "categorie": "Algorithmes",
        "mots_cles": ["philippôt", "algorithme", "nombres premiers", "ratio", "distance"],
        "contenu": "La méthode de Philippôt révèle un ratio constant de 1/2 entre certains ensembles de nombres premiers, utilisant deux algorithmes : préliminaire et spectral.",
        "document_source": "algotithme_manus_methode_philippot.docx",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "titre": "Relations cosmologiques",
        "description": "Connections entre géométrie et constantes cosmologiques",
        "categorie": "Cosmologie",
        "mots_cles": ["cosmologie", "vitesse lumière", "planck", "terre", "soleil"],
        "contenu": "La théorie établit des liens entre les modèles géométriques et les constantes cosmologiques comme la vitesse de la lumière et la longueur de Planck.",
        "document_source": "univers_au_carre_partie2.pdf",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
]

# Initialisation de la base de données
@app.on_event("startup")
async def startup_event():
    # Vérifier si la collection concepts existe et l'initialiser si nécessaire
    concepts_count = await db.concepts.count_documents({})
    if concepts_count == 0:
        await db.concepts.insert_many(CONCEPTS_BASE)
        print("Base de connaissances initialisée avec succès")

# Routes API

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "L'univers est au carré API"}

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

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(chat_message: ChatMessage):
    """Chat avec l'IA spécialisée dans la théorie 'L'univers est au carré'"""
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    # Générer un session_id si non fourni
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    # Contexte spécialisé pour la théorie
    system_message = """Tu es un expert de la théorie 'L'univers est au carré' développée par Philippe Thomas Savard. 
    Tu ne réponds QU'AUX QUESTIONS liées à cette théorie spécifique.
    
    La théorie comprend :
    1. Une approche géométrique des nombres premiers (tesseracts, spirales, hypercubes)
    2. L'analyse numérique métrique appliquée aux nombres premiers
    3. Le rôle de la fonction digamma dans les calculs
    4. Le théorème de Philippôt sur l'intrication quantique
    5. La méthode de Philippôt pour déterminer les nombres premiers (ratio 1/2)
    6. Les relations entre géométrie et constantes cosmologiques
    
    Si on te pose une question non liée à cette théorie, réponds poliment que tu es spécialisé uniquement dans 'L'univers est au carré' et invite à poser des questions sur cette théorie.
    
    Réponds en français, de manière pédagogique et accessible."""
    
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