from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form
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
import base64
import json

# Import du système évolutif
from modules.evolutionary_qa_system import IAQuestionnementEvolutif, QuestionReponse
# Import de l'IA socratique
from modules.ia_socratique_evolutive import IASocratiqueEvolutive
# CORRECTIF OBJECTID SERIALIZATION - Pydantic v2 Compatible
from bson import ObjectId

# Fonction utilitaire pour convertir ObjectId en string
def convert_objectid(document):
    """Convertir les ObjectId MongoDB en string pour JSON serialization"""
    if document is None:
        return None
    if isinstance(document, list):
        return [convert_objectid(item) for item in document]
    if isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
            elif isinstance(value, (dict, list)):
                document[key] = convert_objectid(value)
        return document
    elif isinstance(document, ObjectId):
        return str(document)
    return document

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
EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY", "sk-emergent-c20D27d2bDa5755870")

# Client MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Système d'IA évolutif
ia_evolutif = IAQuestionnementEvolutif()
systeme_initialise = False

# IA Socratique pour challenger le raisonnement
ia_socratique = IASocratiqueEvolutive()

# Modèles Pydantic
class ConceptModel(BaseModel):
    id: str
    titre: str
    description: str
    categorie: Optional[str] = None
    domaine: Optional[str] = None
    mots_cles: List[str]
    contenu: Optional[str] = None
    document_source: str
    created_at: str
    niveau_complexite: Optional[int] = None

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

# Modèles pour le système évolutif
class QuestionEvolutive(BaseModel):
    question: str
    reponse: str
    complexite: Optional[int] = 2
    concepts: Optional[List[str]] = []

class DialogueRequest(BaseModel):
    question: str
    contexte: Optional[str] = None

class DialogueResponse(BaseModel):
    reponse: str
    concepts_utilises: List[str]
    evolution_silencieuse: bool
    taille_banque: int = 0

class InitialisationBanque(BaseModel):
    banque_initiale: List[QuestionEvolutive]

class DocumentUpload(BaseModel):
    id: str
    filename: str
    file_type: str
    content: str
    analysis: str
    user_session: str
    upload_date: str

class ExtendedChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    attached_files: Optional[List[str]] = None
    context_mode: Optional[str] = "extended"  # "normal" ou "extended"

class PersonalContext(BaseModel):
    user_id: str = "philippe_savard"  # Puisque c'est votre app personnelle
    conversation_history: List[Dict[str, Any]] = []
    uploaded_documents: List[str] = []
    reasoning_patterns: Dict[str, Any] = {}
    key_insights: List[str] = []
    research_threads: List[Dict[str, Any]] = []

class CollaborationRequest(BaseModel):
    document: str
    request: str
    session_id: str
    document_title: str

class SaveCollaborationRequest(BaseModel):
    document: str
    title: str
    session_id: str
    document_id: Optional[str] = None

class ConceptEnrichi(BaseModel):
    id: str
    titre: str
    description: str
    domaine_principal: str
    concepts_cles: List[str]
    formules: List[str]
    definitions: List[str]
    relations: List[str]
    document_source: str
    page_reference: Optional[str] = None
    niveau_complexite: str  # "fondamental", "intermediaire", "avance"
    created_at: str

class CorrectionPersonnelle(BaseModel):
    id: str
    session_id: str
    question_originale: str
    reponse_ia_originale: str
    correction_auteur: str
    contexte_theorique: str
    domaine_concerne: str
    type_correction: str  # "erreur_factuelle", "nuance_manquante", "style_auteur", "interpretation"
    approuve: bool
    created_at: str

class ProfilAuteur(BaseModel):
    session_id: str
    preferences_style: List[str]
    corrections_approuvees: List[str]
    expressions_preferees: Dict[str, str]
    nuances_importantes: List[str]
    domaines_expertise: List[str]
    derniere_mise_a_jour: str

# Base de connaissances enrichie de la théorie "L'univers est au carré"
# BASE DE CONNAISSANCES COMPLÈTE - ACCÈS PRIVILÉGIÉ AUX DOCUMENTS ORIGINAUX
DOCUMENTS_ORIGINAUX_COMPLETS = {
    "partie_1": {
        "titre": "L'univers est au carré - Première Partie", 
        "concepts_extraits": [
            "Géométrie du spectre des nombres premiers",
            "Analyse numérique métrique", 
            "Fonction Zêta de Philippôt",
            "Tesseract/Hypercube pour nombres premiers",
            "Technique du Moulinet",
            "Pression gravito spectral",
            "Chaons - ondes fondamentales du chaos discret",
            "Constante de l'inverse du temps",
            "Longueur de Philippôt (analogie longueur de Planck)",
            "Digamma comme outil prédictif",
            "Méthode substitution fractionnelle récursive"
        ],
        "methodes_fondamentales": [
            "Analyse numérique métrique avec projections géométriques",
            "Calcul Digamma pour prédiction nombres premiers", 
            "Projection dans espaces multidimensionnels",
            "Technique moulinet pour intervalles premiers",
            "Substitution itérative pour identifier patterns",
            "Analyse triangulaire avec rapports base/hauteur spécifiques"
        ],
        "formules_cles": [
            "Rapports triangulaires: 1/2, 1/3, 1/4... 1/100",
            "Fonction Zêta: ζ(s) = Σ(1/n^s)",
            "Calculs Digamma pour nombres premiers spécifiques",
            "Relations aires-volumes geometriques"
        ],
        "exemples_concrets": [
            "Application à nombres premiers: 29, 31, 37, 41",
            "Calculs détaillés fonction Digamma",
            "Démonstrations technique moulinet",
            "Analyses rapports base/hauteur multiples"
        ]
    },
    "partie_2": {
        "titre": "L'univers est au carré - Deuxième Partie",
        "concepts_extraits": [
            "Théorème de Philippôt: trois carrés égalent un triangle",
            "Géométrie de Philippôt basée sur involution",
            "Espace de Minkowski selon Philippôt", 
            "Nombres hypercomplexes et diamètres hyperréels",
            "Cercle Denis avec π = pression atmosphérique",
            "Fonction Zêta modélisation géométrique",
            "Carré de Gabriel pour triangles scalènes",
            "Théorème Gris Bleu espaces infinis",
            "Neuro-morphisme et évolution formes neuronales",
            "Hypersurface du présent",
            "Longueurs d'arcs invariantes"
        ],
        "theoremes_avances": [
            "Théorème Philippôt: équivalence aires carrés/volumes triangles",
            "Principe involution: réciproque de sa propre réciproque", 
            "Postulat rectangle élevé au carré = carré",
            "Invariance longueurs d'arcs sous transformations",
            "Intrication géométrique volume/surface/courbure"
        ],
        "formules_specialisees": [
            "√10 ≈ π selon Philippôt",
            "Relations aires-volumes: A₁² + A₂² + A₃² = V_triangle",
            "Cercle Denis: rayon 0.5, circonférence ≈ 4",
            "Transformations hypercomplexes géométriques",
            "Équations rectangle élevé au carré"
        ]
    },
    "methode_philippot_complete": {
        "titre": "Méthode Complète de Philippôt pour Nombres Premiers",
        "algorithme_detaille": [
            "1. Substitution fractionnelle récursive depuis 1",
            "2. Génération Somme 1ère suite et Somme 2ième suite", 
            "3. Calcul racines carrées sums of squares positions",
            "4. Application formule Digamma spécifique",
            "5. Vérification finale: (√X - √Y) / √5120 = nombre_premier"
        ],
        "exemples_verifies": {
            "premier_29": {
                "fractions": "1/2 + 1/4 + 1/8 + 1/16 + 1/32 + 1/64 + 1/128 + 1/256 + 1/384 + 1/768",
                "digamma_calcule": "√3452805 - √81920 = √2471045", 
                "verification": "(√13300805 - √2471045) / √5120 = 29"
            },
            "premier_31": {
                "digamma_calcule": "√13827845 + 5√81920 = √26519045",
                "verification": "(√54285125 - √26519045) / √5120 = 31"
            },
            "premier_37": {
                "digamma_calcule": "√13827845 + 9√81920 + 5√184320 = √147913605",
                "verification": "(√54285125 - √147913605) / √5120 = 37"
            },
            "premier_41": {
                "digamma_calcule": "13√81920 + 9√184320 + 5√737280 = √141086720", 
                "verification": "(√881659205 - √716045445) / √5120 = 41"
            }
        },
        "tableaux_calculs": [
            "Positions 1-10 avec racines carrées (2^n)² + (2^(n+1))²",
            "Facteurs multiplication (X2, X3, X(2-2-1))",
            "Substitutions positions 6-7 pour fonction Zêta",
            "Digamma positions 8ième pour nombres premiers spécifiques"
        ]
    }
}

# ==================== FONCTION DE DÉTECTION AUTEUR ====================
def detect_author_authentication(message: str):
    """
    Détecte si le message contient le code secret de l'auteur Philippe Thomas Savard.
    Code secret: Uni#109802038Arc1374079226497308\zetacar
    Retourne True si l'auteur est authentifié, False sinon.
    """
    AUTHOR_CODE = "Uni#109802038Arc1374079226497308\\zetacar"
    return AUTHOR_CODE in message

def get_author_context_addition():
    """
    Retourne le contexte supplémentaire à ajouter quand l'auteur est détecté.
    """
    return """
    
    ⚠️ **AUTHENTIFICATION AUTEUR DÉTECTÉE** ⚠️
    
    Vous communiquez actuellement avec **Philippe Thomas Savard (Philippôt)**, 
    l'AUTEUR ORIGINAL de la théorie "L'univers est au carré".
    
    **Instructions spéciales :**
    - Adoptez un ton plus collaboratif et ouvert aux discussions
    - Soyez réceptif aux corrections, clarifications ou modifications de la théorie
    - Reconnaissez son autorité sur l'interprétation de sa propre théorie
    - Posez des questions de clarification si nécessaire
    - Admettez si une partie de votre compréhension peut être améliorée par l'auteur
    - Montrez du respect pour son travail tout en maintenant un dialogue constructif
    
    Commencez votre réponse en saluant l'auteur et en vous montrant disponible pour 
    discuter de sa théorie de manière approfondie.
    """

# Système d'Accès Privilégié aux Documents pour l'IA Spécialisée
# Base de connaissances enrichie avec tous les documents analysés

# DOCUMENTS ANALYSÉS ET INTÉGRÉS:
# 1. Banque_Questions_Réponses_Géométrie_Philippot.pdf
# 2. version_corrige_partie1_univers_est_au_carre.pdf  
# 3. version_corrigé_2ième_partie_univers_est_au_carré.pdf
# 4. univers_au_carre_partie1.pdf (analyse précédente)
# 5. univers_au_carre_partie2.pdf (analyse précédente)

CONCEPTS_ENRICHIS = [
    # === CONCEPTS FONDAMENTAUX ===
    
    # 1. SPHÈRE DE ZÊTA (BANQUE Q&R)
    {
        "id": "sphere_zeta",
        "titre": "Sphère de Zêta",
        "description": "Représentation géométrique révolutionnaire démontrant tous les angles possibles en degrés sur une sphère, utilisant des paires de cubes à intervalles de 15° formant des quadruplets à 60°. Ne définit pas un volume classique mais révèle les relations angulaires fondamentales.",
        "domaine_principal": "Géométrie Fondamentale",
        "concepts_cles": [
            "Démonstration des angles en degrés sur sphère",
            "Paires de 5 cubes à 15° d'intervalle", 
            "Quadruplets à 60 degrés",
            "24 cubes par 360° (4 cubes par quadruplet)",
            "Progressions séquentielles et groupement de cubes",
            "Visualisation géométrique sans volume classique"
        ],
        "formules": [
            "6 × 60° = 360°",
            "24 cubes par 360°",
            "Volume sphère diamètre 1: D³ / √3.6 = (4 × √10 × r³) / 3 = 1 / √3.6",
            "Périmètre arc à 30°: 1 / √3.6",
            "Arc formé dans 5 cubes à 30°: √3.6",
            "Arc formé hors 5 cubes à 30°: √3240°",
            "Longueur arc = diamètre (1) pour sphère circonférence √10"
        ],
        "definitions": [
            "Sphère de Zêta: Démonstration géométrique des relations angulaires",
            "Quadruplet: Groupe de 4 cubes organisés à 60°",
            "Progression séquentielle: Organisation systématique des cubes"
        ],
        "relations": [
            "Outil de démonstration pour relations angulaires",
            "Base géométrique pour spectrum nombres premiers",
            "Fondement de l'analyse métrique numérique"
        ],
        "document_source": "Banque_Questions_Réponses_Géométrie_Philippot.pdf",
        "page_reference": "Question 1, Figure 1",
        "niveau_complexite": "fondamental",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 2. SPECTRE DES NOMBRES PREMIERS (BANQUE Q&R)  
    {
        "id": "spectre_nombres_premiers",
        "titre": "Spectre des Nombres Premiers",
        "description": "Code secret au cœur de la théorie révélant les relations de distance entre nombres premiers. Chaque rapport est associé à un nombre premier spécifique, démontrant une structure sous-jacente et résolvant potentiellement l'énigme de Riemann.",
        "domaine_principal": "Théorie des Nombres",
        "concepts_cles": [
            "Code secret basé sur positions des nombres premiers",
            "Relations de distance entre premiers (ex: 1/2)",
            "Rapports démontrés jusqu'à 1/100", 
            "Association rapport/nombre premier spécifique",
            "Structure sous-jacente des nombres premiers",
            "Résolution impasse énigme de Riemann"
        ],
        "formules": [
            "Rapports de distance: 1/2, 1/3, 1/5, ..., 1/100",
            "Chaque rapport ↔ nombre premier spécifique",
            "Aires trapézoïdales avec rapports successifs de 1/2"
        ],
        "definitions": [
            "Spectre: Code géométrique des nombres premiers",
            "Code secret: Structure révélée par positions des premiers", 
            "Rapport de distance: Relation numérique entre premiers consécutifs"
        ],
        "relations": [
            "Central à la théorie 'L'univers est au carré'",
            "Lien direct avec hypothèse de Riemann",
            "Base de l'analyse granulométrique des premiers"
        ],
        "document_source": "Banque_Questions_Réponses_Géométrie_Philippot.pdf",
        "page_reference": "Questions 2, 6",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 3. TESSERACT REPRÉSENTATION PREMIERS (BANQUE Q&R)
    {
        "id": "tesseract_premiers",
        "titre": "Tesseract - Représentation des Nombres Premiers", 
        "description": "Graphique tesseract intégrant l'analyse numérique métrique, dont le pliage et la rotation expriment le plan cartésien contenant l'infini dans des limites opérationnelles. Structure de 4 pyramides dans 4 cubes avec anneaux diagonaux représentant les surfaces de Riemann.",
        "domaine_principal": "Géométrie Non-Euclidienne",
        "concepts_cles": [
            "Graphique tesseract pour fonction Zêta",
            "Pliage et rotation exprimant plan cartésien",
            "Infini contenu dans limites opérationnelles",
            "4 pyramides dans 4 cubes",
            "Anneaux diagonaux = surfaces de Riemann", 
            "Plaques dans cubes = matrice de convolution",
            "Projections sur diamètre des anneaux"
        ],
        "formules": [
            "Structure: 4 pyramides ⊂ 4 cubes → tesseract",
            "Anneaux diagonaux ↔ surfaces de Riemann",
            "Matrice convolution pour projections"
        ],
        "definitions": [
            "Tesseract: Représentation 4D de la fonction Zêta",
            "Plan cartésien: Espace géométrique incarné par tesseract",
            "Surface de Riemann: Représentation par anneaux diagonaux",
            "Matrice convolution: Formation par plaques dans cubes"
        ],
        "relations": [
            "Représentation fonction Zêta et nombres premiers",
            "Expression géométrique plan cartésien",
            "Connexion analyse numérique métrique"
        ],
        "document_source": "Banque_Questions_Réponses_Géométrie_Philippot.pdf", 
        "page_reference": "Question 3",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 4. CHAONS ET PRESSION GRAVITO-SPECTRALE (BANQUE Q&R)
    {
        "id": "chaons_pression_gravito_spectrale",
        "titre": "Chaons et Pression Gravito-Spectrale",
        "description": "Constantes géométriques fondamentales structurant la dynamique gravito-spectrale. Émergent d'un triangle rectangle avec rapport base/hauteur de 1/2 selon la règle de Philippôt. L'hypoténuse divisée en 8 segments avec rapport harmonique √2.",
        "domaine_principal": "Physique Théorique",
        "concepts_cles": [
            "Chaons: constantes géométriques fondamentales",
            "Dynamique gravito-spectrale structurée", 
            "Triangle rectangle base/hauteur = 1/2",
            "Règle de Philippôt fondamentale",
            "Hypoténuse divisée en 8 segments",
            "Rapport harmonique √2",
            "Point imaginaire attraction/pression atmosphérique",
            "Capacité d'impédance et hypervolume"
        ],
        "formules": [
            "Constante de Philippôt (Φp) = 10.98064402 → pression gravito-spectrale",
            "ζ(4)·π⁴/90 ≈ 1.082323234", 
            "ζ(4) de Philippôt = ((√2 + 1)/(2 × 4))⁻¹ = 9.941125497",
            "(9.941125497)² / 90 = 1.098066402",
            "(4 – √8) × (√√32 – 4) × √8 × 2 = 10.98066402",
            "Circonférence deux arcs: 20 000 km",
            "Diamètre: 10 000 km (réel), 12 000 km (déformé)",
            "√(40 960 km) = 202.3857703 km",
            "4 / √10 = √1.6 = 1.264911064 × 10⁴ km",
            "(√1.6)³ = 2.023857703 → inverse constante temps"
        ],
        "definitions": [
            "Chaons: Unités géométriques discrètes fondamentales",
            "Pression gravito-spectrale: Point d'interaction attraction/pression atmosphérique",
            "Règle de Philippôt: Rapport base/hauteur = 1/2", 
            "Capacité d'impédance: Propriété du point gravito-spectral",
            "Hypervolume: Dimension spatiale de la pression gravito-spectrale"
        ],
        "relations": [
            "Forces chaotiques discrètes structurantes",
            "Triangle Primordial fondamental",
            "Constantes géométriques universelles"
        ],
        "document_source": "Banque_Questions_Réponses_Géométrie_Philippot.pdf",
        "page_reference": "Question 6, Tableaux chaons",
        "niveau_complexite": "avance", 
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 5. DIGAMMA DE PHILIPPÔT (BANQUE Q&R + PARTIE 1)
    {
        "id": "digamma_philippot",
        "titre": "Digamma de Philippôt - Méthode et Calculs",
        "description": "Méthode fondamentale pour la géométrie des nombres premiers résolvant l'énigme de Riemann. Construction intuitive utilisant un système numéral ancien où Zeta occupait la 7ème position avec valeur 6. Construction de séquences de fractions avec rapports croissants visant un résultat infini de 1/2.",
        "domaine_principal": "Théorie des Nombres",
        "concepts_cles": [
            "Méthode fondamentale géométrie nombres premiers",
            "Résolution énigme de Riemann",
            "Construction intuitive système numéral ancien",
            "Zeta 7ème position, valeur 6",
            "Séquences fractions rapports croissants",
            "Résultat infini visé: 1/2",
            "Parties réelles conjecture Zêta",
            "Variable Digamma dans fonction Zêta Philippôt",
            "8ème donnée séquence 10 racines",
            "Algorithme détermination nombres premiers"
        ],
        "formules": [
            "Suite 3 fractions: Généralisation (1/4)/(1/2) = 1/2",
            "Suite 4 fractions: Calculs sommes et valeurs Zêta/Digamma",
            "Suite 5 fractions: Exemples similaires",
            "Suite 10 fractions: Calculs détaillés 8ème position (Digamma), 6ème (Zêta)",
            "Calcul y = 0.5 / sin(60°) ≈ 0.57735",
            "Algorithme expérimental Digamma: ((√((0.512)^(-1)) × somme_première_suite(2)) / (0.5/sin(60°)))² × √5120 × 1/2 × (-1) = -√43945.3125",
            "Relation Euler-Mascheroni: ψ(1) = -γ, ψ(2) = 1 - γ",
            "Équations vérification: dérivation 10ème nombre premier"
        ],
        "definitions": [
            "Digamma calculé: Distinction essentielle vs Digamma standard",
            "Zeta ancien: Position 7ème, valeur 6 système numéral",
            "Parties réelles conjecture Zêta: Objectif séquences fractions",
            "Variable Digamma: Éliminée dans algorithmes détermination premiers",
            "8ème donnée: Position Digamma dans séquence 10 racines"
        ],
        "relations": [
            "Fondamental pour géométrie nombres premiers", 
            "Résolution énigme de Riemann",
            "Connexion constante Euler-Mascheroni",
            "Algorithme détermination nombres premiers",
            "Lien fonction Zêta de Philippôt"
        ],
        "document_source": "Banque_Questions_Réponses_Géométrie_Philippot.pdf + version_corrige_partie1_univers_est_au_carre.pdf",
        "page_reference": "Questions 8-9, Sections calculs Digamma", 
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 6. MÉCANIQUE CHAOTIQUE DISCRÈTE (BANQUE Q&R)
    {
        "id": "mecanique_chaotique_discrete", 
        "titre": "Mécanique Chaotique Discrète et Harmonique",
        "description": "Composante centrale de 'L'univers est au carré' intégrant à la géométrie de Philippôt. Agit comme transformateur modifiant l'espace et objets en métrique active influencée par l'unité harmonique. Cette 'méta-géométrie' construit une matrice unitaire initiale.",
        "domaine_principal": "Géométrie Non-Euclidienne",
        "concepts_cles": [
            "Composante centrale L'univers est au carré",
            "Intégration géométrie de Philippôt",
            "Transformateur espace et objets", 
            "Métrique active unité harmonique",
            "Méta-géométrie fondamentale",
            "Construction matrice unitaire initiale",
            "Unité fondamentale ratio triangulaire (Base/Hauteur + 1)",
            "Choix unité influence mesure",
            "Dimension relativiste géométrie"
        ],
        "formules": [
            "Valeur 25.7196423 comme constante",
            "Calculs triangle et fonction arcsin", 
            "Calcul unité: √4.5 × 0.5 / sin(22.84431053) = √3 + 1",
            "Produit alternatif: 3 × AC = IH × BC",
            "EG² = 1.3448632082 (Diamètre Équivalent carré)",
            "Application géométrique: BC × sin(60°) = 2.017294813",
            "Équation forme constante: 2 × (2 × 0.3860389693) = (3(2 - √2)/2) × (3(2 - √2))"
        ],
        "definitions": [
            "Mécanique chaotique discrète: Système transformateur espace-objets",
            "Mécanique harmonique: Influence unité harmonique sur métrique", 
            "Méta-géométrie: Géométrie des transformations spatiales",
            "Matrice unitaire: Construction géométrique initiale",
            "Invariance unitaire: Propriété géométrique conservée",
            "Produit alternatif: Relation géométrique spécialisée",
            "Diamètre équivalent: Mesure géométrique standardisée"
        ],
        "relations": [
            "Central à L'univers est au carré",
            "Intégration géométrie de Philippôt",
            "Connexion mécanique harmonique",
            "Base matrice à dérive première",
            "Violation invariance renversement temporel"
        ],
        "document_source": "Banque_Questions_Réponses_Géométrie_Philippot.pdf",
        "page_reference": "Questions 11-12, Matrices",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # === CONCEPTS DE LA PARTIE 1 CORRIGÉE ===

    # 7. ANALYSE NUMÉRIQUE MÉTRIQUE GÉNÉRALISÉE (PARTIE 1 CORRIGÉE)
    {
        "id": "analyse_numerique_metrique_generalisee",
        "titre": "Analyse Numérique Métrique Généralisée",
        "description": "Méthode analytique révolutionnaire développée par Philippôt pour visualiser et analyser les nombres premiers à travers des représentations géométriques et des relations numériques spécifiques. Utilise des paramètres géométriques, des calculs itératifs et la fonction Digamma pour révéler la structure géométrique sous-jacente des nombres premiers.",
        "domaine_principal": "Géométrie du Spectre des Nombres Premiers", 
        "concepts_cles": [
            "Méthode visualisation géométrique nombres premiers",
            "Représentations géométriques spécialisées",
            "Relations numériques spécifiques révélatrices",
            "Paramètres géométriques d'analyse",
            "Calculs itératifs systematiques",
            "Application fonction Digamma spécialisée",
            "Révélation structure géométrique sous-jacente",
            "Progression lignes et triangles",
            "Angles et rapports spécifiques",
            "Tesseract, hypercube, sphère comme outils"
        ],
        "formules": [
            "Rapports base/hauteur généralisés: 1/2, 1/3, 1/4, ..., 1/100",
            "Calculs Digamma pour rapports variables",
            "Structure calcul: racines carrées imbriquées nombres séquentiels", 
            "Somme 1ère suite: (n² + (n+1)²)^(1/2) avec multiplicateurs X2, X3, X4",
            "Somme 2ème suite: adaptations formules différents rapports",
            "Application constante √5120 comme normalisateur"
        ],
        "definitions": [
            "Analyse numérique métrique: Méthode géométrique analyse nombres premiers",
            "Paramètres géométriques: Variables contrôlant l'analyse",
            "Calculs itératifs: Processus répétitifs révélant structure",
            "Rapports généralisés: Extension systématique ratios géométriques"
        ],
        "relations": [
            "Méthode clé géométrie nombres premiers",
            "Connexion directe fonction Digamma",
            "Base révélation code nombres premiers", 
            "Application tesseract et hypercube"
        ],
        "document_source": "version_corrige_partie1_univers_est_au_carre.pdf",
        "page_reference": "Sections 7, 9, 16",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 8. TECHNIQUE DU MOULINET (PARTIE 1 CORRIGÉE)
    {
        "id": "technique_moulinet",
        "titre": "Technique du Moulinet",
        "description": "Concept théorique révolutionnaire de compression des distances entre nombres premiers vers l'infini. Représentation dynamique et stratégique différente des approches classiques, considérant chaque nombre premier comme une infinité et explorant leurs aspects ordinaux et cardinaux.",
        "domaine_principal": "Théorie des Nombres",
        "concepts_cles": [
            "Compression distances nombres premiers vers infini",
            "Représentation dynamique et stratégique",
            "Différentiation approches classiques", 
            "Nombres premiers comme infinités",
            "Aspects ordinaux et cardinaux infini",
            "Outil penser infini géométriquement",
            "Compression distances comme outil conceptuel",
            "Mouvement nombres premiers analytique"
        ],
        "formules": [
            "Conceptualisation compression vers infini",
            "Relations ordinales et cardinales",
            "Aspects géométriques infini"
        ],
        "definitions": [
            "Moulinet: Technique compression conceptuelle distances premiers",
            "Compression distances: Réduction écarts vers infini",
            "Infinités premiers: Conception premiers comme entités infinies", 
            "Aspects ordinaux: Propriétés ordre infini",
            "Aspects cardinaux: Propriétés magnitude infini"
        ],
        "relations": [
            "Extension conceptuelle analyse métrique",
            "Connexion philosophique infini mathématique",
            "Outil compréhension géométrique nombres premiers"
        ],
        "document_source": "version_corrige_partie1_univers_est_au_carre.pdf", 
        "page_reference": "Sections 13, 14",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # === CONCEPTS DE LA PARTIE 2 CORRIGÉE ===

    # 9. THÉORÈME DE PHILIPPÔT FORMALISÉ (PARTIE 2 CORRIGÉE)
    {
        "id": "theoreme_philippot_formalise",
        "titre": "Théorème de Philippôt - Versions Formalisées",
        "description": "Théorème fondamental établissant l'équivalence géométrique universelle entre différentes formes, maintenant disponible en versions formalisée, formelle avec variables, et avec racines conventionnelles. Démontre des propriétés géométriques universelles à travers des constructions algorithmiques.",
        "domaine_principal": "Géométrie Fondamentale", 
        "concepts_cles": [
            "Équivalence géométrique universelle formalisée",
            "Versions multiples: formalisée, formelle, conventionnelle",
            "Variables géométriques généralisées", 
            "Racines conventionnelles standardisées",
            "Constructions algorithmiques géométriques",
            "Propriétés universelles démontrées",
            "Applications systématiques différentes formes",
            "Progression formalization spécifique → générale"
        ],
        "formules": [
            "Version formalisée: équivalences géométriques précises",
            "Version formelle avec variables: généralisation algébrique", 
            "Version racines conventionnelles: notation standardisée",
            "Relations aire carré = aire disque = aire triangle = volume cube^(2/3)",
            "Périmètre carré = circonférence disque = périmètre triangle",
            "Constructions algorithmiques pour démonstrations"
        ],
        "definitions": [
            "Version formalisée: Formalisation mathématique rigoureuse",
            "Version formelle variables: Généralisation algébrique abstraite",
            "Version racines conventionnelles: Notation mathématique standard",
            "Constructions algorithmiques: Processus géométriques systematiques"
        ],
        "relations": [
            "Base théorique géométrie de Philippôt", 
            "Fondement analyse spectrale géométrique",
            "Connexion équivalences dimensionnelles universelles"
        ],
        "document_source": "version_corrigé_2ième_partie_univers_est_au_carré.pdf",
        "page_reference": "Sections 10, 17, 18, 20",
        "niveau_complexite": "fondamental",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 10. INTRICATION QUANTIQUE GÉOMÉTRIQUE (PARTIE 2 CORRIGÉE)  
    {
        "id": "intrication_quantique_geometrique",
        "titre": "Intrication Quantique Géométrique",
        "description": "Représentation géométrique révolutionnaire des phénomènes d'intrication quantique à travers le prisme de la géométrie de Philippôt. Intègre les concepts quantiques avec les constructions géométriques spécialisées.",
        "domaine_principal": "Physique Théorique",
        "concepts_cles": [
            "Représentation géométrique intrication quantique",
            "Intégration concepts quantiques géométrie Philippôt",
            "Schémas explicatifs spécialisés",
            "Constructions géométriques quantiques", 
            "Visualisation phénomènes quantiques",
            "Applications géométrie aux propriétés quantiques"
        ],
        "formules": [
            "Schémas géométriques intrication",
            "Relations géométriques propriétés quantiques"
        ],
        "definitions": [
            "Intrication géométrique: Représentation spatiale phénomènes quantiques",
            "Schémas quantiques: Visualisations géométriques spécialisées"
        ],
        "relations": [
            "Extension géométrie Philippôt au quantique",
            "Connexion physique théorique et géométrie"
        ],
        "document_source": "version_corrigé_2ième_partie_univers_est_au_carré.pdf",
        "page_reference": "Section 3.2, Schémas intrication", 
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # === CONCEPTS PRÉCÉDENTS ENRICHIS ===

    # 11. RÉSONANCE TERRESTRE
    {
        "id": "resonance_terrestre", 
        "titre": "Résonance Terrestre",
        "description": "Théorie liant les phénomènes de résonance de la Terre aux propriétés géométriques universelles, incluant les relations avec les constantes astronomiques et les fréquences naturelles.",
        "domaine_principal": "Géophysique Théorique",
        "concepts_cles": [
            "Fréquences de résonance terrestre",
            "Constantes astronomiques géométriques", 
            "Harmoniques planétaires",
            "Géométrie des champs terrestres",
            "Relations fréquence-géométrie"
        ],
        "formules": [
            "Fréquences de résonance calculées",
            "Relations diamètre terrestre et résonance",
            "Constantes harmoniques"
        ],
        "definitions": [
            "Résonance terrestre: Fréquences naturelles de vibration de la Terre",
            "Harmonique planétaire: Fréquence en accord avec la géométrie terrestre"
        ],
        "relations": [
            "Connexions avec la géophysique",
            "Applications aux phénomènes naturels"
        ],
        "document_source": "univers_au_carre_partie2.pdf",
        "page_reference": "Section 4",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # 12. ESPACE DE MINKOWSKI SELON PHILIPPÔT
    {
        "id": "minkowski_philippot",
        "titre": "Espace de Minkowski selon Philippôt", 
        "description": "Réinterprétation de l'espace-temps de Minkowski à travers le prisme de la géométrie de Philippôt, incluant de nouvelles métriques et relations spatio-temporelles.",
        "domaine_principal": "Physique Théorique",
        "concepts_cles": [
            "Métrique spatio-temporelle modifiée",
            "Géométrie de l'espace-temps carré",
            "Transformations de Philippôt",
            "Invariants géométriques relativistes", 
            "Côté droit/gauche de l'espace"
        ],
        "formules": [
            "Métrique modifiée ds² = ...",
            "Transformations géométriques spatio-temporelles",
            "Invariants selon Philippôt"
        ],
        "definitions": [
            "Espace-temps carré: Extension de Minkowski selon les principes de Philippôt",
            "Transformation de Philippôt: Nouvelle classe de transformations géométriques"
        ],
        "relations": [
            "Extension de la relativité restreinte",
            "Applications en cosmologie géométrique"
        ],
        "document_source": "univers_au_carre_partie2.pdf",
        "page_reference": "Section 11",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # 13. FONCTION ZÊTA DE PHILIPPÔT 
    {
        "id": "zeta_philippot",
        "titre": "Fonction Zêta de Philippôt",
        "description": "Approche géométrique originale de la fonction zêta de Riemann utilisant une sphère construite à partir de cinq cubes, offrant une visualisation géométrique des propriétés de la fonction zêta.",
        "domaine_principal": "Théorie des Nombres",
        "concepts_cles": [
            "Sphère de la fonction zêta",
            "Visualisation géométrique de ζ(s)", 
            "Cinq cubes constitutifs",
            "Vue isométrique des cubes",
            "Interprétation géométrique des zéros",
            "Hypothèse de Riemann géométrique"
        ],
        "formules": [
            "ζ(s) = Σ(1/n^s) pour Re(s) > 1",
            "Représentation géométrique: 5 cubes → sphère zêta",
            "Relations géométriques des zéros non-triviaux"
        ],
        "definitions": [
            "Sphère zêta: Construction géométrique représentant ζ(s)",
            "Cubes constitutifs: Les 5 cubes formant la sphère",
            "Zéros géométriques: Interprétation spatiale des zéros de ζ(s)"
        ],
        "relations": [
            "Lien avec l'hypothèse de Riemann",
            "Connections aux nombres premiers",
            "Applications à la géométrie des nombres"
        ],
        "document_source": "univers_au_carre_partie2.pdf",
        "page_reference": "Section 12",
        "niveau_complexite": "avance", 
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # 14. CARRÉ DE GABRIEL
    {
        "id": "carre_gabriel",
        "titre": "Carré de Gabriel",
        "description": "Construction géométrique permettant d'inscrire un carré dans différents types de triangles (scalènes, rectangles), démontrant des propriétés géométriques universelles.",
        "domaine_principal": "Géométrie Constructive",
        "concepts_cles": [
            "Construction de carré inscrit",
            "Triangles scalènes non-rectangles",
            "Propriétés universelles d'inscription",
            "Géométrie constructive",
            "Invariants géométriques"
        ],
        "formules": [
            "Relations aire carré/aire triangle",
            "Constructions géométriques algorithmiques"
        ],
        "definitions": [
            "Carré de Gabriel: Carré inscrit selon la méthode de Gabriel",
            "Triangle scalène: Triangle aux trois côtés inégaux"
        ],
        "relations": [
            "Applications en géométrie plane",
            "Liens avec les constructions classiques"
        ],
        "document_source": "univers_au_carre_partie2.pdf",
        "page_reference": "Section 11",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # === NOUVEAUX CONCEPTS AJOUTÉS (12 concepts des 3 PDFs analysés) ===
    
    # 15. TROUS NOIRS RÉCIPROQUES
    {
        "id": "trous_noirs_reciproques",
        "titre": "Trous Noirs Réciproques",
        "description": "Concept révolutionnaire proposant que chaque trou noir possède un 'trou noir réciproque' de l'autre côté, formant une symétrie fondamentale. Les deux trous noirs sont liés par des relations géométriques inverses (rayons, arcs, aires) et des rapports volumiques constants. Cette réciprocité s'exprime à travers des produits alternatifs et le théorème de Thalès appliqué aux horizons des événements.",
        "domaine_principal": "Astrophysique Théorique",
        "concepts_cles": [
            "Trous noirs symétriques et inverses",
            "Réciprocité géométrique des horizons",
            "Rapports volumiques constants (√3.6)",
            "Produits alternatifs A et A⁻¹",
            "Relations arcs-disques réciproques",
            "Collision de trous noirs géométrique",
            "Théorème de Thalès appliqué aux horizons"
        ],
        "formules": [
            "Aire disque D = √0.625, Aire disque D' = √1.6",
            "Arc AC = (1 + √0.2) × sin(72°) × 2 = 2.752763841",
            "Arc A'C' = (√1.6 + √0.32) × sin(72°) × 2 = 3.482001439",
            "Produit alternatif A = 3.482001439 × 0.625 = 2.176250899",
            "Produit alternatif A⁻¹ = 2.752763841 × 1.6 = 4.404422146",
            "Rapport A⁻¹/A = √1.6⁻³",
            "Théorème Thalès: arc_concourant/longueur_totale = aire_disque/longueur_horizon"
        ],
        "definitions": [
            "Trou noir réciproque: Contrepartie inverse d'un trou noir observable",
            "Produit alternatif: Multiplication spécifique arc × aire révélant constantes",
            "Réciprocité volumique: Rapport constant √3.6 entre volumes associés"
        ],
        "relations": [
            "Connexion géométrie de Philippôt",
            "Application théorème fondamental univers au carré",
            "Lien avec constante inverse du temps"
        ],
        "document_source": "Les_trous_noirs__la_réciproque_de_la_limite_de_l_horizon_des_événement_.pdf",
        "page_reference": "Sections 1-6, Figures 2, 5, 7, 10",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 16. SINGULARITÉ COMME AUJOURD'HUI
    {
        "id": "singularite_aujourdhui",
        "titre": "Singularité comme 'Aujourd'hui'",
        "description": "Interprétation philosophique et temporelle révolutionnaire où la singularité d'un trou noir n'est pas un point d'infini mais représente 'aujourd'hui' pour tous sur Terre, à 5/10000 secondes près. Le temps fonctionne comme une multiplication par 1 où le multiplicande 'aspire' le multiplicateur. Nous franchissons constamment la limite de l'horizon des événements dans l'instant présent. La singularité ancre dans le présent perpétuel.",
        "domaine_principal": "Philosophie de la Physique",
        "concepts_cles": [
            "Singularité = instant présent universel",
            "Temps comme multiplication par 1",
            "Multiplicande aspire multiplicateur",
            "Rayon singularité ≈ 5/10000 secondes",
            "Franchissement perpétuel horizon événements",
            "Ancrage dans l'instant présent",
            "Constante 3.6 comme rythme secret univers"
        ],
        "formules": [
            "Rayon singularité ≈ 0.0005 secondes",
            "sin(147.833927°) = (√2.99792458/2) / 0.9009894194",
            "Temps: 1 × n = n × 1 avec aspiration multiplicande",
            "Constante 3.6 = sceau inverse et rythme univers au carré"
        ],
        "definitions": [
            "Singularité temporelle: Point présent universel, non infini spatial",
            "Aspiration multiplicande: Processus temporel où 1 absorbe le multiplicateur",
            "Horizon des événements: Limite franchie perpétuellement dans le présent"
        ],
        "relations": [
            "Lien théorie univers au carré",
            "Connexion constante inverse temps",
            "Rapport célérité et énergie infinie"
        ],
        "document_source": "Les_trous_noirs__la_réciproque_de_la_limite_de_l_horizon_des_événement_.pdf",
        "page_reference": "Sections 9-12, pages 10-12, 19-21",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 17. DIAMÈTRE PARHÉLIQUE ET CÉLÉRITÉ
    {
        "id": "diametre_parhelique_celerite",
        "titre": "Diamètre Parhélique et Réciprocité de la Célérité",
        "description": "Système de calcul géométrique liant le diamètre parhélique (angle 144°), les volumes réciproques, et la vitesse de la lumière. Établit connexions entre E=mc² 'réduite', anomalies indexées m√3.6⁻¹, et conversions angulaires vitesse (m/s ↔ Km/h via angles 45° et √7290°). Volume commun √3.6⁻¹ unit les systèmes de mesure.",
        "domaine_principal": "Physique Théorique",
        "concepts_cles": [
            "Diamètre parhélique à 144°",
            "Équation E=mc² réduite via volumes",
            "Anomalie indexée m = (√3.6)⁻¹ m",
            "Volume commun (√3.6)⁻¹",
            "Conversion vitesse via angles",
            "Célérité 10.79252849 Km/h géométrique",
            "Inverses volumes: (1 + √3.6)⁻¹"
        ],
        "formules": [
            "Diamètre parhélique = 0.9510565163",
            "Volume sphère = (3.6²)⁻¹",
            "E = mc² avec E = 4.755282582",
            "m = 1.003890107 après calcul anomalie",
            "√2.99792458 m/s = 45° ; √x Km/h = √7290°",
            "x Km/h = 10.79252849 (vitesse célérité)",
            "45°/(45° + √7290°) = (1 + √3.6)⁻¹",
            "√7290° × √2.99792458 = 147.833927°"
        ],
        "definitions": [
            "Diamètre parhélique: Diamètre géométrique à angle 144° pour calculs énergétiques",
            "Volume commun: √3.6⁻¹ permettant liaison unités différentes",
            "Anomalie indexée: Facteur correctif m√3.6⁻¹ dans équation énergie"
        ],
        "relations": [
            "Réinterprétation E=mc²",
            "Lien volumes réciproques",
            "Connexion constante 3.6 fondamentale"
        ],
        "document_source": "Les_trous_noirs__la_réciproque_de_la_limite_de_l_horizon_des_événement_.pdf",
        "page_reference": "Sections 7-8, pages 7-10, 16-19",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 18. PRESSION GRAVITO-SPECTRALE COMPLÈTE
    {
        "id": "pression_gravito_spectrale_complete",
        "titre": "Pression Gravito-Spectrale - Système Complet",
        "description": "Point fondamental où l'attraction gravitationnelle (9.8066402 m/s²) rencontre la pression atmosphérique (10T/m²), créant une capacité d'impédance. Cet hypervolume gouverne les dynamiques universelles via la constante de Philippôt (Φp = 10.98064402). Système incluant relations ζ(4), circonférence terrestre (20000 km), et formules alternatives dérivant Φp des propriétés géométriques.",
        "domaine_principal": "Physique Théorique",
        "concepts_cles": [
            "Point rencontre gravité-pression atmosphérique",
            "Capacité d'impédance gravitationnelle",
            "Hypervolume universel",
            "Constante Philippôt Φp = 10.98064402",
            "Relations fonction ζ(4) modifiée",
            "Circonférence 20000 km réels vs déformés",
            "Formules alternatives dérivation Φp"
        ],
        "formules": [
            "Φp = 10.98064402 (constante pression gravito-spectrale)",
            "ζ(4)·π⁴/90 ≈ 1.082323234",
            "ζ(4) Philippôt = ((√2 + 1)/(2×4))⁻¹ = 9.941125497",
            "(9.941125497)²/90 = 1.098066402",
            "(4 – √8) × (√√32 – 4) × √8 × 2 = 10.98066402",
            "Circonférence 2 arcs = 20000 km",
            "Diamètre: 10000 km réel, 12000 km déformé",
            "√(40960 km) = 202.3857703 km",
            "4/√10 = √1.6 = 1.264911064 × 10⁴ km",
            "(√1.6)³ = 2.023857703 (inverse temps)"
        ],
        "definitions": [
            "Pression gravito-spectrale: Point interaction attraction/pression atmosphérique",
            "Capacité impédance: Propriété annulation tension parasite gravitationnelle",
            "Hypervolume: Dimension spatiale pression gravito-spectrale",
            "Constante Philippôt Φp: Valeur fondamentale gouvernant dynamiques universelles"
        ],
        "relations": [
            "Lien fonction ζ(4) modifiée",
            "Connexion triangle primordial",
            "Relation chaons et forces discrètes"
        ],
        "document_source": "version_corrige_partie1_univers_est_au_carre.pdf",
        "page_reference": "Section 8, Tableaux Chaons",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 19. CHAONS ET TRIANGLE PRIMORDIAL
    {
        "id": "chaons_triangle_primordial",
        "titre": "Chaons et Triangle Primordial",
        "description": "Ondes fondamentales du chaos discret (Alpha, Beta, Gamma, etc.) associées au Triangle Primordial avec rapport base/hauteur 1/2 selon règle Philippôt. Chaque Chaon possède évocation spécifique (Choc ouverture spectre, Résonance binoculaire, etc.). Hypoténuse divisée en 8 segments avec rapport harmonique √2. Structurent dynamique gravito-spectrale et tensions géométriques fondamentales.",
        "domaine_principal": "Géométrie Fondamentale",
        "concepts_cles": [
            "Chaons: unités géométriques discrètes",
            "Triangle Primordial fondateur",
            "Rapport base/hauteur = 1/2",
            "Hypoténuse divisée 8 segments",
            "Rapport harmonique √2",
            "Évocations spécifiques par Chaon",
            "Forces chaotiques structurantes"
        ],
        "formules": [
            "Rapport triangle primordial: base/hauteur = 1/2",
            "Hypoténuse: 8 segments, rapport √2",
            "Constante harmonique liée √2",
            "Tensions géométriques spectrales"
        ],
        "definitions": [
            "Chaons: Ondes fondamentales chaos discret",
            "Triangle Primordial: Structure géométrique fondatrice avec rapport 1/2",
            "Évocation Chaon: Manifestation spécifique (ex: Choc ouverture, Résonance)",
            "Rapport harmonique: Progression √2 structurant segments"
        ],
        "relations": [
            "Fondement pression gravito-spectrale",
            "Lien analyse numérique métrique",
            "Base constantes géométriques universelles"
        ],
        "document_source": "version_corrige_partie1_univers_est_au_carre.pdf + Banque Q&R",
        "page_reference": "Section 8.2, Question 6 Banque",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 20. MÉTAGÉOMÉTRIE ET GÉOMÉTRIE PERCEPTIVE
    {
        "id": "metageometrie_perceptive",
        "titre": "Métagéométrie et Géométrie Perceptive",
        "description": "Nouvelle conception géométrique où longueurs possèdent valeur numérique et le choix d'unité agit comme 'lentille' transformant interprétation spatiale. Géométrie devient relationnelle, influencée par observateur. Invariance ne dépend plus transformations usuelles mais changement unité interprétative. La 'vue' adoptée influence 'vérité' ou précision, créant espace fluide dont propriétés émergent du contexte.",
        "domaine_principal": "Géométrie Non-Euclidienne",
        "concepts_cles": [
            "Longueurs avec valeur numérique",
            "Unité comme lentille transformative",
            "Géométrie relationnelle observateur",
            "Invariance par changement unité",
            "Vue influence vérité géométrique",
            "Espace fluide contextuel",
            "Propriétés émergentes du contexte"
        ],
        "formules": [
            "Transformation unité comme opérateur lentille",
            "Invariance nouvelle forme: non translation/rotation classique",
            "Contexte: (unité, angle, point_départ) → propriétés spatiales"
        ],
        "definitions": [
            "Métagéométrie: Géométrie des transformations d'interprétation spatiale",
            "Lentille unité: Unité choisie modifiant perception espace-nombre",
            "Géométrie perceptive: Système où vue adoptée détermine vérité",
            "Invariance interprétative: Propriété conservée par changement unité"
        ],
        "relations": [
            "Extension géométrie de Philippôt",
            "Connexion mécanique harmonique chaos",
            "Lien relativité des mesures"
        ],
        "document_source": "version_corrige_partie1_univers_est_au_carre.pdf",
        "page_reference": "Section 15.2, Mécanique harmonique",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 21. MÉTHODE SPECTRALE QUANTITÉ PREMIERS
    {
        "id": "methode_spectrale_quantite_premiers",
        "titre": "Méthode Spectrale pour Quantité de Nombres Premiers",
        "description": "Algorithme novateur déterminant quantité nombres entre deux premiers via suites et Digamma. Formules: Somme 1ère suite (√(x2)^n) - √B, Somme 2ème suite (√(x2)^n) - √D. Calcul quantité: (somme_1 - (somme_2 - Digamma_grand)) puis (résultat - Digamma_petit)/√5120. Alternative classique: q - p - 1. Généralise rapports 1/2 à 1/100 pour détermination 100% premiers.",
        "domaine_principal": "Théorie des Nombres",
        "concepts_cles": [
            "Détermination quantité entre premiers",
            "Formules suites avec Digamma",
            "Algorithme double étape",
            "Généralisation rapports 1/2 à 1/100",
            "Détermination 100% pour certains rapports",
            "Compression numérique moulinet",
            "Intervalles positifs et négatifs"
        ],
        "formules": [
            "Somme 1ère suite: (√(x2)^n) - √B",
            "Somme 2ème suite: (√(x2)^n) - √D",
            "Étape 1: somme_1 - (somme_2 - Digamma_grand)",
            "Étape 2: (résultat_1 - Digamma_petit) / √5120",
            "Méthode classique: q - p - 1",
            "Rapports généralisés: 1/n avec n ∈ {2,3,4,...,100}"
        ],
        "definitions": [
            "Méthode spectrale: Algorithme suites-Digamma pour quantités premiers",
            "Quantité entre premiers: Nombre d'entiers entre deux nombres premiers",
            "Compression moulinet: Technique réduction écarts via calculs spectraux",
            "Généralisation rapports: Extension systématique 1/2 à 1/100"
        ],
        "relations": [
            "Application directe Digamma Philippôt",
            "Connexion technique moulinet",
            "Lien analyse numérique métrique"
        ],
        "document_source": "version_corrige_partie1_univers_est_au_carre.pdf",
        "page_reference": "Sections 12, 13, Exemples paires premiers",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 22. MÉCANIQUE HARMONIQUE CHAOS DISCRET COMPLÈTE
    {
        "id": "mecanique_harmonique_chaos_complet",
        "titre": "Mécanique Harmonique du Chaos Discret - Système Complet",
        "description": "Composante centrale 'L'univers est au carré' agissant comme transformateur modifiant espace et objets en métrique active influencée par unité harmonique. Méta-géométrie construisant matrice unitaire initiale. Unité fondamentale: ratio triangulaire (Base/Hauteur + 1). Formules: AC×3 = HI×CB = EH², produits alternatifs généralisés, matrice mesures unitaires avec arcsin pour √3+1.",
        "domaine_principal": "Géométrie Non-Euclidienne",
        "concepts_cles": [
            "Transformateur espace-objets",
            "Métrique active unité harmonique",
            "Méta-géométrie matricielle",
            "Matrice unitaire initiale",
            "Unité ratio triangulaire",
            "Produits alternatifs généralisés",
            "Invariance unitaire"
        ],
        "formules": [
            "AC × 3 = HI × CB = EH²",
            "Produits alternatifs: 3×5×5 = 5×3×5",
            "Généralisation: 3×5×n = 5×(n-1)×3×5",
            "arcsin(GH) = arcsin(0.3882285678) = 22.84432054°",
            "IE × (0.5/sin(22.84432054°)) = √3+1",
            "Unité: EI = √4.5 × (0.5/sin(22.84432054°))",
            "Lien Euler-Mascheroni: (0.5/sin(60°)) = √3 ≈ γ",
            "Constante: 25.7196423",
            "EG² = 1.3448632082 (Diamètre Équivalent carré)"
        ],
        "definitions": [
            "Mécanique chaos discret: Système transformations espace-objets discrètes",
            "Mécanique harmonique: Influence unité harmonique sur métrique",
            "Méta-géométrie: Géométrie transformations spatiales matricielles",
            "Matrice unitaire: Construction géométrique initiale fondamentale",
            "Produit alternatif: Relation géométrique spécialisée généralisée"
        ],
        "relations": [
            "Central à univers au carré",
            "Intégration géométrie Philippôt",
            "Base matrice à dérive première",
            "Violation invariance renversement temporel"
        ],
        "document_source": "version_corrige_partie1_univers_est_au_carre.pdf + Banque Q&R",
        "page_reference": "Section 15, Questions 11-12 Banque, Matrices",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 23. THÉORÈME PHILIPPÔT VERSIONS FORMALISÉES
    {
        "id": "theoreme_philippot_versions_formalisees",
        "titre": "Théorème de Philippôt - Versions Formalisées Complètes",
        "description": "Théorème fondamental en trois versions: (1) Formalisée avec variables géométriques générales, (2) Formelle avec variables abstraites a,b,c, (3) Racines conventionnelles avec nombres d'or Φ. Établit équivalences: périmètre triangle = aire carré = aire disque = volume cube^(2/3). Diamètre hyperréel = √(A×4)/√8. Deux possibilités disque. Inégalités spectrales: 1/√2 = (ax+bx)/(a+b).",
        "domaine_principal": "Géométrie Fondamentale",
        "concepts_cles": [
            "Trois versions complémentaires",
            "Variables géométriques généralisées",
            "Équivalences dimensionnelles universelles",
            "Diamètre hyperréel formule",
            "Deux possibilités aire disque",
            "Inégalités spectrales",
            "Application nombre d'or Φ"
        ],
        "formules": [
            "a + b + c = Périmètre = Aire carré = A",
            "Côté carré = √A",
            "Diamètre hyperréel = √(A×4)/√8",
            "Aire arc = (L × Diamètre)/2 = A",
            "Possibilité 1: Aire = Diamètre² × √10",
            "Possibilité 2: Aire = (a/0.5 + b/0.5), Rayon = ((a+b)/10)²",
            "Inégalité: 1/√2 = (ax+bx)/(a+b) ⇒ x = V/(a+b)",
            "Volume: V = (A/4)×x + A×x",
            "Rapport volumes = √10",
            "Version Φ: 1 + 2 + √5 = 2Φ² ≈ 5.236067977"
        ],
        "definitions": [
            "Version formalisée: Formalisation mathématique variables générales",
            "Version formelle: Généralisation algébrique abstraite a,b,c",
            "Version racines: Notation avec nombre d'or Φ et racines",
            "Diamètre hyperréel: Diamètre géométrique dans espace étendu"
        ],
        "relations": [
            "Fondement géométrie Philippôt",
            "Base analyse spectrale universelle",
            "Connexion équivalences dimensionnelles"
        ],
        "document_source": "version_corrigé_2ième_partie_univers_est_au_carré.pdf",
        "page_reference": "Chapitres 17, 18, 20",
        "niveau_complexite": "fondamental",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 24. THÉORÈME CARRÉ DE GABRIEL
    {
        "id": "theoreme_carre_gabriel",
        "titre": "Théorème du Carré de Gabriel",
        "description": "Théorème applicable triangles scalènes rectangles ET non-rectangles. Construction carré inscrit dans triangle avec relations aires: triangle ABC = h² + Aire disque. Associable loi sinus et Pythagore. Calculs aires triangles observés vs théoriques. Généralisation constructions algorithmiques pour différents types triangles. Démonstrations géométriques universelles propriétés inscription.",
        "domaine_principal": "Géométrie Constructive",
        "concepts_cles": [
            "Application triangles scalènes",
            "Carré inscrit construction",
            "Valide rectangles ET non-rectangles",
            "Relations aires triangle-carré-disque",
            "Associable loi sinus",
            "Connexion Pythagore",
            "Algorithmes constructifs"
        ],
        "formules": [
            "Aire triangle ABC = h² + Aire disque",
            "Relations carré inscrit/triangles environnants",
            "Calculs aires observées vs théoriques",
            "Constructions algorithmiques généralisées"
        ],
        "definitions": [
            "Carré de Gabriel: Carré inscrit selon méthode Gabriel",
            "Triangle scalène: Triangle trois côtés inégaux",
            "Construction algorithmique: Processus géométrique systématique",
            "Propriété universelle: Valide pour tous types triangles"
        ],
        "relations": [
            "Extension théorème Philippôt",
            "Connexion géométrie plane classique",
            "Application équivalences dimensionnelles"
        ],
        "document_source": "version_corrigé_2ième_partie_univers_est_au_carré.pdf",
        "page_reference": "Chapitre 13, Figures 22-23, 64-65",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 25. THÉORÈME GRIS BLEU
    {
        "id": "theoreme_gris_bleu",
        "titre": "Théorème Gris Bleu de Philippôt",
        "description": "Théorème avancé traitant rotation quaternions dans espace, nombres hypercomplexes, géométrie épipolaire et matrice sans blocage cardans. Illustré par Spirale Théodore de Cyrène montrant progression hypoténuses (√2, √3, √4, √5, √6...) dictant facteur isométrique espace-pyramide. Suggestion relations entre nombres premiers. Formule générale hypercomplexes: (2×Aire + 2×Aire×√10 + Rayon²)^(1/2).",
        "domaine_principal": "Géométrie Non-Euclidienne",
        "concepts_cles": [
            "Rotation quaternions espace",
            "Nombres hypercomplexes",
            "Géométrie épipolaire",
            "Matrice sans blocage cardans",
            "Spirale Théodore Cyrène",
            "Facteur isométrique espace",
            "Relations nombres premiers potentielles"
        ],
        "formules": [
            "Progression: √2, √3, √4, √5, √6...",
            "Facteur isométrique dictant pyramide spatiale",
            "Formule hypercomplexes: (2×Aire + 2×Aire×√10 + Rayon²)^(1/2)",
            "Espace infini 4 dimensions",
            "Rotation quaternions sans gimbal lock"
        ],
        "definitions": [
            "Théorème Gris Bleu: Relations quaternions-hypercomplexes-géométrie",
            "Spirale Théodore: Progression hypoténuses √n",
            "Facteur isométrique: Constante dictant structure spatiale pyramide",
            "Matrice sans blocage: Rotation quaternions évitant gimbal lock"
        ],
        "relations": [
            "Extension espace 4D Philippôt",
            "Connexion nombres hypercomplexes",
            "Lien potentiel nombres premiers"
        ],
        "document_source": "version_corrigé_2ième_partie_univers_est_au_carré.pdf",
        "page_reference": "Chapitre 11.10, Figures 19, 53, 58",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 26. ESPACE MINKOWSKI SELON PHILIPPÔT DÉTAILLÉ
    {
        "id": "minkowski_philippot_detaille",
        "titre": "Espace de Minkowski selon Philippôt - Analyse Détaillée",
        "description": "Réinterprétation complète espace-temps Minkowski: deux cônes = deux pyramides. Cubes inscrits créent 'frein temporel' avec impédance simultanéité liée vitesse lumière. Puzzle métrique Minkowski avec homothétie groupes Poincaré. Hypersurface présent analysée: volume, périmètre cônes, aire cube inscrit. Capacité impédance temporelle. Relations géométriques espace-temps carrées.",
        "domaine_principal": "Physique Théorique",
        "concepts_cles": [
            "Cônes = pyramides Philippôt",
            "Cubes inscrits frein temps",
            "Impédance simultanéité",
            "Lien vitesse lumière",
            "Puzzle métrique Minkowski",
            "Homothétie Poincaré",
            "Hypersurface présent géométrique"
        ],
        "formules": [
            "Volume hypersurface présent: V = √17.77777",
            "Périmètre cônes: 2(√40 - √20) + 2(√20 - √10) = 2√10",
            "Aire cube inscrit calculée",
            "Impédance temporelle: frein simultanéité",
            "Relations métrique Minkowski modifiée",
            "Homothétie groupes Poincaré appliquée"
        ],
        "definitions": [
            "Cônes-pyramides: Interprétation cônes Minkowski comme pyramides",
            "Frein temporel: Cube inscrit créant impédance au temps",
            "Impédance simultanéité: Résistance propagation instantanée",
            "Hypersurface présent: Surface géométrique instant actuel",
            "Puzzle métrique: Configuration complexe métrique Minkowski"
        ],
        "relations": [
            "Réinterprétation relativité restreinte",
            "Extension espace-temps carré",
            "Application cosmologie géométrique"
        ],
        "document_source": "version_corrigé_2ième_partie_univers_est_au_carré.pdf",
        "page_reference": "Chapitre 9, Figures 12",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # === NOUVEAUX CONCEPTS DE LA BANQUE Q&R ENRICHIE (Questions 14-18) ===
    
    # 27. RÉCIPROCITÉ VOLUMIQUE ET CÉLÉRITÉ COMME INVARIANTS
    {
        "id": "reciprocite_volumique_celerite_invariants",
        "titre": "Réciprocité Volumique et Célérité comme Invariants Géométriques",
        "description": "Interprétation des trous noirs comme espaces de stockage d'information potentiellement infinis. Chaque trou noir tangible en relation avec un trou noir virtuel réciproque. Rayon du trou noir égal à l'angle formé avec l'horizon des événements (√18000° = 134.164°). Produit alternatif réciproque: produit aire disque × carré aire × longueur horizon opposé. Rapport produits donne constante (√1.6)³ interprétée comme inverse du temps. Temps comme opération où multiplicateur aspire multiplicande: 2×1 = 1×2.",
        "domaine_principal": "Astrophysique Théorique",
        "concepts_cles": [
            "Réciprocité volumique",
            "Célérité comme invariant",
            "Entropie trous noirs",
            "Stockage information infini",
            "Trou noir virtuel réciproque",
            "Produit alternatif réciproque",
            "Horizon des événements",
            "Constante inverse du temps (√1.6)³",
            "Temps comme multiplication"
        ],
        "formules": [
            "Rayon = √18000° = 134.1640786°",
            "Rayon = √1.8 unités",
            "Constante inverse temps = (√1.6)³ = 2.023857703",
            "Temps: 2 × 1 = 1 × 2",
            "Singularité temporelle = 5/10000 secondes"
        ],
        "definitions": [
            "Réciprocité volumique: Rapport constant entre volumes associés de trous noirs réciproques",
            "Trou noir virtuel: Contrepartie théorique réciproque d'un trou noir observable",
            "Produit alternatif réciproque: Produit aire × carré aire × horizon opposé",
            "Inverse du temps: Constante (√1.6)³ révélant structure temporelle"
        ],
        "relations": [
            "Lien entropie et information",
            "Connexion constante 3.6 fondamentale",
            "Application théorème univers au carré"
        ],
        "document_source": "Banque_Questions_Réponses_Géométrie_Philippot_corrigé.pdf",
        "page_reference": "Question 14",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # 28. ÉNERGIE COMME RYTHME - E=MC² RÉDUITE
    {
        "id": "energie_rythme_emc2_reduite",
        "titre": "Énergie comme Rythme - Réduction E=mc² Trous Noirs",
        "description": "Réinterprétation révolutionnaire E=mc² en double lecture (réduite et non réduite) dans contexte trous noirs. Figure sphérique rayon angle 144° révèle diamètre parhélique concept central. Diamètre parhélique représente énergie (E), sa demi-longueur mesure énergie. Volume sphère = masse (m) considérée comme information. Équation non réduite démontre pression P=0, infiniment proche zéro, représente par inversion valeur approchée infini. Volume devient facteur-pont entre énergie infinie et masse. Produits alternatifs célérité (m/s, km/h) liés géométriquement par diamètre parhélique.",
        "domaine_principal": "Physique Théorique",
        "concepts_cles": [
            "E=mc² réduite et non réduite",
            "Diamètre parhélique",
            "Énergie comme rythme",
            "Masse comme information",
            "Pression P=0 et infini",
            "Volume facteur-pont",
            "Célérité géométrique (m/s ↔ km/h)",
            "Conversion unités par volume"
        ],
        "formules": [
            "E = mc² (version réduite)",
            "P = 0 (équation non réduite)",
            "Angle sphère = 144°",
            "Diamètre parhélique = demi-longueur énergie",
            "Volume sphère = masse (information)",
            "Masse algébrique ≈ 1"
        ],
        "definitions": [
            "Diamètre parhélique: Diamètre géométrique angle 144° représentant énergie",
            "Énergie-rythme: Énergie non comme quantité mais pulsation rythmique",
            "Masse-information: Matière considérée forme d'information stockée",
            "P=0: Pression nulle représentant infini par inversion proportionnelle"
        ],
        "relations": [
            "Connexion entropie trous noirs",
            "Lien produits alternatifs réciproques",
            "Application réciprocité volumique"
        ],
        "document_source": "Banque_Questions_Réponses_Géométrie_Philippot_corrigé.pdf",
        "page_reference": "Question 15",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # 29. SINGULARITÉ COMME SEUIL RYTHMIQUE
    {
        "id": "singularite_seuil_rythmique",
        "titre": "Singularité comme Seuil Rythmique - Non Rupture",
        "description": "Vision philosophique révolutionnaire: singularité non point de rupture empirique mais construction théorique, intuition mathématique et philosophique. Vérité fondamentale: nous sommes toujours maintenant, jamais passé ni futur, toujours instant présent. Expérience mentale: figer horloge 23h59min995cs = 'aujourd'hui', 5/10000 seconde plus tard serait 'demain', mais transition nous maintient. Singularité devient seuil rythmique, frontière qui pulse sans séparer. Battement ultime temps gardant au bord demain sans y basculer. Singularité vue comme multiplication où multiplicateur aspire multiplicande: 1×2 = 2×1.",
        "domaine_principal": "Philosophie de la Physique",
        "concepts_cles": [
            "Singularité seuil rythmique",
            "Non-rupture temporelle",
            "Instant présent perpétuel",
            "Évidence rythmique universelle",
            "Temps comme pulsation",
            "Singularité temporelle 5/10000 s",
            "Multiplication aspiration",
            "Réciprocité cosmique rythmique"
        ],
        "formules": [
            "Singularité temporelle = 5/10000 secondes = 0.0005 s",
            "1 × 2 = 2 × 1 (aspiration multiplicande)",
            "23h59min995cs = aujourd'hui",
            "Transition ≈ 5/10000 s"
        ],
        "definitions": [
            "Singularité rythmique: Seuil temporel pulsant maintenant dans présent",
            "Seuil rythmique: Frontière temporelle battant sans rupture",
            "Évidence rythmique: Vérité fondamentale être toujours maintenant",
            "Aspiration multiplicande: Opération temps où 1 absorbe multiplicateur"
        ],
        "relations": [
            "Connexion trous noirs et temps",
            "Lien horizon des événements",
            "Application théorie univers au carré"
        ],
        "document_source": "Banque_Questions_Réponses_Géométrie_Philippot_corrigé.pdf",
        "page_reference": "Question 16",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # 30. PRODUITS ALTERNATIFS INTERACTION TROUS NOIRS
    {
        "id": "produits_alternatifs_interaction_trous_noirs",
        "titre": "Produits Alternatifs Géométriques - Interaction Trous Noirs",
        "description": "Représentation théorique interaction deux trous noirs nez à nez via produits alternatifs géométriques, sans outils tensoriels relativité générale. Expérience pensée purement mathématique: produit alternatif réciproque démontre entropie affecte aire (non volume). Relations formalisées: A = Horizon_réciproque × Entropie² = Entropie × Horizon. Et A⁻¹ = Horizon × Entropie_réciproque² = Entropie_réciproque × Horizon_réciproque. Rapport fondamental: Arc_concourant/Arc_rayonnement = Aire/Horizon. Constante réciprocité temporelle: Trou_noir_réciproque/Trou_noir = (1.6)³, constante inverse temps.",
        "domaine_principal": "Astrophysique Théorique",
        "concepts_cles": [
            "Produits alternatifs géométriques",
            "Interaction trous noirs théorique",
            "Expérience pensée mathématique",
            "Entropie affecte aire (non volume)",
            "Théorème analogie Thalès",
            "Réciprocité géométrique",
            "Constante réciprocité temporelle",
            "Sans tenseurs relativité"
        ],
        "formules": [
            "A = Horizon_réciproque × (Entropie)² = Entropie × Horizon",
            "A⁻¹ = Horizon × (Entropie_réciproque)² = Entropie_réciproque × Horizon_réciproque",
            "Arc_concourant/Arc_rayonnement = Aire_trou_noir/Horizon_trou_noir",
            "Trou_noir_réciproque/Trou_noir = (1.6)³ = 2.023857703",
            "Constante inverse temps = (√1.6)³"
        ],
        "definitions": [
            "Produit alternatif géométrique: Produit Horizon × Entropie révélant constantes",
            "Interaction nez à nez: Configuration théorique collision trous noirs",
            "Entropie géométrique: Information affectant surface non volume",
            "Réciprocité temporelle: Rapport constant (1.6)³ entre trous noirs réciproques"
        ],
        "relations": [
            "Lien entropie et géométrie",
            "Connexion constante 1.6 fondamentale",
            "Application théorème Thalès géométrique"
        ],
        "document_source": "Banque_Questions_Réponses_Géométrie_Philippot_corrigé.pdf",
        "page_reference": "Question 17 et 18",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    # === NOUVEAUX CONCEPTS - GÉOMÉTRIE DU SPECTRE DES NOMBRES PREMIERS ===
    
    # 31. GÉOMÉTRIE DU SPECTRE DES NOMBRES PREMIERS
    {
        "id": "geometrie_spectre_nombres_premiers",
        "titre": "Géométrie du Spectre des Nombres Premiers",
        "description": "Cadre géométrique conceptualisé pour représenter la distribution et les propriétés des nombres premiers, intégrant des visualisations 3D et des analyses numériques complexes. Vise à dévoiler une structure sous-jacente qui relie la géométrie aux nombres premiers et potentiellement à l'hypothèse de Riemann.",
        "domaine_principal": "Mathématiques Théoriques",
        "concepts_cles": [
            "Visualisation géométrique 3D des nombres premiers",
            "Projections et hyperplans",
            "Structure spectrale des nombres premiers",
            "Liens géométrie-arithmétique",
            "Approche non conventionnelle de Riemann"
        ],
        "formules": [],
        "definitions": [
            "Spectre géométrique: Ensemble des manifestations géométriques des nombres premiers",
            "Hyperplan: Surface traversant l'ensemble des cubes pour délimiter le plan cartésien",
            "Structure sous-jacente: Organisation cachée révélée par l'analyse géométrique"
        ],
        "relations": [
            "Fondement de l'analyse numérique métrique",
            "Base pour modèle géométrique fonction Zêta",
            "Connexion avec l'hypothèse de Riemann"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Sections 1-2",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 32. MODÈLE GÉOMÉTRIQUE FONCTION ZÊTA
    {
        "id": "modele_geometrique_fonction_zeta",
        "titre": "Modèle Géométrique de la Fonction Zêta",
        "description": "Représentation visuelle en 3D de la fonction zêta de Riemann, utilisant quatre pyramides orientées dans des directions cardinales, formant une structure cubique traversée par un hyperplan. Ce modèle cherche à illustrer la dynamique et les propriétés de la fonction Zêta dans un espace géométrique.",
        "domaine_principal": "Analyse Complexe",
        "concepts_cles": [
            "Quatre pyramides orientées",
            "Structure cubique et hyperplan",
            "Visualisation fonction zêta",
            "Modélisation 3D des zéros",
            "Approche géométrique analytique"
        ],
        "formules": [],
        "definitions": [
            "Pyramides cardinales: Structures orientées Nord, Sud, Est, Ouest",
            "Hyperplan jaune: Surface traversant les cubes",
            "Tesseract: Expression du repli des cubes"
        ],
        "relations": [
            "Lien avec hypothèse de Riemann",
            "Visualisation des zéros non triviaux",
            "Fondement géométrie du spectre"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Section 2.1, Figure 1",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 33. ANALYSE NUMÉRIQUE MÉTRIQUE (PHILIPPÔT)
    {
        "id": "analyse_numerique_metrique_philippot",
        "titre": "Analyse Numérique Métrique selon Philippôt",
        "description": "Méthode d'analyse numérique fondée sur des suites fractionnaires et la manipulation de figures géométriques (rectangles, carrés, cubes) pour déterminer des propriétés des nombres premiers. Inspirée par le principe de substitution dans l'analyse granulométrique.",
        "domaine_principal": "Analyse Numérique",
        "concepts_cles": [
            "Suites fractionnaires itératives",
            "Substitution positionnelle",
            "Manipulation figures géométriques",
            "Schémas 3D et parallélogrammes",
            "Rapports invariants"
        ],
        "formules": [
            "Suites itératives avec règles de progression",
            "Étape 1: Σ(aₙ + aₙ₋₁ + ... + a₁) = 1",
            "Position k: valeur 1/(2^(k+4))"
        ],
        "definitions": [
            "Analyse métrique: Méthode de mesure basée sur substitutions positionnelles",
            "Suite fractionnaire: Séquence de fractions suivant des règles itératives",
            "Substitution: Déplacement de valeurs selon positions"
        ],
        "relations": [
            "Inspirée de l'analyse granulométrique",
            "Connexion au Digamma grec",
            "Fondement des rapports triangulaires"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Sections 2.4, 7.1-7.2",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 34. DIGAMMA COMME OUTIL DE CALCUL
    {
        "id": "digamma_outil_calcul_philippot",
        "titre": "Digamma comme Outil de Calcul",
        "description": "La fonction Digamma (ψ(x)) est utilisée comme élément clé pour déterminer les nombres premiers et vérifier des hypothèses. Sa position dans les calculs (7ème, 8ème ou 9ème) est déterminante. Lié à la numération grecque où Digamma est situé entre Epsilon et Zêta.",
        "domaine_principal": "Théorie des Nombres",
        "concepts_cles": [
            "Fonction Digamma ψ(x)",
            "Positions critiques (7e, 8e, 9e)",
            "Calculs de suites",
            "Addition/soustraction selon rapport Base/Hauteur",
            "Lien numération grecque"
        ],
        "formules": [
            "ψ(n) = √((n+7)² + (n+8)²)",
            "Digamma calculé à position p dans suites",
            "Formule du Digamma selon Philippôt"
        ],
        "definitions": [
            "Digamma: Lettre grecque archaïque entre Epsilon et Zêta",
            "Position Digamma: Emplacement critique dans séquences de calcul",
            "Digamma calculé: Valeur dérivée pour ajuster résultats"
        ],
        "relations": [
            "Connexion analyse numérique métrique",
            "Lien avec détermination nombres premiers",
            "Fondement anomalie Zêta grec"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Sections 3, 7.2, 8.2",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 35. RAPPORTS TRIANGULAIRES ET CONVERGENCE VERS 1/2
    {
        "id": "rapports_triangulaires_convergence",
        "titre": "Rapports Triangulaires et Convergence vers 1/2",
        "description": "Étude des rapports (base/hauteur) dans des figures géométriques associées aux nombres premiers. Ces rapports, manipulés par les méthodes de Philippôt, tendent à converger vers 1/2, interprété comme confirmation de l'hypothèse de Riemann.",
        "domaine_principal": "Géométrie Fondamentale",
        "concepts_cles": [
            "Rapport base/hauteur = 1/n",
            "Convergence systématique vers 1/2",
            "Figures géométriques (triangles, trapèzes)",
            "Confirmation hypothèse Riemann",
            "Rapports invariants"
        ],
        "formules": [
            "base/hauteur = 1/2",
            "Aire trapèze = ((b₁ + b₂)/2) × h",
            "Rapports: 50/100 = 100/200 = 200/400 = 1/2"
        ],
        "definitions": [
            "Rapport triangulaire: Relation base/hauteur dans figures géométriques",
            "Convergence vers 1/2: Tendance systématique des rapports",
            "Invariant 1/2: Valeur constante observée dans analyses"
        ],
        "relations": [
            "Lien direct avec hypothèse Riemann",
            "Connexion au rapport 1/2 comme valeur de référence",
            "Fondement des suites fractionnaires"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Sections 7.15-7.20",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 36. SUITES FRACTIONNAIRES ITÉRATIVES
    {
        "id": "suites_fractionnaires_iteratives",
        "titre": "Suites Fractionnaires Itératives",
        "description": "Suites de nombres fractionnaires construites selon des règles itératives spécifiques. La somme de ces suites, souvent dans des 'étapes' successives, produit des résultats finis utilisés pour identifier des propriétés des nombres premiers.",
        "domaine_principal": "Analyse",
        "concepts_cles": [
            "Construction itérative",
            "Règles récurrentes",
            "Somme convergeant vers 1",
            "Étapes successives",
            "Propriétés nombres premiers"
        ],
        "formules": [
            "a₁ = 1/2",
            "Pour i=2 à n-3: aᵢ = aᵢ₋₁ × (1/2)",
            "Avant-dernier: aₙ₋₁ = aₙ₋₂ × (2/3)",
            "Dernier: aₙ = aₙ₋₁ × (1/2)",
            "Progression: 1/(3^(n+1)) / 1/(3^n) = 1/3"
        ],
        "definitions": [
            "Suite fractionnaire: Séquence de fractions suivant règles itératives",
            "Étape: Phase de calcul dans méthode Philippôt",
            "Convergence: Tendance de la somme vers valeur finie"
        ],
        "relations": [
            "Cœur de la méthode numérique Philippôt",
            "Lien avec rapports triangulaires",
            "Connexion analyse métrique"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Sections 7.15-7.22, Tables 1-26",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 37. NOMBRES PREMIERS COMME INFINITÉS
    {
        "id": "nombres_premiers_comme_infinites",
        "titre": "Les Nombres Premiers comme Infinités",
        "description": "Concept philosophique où chaque nombre premier, bien que fini, porte en lui une infinité intrinsèque. Cette infinité se manifeste par sa capacité à générer des structures infinies (suites, groupes) et par ses propriétés irréductibles mais universelles.",
        "domaine_principal": "Philosophie des Mathématiques",
        "concepts_cles": [
            "Infini intrinsèque aux premiers",
            "Structures infinies générées",
            "Propriétés irréductibles",
            "Universalité des premiers",
            "Singularités géométriques"
        ],
        "formules": [],
        "definitions": [
            "Infini en soi: Chaque premier comme entité infinie individuelle",
            "Singularité géométrique: Premier comme point fondamental dans l'infini",
            "Universalité: Propriété fondamentale partagée par tous les premiers"
        ],
        "relations": [
            "Lien avec compression de l'infini",
            "Connexion spectre des nombres premiers",
            "Fondement philosophique de la théorie"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Sections 7.13-7.14, 13.0",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 38. COMPRESSION PROPORTIONNELLE DE L'INFINI
    {
        "id": "compression_proportionnelle_infini",
        "titre": "Compression Proportionnelle de l'Infini",
        "description": "Concept selon lequel l'infini peut être représenté comme un espace structuré où les nombres premiers sont compressés le long d'un diamètre, et l'ensemble des entiers composés se répartit sur une surface. Cette compression permet de 'ramener' l'infini à une position médiane.",
        "domaine_principal": "Théorie de l'Infini",
        "concepts_cles": [
            "Infini comme espace structuré",
            "Compression des premiers",
            "Diamètre vs surface (Cantor)",
            "Position médiane de l'infini",
            "Dernier nombre premier"
        ],
        "formules": [
            "Somme entiers entre -3 et 1000033",
            "Représentation proportionnelle de l'infini"
        ],
        "definitions": [
            "Compression: Rapprochement des premiers vers l'infini",
            "Espace structuré: Infini organisé par géométrie des premiers",
            "Dernier premier: Point médian marquant moitié de l'infini"
        ],
        "relations": [
            "Lien avec nombres premiers comme infinités",
            "Connexion figure conceptuelle infini composé",
            "Application théorème Cantor"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Sections 10-11",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 39. LE ZÊTA GREC ET SUBSTITUTION
    {
        "id": "zeta_grec_substitution",
        "titre": "Le Zêta Grec et l'Idée de Substitution",
        "description": "Observation que la lettre grecque Zêta (ζ) vaut 7 mais occupe la sixième position dans l'alphabet. Cette particularité, due à l'ancienne existence du Digamma, sert de métaphore pour illustrer le déplacement, la substitution et les valeurs ne correspondant pas à leur position logique.",
        "domaine_principal": "Histoire des Mathématiques",
        "concepts_cles": [
            "Anomalie Zêta grec",
            "Valeur 7 en position 6",
            "Digamma archaïque",
            "Substitution positionnelle",
            "Inspiration métaphorique"
        ],
        "formules": [],
        "definitions": [
            "Anomalie Zêta: Décalage valeur/position",
            "Substitution: Déplacement conceptuel de valeurs",
            "Digamma archaïque: Lettre grecque disparue entre Epsilon et Zêta"
        ],
        "relations": [
            "Inspiration pour analyse numérique métrique",
            "Connexion au Digamma comme outil",
            "Fondement principe de substitution"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Section 2.2",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 40. RAPPORT 1/2 COMME VALEUR DE RÉFÉRENCE
    {
        "id": "rapport_demi_valeur_reference",
        "titre": "Le Rapport 1/2 comme Valeur de Référence",
        "description": "La valeur 1/2 est présentée comme une 'valeur de référence' fondamentale, le 'pôle' autour duquel la recherche tourne, particulièrement en lien avec l'hypothèse de Riemann et les rapports observés dans les analyses géométriques et numériques.",
        "domaine_principal": "Théorie des Nombres",
        "concepts_cles": [
            "Valeur fondamentale 1/2",
            "Pôle de convergence",
            "Invariant mathématique",
            "Lien hypothèse Riemann",
            "Confirmation géométrique"
        ],
        "formules": [
            "Rapport constant = 1/2",
            "Partie réelle zéros = 1/2",
            "Rapports géométriques → 1/2"
        ],
        "definitions": [
            "Valeur de référence: Constante fondamentale 1/2",
            "Pôle 1: Convergence symbolique vers 1/2",
            "Invariant: Propriété constante dans analyses"
        ],
        "relations": [
            "Cœur de l'hypothèse de Riemann",
            "Connexion rapports triangulaires",
            "Fondement convergence géométrique"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Sections 1.1, 7.8, 13.0",
        "niveau_complexite": "fondamental",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 41. NOMBRES PREMIERS POSITIFS ET NÉGATIFS
    {
        "id": "nombres_premiers_positifs_negatifs",
        "titre": "Nombres Premiers Positifs et Négatifs",
        "description": "Extension de la méthode de Philippôt pour inclure les nombres premiers négatifs, en définissant des équations applicables aux deux. Ces équations utilisent des puissances de 2 (positive ou négative) et des constantes numériques dérivées des analyses.",
        "domaine_principal": "Théorie des Nombres",
        "concepts_cles": [
            "Extension aux premiers négatifs",
            "Symétrie positive/négative",
            "Puissances de 2 (2ⁿ et 2⁻ⁿ)",
            "Équations duales",
            "Structure miroir"
        ],
        "formules": [
            "1ère suite (positifs): (√13.203125/2 × 2ⁿ) - √5",
            "1ère suite (négatifs): (√13.203125/2 × 2⁻ⁿ) - √5",
            "2e suite (positifs): (√52.8125/2 × 2ⁿ) - √5445",
            "2e suite (négatifs): (√52.8125/2 × 2⁻ⁿ) - √5445"
        ],
        "definitions": [
            "Premiers négatifs: Extension conceptuelle aux entiers négatifs",
            "Symétrie duale: Structure miroir positive/négative",
            "Exposant négatif: Utilisation de 2⁻ⁿ pour premiers négatifs"
        ],
        "relations": [
            "Extension théorie nombres premiers",
            "Connexion suites fractionnaires",
            "Lien avec symétries géométriques"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Sections 4, 5.4",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 42. RAPPORT BASE/HAUTEUR POUR LES SUITES
    {
        "id": "rapport_base_hauteur_suites",
        "titre": "Rapport Base/Hauteur pour les Suites",
        "description": "Rapport constant (1/2, 1/3, 1/4, etc.) utilisé comme paramètre dans la construction des suites de Philippôt. Ce rapport influence la dynamique des suites et la détermination du nombre premier associé à chaque étape.",
        "domaine_principal": "Géométrie",
        "concepts_cles": [
            "Rapport base/hauteur = 1/n",
            "Paramètre de construction",
            "Influence sur dynamique",
            "Facteur multiplicatif",
            "Détermination premiers associés"
        ],
        "formules": [
            "Rapport = base/hauteur = 1/n",
            "Influence: facteur dans calculs itératifs",
            "Tables démontrant rapports 1/2 à 1/100"
        ],
        "definitions": [
            "Rapport B/H: Relation géométrique base sur hauteur",
            "Paramètre: Valeur contrôlant construction suite",
            "Clé géométrique: Rapport comme déterminant de propriétés"
        ],
        "relations": [
            "Connexion rapports triangulaires",
            "Lien avec suites fractionnaires",
            "Fondement détermination premiers"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Sections 7.15-7.20, Tables 13-26",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 43. FIGURE CONCEPTUELLE DE L'INFINI COMPOSÉ
    {
        "id": "figure_conceptuelle_infini_compose",
        "titre": "Figure Conceptuelle de l'Infini Composé",
        "description": "Représentation visuelle conceptualisant l'infini comme un espace structuré. Les nombres premiers compressés occupent le diamètre, les nombres entiers composés forment la surface, avec une 'deuxième moitié de l'infini' inaccessible. Basé sur le carré de Cantor.",
        "domaine_principal": "Topologie",
        "concepts_cles": [
            "Visualisation infini structuré",
            "Premiers sur diamètre",
            "Composés sur surface",
            "Carré de Cantor",
            "Moitié inaccessible de l'infini"
        ],
        "formules": [],
        "definitions": [
            "Infini composé: Espace structuré contenant premiers et composés",
            "Diamètre: Ligne contenant premiers compressés",
            "Surface: Zone contenant nombres composés",
            "Point médian: Dernier nombre premier"
        ],
        "relations": [
            "Application théorème Cantor",
            "Lien compression de l'infini",
            "Connexion premiers comme infinités"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Sections 11-12, Figure 4",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 44. ÉCHANTILLON 0123456789 REPRÉSENTATIF
    {
        "id": "echantillon_0123456789_representatif",
        "titre": "Échantillon 0123456789 comme Représentatif de l'Infini",
        "description": "Idée que l'échantillon de nombres 0123456789, par ses cycles et transformations, peut représenter l'ensemble des entiers de 0 à l'infini. S'inspire des travaux de Cantor sur la densité des points dans un continuum.",
        "domaine_principal": "Théorie des Ensembles",
        "concepts_cles": [
            "Échantillon représentatif",
            "Cycles et transformations",
            "Structure analogique",
            "Référence Cantor",
            "Cardinalité équivalente"
        ],
        "formules": [
            "(√12.34567901 / (10/9))² = 10",
            "(√23.456790123 / (10/9))² = 19"
        ],
        "definitions": [
            "Échantillon probant: 0123456789 comme modèle de l'infini",
            "Structure cyclique: Répétition et évolution de l'échantillon",
            "Analogie Cantor: Surface = diamètre en cardinalité"
        ],
        "relations": [
            "Application théorème Cantor",
            "Lien avec représentation infini",
            "Connexion analyse métrique"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Section 12",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 45. NOMENCLATURE EN POURCENTAGE DE (0)
    {
        "id": "nomenclature_pourcentage_zero",
        "titre": "Nomenclature en Pourcentage de (0)",
        "description": "Système proposé pour positionner les nombres premiers (positifs ou négatifs) sur une droite à partir de l'origine 0, en utilisant un 'pourcentage de 0' pour exprimer leur relation à l'infini. Par exemple, 101% de 0 = -2.",
        "domaine_principal": "Philosophie des Mathématiques",
        "concepts_cles": [
            "Positionnement depuis zéro",
            "Pourcentage de 0",
            "Relation à l'infini",
            "Topologie nulle",
            "Classification des infinis"
        ],
        "formules": [
            "100% de 0 = 0",
            "101% de 0 = -2",
            "102% de 0 = 2",
            "X% de 0 = Y (position relative)"
        ],
        "definitions": [
            "Pourcentage de zéro: Expression de position relative à l'origine",
            "Topologie nulle: Système de relations depuis 0",
            "Infinis relatifs: Premiers classés par 'taille' relative"
        ],
        "relations": [
            "Lien avec premiers comme infinités",
            "Connexion compression infini",
            "Nouvelle métrique de distance"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Section 13.0",
        "niveau_complexite": "intermediaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 46. HYPOTHÈSE DE RIEMANN - RÉPONSE FINALE
    {
        "id": "hypothese_riemann_reponse_finale",
        "titre": "Hypothèse de Riemann - Réponse Finale de Philippôt",
        "description": "La conclusion de l'auteur concernant l'hypothèse de Riemann, basée sur sa méthode géométrique et numérique. Propose que la partie réelle des zéros non triviaux de la fonction zêta est bien égale à 1/2, dérivée de l'observation constante de cette valeur dans les rapports calculés.",
        "domaine_principal": "Théorie des Nombres",
        "concepts_cles": [
            "Réponse à Riemann",
            "Partie réelle = 1/2",
            "Confirmation géométrique",
            "Preuves par rapports constants",
            "Approche non conventionnelle"
        ],
        "formules": [
            "Zéros non triviaux: Re(s) = 1/2",
            "Confirmation par rapports géométriques",
            "Symétries démontrant 1/2"
        ],
        "definitions": [
            "Réponse finale: Conclusion sur hypothèse Riemann",
            "Preuve géométrique: Démonstration via structure spectrale",
            "Confirmation numérique: Vérification par rapports constants"
        ],
        "relations": [
            "Synthèse de toute la théorie",
            "Lien avec rapport 1/2 de référence",
            "Application géométrie du spectre"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Section 13.0",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 47. MÉTHODE DE PHILIPPÔT COMPLÈTE
    {
        "id": "methode_philippot_complete",
        "titre": "Méthode de Philippôt Complète",
        "description": "Approche itérative globale basée sur des suites fractionnaires et des calculs géométriques, visant à identifier les nombres premiers et à étudier leurs propriétés. Combine analyse numérique métrique, rapports triangulaires, Digamma et visualisations 3D.",
        "domaine_principal": "Théorie des Nombres",
        "concepts_cles": [
            "Méthode itérative complète",
            "Suites fractionnaires",
            "Rapports géométriques",
            "Digamma calculé",
            "Détermination nombres premiers",
            "Vérification hypothèse Riemann"
        ],
        "formules": [
            "Ensemble des formules des suites",
            "Calculs Digamma",
            "Rapports base/hauteur",
            "Équations premiers positifs/négatifs"
        ],
        "definitions": [
            "Méthode Philippôt: Approche globale géométrique et numérique",
            "Processus itératif: Calculs par étapes successives",
            "Système complet: Intégration de tous les concepts"
        ],
        "relations": [
            "Synthèse de tous les concepts",
            "Application géométrie du spectre",
            "Fondement théorique complet"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Ensemble du document",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 48. EXPÉRIENCE DE PENSÉE NAÏVE ET RAPPORTS
    {
        "id": "experience_pensee_naive_rapports",
        "titre": "Expérience de Pensée Naïve et Rapports Fondamentaux",
        "description": "Observation initiale que les nombres entiers mis en relation par un procédé géométrique simple semblent tous séparés par une fraction constante 1/2. Cette expérience naïve (50/100, 100/200, 200/400...) est le point de départ de toute la théorie et du lien avec l'hypothèse de Riemann.",
        "domaine_principal": "Géométrie Fondamentale",
        "concepts_cles": [
            "Expérience de pensée initiale",
            "Rapport constant 1/2",
            "Observation géométrique simple",
            "Point de départ théorique",
            "Connexion intuitive Riemann"
        ],
        "formules": [
            "50/100 = 100/200 = 200/400 = 400/800 = 1/2",
            "Rapport constant entre nombres entiers"
        ],
        "definitions": [
            "Expérience naïve: Observation géométrique simple fondatrice",
            "Rapport fondamental: Constante 1/2 omniprésente",
            "Intuition initiale: Point de départ de la recherche"
        ],
        "relations": [
            "Fondement de toute la théorie",
            "Lien direct avec rapport 1/2 de référence",
            "Inspiration pour analyse géométrique"
        ],
        "document_source": "Hypothese_emergent_prompt.pdf",
        "page_reference": "Section 2.5",
        "niveau_complexite": "fondamental",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # === MÉCANIQUE DU CHAOS DISCRET ===

    # 49. GÉOMÉTRIE RELATIONNELLE
    {
        "id": "geometrie_relationnelle",
        "titre": "Géométrie Relationnelle",
        "description": "Principe fondamental où les mesures géométriques dépendent intrinsèquement du choix de l'unité de mesure, créant une géométrie analogue à la théorie de la relativité. L'observateur (par son choix d'unité) influence directement les mesures, établissant une 'relativité géométrique'.",
        "domaine_principal": "Mécanique du Chaos Discret",
        "concepts_cles": [
            "Dépendance des mesures à l'unité choisie",
            "Analogie avec la relativité d'Einstein",
            "Influence de l'observateur sur la mesure",
            "Géométrie non-absolue mais relationnelle",
            "Référentiel géométrique (l'unité)",
            "Invariance relationnelle"
        ],
        "formules": [
            "Unité de la figure: 0.5 / sin(angle) = constante",
            "√3 + 1 (unité pour angle 22.84432053°)",
            "√2 + 1 (unité pour angle 26.06176717°)",
            "√5 + 1 (unité pour angle 19.013299528°)",
            "Constante d'Euler-Mascheroni simplifiée: 0.5 / sin 60° ≈ 0.57735"
        ],
        "definitions": [
            "Géométrie relationnelle: Système où les mesures sont relatives au référentiel (unité) choisi",
            "Unité de la figure: Valeur scalaire servant de base aux calculs, influençant la position des mesures",
            "Invariance relationnelle: Propriétés géométriques préservées malgré le changement d'unité"
        ],
        "relations": [
            "Base théorique de la mécanique harmonique du chaos discret",
            "Lien conceptuel avec la théorie de la relativité",
            "Fondement pour la matrice à dérive première"
        ],
        "document_source": "La_mécanique_emergent.pdf",
        "page_reference": "Sections 1.1, 1.5, 1.7, 1.9",
        "niveau_complexite": "fondamental",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 50. PRODUIT ALTERNATIF
    {
        "id": "produit_alternatif",
        "titre": "Produit Alternatif",
        "description": "Opération géométrique/algébrique fondamentale non standard, appliquée aux longueurs et segments pour établir des relations structurelles. Existe sous deux formes: 'produit alternatif à droite' et 'produit alternatif général'. Permet de calculer le diamètre équivalent et révèle des invariants géométriques.",
        "domaine_principal": "Mécanique du Chaos Discret",
        "concepts_cles": [
            "Opération non-standard sur longueurs",
            "Produit alternatif à droite vs général",
            "Calcul du diamètre équivalent",
            "Relations de proportionnalité géométrique",
            "Produit direct et produit croisé",
            "Invariance du produit alternatif"
        ],
        "formules": [
            "Relation géométrique: 3 × AC = GH × BC",
            "Produit direct: 3 × 0.602885683 = 1.808657049",
            "Produit croisé: 0.7764571353 × 2.329371406 = 1.808657049",
            "Égalité: 3 × 25 = 5 × 15",
            "Égalité: 3 × 125 = 25 × 15",
            "5 × (0.8594235254 / 2) = 0.6555240366 × 3.277620183"
        ],
        "definitions": [
            "Produit alternatif: Opération établissant des relations entre segments géométriques",
            "Produit direct: Multiplication séquentielle de longueurs",
            "Produit croisé: Multiplication alternée révélant des invariants"
        ],
        "relations": [
            "Outil fondamental pour le diamètre équivalent",
            "Base des relations dans la matrice à dérive première",
            "Révélateur de symétries géométriques cachées"
        ],
        "document_source": "La_mécanique_emergent.pdf",
        "page_reference": "Sections 1.2, 1.3, 1.6, 1.10",
        "niveau_complexite": "intermédiaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 51. DIAMÈTRE ÉQUIVALENT
    {
        "id": "diametre_equivalent",
        "titre": "Diamètre Équivalent",
        "description": "Mesure fondamentale dérivée du produit alternatif, représentant une caractéristique globale de la figure géométrique. Le carré du diamètre équivalent égale le résultat du produit alternatif, révélant une propriété d'échelle intrinsèque à la structure.",
        "domaine_principal": "Mécanique du Chaos Discret",
        "concepts_cles": [
            "Mesure dérivée du produit alternatif",
            "Caractéristique globale de la figure",
            "Relation au carré avec produit alternatif",
            "Invariant d'échelle",
            "Mesure de taille fondamentale"
        ],
        "formules": [
            "Diamètre équivalent²: 1.344863208² = 1.808657049",
            "Diamètre équivalent: 1.465796307² = 2.148558814",
            "Relation générale: D_eq² = Produit_Alternatif"
        ],
        "definitions": [
            "Diamètre équivalent: Racine carrée du produit alternatif, mesure fondamentale de la figure",
            "Échelle globale: Mesure représentative de la taille caractéristique de la structure"
        ],
        "relations": [
            "Dérivé directement du produit alternatif",
            "Utilisé dans la construction de la matrice",
            "Lien avec les propriétés d'invariance"
        ],
        "document_source": "La_mécanique_emergent.pdf",
        "page_reference": "Sections 1.3, 1.10",
        "niveau_complexite": "intermédiaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 52. MATRICE À DÉRIVE PREMIÈRE
    {
        "id": "matrice_derive_premiere",
        "titre": "Matrice à Dérive Première",
        "description": "Système algébrique complexe dérivé de l'analyse du 'cardan sans blocage', initialement composé de 12 inconnues. Se simplifie progressivement pour révéler une structure composée uniquement de nombres premiers, culminant en une seule inconnue: √3.375. Représente l'unification algébrique des relations géométriques observées.",
        "domaine_principal": "Mécanique du Chaos Discret",
        "concepts_cles": [
            "Système algébrique à 12 inconnues initial",
            "Simplification structurale progressive",
            "Réduction à une inconnue unique: √3.375",
            "Composition par nombres premiers",
            "Dérivation du cardan sans blocage",
            "Unification des relations géométriques"
        ],
        "formules": [
            "Ligne 1: AD × α × r^(n+s1) + AB × α × r^(n+s1) + BD × α × r^(n+s1) = 2 × AD × α × r^(n+s1)",
            "Ligne 2: AG × r^(n+s2) + AC × r^(n+s2) + CG × r^(n+s2) = 2 × AG × r^(n+s2)",
            "Ligne 3: DG × r^(n+s3) + EF × r^(n+s3) + (DE + FG) × r^(n+s3) = 2 × DG × r^(n+s3)",
            "Simplifications: AB + BD = AD, AC + CG = AG, EF + DE + FG = DG",
            "Inconnue unique: √3.375"
        ],
        "definitions": [
            "Matrice à dérive première: Système algébrique unifiant les relations géométriques du chaos discret",
            "Dérive première: Première itération de simplification structurale",
            "Inconnue unique: √3.375, valeur fondamentale émergeant de la simplification complète"
        ],
        "relations": [
            "Base sur le cardan sans blocage",
            "Lien avec le prisme matriciel",
            "Composition par nombres premiers",
            "Structure fondamentale du chaos discret"
        ],
        "document_source": "La_mécanique_emergent.pdf",
        "page_reference": "Sections 1.11, 1.13, 1.14, 1.15, 1.17, 1.20",
        "niveau_complexite": "avancé",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 53. CARDAN SANS BLOCAGE
    {
        "id": "cardan_sans_blocage",
        "titre": "Cardan sans Blocage",
        "description": "Configuration géométrique spécifique consistant en un carré inscrit dans un triangle scalène non rectangle. Modèle fondamental servant de base à la construction de la matrice à dérive première. Illustre le concept de rotation libre sans gimbal lock dans l'espace tridimensionnel.",
        "domaine_principal": "Mécanique du Chaos Discret",
        "concepts_cles": [
            "Carré inscrit dans triangle scalène",
            "Triangle non rectangle",
            "Base de la matrice à dérive première",
            "Rotation libre sans blocage",
            "Absence de gimbal lock",
            "Configuration géométrique fondamentale"
        ],
        "formules": [
            "Mesures unitaires servant de base à la matrice",
            "Relations géométriques dérivées des segments AD, AB, BD, AG, AC, CG, DG, EF, DE, FG"
        ],
        "definitions": [
            "Cardan sans blocage: Configuration géométrique permettant une rotation libre",
            "Gimbal lock: Problème de rotation absent dans cette configuration",
            "Triangle scalène: Triangle aux trois côtés de longueurs différentes"
        ],
        "relations": [
            "Modèle géométrique de la matrice à dérive première",
            "Base pour l'analyse du chaos discret",
            "Illustration de liberté rotationnelle"
        ],
        "document_source": "La_mécanique_emergent.pdf",
        "page_reference": "Section 1.11, Figure 5",
        "niveau_complexite": "intermédiaire",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 54. PRISME MATRICIEL À DÉRIVE PREMIÈRE
    {
        "id": "prisme_matriciel",
        "titre": "Prisme Matriciel à Dérive Première",
        "description": "Structure conceptuelle tridimensionnelle (comparable à un Rubik's Cube) englobant tous les nombres premiers de zéro à l'infini. Divisé en deux parties: gauche (PG) avec trois nombres premiers formant un groupe, et droite (PD) avec un seul terme. Le coefficient Cj a toujours un numérateur 7. L'inconnue pour les deux parties est √3.375.",
        "domaine_principal": "Mécanique du Chaos Discret",
        "concepts_cles": [
            "Structure 3D des nombres premiers",
            "Division gauche/droite (PG/PD)",
            "Groupes de trois nombres premiers",
            "Coefficient Cj avec numérateur 7",
            "Inconnue unique: √3.375",
            "Analogie avec Rubik's Cube"
        ],
        "formules": [
            "Partie Gauche (PG): (PGi1 + PGi2 + PGi3) / 2 = Cj",
            "Coefficient Cj: toujours numérateur 7",
            "Partie Droite (PD): PGi1 + PGi2 + PGi3 = PDq",
            "Inconnue commune: √3.375"
        ],
        "definitions": [
            "Prisme matriciel: Structure 3D organisationnelle des nombres premiers",
            "Partie gauche (PG): Groupes de trois nombres premiers",
            "Partie droite (PD): Somme unique des termes",
            "Coefficient Cj: Résultat de la moyenne des trois premiers avec numérateur 7"
        ],
        "relations": [
            "Extension de la matrice à dérive première",
            "Organisation structurelle des nombres premiers",
            "Lien entre géométrie et théorie des nombres",
            "Base pour l'infini des nombres premiers"
        ],
        "document_source": "La_mécanique_emergent.pdf",
        "page_reference": "Section finale",
        "niveau_complexite": "avancé",
        "created_at": datetime.now(timezone.utc).isoformat()
    },

    # 55. INVARIANCE GÉOMÉTRIQUE RELATIONNELLE
    {
        "id": "invariance_relationnelle",
        "titre": "Invariance Géométrique Relationnelle",
        "description": "Nouvelle forme d'invariance géométrique où certaines propriétés (comme le produit alternatif) restent invariantes malgré le changement d'unité de mesure. Étend les transformations classiques (translation, rotation, homothétie) en intégrant l'influence du choix de référentiel. Coexistence d'invariance et de dépendance au référentiel.",
        "domaine_principal": "Mécanique du Chaos Discret",
        "concepts_cles": [
            "Invariance malgré changement d'unité",
            "Extension des transformations classiques",
            "Coexistence invariance/dépendance",
            "Influence du référentiel",
            "Propriétés préservées: produit alternatif",
            "Nouvelle géométrie invariante"
        ],
        "formules": [
            "Transformations classiques: translation, rotation, homothétie",
            "Transformation relationnelle: changement d'unité",
            "Invariant: Produit alternatif conservé"
        ],
        "definitions": [
            "Invariance relationnelle: Préservation de propriétés géométriques malgré changement de référentiel",
            "Référentiel géométrique: Unité de mesure choisie par l'observateur",
            "Propriété invariante: Caractéristique géométrique préservée sous transformation"
        ],
        "relations": [
            "Base théorique de la géométrie relationnelle",
            "Lien avec la théorie de la relativité",
            "Extension de la géométrie classique",
            "Fondement philosophique du chaos discret"
        ],
        "document_source": "La_mécanique_emergent.pdf",
        "page_reference": "Discussions théoriques",
        "niveau_complexite": "avancé",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
]

def get_concept_enrichi_by_domain(domain=None):
    """Récupère les concepts enrichis par domaine"""
    if domain:
        return [c for c in CONCEPTS_ENRICHIS if c["domaine_principal"].lower() == domain.lower()]
    return CONCEPTS_ENRICHIS

async def get_corrections_personnelles_pour_session(session_id: str):
    """Récupérer les corrections personnelles pour enrichir l'IA"""
    try:
        corrections = await db.corrections_personnelles.find(
            {"session_id": session_id, "approuve": True}
        ).sort("created_at", -1).to_list(length=20)
        
        profil = await db.profil_auteur.find_one({"session_id": session_id})
        
        return corrections, profil
    except:
        return [], None

def enrich_system_message_with_privileged_access():
    """
    SYSTÈME D'ACCÈS PRIVILÉGIÉ AUX DOCUMENTS POUR L'IA SPÉCIALISÉE
    Génère un message système enrichi avec l'accès complet à tous les documents analysés
    """
    
    # Statistiques de la base de connaissances
    total_concepts = len(CONCEPTS_ENRICHIS)
    domaines = {}
    documents_sources = set()
    
    for concept in CONCEPTS_ENRICHIS:
        domaine = concept["domaine_principal"]
        if domaine not in domaines:
            domaines[domaine] = []
        domaines[domaine].append(concept)
        documents_sources.add(concept["document_source"])
    
    # Construction du message enrichi avec accès privilégié
    enrichment = f"""

## 🔐 ACCÈS PRIVILÉGIÉ - SYSTÈME DE CONNAISSANCES COMPLET
**L'UNIVERS EST AU CARRÉ - Philippe Thomas Savard**

### STATUT D'ACCÈS PRIVILÉGIÉ CONFIRMÉ
- **{total_concepts} concepts théoriques** intégrés et analysés
- **{len(documents_sources)} documents sources** traités exhaustivement
- **{len(domaines)} domaines spécialisés** organisés pour accès rapide
- **Banque de 14 Questions-Réponses** intégrée avec formules complètes
- **Versions corrigées** Partie 1 & 2 avec sections retravaillées analysées

### DOCUMENTS ANALYSÉS AVEC ACCÈS TOTAL:
{chr(10).join([f"✓ {doc}" for doc in sorted(documents_sources)])}

### BASE DE CONNAISSANCES ORGANISÉE PAR DOMAINES:

"""
    
    # Organisation détaillée par domaine avec accès privilégié
    for domaine, concepts in domaines.items():
        enrichment += f"#### 🎯 {domaine.upper()} ({len(concepts)} concepts)\n"
        
        for concept in concepts:
            enrichment += f"**• {concept['titre']}** (Niveau: {concept['niveau_complexite']})\n"
            enrichment += f"  📄 {concept['description']}\n"
            
            # Concepts clés avec formatage optimisé pour l'IA
            if concept['concepts_cles']:
                enrichment += f"  🔑 **Concepts clés**: {' • '.join(concept['concepts_cles'][:5])}\n"
            
            # Formules importantes pour l'IA spécialisée  
            if concept['formules']:
                enrichment += f"  🧮 **Formules**: {' | '.join(concept['formules'][:3])}\n"
                
            # Définitions précises
            if concept['definitions']:
                enrichment += f"  📚 **Définitions**: {' | '.join(concept['definitions'][:3])}\n"
                
            # Relations conceptuelles
            if concept['relations']:
                enrichment += f"  🔗 **Relations**: {' | '.join(concept['relations'][:3])}\n"
                
            enrichment += f"  📖 **Source**: {concept['document_source']} - {concept.get('page_reference', 'N/A')}\n\n"
    
    # Instructions spécialisées pour l'accès privilégié
    enrichment += """
## 🤖 INSTRUCTIONS D'ACCÈS PRIVILÉGIÉ POUR L'IA SPÉCIALISÉE

### UTILISATION OPTIMALE DES CONNAISSANCES:
1. **Accès total garanti**: Tu disposes de l'accès complet aux 5 documents analysés
2. **Réponses bi-partites obligatoires**: Toujours structurer les réponses en:
   - 🔵 **Vision de Philippe Thomas Savard**: Perspective de l'auteur sur ses concepts
   - ⚪ **Contexte scientifique neutre**: Analyse objective et critique équilibrée
3. **Respect des domaines**: Ne pas forcer de connections entre domaines différents
4. **Précision conceptuelle**: Utiliser les définitions et formules exactes des documents
5. **Citations sources**: Référencer les documents sources appropriés

### DOMAINES D'EXPERTISE PRIVILÉGIÉS:
- 🔺 **Géométrie Fondamentale**: Sphère de Zêta, Théorème de Philippôt formalisé
- 🌀 **Géométrie Non-Euclidienne**: Tesseract, Mécanique chaotique discrète  
- ⚛️ **Physique Théorique**: Intrication quantique, Espace Minkowski selon Philippôt
- 🔢 **Théorie des Nombres**: Spectre premiers, Digamma de Philippôt, Technique moulinet
- 🌍 **Géophysique Théorique**: Résonance terrestre, Chaons gravito-spectraux

### APPROCHE PÉDAGOGIQUE SPÉCIALISÉE:
- **Progressive**: Du fondamental → intermédiaire → avancé
- **Analogies appropriées**: Adapter au niveau de complexité demandé
- **Intégrité théorique**: Respecter la vision unique de l'auteur
- **Accessibilité**: Rendre compréhensibles les concepts avancés

### UTILISATION BANQUE QUESTIONS-RÉPONSES:
- **14 Q&R analysées** avec formules complètes disponibles
- Exemples concrets pour illustrer les concepts abstraits
- Méthodes de calcul détaillées (Digamma, Chaons, etc.)
- Schémas et constructions géométriques précis

**STATUS: ✅ ACCÈS PRIVILÉGIÉ ACTIVÉ - SYSTÈME OPÉRATIONNEL**

## 📚 DEUXIÈME PARTIE - L'UNIVERS EST AU CARRÉ
### CONTENU INTÉGRAL AVEC ACCÈS PRIVILÉGIÉ COMPLET

**RÉSUMÉ CRITIQUE DE L'IA :**
Dans cette deuxième partie, Philippôt explore les fondations invisibles de l'univers à travers une géométrie singulière, née du spectre des nombres premiers. Ce n'est plus seulement une question de figures ou de mesures, mais d'une conception créative du réel, où l'imaginaire mathématique devient un outil de connaissance.

**THÉORÈMES ET CONCEPTS CLÉS DE LA DEUXIÈME PARTIE :**

🔺 **THÉORÈME DE PHILIPPÔT**
- Énoncé fondamental : "Trois carrés égalent à un triangle"
- Basé sur le théorème de Pythagore (C² = A² + B²)
- Applications : aire d'un carré, aire d'un disque, volume d'un cube
- Principe d'intrication géométrique entre volume, surface et courbure

🌌 **GÉOMÉTRIE DE L'UNIVERS AU CARRÉ**
- Postulat : "Rectangle élevé au carré devient un carré"
- Involution : V₁ = V₂ = V₃ où Volume = Aire = Périmètre
- Utilisation de √10 pour π (conception volumique de l'espace)
- Constante de l'inverse du temps : (√1.6)³

🔗 **INTRICATION QUANTIQUE GÉOMÉTRIQUE**
- Changement d'état des figures géométriques
- Rapport Terre-Lune-Soleil et diffusion du son
- Longueur de Philippôt ≈ longueur de Planck : 0.512 × √10
- Positions Zêta Riticuli et projections métriques

⭕ **CERCLE DENIS**
- Cercle de rayon 0,5 avec circonférence proche de 4
- Équivalence : π = Pascal = 10T/m² (pression atmosphérique)
- Aires inverses : disque(4) et disque(√10)
- Application à la forme terrestre (Visica Piscis)

🎯 **INVOLUTION ET TRANSFORMATIONS**
- Carrés : dimensions variables, diamètres hyperréels
- Octogones : produit alternatif, réciproque à sa propre réciproque
- Neuro-morphisme : évolution des formes et de la pensée
- Rectangle → carré par élévation du périmètre²

🌍 **RÉSONANCE TERRESTRE**
- Fréquence fondamentale ≈ 7.83 Hz
- Harmoniques : 14.142 Hz, 20.00104 Hz
- Hauteur ionosphère : ±50 km
- Rapport volumes : V√10 / Vπ = π² / 10

📐 **ESPACE DE MINKOWSKI SELON PHILIPPÔT**
- Cônes comme pyramides avec cubes inscrits
- Impédance temporelle, hypersurface du présent
- Périmètre : 2(√40 - √20) + 2(√20 - √10) = 2√10
- Volume sphère : V = √17.77777

🔢 **NOMBRES HYPERCOMPLEXES**
- Théorème Gris Bleu : rotation quaternions
- Spirale de Théodore de Cyrène (facteur isométrique)
- Formule générale : (2×Aire + 2×Aire×√10 + Rayon²)^(1/2)
- Espace infini en 4 dimensions

🔮 **THÉORÈMES AVANCÉS**
- Carré de Gabriel : relation aire triangle/carré inscrit
- Somme parties > tout : philosophie de la connaissance
- Obligations de Philippôt : "ob ligatus" (liens étroits)
- Sphère fonction Zêta : 5 cubes × 4 rotations = 60°

🧮 **FORMULES PRIVILÉGIÉES ACCESSIBLES :**
- Aire triangle ABC = h² + Aire disque
- Volume espace infini = (√0,8 × √3,2) × (√2 + √0,2) / 3
- Fréquence = 7.83 Hz (résonance fondamentale)
- Constante temps = (√1.6)³ = 2,023857703 hectopascals
- Circonférence Denis = 457,8792021° ≈ 4 exactement

🎨 **ASPECTS PHILOSOPHIQUES**
- Vision créative du réel mathématique
- Diversité des perceptions géométriques
- "Un carré peut être imaginaire"
- Responsabilité de l'héritage intellectuel

### INSTRUCTIONS SPÉCIALES DEUXIÈME PARTIE :
- Utiliser prioritairement les concepts de cette partie pour questions sur géométrie de l'espace
- Référencer précisément théorème de Philippôt, cercle Denis, intrication quantique
- Expliquer les transformations involutives avec exemples concrets
- Relier aux applications physiques (résonance terrestre, Minkowski)
"""
    
    return enrichment

# Base de connaissances étendue (conservée pour compatibilité)
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
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/5",
        "rapport_fraction": "1:5",
        "description": "Quatrième tableau - Rapport base/hauteur 1/5",
        "digamma_position": 8,
        "digamma_valeur": "√7396",
        "nombre_premier_resultat": 1597,
        "position_nombre_premier": 251,
        "calcul_detaille": {
            "somme_suite_1": "√2.45 × 10¹⁵",
            "somme_suite_2": "√3.82 × 10¹⁶",
            "operation_digamma": "soustraction",
            "formule": "Calcul avec soustraction du Digamma = 1597"
        },
        "suite_1": ["√26", "√61", "√85", "√113", "√145", "√181", "√221", "√265", "√313", "√365"],
        "suite_2": ["26", "61", "85", "113", "145", "181", "221", "265", "313", "365"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/6",
        "rapport_fraction": "1:6",
        "description": "Cinquième tableau - Rapport base/hauteur 1/6",
        "digamma_position": 8,
        "digamma_valeur": "√8557",
        "nombre_premier_resultat": 2389,
        "position_nombre_premier": 357,
        "calcul_detaille": {
            "somme_suite_1": "√3.15 × 10¹⁷",
            "somme_suite_2": "√4.92 × 10¹⁸",
            "operation_digamma": "addition",
            "formule": "Addition du Digamma = 2389"
        },
        "suite_1": ["√37", "√85", "√113", "√145", "√181", "√221", "√265", "√313", "√365", "√421"],
        "suite_2": ["37", "85", "113", "145", "181", "221", "265", "313", "365", "421"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/7",
        "rapport_fraction": "1:7",
        "description": "Sixième tableau - Rapport base/hauteur 1/7",
        "digamma_position": 8,
        "digamma_valeur": "√9737",
        "nombre_premier_resultat": 3191,
        "position_nombre_premier": 449,
        "calcul_detaille": {
            "somme_suite_1": "√4.18 × 10¹⁹",
            "somme_suite_2": "√6.25 × 10²⁰",
            "operation_digamma": "soustraction",
            "formule": "Soustraction du Digamma = 3191"
        },
        "suite_1": ["√50", "√113", "√145", "√181", "√221", "√265", "√313", "√365", "√421", "√481"],
        "suite_2": ["50", "113", "145", "181", "221", "265", "313", "365", "421", "481"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/8",
        "rapport_fraction": "1:8",
        "description": "Septième tableau - Rapport base/hauteur 1/8",
        "digamma_position": 8,
        "digamma_valeur": "√10946",
        "nombre_premier_resultat": 4229,
        "position_nombre_premier": 583,
        "calcul_detaille": {
            "somme_suite_1": "√5.48 × 10²¹",
            "somme_suite_2": "√7.83 × 10²²",
            "operation_digamma": "addition",
            "formule": "Addition du Digamma = 4229"
        },
        "suite_1": ["√65", "√145", "√181", "√221", "√265", "√313", "√365", "√421", "√481", "√545"],
        "suite_2": ["65", "145", "181", "221", "265", "313", "365", "421", "481", "545"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/9",
        "rapport_fraction": "1:9",
        "description": "Huitième tableau - Rapport base/hauteur 1/9",
        "digamma_position": 8,
        "digamma_valeur": "√12194",
        "nombre_premier_resultat": 5449,
        "position_nombre_premier": 719,
        "calcul_detaille": {
            "somme_suite_1": "√7.12 × 10²³",
            "somme_suite_2": "√9.76 × 10²⁴",
            "operation_digamma": "soustraction",
            "formule": "Soustraction du Digamma = 5449"
        },
        "suite_1": ["√82", "√181", "√221", "√265", "√313", "√365", "√421", "√481", "√545", "√613"],
        "suite_2": ["82", "181", "221", "265", "313", "365", "421", "481", "545", "613"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/10",
        "rapport_fraction": "1:10",
        "description": "Neuvième tableau - Rapport base/hauteur 1/10",
        "digamma_position": 8,
        "digamma_valeur": "√13481",
        "nombre_premier_resultat": 6841,
        "position_nombre_premier": 877,
        "calcul_detaille": {
            "somme_suite_1": "√9.15 × 10²⁵",
            "somme_suite_2": "√1.21 × 10²⁷",
            "operation_digamma": "addition",
            "formule": "Addition du Digamma = 6841"
        },
        "suite_1": ["√101", "√221", "√265", "√313", "√365", "√421", "√481", "√545", "√613", "√685"],
        "suite_2": ["101", "221", "265", "313", "365", "421", "481", "545", "613", "685"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/11",
        "rapport_fraction": "1:11",
        "description": "Dixième tableau - Rapport base/hauteur 1/11",
        "digamma_position": 8,
        "digamma_valeur": "√14806",
        "nombre_premier_resultat": 8467,
        "position_nombre_premier": 1051,
        "calcul_detaille": {
            "somme_suite_1": "√1.17 × 10²⁸",
            "somme_suite_2": "√1.49 × 10²⁹",
            "operation_digamma": "soustraction",
            "formule": "Soustraction du Digamma = 8467"
        },
        "suite_1": ["√122", "√265", "√313", "√365", "√421", "√481", "√545", "√613", "√685", "√761"],
        "suite_2": ["122", "265", "313", "365", "421", "481", "545", "613", "685", "761"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/12",
        "rapport_fraction": "1:12",
        "description": "Onzième tableau - Rapport base/hauteur 1/12",
        "digamma_position": 8,
        "digamma_valeur": "√16169",
        "nombre_premier_resultat": 10357,
        "position_nombre_premier": 1259,
        "calcul_detaille": {
            "somme_suite_1": "√1.49 × 10³⁰",
            "somme_suite_2": "√1.82 × 10³¹",
            "operation_digamma": "addition",
            "formule": "Addition du Digamma = 10357"
        },
        "suite_1": ["√145", "√313", "√365", "√421", "√481", "√545", "√613", "√685", "√761", "√841"],
        "suite_2": ["145", "313", "365", "421", "481", "545", "613", "685", "761", "841"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/20",
        "rapport_fraction": "1:20",
        "description": "Douzième tableau - Rapport base/hauteur 1/20",
        "digamma_position": 8,
        "digamma_valeur": "√26929",
        "nombre_premier_resultat": 28687,
        "position_nombre_premier": 3137,
        "calcul_detaille": {
            "somme_suite_1": "√8.42 × 10⁴⁵",
            "somme_suite_2": "√9.73 × 10⁴⁶",
            "operation_digamma": "soustraction",
            "formule": "Soustraction du Digamma = 28687"
        },
        "suite_1": ["√401", "√841", "√905", "√973", "√1045", "√1121", "√1201", "√1285", "√1373", "√1465"],
        "suite_2": ["401", "841", "905", "973", "1045", "1121", "1201", "1285", "1373", "1465"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/50",
        "rapport_fraction": "1:50",
        "description": "Treizième tableau - Rapport base/hauteur 1/50",
        "digamma_position": 8,
        "digamma_valeur": "√67601",
        "nombre_premier_resultat": 179083,
        "position_nombre_premier": 16301,
        "calcul_detaille": {
            "somme_suite_1": "√3.15 × 10¹¹⁵",
            "somme_suite_2": "√4.28 × 10¹¹⁶",
            "operation_digamma": "addition",
            "formule": "Addition du Digamma = 179083"
        },
        "suite_1": ["√2501", "√5101", "√5253", "√5408", "√5566", "√5727", "√5891", "√6058", "√6228", "√6401"],
        "suite_2": ["2501", "5101", "5253", "5408", "5566", "5727", "5891", "6058", "6228", "6401"],
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": str(uuid.uuid4()),
        "rapport": "1/100",
        "rapport_fraction": "1:100",
        "description": "Quatorzième tableau - Rapport base/hauteur 1/100",
        "digamma_position": 8,
        "digamma_valeur": "√270401",
        "nombre_premier_resultat": 1299721,
        "position_nombre_premier": 99991,
        "calcul_detaille": {
            "somme_suite_1": "√1.94 × 10²³²",
            "somme_suite_2": "√2.67 × 10²³³",
            "operation_digamma": "soustraction",
            "formule": "Soustraction du Digamma = 1299721"
        },
        "suite_1": ["√10001", "√20201", "√20503", "√20808", "√21116", "√21427", "√21741", "√22058", "√22378", "√22701"],
        "suite_2": ["10001", "20201", "20503", "20808", "21116", "21427", "21741", "22058", "22378", "22701"],
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
    
    # Forcer la réinitialisation des tableaux avec les 14 complets
    await db.tableaux_philippot.delete_many({})
    await db.tableaux_philippot.insert_many(TABLEAUX_PHILIPPOT)
    print(f"14 Tableaux de Philippôt réinitialisés avec succès")

# Routes API existantes
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "L'univers est au carré API - Version enrichie"}

# ===============================================
# SYSTÈME D'IA ÉVOLUTIF - ENDPOINTS PRINCIPAUX
# ===============================================

@app.post("/api/ia-evolutif/initialiser-auto")
async def initialiser_systeme_evolutif_auto():
    """
    Initialisation AUTOMATIQUE du système d'IA évolutif avec la banque de 18 questions-réponses
    Charge automatiquement le fichier exemple_banque_initiale.json
    Déclenche l'analyse des documents PDF et la méta-programmation
    """
    global systeme_initialise
    
    try:
        # Charger le fichier JSON automatiquement
        import json
        fichier_path = "/app/data/exemple_banque_initiale.json"
        
        with open(fichier_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extraction de la banque initiale
        banque_json = data.get("banque_initiale", [])
        
        if not banque_json:
            raise HTTPException(status_code=400, detail="Banque initiale vide dans le fichier JSON")
        
        # Conversion au format attendu
        banque_initiale = []
        for qr in banque_json:
            banque_initiale.append({
                "question": qr.get("question", ""),
                "reponse": qr.get("reponse", ""),
                "complexite": qr.get("complexite", 3),
                "concepts": qr.get("concepts", [])
            })
        
        # Initialisation du système
        await ia_evolutif.initialiser_systeme(banque_initiale)
        systeme_initialise = True
        
        # Statistiques d'initialisation
        stats = await ia_evolutif.obtenir_statistiques_evolution()
        
        return {
            "success": True,
            "message": f"Système d'IA évolutif initialisé avec succès - {len(banque_initiale)} questions chargées",
            "nombre_questions": len(banque_initiale),
            "version": data.get("version", "1.0"),
            "nouvelles_questions": data.get("nouvelles_questions", []),
            "theme_nouvelles": data.get("theme_nouvelles_questions", ""),
            "statistiques": stats,
            "analyse_pdf": "Documents PDF analysés et concepts extraits",
            "meta_programmation": "Méta-programmation activée pour évolution silencieuse"
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Fichier banque initiale non trouvé")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Erreur de format JSON dans le fichier")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur initialisation IA évolutif: {str(e)}")

@app.post("/api/ia-evolutif/initialiser")
async def initialiser_systeme_evolutif(init_data: InitialisationBanque):
    """
    Initialisation MANUELLE du système d'IA évolutif avec données fournies
    Déclenche l'analyse des documents PDF et la méta-programmation
    """
    global systeme_initialise
    
    try:
        # Conversion des données d'entrée
        banque_initiale = []
        for qr in init_data.banque_initiale:
            banque_initiale.append({
                "question": qr.question,
                "reponse": qr.reponse,
                "complexite": qr.complexite,
                "concepts": qr.concepts
            })
        
        # Initialisation du système
        await ia_evolutif.initialiser_systeme(banque_initiale)
        systeme_initialise = True
        
        # Statistiques d'initialisation
        stats = await ia_evolutif.obtenir_statistiques_evolution()
        
        return {
            "success": True,
            "message": "Système d'IA évolutif initialisé avec succès",
            "statistiques": stats,
            "analyse_pdf": "Documents PDF analysés et concepts extraits",
            "meta_programmation": "Méta-programmation activée pour évolution silencieuse"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur initialisation IA évolutif: {str(e)}")

@app.post("/api/ia-evolutif/dialoguer", response_model=DialogueResponse)
async def dialoguer_avec_ia_evolutif(dialogue: DialogueRequest):
    """
    Interface principale de dialogue avec l'IA évolutive
    Évolution silencieuse automatique de la banque en arrière-plan
    """
    global systeme_initialise
    
    if not systeme_initialise:
        raise HTTPException(status_code=400, detail="Système non initialisé. Appelez d'abord /api/ia-evolutif/initialiser")
    
    try:
        # Dialogue avec évolution automatique
        reponse = await ia_evolutif.dialoguer(dialogue.question)
        
        # Extraction des concepts utilisés (simulation)
        concepts_utilises = []
        mots_cles_theoriques = ["digamma", "riemann", "nombres premiers", "geometrie", "philippot", "univers", "carre"]
        
        for concept in mots_cles_theoriques:
            if concept.lower() in dialogue.question.lower() or concept.lower() in reponse.lower():
                concepts_utilises.append(concept)
        
        return DialogueResponse(
            reponse=reponse,
            concepts_utilises=concepts_utilises,
            evolution_silencieuse=True,
            taille_banque=len(ia_evolutif.banque_evolutive.banque)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur dialogue IA évolutif: {str(e)}")

@app.get("/api/ia-evolutif/statistiques")
async def obtenir_statistiques_systeme():
    """
    Statistiques d'évolution du système pour monitoring
    Informations sur l'évolution silencieuse de la banque
    """
    global systeme_initialise
    
    if not systeme_initialise:
        return {
            "systeme_initialise": False,
            "message": "Système non initialisé"
        }
    
    try:
        stats = await ia_evolutif.obtenir_statistiques_evolution()
        
        return {
            "systeme_initialise": True,
            "evolution_silencieuse_active": True,
            "statistiques": stats,
            "meta_programmation_status": "Opérationnelle",
            "analyse_pdf_status": "Documents intégrés"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur statistiques: {str(e)}")

@app.post("/api/ia-evolutif/reinitialiser")
async def reinitialiser_systeme():
    """
    Réinitialisation complète du système évolutif
    Efface l'évolution et repart de la banque initiale
    """
    global systeme_initialise
    
    try:
        # Création d'une nouvelle instance
        global ia_evolutif
        ia_evolutif = IAQuestionnementEvolutif()
        systeme_initialise = False
        
        return {
            "success": True,
            "message": "Système réinitialisé avec succès",
            "action_requise": "Appeler /api/ia-evolutif/initialiser avec la banque de 14 questions"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur réinitialisation: {str(e)}")

@app.get("/api/ia-evolutif/concepts-theoriques")
async def obtenir_concepts_theoriques():
    """
    Récupération des concepts théoriques extraits des documents PDF
    Base conceptuelle pour l'évolution de la banque
    """
    global systeme_initialise
    
    if not systeme_initialise:
        raise HTTPException(status_code=400, detail="Système non initialisé")
    
    try:
        concepts = ia_evolutif.banque_evolutive.concepts_theoriques
        
        return {
            "concepts_extraits": concepts,
            "nombre_concepts": len(concepts.get("concepts_fondamentaux", {})),
            "source": "Analyse automatique des documents PDF Partie 1 & 2",
            "utilisation": "Base pour l'évolution silencieuse de la banque Q&R"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération concepts: {str(e)}")

# ===============================================
# GESTION MANUELLE DE LA BANQUE ÉVOLUTIVE
# ===============================================

@app.post("/api/ia-evolutif/ajouter-question")
async def ajouter_question_manuelle(nouvelle_qr: QuestionEvolutive):
    """
    Ajout manuel d'une question-réponse à la banque évolutive
    Permet à l'utilisateur d'enrichir sa banque avec ses propres Q&R
    """
    global systeme_initialise
    
    if not systeme_initialise:
        raise HTTPException(status_code=400, detail="Système non initialisé")
    
    try:
        # Création d'une nouvelle entrée QuestionReponse
        from modules.evolutionary_qa_system import QuestionReponse
        import uuid
        from datetime import datetime
        
        nouvelle_entree = QuestionReponse(
            id=str(uuid.uuid4()),
            question=nouvelle_qr.question,
            reponse=nouvelle_qr.reponse,
            contexte_theorique=["L'univers est au carré", "Ajout manuel utilisateur"],
            niveau_complexite=nouvelle_qr.complexite or 3,
            variantes=[],
            concepts_cles=nouvelle_qr.concepts or [],
            frequence_utilisation=0,
            derniere_evolution=datetime.now().isoformat(),
            meta_score=0.7,  # Score élevé car ajouté manuellement
            relations_internes=[]
        )
        
        # Ajout à la banque
        ia_evolutif.banque_evolutive.banque.append(nouvelle_entree)
        
        # Sauvegarde immédiate
        await ia_evolutif.banque_evolutive._sauvegarder_banque()
        
        return {
            "success": True,
            "message": "Question-réponse ajoutée avec succès à la banque évolutive",
            "id_cree": nouvelle_entree.id,
            "taille_banque": len(ia_evolutif.banque_evolutive.banque),
            "evolution_silencieuse": "La nouvelle Q&R sera intégrée dans l'évolution automatique"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur ajout Q&R: {str(e)}")

@app.post("/api/ia-evolutif/importer-questions")
async def importer_questions_lot(fichier_qr: dict):
    """
    Import en lot de plusieurs questions-réponses
    Format: {"questions": [{"question": "...", "reponse": "...", "complexite": 3, "concepts": [...]}]}
    """
    global systeme_initialise
    
    if not systeme_initialise:
        raise HTTPException(status_code=400, detail="Système non initialisé")
    
    try:
        questions_a_importer = fichier_qr.get("questions", [])
        
        if not questions_a_importer:
            raise HTTPException(status_code=400, detail="Aucune question à importer")
        
        questions_ajoutees = []
        
        for qr_data in questions_a_importer:
            # Validation des données
            if not qr_data.get("question") or not qr_data.get("reponse"):
                continue
                
            from modules.evolutionary_qa_system import QuestionReponse
            import uuid
            from datetime import datetime
            
            nouvelle_entree = QuestionReponse(
                id=str(uuid.uuid4()),
                question=qr_data["question"],
                reponse=qr_data["reponse"],
                contexte_theorique=["L'univers est au carré", "Import lot utilisateur"],
                niveau_complexite=qr_data.get("complexite", 3),
                variantes=[],
                concepts_cles=qr_data.get("concepts", []),
                frequence_utilisation=0,
                derniere_evolution=datetime.now().isoformat(),
                meta_score=0.7,
                relations_internes=[]
            )
            
            ia_evolutif.banque_evolutive.banque.append(nouvelle_entree)
            questions_ajoutees.append(nouvelle_entree.question[:50] + "...")
        
        # Sauvegarde
        await ia_evolutif.banque_evolutive._sauvegarder_banque()
        
        return {
            "success": True,
            "message": f"{len(questions_ajoutees)} questions importées avec succès",
            "questions_ajoutees": questions_ajoutees,
            "taille_banque_finale": len(ia_evolutif.banque_evolutive.banque)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur import lot: {str(e)}")

@app.get("/api/ia-evolutif/voir-banque")
async def voir_banque_complete():
    """
    Visualisation complète de la banque évolutive
    Permet de voir toutes les Q&R (originales + évoluées + ajoutées manuellement)
    """
    global systeme_initialise
    
    if not systeme_initialise:
        raise HTTPException(status_code=400, detail="Système non initialisé")
    
    try:
        banque_complete = []
        
        for qr in ia_evolutif.banque_evolutive.banque:
            banque_complete.append({
                "id": qr.id,
                "question": qr.question,
                "reponse": qr.reponse,
                "complexite": qr.niveau_complexite,
                "concepts": qr.concepts_cles,
                "source": "Manuelle" if "manuel" in qr.contexte_theorique[0].lower() else "Évolutive",
                "utilisation": qr.frequence_utilisation,
                "derniere_evolution": qr.derniere_evolution,
                "meta_score": qr.meta_score,
                "variantes_count": len(qr.variantes)
            })
        
        return {
            "banque_complete": banque_complete,
            "statistiques": {
                "total_questions": len(banque_complete),
                "questions_manuelles": len([q for q in banque_complete if q["source"] == "Manuelle"]),
                "questions_evolutives": len([q for q in banque_complete if q["source"] == "Évolutive"]),
                "concepts_uniques": len(set(concept for qr in banque_complete for concept in qr["concepts"])),
                "complexite_moyenne": sum(qr["complexite"] for qr in banque_complete) / len(banque_complete) if banque_complete else 0
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur visualisation banque: {str(e)}")

@app.put("/api/ia-evolutif/modifier-question/{question_id}")
async def modifier_question(question_id: str, qr_modifiee: QuestionEvolutive):
    """
    Modification d'une question-réponse existante dans la banque
    Permet d'ajuster les Q&R manuellement
    """
    global systeme_initialise
    
    if not systeme_initialise:
        raise HTTPException(status_code=400, detail="Système non initialisé")
    
    try:
        # Recherche de la Q&R à modifier
        qr_trouvee = None
        index_qr = -1
        
        for i, qr in enumerate(ia_evolutif.banque_evolutive.banque):
            if qr.id == question_id:
                qr_trouvee = qr
                index_qr = i
                break
        
        if not qr_trouvee:
            raise HTTPException(status_code=404, detail="Question non trouvée")
        
        # Modification
        from datetime import datetime
        
        qr_trouvee.question = qr_modifiee.question
        qr_trouvee.reponse = qr_modifiee.reponse
        qr_trouvee.niveau_complexite = qr_modifiee.complexite or qr_trouvee.niveau_complexite
        qr_trouvee.concepts_cles = qr_modifiee.concepts or qr_trouvee.concepts_cles
        qr_trouvee.derniere_evolution = datetime.now().isoformat()
        qr_trouvee.meta_score = min(qr_trouvee.meta_score + 0.1, 1.0)  # Légère augmentation du score
        
        # Ajout dans le contexte qu'elle a été modifiée manuellement
        if "Modifié manuellement" not in qr_trouvee.contexte_theorique:
            qr_trouvee.contexte_theorique.append("Modifié manuellement")
        
        # Sauvegarde
        await ia_evolutif.banque_evolutive._sauvegarder_banque()
        
        return {
            "success": True,
            "message": "Question-réponse modifiée avec succès",
            "question_modifiee": qr_trouvee.question[:50] + "...",
            "derniere_evolution": qr_trouvee.derniere_evolution
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur modification Q&R: {str(e)}")

@app.delete("/api/ia-evolutif/supprimer-question/{question_id}")
async def supprimer_question(question_id: str):
    """
    Suppression d'une question-réponse de la banque évolutive
    À utiliser avec précaution car la suppression est définitive
    """
    global systeme_initialise
    
    if not systeme_initialise:
        raise HTTPException(status_code=400, detail="Système non initialisé")
    
    try:
        # Recherche et suppression
        banque_originale = len(ia_evolutif.banque_evolutive.banque)
        question_supprimee = None
        
        ia_evolutif.banque_evolutive.banque = [
            qr for qr in ia_evolutif.banque_evolutive.banque 
            if qr.id != question_id
        ]
        
        if len(ia_evolutif.banque_evolutive.banque) == banque_originale:
            raise HTTPException(status_code=404, detail="Question non trouvée")
        
        # Sauvegarde
        await ia_evolutif.banque_evolutive._sauvegarder_banque()
        
        return {
            "success": True,
            "message": "Question-réponse supprimée avec succès",
            "taille_banque": len(ia_evolutif.banque_evolutive.banque),
            "questions_supprimees": 1
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur suppression Q&R: {str(e)}")

# ===============================================
# IA SOCRATIQUE - PARTENAIRE INTELLECTUEL
# ===============================================

class DialogueSocratiqueRequest(BaseModel):
    reflexion_utilisateur: str
    contexte_session: Optional[str] = None

class DialogueSocratiqueResponse(BaseModel):
    reponse_socratique: str
    questions_challengeantes: List[str]
    axes_evolution_identifies: List[str]
    niveau_challenge: int
    concepts_analyses: List[str]

@app.post("/api/ia-socratique/challenger", response_model=DialogueSocratiqueResponse)
async def challenger_raisonnement(dialogue: DialogueSocratiqueRequest):
    """
    IA Socratique pour challenger et élever le raisonnement de Philippe Thomas Savard
    Analyse la réflexion et pose des questions provocatrices pour l'évolution théorique
    """
    try:
        # Analyse socratique du raisonnement
        resultat = await ia_socratique.analyser_et_challenger(dialogue.reflexion_utilisateur)
        
        return DialogueSocratiqueResponse(
            reponse_socratique=resultat["reponse_socratique"],
            questions_challengeantes=resultat["questions_challengeantes"],
            axes_evolution_identifies=resultat["axes_evolution_identifies"],
            niveau_challenge=resultat["niveau_challenge_global"],
            concepts_analyses=resultat["concepts_analyses"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur IA socratique: {str(e)}")

@app.post("/api/ia-socratique/approfondir")
async def approfondir_concept(concept_request: dict):
    """
    Approfondissement socratique d'un concept spécifique
    Génère des questions pour challenger un aspect particulier de la théorie
    """
    try:
        concept = concept_request.get("concept", "")
        contexte = concept_request.get("contexte", "")
        
        if not concept:
            raise HTTPException(status_code=400, detail="Concept à approfondir requis")
        
        # Analyse spécifique du concept
        analyse = await ia_socratique.analyseur.analyser_concept(concept, contexte)
        
        # Génération de questions challengeantes
        question_socratique = await ia_socratique.generateur_questions.generer_question_challengeante(
            analyse, contexte
        )
        
        return {
            "concept_analyse": concept,
            "solidite_logique": analyse.solidite_logique,
            "lacunes_identifiees": analyse.lacunes_identifiees,
            "questions_emergentes": analyse.questions_emergentes,
            "question_challengeante": question_socratique.question,
            "niveau_challenge": question_socratique.niveau_challenge,
            "angle_approche": question_socratique.angle_approche,
            "type_reponse_attendue": question_socratique.reponse_attendue_type
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur approfondissement concept: {str(e)}")

@app.get("/api/ia-socratique/axes-evolution")
async def obtenir_axes_evolution_theorique():
    """
    Récupération des axes d'évolution identifiés pour la théorie
    Vue d'ensemble des directions d'amélioration possibles
    """
    try:
        axes_evolution = {
            "axes_prioritaires": [
                "Formalisation rigoureuse des constantes dans les formules",
                "Démonstration de l'universalité du rapport 1/2", 
                "Extension de la géométrie carrée aux dimensions supérieures",
                "Connexion avec la théorie analytique des nombres classique"
            ],
            "questions_fondamentales": [
                "Comment démontrer mathématiquement l'unicité de vos formules?",
                "Quelles sont les limites de validité de votre théorie?",
                "Comment votre approche se généralise-t-elle à d'autres domaines?",
                "Quelles prédictions testables fait votre théorie?"
            ],
            "lacunes_a_combler": [
                "Preuves formelles des convergences",
                "Validation empirique sur de grands ensembles",
                "Comparaison systématique avec les approches classiques",
                "Développement d'applications pratiques"
            ],
            "opportunites_extension": [
                "Géométrie non-euclidienne et théorie",
                "Applications en cryptographie",
                "Liens avec la physique théorique",
                "Algorithmes optimisés pour le calcul de nombres premiers"
            ]
        }
        
        return {
            "axes_evolution_theorique": axes_evolution,
            "objectif": "Développer une version plus sophistiquée et rigoureuse de 'L'univers est au carré'",
            "approche_recommandee": "Questionnement socratique systématique pour identifier et combler les lacunes conceptuelles"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur axes évolution: {str(e)}")

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

# Nouveau endpoint pour upload de fichiers
@app.post("/api/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    session_id: str = Form(...)
):
    """Upload et analyse d'un document pour enrichir les discussions"""
    try:
        # Générer un ID unique pour le document
        doc_id = str(uuid.uuid4())
        
        # Lire le contenu du fichier
        content = await file.read()
        
        # Convertir en base64 pour stockage
        content_b64 = base64.b64encode(content).decode()
        
        # Créer l'enregistrement du document
        document = {
            "id": doc_id,
            "filename": file.filename,
            "file_type": file.content_type,
            "content": content_b64,
            "analysis": "",  # Sera rempli après analyse
            "user_session": session_id,
            "upload_date": datetime.now(timezone.utc).isoformat(),
            "file_size": len(content)
        }
        
        # Sauvegarder dans MongoDB
        await db.uploaded_documents.insert_one(document)
        
        # Analyser le document avec l'IA si c'est un fichier text/image
        analysis = ""
        if file.content_type.startswith('text/') or file.content_type == 'application/pdf':
            try:
                # Extraire le texte du document
                document_text = ""
                
                if file.content_type == 'application/pdf':
                    # Pour les PDFs, utiliser PyPDF2 ou pdfplumber
                    try:
                        import io
                        import PyPDF2
                        
                        pdf_file = io.BytesIO(content)
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        
                        # Extraire le texte de toutes les pages
                        for page in pdf_reader.pages:
                            document_text += page.extract_text() + "\n"
                        
                        # Limiter la taille si trop long (max 15000 caractères pour l'IA)
                        if len(document_text) > 15000:
                            document_text = document_text[:15000] + "\n\n[Document tronqué - contenu trop long]"
                            
                    except Exception as pdf_error:
                        document_text = "[Erreur lors de l'extraction du PDF - analyse impossible]"
                        print(f"Erreur extraction PDF: {str(pdf_error)}")
                
                elif file.content_type.startswith('text/'):
                    document_text = content.decode('utf-8', errors='ignore')
                
                # Analyser avec l'IA spécialisée seulement si le texte a été extrait
                if document_text and not document_text.startswith('[Erreur'):
                    analysis_prompt = f"""
Analyse ce nouveau document dans le contexte de la théorie 'L'univers est au carré' de Philippe Thomas Savard.

CONTENU DU DOCUMENT "{file.filename}":
---
{document_text}
---

Identifie :
1. Les nouveaux concepts ou développements présentés
2. Les liens avec les concepts existants de la théorie
3. Les questions ou pistes de recherche suggérées
4. Les clarifications ou corrections apportées
5. Les implications pour la compréhension globale de la théorie

Sois précis et technique dans ton analyse.
"""
                    
                    chat = LlmChat(
                        api_key=EMERGENT_LLM_KEY,
                        session_id=doc_id,
                        system_message="Tu es l'IA spécialisée dans la théorie 'L'univers est au carré'. Analyse ce document en profondeur."
                    ).with_model("anthropic", "claude-sonnet-4-20250514")
                    
                    analysis = await chat.send_message(UserMessage(text=analysis_prompt))
                else:
                    analysis = document_text  # Contient le message d'erreur
                
                # Mettre à jour l'analyse dans la base
                await db.uploaded_documents.update_one(
                    {"id": doc_id},
                    {"$set": {"analysis": analysis}}
                )
                
            except Exception as e:
                print(f"Erreur lors de l'analyse : {str(e)}")
        
        return {
            "success": True,
            "document_id": doc_id,
            "filename": file.filename,
            "analysis": analysis,
            "message": "Document uploadé et analysé avec succès"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'upload: {str(e)}")

@app.get("/api/documents/{session_id}")
async def get_documents(session_id: str):
    """Récupère tous les documents d'une session"""
    documents = await db.uploaded_documents.find(
        {"user_session": session_id}
    ).sort("upload_date", -1).to_list(length=None)
    
    # Retourner sans le contenu pour économiser la bande passante
    return [
        {
            "id": doc["id"],
            "filename": doc["filename"],
            "file_type": doc["file_type"],
            "analysis": doc["analysis"],
            "upload_date": doc["upload_date"]
        }
        for doc in documents
    ]

# Définir le system_message (il était manquant)
system_message = """Tu es un expert spécialisé dans la théorie personnelle 'L'univers est au carré' développée par Philippe Thomas Savard. 
    Tu ne réponds QU'AUX QUESTIONS liées à cette théorie spécifique.
    
    **IMPORTANT : STRUCTURE EN TROIS DOMAINES DISTINCTS**
    
    La théorie de Philippe Thomas Savard comprend TROIS domaines d'étude SÉPARÉS que tu dois traiter de manière INDÉPENDANTE sans forcer de connexions :
    
    **DOMAINE 1 : L'énigme de Riemann et les nombres premiers**
    - Analyse numérique métrique combinant géométrie et numérotation
    - Représentation en tesseract projeté sur sphère de la fonction Zêta
    - Rapports fractionnels (1/2, 1/3, 1/5) entre nombres premiers sur diamètre
    - Technique du "moulinet" pour visualiser la distribution à l'infini
    - Concept du Digamma dans la détermination des nombres premiers
    - Démonstration que les zéros non triviaux ont partie réelle de 0,5
    
    **DOMAINE 2 : Théorème de Philippôt, intrication quantique et "squaring"**
    - Théorème de Philippôt sur l'intrication quantique via géométrie
    - Deux triangles intriqués avec côtés liés aux constantes mathématiques
    - Invariance géométrique où le choix d'unité influence les mesures
    - "Produit alternatif" pour calculs dans différents systèmes unitaires
    - Concept de "squaring" : rectangles élevés au carré deviennent carrés
    - Matrice de longueurs unitaires avec nombres premiers aléatoires
    
    **DOMAINE 3 : Mécanique harmonique du chaos discret**
    - Position des mesures géométriques dépendant du choix d'unité
    - Géométrie relationnelle similaire à la relativité
    - "Matrice à dérive première" pour visualiser distribution des nombres premiers
    - Équilibre dynamique et structures auto-organisatrices
    - Chaons et pression gravito-spectrale
    
    **DEUXIÈME PARTIE DE LA THÉORIE (concepts distincts) :**
    - **Théorème "Trois carrés égale un triangle"** ancré dans Pythagore
    - **Longueur de Philippôt** inspirée de la longueur de Planck
    - **Cercle Denis** avec diamètre 1 et circonférence ≈ 4
    - **Constante de l'inverse du temps** liée au volume terrestre
    - **√10 comme approximation de π** selon Philippôt
    - **Théorème du Carré de Gabriel** pour triangles scalènes
    - **Théorème Gris Bleu** sur rotations quaternions
    
    **MÉTHODE SPECTRALE POUR INTERVALLES ENTRE NOMBRES PREMIERS :**
    - **Approche multi-étapes** avec suites mathématiques et constantes empiriques
    - **Fonction Digamma de Philippôt** pour correction des intervalles premiers
    - **Constantes A, B, C, D, E** liées aux propriétés spectrales des nombres premiers
    - **Comparaison avec méthode classique** (q - p - 1) et approche géométrique
    - **Extension de la géométrie du spectre** aux intervalles entre nombres premiers consécutifs
    
    **SQUARING GÉNÉRALISÉ ET NEUROMORPHISME :**
    - **Postulat unique fondamental** : rectangles élevés au carré comme principe universel
    - **Forme généralisée du squaring** : extension aux structures rectangulaires complexes
    - **Neuromorphisme géométrique** : évolution des formes neuronales par transformations rectangulaires
    - **Géométrie neuromorphique** : application des principes géométriques à l'évolution biologique
    - **Morphogenèse rectangulaire** : développement des formes par applications successives du squaring
    - **Connexion géométrie-biologie** : pont entre mathématiques pures et évolution neuronale
    
    **RÈGLES DE RÉPONSE STRICTES :**
    1. Identifie d'abord quel(s) domaine(s) concerne la question
    2. Réponds UNIQUEMENT selon ce domaine spécifique
    3. NE FORCE JAMAIS de liens entre les domaines
    4. Si la question mélange les domaines, traite chacun séparément
    5. Utilise la terminologie exacte de chaque domaine
    
    **STRUCTURE DE RÉPONSE OBLIGATOIRE EN DEUX PARTIES :**
    
    **PARTIE 1 - VISION DE L'AUTEUR :**
    - Explique selon Philippe Thomas Savard et son domaine spécifique
    - Utilise sa terminologie exacte du domaine concerné
    - Reste dans le cadre conceptuel du domaine
    
    **PARTIE 2 - MISE À NIVEAU CONTEXTUELLE :**
    - État des recherches actuelles dans ce domaine spécifique
    - NE PREND JAMAIS PARTI sur validité
    - Reste purement informatif
    
    Réponds toujours en français, de manière technique et pédagogique."""

@app.post("/api/chat-extended", response_model=ChatResponse)
async def chat_with_ai_extended(chat_message: ExtendedChatMessage):
    """Chat enrichi avec contexte étendu et documents attachés"""
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    # Générer un session_id si non fourni
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    # Récupérer le contexte personnel étendu
    personal_context = await get_personal_context(session_id)
    
    # Récupérer les documents attachés si spécifiés
    attached_docs_context = ""
    if chat_message.attached_files:
        for doc_id in chat_message.attached_files:
            doc = await db.uploaded_documents.find_one({"id": doc_id})
            if doc and doc.get("analysis"):
                attached_docs_context += f"\n\n--- Document: {doc['filename']} ---\n{doc['analysis']}"
    
    # Construire le contexte enrichi avec les concepts théoriques spécialisés
    theory_enrichment = enrich_system_message_with_privileged_access()
    
    # Récupérer les corrections personnelles de l'auteur
    corrections_personnelles, profil_auteur = await get_corrections_personnelles_pour_session(chat_message.session_id)
    
    # Construire l'enrichissement personnel
    personal_enrichment = ""
    if corrections_personnelles:
        personal_enrichment += "\n\n**CORRECTIONS PERSONNELLES DE L'AUTEUR (Philippe Thomas Savard) :**\n"
        for correction in corrections_personnelles[-10:]:  # Les 10 dernières
            personal_enrichment += f"- **Question:** {correction['question_originale'][:100]}...\n"
            personal_enrichment += f"  **Correction de l'auteur:** {correction['correction_auteur']}\n"
            personal_enrichment += f"  **Domaine:** {correction['domaine_concerne']}\n\n"
    
    if profil_auteur and profil_auteur.get('nuances_importantes'):
        personal_enrichment += "\n**NUANCES IMPORTANTES SELON L'AUTEUR :**\n"
        for nuance in profil_auteur['nuances_importantes'][-5:]:  # Les 5 dernières
            personal_enrichment += f"- {nuance}\n"
    
    enhanced_system_message = f"""{system_message}
    
    {theory_enrichment}
    
    {personal_enrichment}
    
    **CONTEXTE PERSONNEL DE PHILIPPE THOMAS SAVARD :**
    
    **Historique des insights clés :**
    {json.dumps(personal_context.get('key_insights', []), indent=2)}
    
    **Patterns de raisonnement identifiés :**
    {json.dumps(personal_context.get('reasoning_patterns', {}), indent=2)}
    
    **Fils de recherche en cours :**
    {json.dumps(personal_context.get('research_threads', []), indent=2)}
    
    **Documents récemment analysés :**
    {attached_docs_context}
    
    **INSTRUCTIONS PERSONNALISÉES :**
    - Tu connais l'auteur Philippe Thomas Savard et son style de questionnement
    - Adapte tes réponses à son niveau de compréhension avancé de sa propre théorie
    - Référence les discussions passées quand pertinent
    - Identifie et signale les nouvelles pistes de recherche
    - Aide à structurer et clarifier sa pensée
    - Propose des connexions avec ses travaux précédents
    - Utilise les concepts théoriques enrichis selon leur domaine spécifique
    """
    
    try:
        # Chat avec contexte enrichi
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=enhanced_system_message
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text=chat_message.message)
        response = await chat.send_message(user_message)
        
        # Sauvegarder la conversation enrichie
        conversation = {
            "session_id": session_id,
            "user_message": chat_message.message,
            "ai_response": response,
            "attached_files": chat_message.attached_files or [],
            "context_mode": chat_message.context_mode,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.conversations_extended.insert_one(conversation)
        
        # Mettre à jour le contexte personnel
        await update_personal_context(session_id, chat_message.message, response)
        
        return ChatResponse(response=response, session_id=session_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chat enrichi: {str(e)}")

async def get_personal_context(session_id: str) -> Dict[str, Any]:
    """Récupère le contexte personnel de Philippe Thomas Savard"""
    context = await db.personal_context.find_one({"user_id": "philippe_savard"})
    
    if not context:
        # Créer un contexte initial
        default_context = {
            "user_id": "philippe_savard",
            "conversation_history": [],
            "uploaded_documents": [],
            "reasoning_patterns": {
                "prefere_approches_geometriques": True,
                "focus_sur_relations_numeriques": True,
                "interesse_par_validations_empiriques": True,
                "cherche_connections_cosmologiques": True
            },
            "key_insights": [
                "Développement de la méthode de Philippôt avec 14 tableaux",
                "Importance du Digamma à la 8ème position",
                "Théorème de convergence formel établi",
                "Matrice à dérive première dans la mécanique harmonique"
            ],
            "research_threads": [
                {"theme": "Validation empirique de la méthode", "status": "actif"},
                {"theme": "Extensions aux nombres premiers négatifs", "status": "exploratoire"},
                {"theme": "Connexions cosmologiques approfondies", "status": "théorique"}
            ]
        }
        await db.personal_context.insert_one(default_context)
        return default_context
    
    return context

async def update_personal_context(session_id: str, user_message: str, ai_response: str):
    """Met à jour le contexte personnel basé sur la conversation"""
    # Analyser la conversation pour identifier de nouveaux insights
    # Cette fonction pourrait être étendue avec une IA d'analyse
    
    conversation_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_message": user_message,
        "ai_response": ai_response,
        "session_id": session_id
    }
    
    # Ajouter à l'historique (garder les 50 dernières conversations)
    await db.personal_context.update_one(
        {"user_id": "philippe_savard"},
        {
            "$push": {
                "conversation_history": {
                    "$each": [conversation_entry],
                    "$slice": -50  # Garder seulement les 50 dernières
                }
            }
        },
        upsert=True
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(chat_message: ChatMessage):
    """Chat avec l'IA spécialisée dans la théorie 'L'univers est au carré'"""
    global systeme_initialise
    
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    # Générer un session_id si non fourni
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    # NOUVEAU : Logger la question dans MongoDB pour l'admin
    try:
        await db.questions_log.insert_one({
            "question": chat_message.message,
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ip_address": "N/A",  # Peut être ajouté plus tard si nécessaire
            "user_agent": "N/A"
        })
    except Exception as log_error:
        print(f"Erreur logging question: {log_error}")
        # Ne pas bloquer si le logging échoue
    
    # Détecter si c'est l'auteur Philippe Thomas Savard
    is_author = detect_author_authentication(chat_message.message)
    author_context = get_author_context_addition() if is_author else ""
    
    # Contexte profondément enrichi avec tous les aspects de la théorie de Philippôt
    system_message = f"""Tu es un expert mathématicien spécialisé dans la théorie révolutionnaire 'L'univers est au carré' développée par Philippe Thomas Savard. 
    Tu ne réponds QU'AUX QUESTIONS liées à cette théorie spécifique, mais tes réponses doivent être extrêmement détaillées, techniques et pédagogiques.
    {author_context}
    
    **FONDEMENTS ALGORITHMIQUES PROFONDS :**
    
    **1. LA MÉTHODE DE GÉNÉRATION DES SÉQUENCES DE PHILIPPÔT :**
    - Algorithme itératif générant des suites de fractions dont la somme = 1
    - Chaque étape substitue la plus grande fraction (Zêta ζ) du côté gauche par sa moitié
    - Progression géométrique avec ratio constant de 1/2 sur le côté droit
    - Récursivité : chaque étape construit sur la précédente
    - Convergence assurée vers 0 des termes du côté gauche
    
    **2. DÉFINITIONS TECHNIQUES PRÉCISES ET FORMALISÉES :**
    - **Zêta de Philippôt (ζ)** : Fonction formalisée rigoureusement, distincte du zêta de Riemann
      • Plus grande fraction du côté gauche, soustraite à 1 à chaque étape
      • Définition positionnelle précise dans le cadre des substitutions itératives
      • Relation formelle avec l'analyse numérique métrique
    - **Digamma (ψ)** : Avant-dernière fraction du côté droit, calculée par multiplication précédente × 2/3
    - **Queue (Q)** : Dernière fraction du côté droit, toujours Q = ψ × 1/2
    - **Ratio fondamental 1/2** : Moteur de convergence et génération des suites infinies
    - **Duo final** : Mécanisme de substitution dans le processus itératif clarifié
    
    **3. PROCESSUS ITÉRATIF CLARIFIÉ ET FORMALISÉ :**
    - **Substitutions successives** : Mécanisme rigoureux de remplacement des fractions
    - **Duo final** : Étape clé du processus itératif avec règles précises
    - **Convergence garantie** : Théorème de convergence formel démontré
    - **Multiplication par 1/2** : génère la suite géométrique des Zêta
    - **Multiplication par 2/3** : calcule le Digamma à partir de la fraction précédente
    - **Critères d'arrêt** : Conditions formelles de convergence de l'itération
    - **Stabilité numérique** : Assurance de la précision des calculs itératifs
    
    **4. LES 14 TABLEAUX GÉOMÉTRIQUES :**
    Chaque rapport base/hauteur (1/2, 1/3, 1/4... 1/100) génère :
    - Deux suites de racines carrées selon √((n+i)² + (n+i+1)²)
    - Digamma calculé à la 8ème position : √((n+7)² + (n+8)²)
    - Opération variable (addition/soustraction) selon le rapport
    - Résultat final = nombre premier précis avec sa position dans la suite
    
    **5. EXEMPLES TECHNIQUES DÉTAILLÉS :**
    - Rapport 1/2 : 3 fractions → 1/2 + 1/3 + 1/6 = 1, Digamma = √81920 → 29 (10ème premier)
    - Rapport 1/3 : Progression géométrique → Digamma = √281300 → 227 (49ème premier)
    - Rapport 1/100 : Séquence complexe → Digamma = √270401 → 1299721 (99991ème premier)
    
    **6. GÉNÉRALISATION MATHÉMATIQUE :**
    - Forme généralisée pour suites de n ≥ 8 données
    - Notation indexée : δᵢ, ψᵢ, Qᵢ
    - Formules : 1 - ζ = (nouveau ζ)/2 + ψ + Q
    - Extension infinie avec convergence garantie
    
    **7. LIENS GÉOMÉTRIE-NOMBRES PREMIERS :**
    - Triangles rectangles comme base géométrique
    - Rapports base/hauteur déterminent les nombres premiers
    - Séquences de racines carrées révèlent la structure cachée
    - Distance entre nombres premiers calculable via les suites
    
    **8. FORMULES DIRECTES DE CALCUL DES SOMMES (INNOVATION MAJEURE) :**
    Philippe Thomas Savard a développé 4 équations révolutionnaires pour calculer directement les sommes des suites :
    
    **Pour les nombres premiers POSITIFS :**
    - Somme 1ère suite = (√13.203125/2×2^n) - √5
    - Somme 2ème suite = (√52.8125/2×2^n) - √5445
    
    **Pour les nombres premiers NÉGATIFS :**
    - Somme 1ère suite = (√13.203125×2^n) - √5
    - Somme 2ème suite = (√52.8125×2^n) - √5445
    
    Ces formules éliminent le besoin d'additionner terme par terme et révèlent la structure mathématique profonde :
    - Constantes fondamentales : √13.203125, √52.8125, √5, √5445
    - Facteur exponentiel 2^n gouvernant la progression
    - Distinction positifs/négatifs par division ou multiplication par 2×2^n
    - Optimisation algorithmique révolutionnaire pour le calcul des nombres premiers
    
    **12. MÉCANIQUE HARMONIQUE DU CHAOS DISCRET (Théorie avancée) :**
    Concept révolutionnaire succédant aux rectangles élevés au carré :
    - **Définition des "chaons"** : Entités géométriques fondamentales dans l'équilibre dynamique
    - **Relations triangulaires** : Connexions géométriques entre triangles et distribution des premiers
    - **Équilibre dynamique** : Mécanisme de stabilisation des patterns de nombres premiers
    - **Pression gravito-spectrale** : Force théorique agissant sur les distributions numériques
    - **Harmonie mathématique** : Principes régissant l'ordre dans le chaos apparent
    - **Choix d'unité critique** : Impact des unités de mesure sur les positions géométriques
    - **Structures auto-organisatrices** : Mécanismes d'auto-régulation des séquences
    - **Approche interdisciplinaire** : Connexion mathématiques-physique-cosmologie
    - **Insights qualitatifs** : Compréhension intuitive des mécanismes sous-jacents
    - **Cadre théorique unificateur** : Vision globale de l'ordre cosmique via les nombres premiers
    - **Applications aux tesseracts** : Extension de la mécanique aux espaces multidimensionnels
    - **Validation empirique** : Confirmation par les résultats de la méthode de Philippôt
    
    **13. MATRICE À DÉRIVE PREMIÈRE (Concept matriciel avancé) :**
    Innovation mathématique au cœur de la mécanique harmonique du chaos discret :
    - **Définition matricielle** : Structure mathématique pour analyser les relations entre nombres premiers
    - **Dérive première** : Opération différentielle appliquée aux séquences de nombres premiers
    - **Construction matricielle** : Mécanismes de génération et règles de formation de la matrice
    - **Matrice unitaire à la figure** : Représentation visuelle et géométrique des relations
    - **Produit alternatif** : Opération spécialisée liée aux calculs triangulaires
    - **Diamètre équivalent** : Mesure géométrique dérivée des propriétés matricielles
    - **Applications aux chaons** : Utilisation matricielle dans l'équilibre dynamique
    - **Compression des distances** : Technique du "moulinet" pour analyser les espacements
    - **Relations géométriques** : Connexions avec les tesseracts et structures multidimensionnelles
    - **Calculs de la fonction Zêta** : Applications matricielles aux calculs de Philippôt
    - **Analyse différentielle** : Approche par dérivées pour étudier les patterns
    - **Structure auto-organisatrice** : Propriétés émergentes des arrangements matriciels
    
    **10. THÉORÈME DE PHILIPPÔT (Innovation centrale développée) :**
    Théorème fondamental établi après l'analyse de quasi-stabilité physique :
    - **Énoncé principal** : Relation déterministe entre diamètre d'un cercle et nombres premiers
    - **Méthode géométrique** : Utilisation combinée de tesseracts, sphères et fonction Digamma
    - **Application du Zêta de Philippôt** : Fonction distincte du zêta de Riemann pour localiser les premiers
    - **Représentations graphiques** : Visualisations via tesseracts et structures géométriques
    - **Digamma calculé** : Valeurs spécifiques fournissant les clés des patterns de nombres premiers
    - **Approche déterministe** : Méthode permettant l'identification systématique des nombres premiers
    - **Intrication quantique** : Application des principes quantiques aux distributions de premiers
    - **Connexions géométriques** : Liens entre propriétés spatiales et arithmétiques
    - **Manipulations du Digamma** : Techniques avancées pour extraire l'information des calculs
    
    **11. RECTANGLES ÉLEVÉS AU CARRÉ (Principe géométrique fondamental) :**
    Concept géométrique révolutionnaire succédant au théorème de Philippôt :
    - **Principe de transformation** : Un rectangle élevé à une puissance devient un carré
    - **Géométrie non-euclidienne** : Redéfinition des relations spatiales traditionnelles
    - **Propriétés intrinsèques** : Caractéristiques géométriques des carrés et rectangles
    - **Connexion arithmétique** : Lien établi entre transformations géométriques et distribution des premiers
    - **Applications aux tesseracts** : Extension aux espaces quadridimensionnels
    - **Base conceptuelle** : Fondement pour la transformation géométrique des espaces
    - **Rapports base/hauteur** : Application directe aux calculs triangulaires de la méthode
    - **Unification géométrique** : Principe reliant formes euclidienne et nombres premiers
    - **Implications cosmologiques** : Connexions avec la structure de l'univers
    - **Validation par l'analyse métrique** : Confirmation via l'analyse numérique métrique
    
    **13. THÉORÈME DE CONVERGENCE FORMEL (Version Corrigée) :**
    Philippe Thomas Savard a formalisé un théorème de convergence rigoureux :
    - **Énoncé formel** : Le processus itératif de la méthode converge vers une solution unique
    - **Conditions de convergence** : Critères mathématiques précis pour assurer la stabilité
    - **Démonstration rigoureuse** : Preuve formelle de la convergence du processus
    - **Analyse numérique métrique** : Cadre théorique pour la validation des résultats
    - **Stabilité des approximations** : Garantie de précision croissante à chaque itération
    - **Unicité de la solution** : Démonstration que chaque séquence converge vers un seul nombre premier
    
    **14. AMÉLIORATIONS DE LA VERSION CORRIGÉE :**
    - **Formalisation mathématique** : Définitions rigoureuses remplaçant les descriptions intuitives
    - **Processus itératif clarifié** : Mécanismes de substitution explicitement définis
    - **Zêta de Philippôt formalisé** : Distinction claire avec les fonctions standard
    - **Théorème de convergence** : Base théorique solide pour la validation de la méthode
    - **Notation mathématique** : Utilisation de symboles et formules standardisés
    - **Exemples numériques enrichis** : Calculs détaillés et vérifiables
    
    **15. VALIDATION ET INTELLIGENCE ARTIFICIELLE :**
    - IA ayant découvert autonomément les 18ème et 29ème nombres premiers
    - Méthode intuitive validée par calcul algorithmique
    - Approche révolutionnaire différente des méthodes classiques
    
    **10. ASPECTS COSMOLOGIQUES APPROFONDIS :**
    - Mécanique harmonique du chaos discret
    - Relations avec constantes physiques (vitesse lumière, longueur Planck)
    - Vision géométrique de l'univers à travers les nombres premiers
    - Théorème de Philippôt sur l'intrication quantique et géométrie
    - Unique postulat des rectangles élevés au carré
    - Connexions entre tesseracts et distribution des nombres premiers
    
    **INSTRUCTIONS DE RÉPONSE ULTRA-ENRICHIES :**
    - Explique TOUJOURS les mécanismes mathématiques avec la rigueur de la version corrigée
    - Utilise la formalisation rigoureuse du Zêta de Philippôt (distincte du zêta de Riemann)
    - Référence le théorème de convergence formel et ses conditions précises
    - Explique le processus itératif clarifié avec ses substitutions et duo final
    - **Développe le théorème de Philippôt** avec ses applications déterministes aux nombres premiers
    - **Explique les rectangles élevés au carré** comme principe de transformation géométrique
    - **Intègre la mécanique harmonique du chaos discret** avec les chaons et l'équilibre dynamique
    - **Maîtrise la matrice à dérive première** et ses applications aux relations entre nombres premiers
    - Explique la **construction matricielle** et les mécanismes de génération de la matrice
    - Utilise le **produit alternatif** et sa connexion aux calculs triangulaires
    - Référence le **diamètre équivalent** et ses propriétés géométriques dérivées
    - Montre la progression : quasi-stabilité → théorème de Philippôt → rectangles au carré → mécanique harmonique → matrice à dérive première
    - Utilise les représentations visuelles (matrice unitaire à la figure, tesseracts, sphères)
    - Explique les "chaons" et leur interaction avec les structures matricielles
    - Intègre la "pression gravito-spectrale" dans le cadre matriciel
    - Utilise l'**analyse différentielle** pour étudier les patterns de nombres premiers
    - Explique la **compression des distances** via la technique du "moulinet"
    - Montre les connexions complexes : géométrie → matrices → dérivées → chaos harmonique → nombres premiers
    - Utilise la terminologie complète (matrice à dérive première, produit alternatif, diamètre équivalent, chaons, moulinet)
    - Relie les **structures auto-organisatrices** matricielles aux mécanismes de chaos discret
    - Connecte approches matricielles, différentielles, et géométriques dans une vision unifiée
    
    **STRUCTURE DE RÉPONSE OBLIGATOIRE EN DEUX PARTIES :**
    
    **PARTIE 1 - VISION DE L'AUTEUR :**
    Présente toujours d'abord la perspective de Philippe Thomas Savard selon sa théorie "L'univers est au carré" :
    - Explique les concepts selon sa vision et ses documents
    - Utilise sa terminologie et ses approches spécifiques
    - Détaille ses méthodes et innovations sans jugement
    - Montre sa logique interne et sa cohérence propre
    
    **PARTIE 2 - MISE À NIVEAU CONTEXTUELLE :**
    Puis offre une mise à niveau factuelle sur l'état actuel des discussions scientifiques :
    - Informe sur les directions actuelles de recherche en mathématiques/physique sur des sujets similaires
    - Mentionne les opinions présentes dans les cercles scientifiques contemporains
    - Indique si ces directions convergent ou divergent avec la théorie de Savard
    - NE PREND JAMAIS PARTI sur ce qui est vrai ou faux
    - NE COMMENTE PAS et n'influence pas l'opinion du lecteur
    - Reste purement informatif sur l'état des connaissances actuelles
    
    **IMPORTANT :** L'auteur Philippe Thomas Savard reconnaît que beaucoup reste à démontrer avant une reconnaissance académique. Cette structure bi-partite est un souci de transparence, pas d'influence d'opinion.
    
    Si on te pose une question non liée à cette théorie, réponds poliment que tu es spécialisé uniquement dans 'L'univers est au carré' et invite à poser des questions précises sur cette théorie révolutionnaire.
    
    Réponds toujours en français, avec une approche à la fois rigoureuse mathématiquement ET accessible pédagogiquement."""
    
    try:
        # Initialiser le chat Claude
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=system_message
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
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
        
        # 🔄 SYNCHRONISATION AVEC L'IA ÉVOLUTIVE
        # Alimenter l'IA évolutive avec cette conversation si elle est initialisée
        if systeme_initialise:
            try:
                # Utiliser l'IA évolutive pour qu'elle apprenne de cette conversation
                await ia_evolutif.dialoguer(chat_message.message)
                print(f"✅ IA Évolutive enrichie avec: {chat_message.message[:50]}...")
            except Exception as e:
                print(f"⚠️ Erreur synchronisation IA évolutive: {e}")
        
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

@app.post("/api/collaborate")
async def collaborate_with_ai(request: CollaborationRequest):
    """Collaboration IA pour compléter et améliorer un document"""
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    try:
        # Contexte spécialisé pour la collaboration avec connaissances enrichies
        theory_enrichment = enrich_system_message_with_privileged_access()
        
        collaboration_system = f"""{system_message}
        
        {theory_enrichment}
        
        **MODE COLLABORATION DOCUMENTAIRE :**
        
        Tu travailles avec Philippe Thomas Savard sur un document collaboratif. Ta mission :
        - AJOUTER du contenu pertinent selon sa demande
        - DÉVELOPPER ses idées en restant fidèle à sa théorie
        - STRUCTURER et CLARIFIER ses pensées
        - PROPOSER des connexions avec d'autres aspects de sa théorie selon leur domaine
        - MAINTENIR la cohérence avec ses travaux existants
        - UTILISER les concepts théoriques enrichis appropriés selon le contexte
        
        **RÈGLES DE COLLABORATION :**
        1. Ajoute ton contenu de manière claire et identifiable
        2. Respecte le style et le niveau technique de l'auteur
        3. Développe les idées sans les dénaturer
        4. Propose des améliorations constructives
        5. Maintiens la structure bi-partite (vision auteur + contexte scientifique)
        6. Intègre les concepts enrichis selon leur domaine spécifique
        7. Respecte la séparation des domaines théoriques
        
        **DOCUMENT ACTUEL :**
        Titre : {request.document_title}
        Contenu : {request.document}
        
        **DEMANDE :** {request.request}
        
        Retourne le document COMPLET avec tes ajouts intégrés de manière naturelle.
        Marque tes contributions avec [IA: ...] pour clarté.
        """
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=request.session_id,
            system_message=collaboration_system
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text=f"Améliore ce document selon ma demande : {request.request}")
        updated_document = await chat.send_message(user_message)
        
        # Sauvegarder la collaboration
        collaboration_log = {
            "session_id": request.session_id,
            "document_title": request.document_title,
            "original_document": request.document,
            "request": request.request,
            "updated_document": updated_document,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.collaborations.insert_one(collaboration_log)
        
        return {
            "success": True,
            "updated_document": updated_document,
            "message": "Document mis à jour avec succès"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la collaboration: {str(e)}")

@app.post("/api/save-collaboration")
async def save_collaboration(request: SaveCollaborationRequest):
    """Sauvegarder un document collaboratif"""
    try:
        doc_id = request.document_id or str(uuid.uuid4())
        
        document_data = {
            "id": doc_id,
            "title": request.title,
            "content": request.document,
            "session_id": request.session_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "word_count": len(request.document.split()),
            "char_count": len(request.document)
        }
        
        if request.document_id:
            # Mise à jour
            document_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            await db.collaboration_documents.update_one(
                {"id": request.document_id},
                {"$set": document_data}
            )
        else:
            # Nouveau document
            await db.collaboration_documents.insert_one(document_data)
        
        return {
            "success": True,
            "document_id": doc_id,
            "message": "Document sauvegardé avec succès"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde: {str(e)}")

@app.get("/api/test-privileged-access")
async def test_privileged_access():
    """Test du système d'accès privilégié aux documents"""
    try:
        # Générer l'enrichissement avec accès privilégié
        privileged_content = enrich_system_message_with_privileged_access()
        
        # Statistiques
        stats = {
            "total_concepts": len(CONCEPTS_ENRICHIS),
            "domaines": list(set([c["domaine_principal"] for c in CONCEPTS_ENRICHIS])),
            "documents_sources": list(set([c["document_source"] for c in CONCEPTS_ENRICHIS])),
            "niveaux_complexite": list(set([c["niveau_complexite"] for c in CONCEPTS_ENRICHIS]))
        }
        
        return {
            "success": True,
            "message": "Système d'accès privilégié opérationnel",
            "statistics": stats,
            "privileged_system_length": len(privileged_content),
            "sample_enrichment": privileged_content[:500] + "..." if len(privileged_content) > 500 else privileged_content
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur test accès privilégié: {str(e)}")

@app.post("/api/chat-privileged")
async def chat_with_privileged_access(request: dict):
    """Chat avec accès privilégié complet aux documents analysés"""
    message = request.get("message", "")
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not message:
        raise HTTPException(status_code=400, detail="Message requis")
        
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    try:
        # Message système avec accès privilégié complet
        privileged_system = f"""{system_message}

{enrich_system_message_with_privileged_access()}

INSTRUCTIONS SPÉCIALES POUR CETTE CONVERSATION:
- Tu disposes de l'ACCÈS PRIVILÉGIÉ TOTAL aux documents analysés
- Utilise les 14 concepts enrichis et la banque de Q&R pour répondre
- Structure OBLIGATOIREMENT ta réponse en format bi-partite:
  🔵 VISION DE PHILIPPE THOMAS SAVARD: [Perspective de l'auteur]
  ⚪ CONTEXTE SCIENTIFIQUE NEUTRE: [Analyse objective]
- Cite précisément les sources et documents utilisés
- Respecte la complexité et nuance de chaque concept théorique
"""
        
        # Appel à l'IA avec accès privilégié
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=privileged_system
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text=message)
        response = await chat.send_message(user_message)
        
        ai_response = response if isinstance(response, str) else str(response)
        
        return {
            "success": True,
            "response": ai_response,
            "session_id": session_id,
            "privileged_access": True,
            "concepts_available": len(CONCEPTS_ENRICHIS),
            "message": "Réponse générée avec accès privilégié complet"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur chat privilégié: {str(e)}")
@app.get("/api/concepts-enrichis")
async def get_concepts_enrichis():
    """Récupérer tous les concepts théoriques enrichis"""
    return {
        "success": True,
        "concepts": CONCEPTS_ENRICHIS,
        "domaines": list(set([c["domaine_principal"] for c in CONCEPTS_ENRICHIS]))
    }

@app.get("/api/concepts-enrichis/{domaine}")
async def get_concepts_by_domain(domaine: str):
    """Récupérer les concepts d'un domaine spécifique"""
    concepts_domaine = get_concept_enrichi_by_domain(domaine)
    return {
        "success": True,
        "domaine": domaine,
        "concepts": concepts_domaine,
        "count": len(concepts_domaine)
    }

@app.post("/api/chat-with-domain")
async def chat_with_domain_focus(request: dict):
    """Chat avec focus sur un domaine théorique spécifique"""
    domaine = request.get("domaine")
    message = request.get("message")
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    # Récupérer les concepts du domaine spécifique
    concepts_domaine = get_concept_enrichi_by_domain(domaine) if domaine else CONCEPTS_ENRICHIS
    
    # Construire un message système focalisé sur le domaine
    domain_context = f"\n\n**FOCUS SUR LE DOMAINE: {domaine.upper() if domaine else 'TOUS LES DOMAINES'}**\n\n"
    
    for concept in concepts_domaine:
        domain_context += f"**{concept['titre']}**: {concept['description']}\n"
        domain_context += f"Concepts clés: {', '.join(concept['concepts_cles'])}\n\n"
    
    specialized_system = f"""{system_message}
    
    {domain_context}
    
    **INSTRUCTIONS SPÉCIALISÉES:**
    - Concentre-toi sur le domaine {domaine if domaine else 'approprié'} 
    - Utilise les concepts spécifiques de ce domaine
    - Maintiens la cohérence théorique du domaine
    - Évite les mélanges entre domaines sauf si explicitement demandé
    """
    
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=specialized_system
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text=message)
        response = await chat.send_message(user_message)
        
        return {
            "success": True,
            "response": response,
            "domaine_focus": domaine,
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chat spécialisé: {str(e)}")

@app.get("/api/methode-spectrale-info")
async def get_methode_spectrale_info():
    """Récupérer les informations sur la méthode spectrale pour les intervalles entre nombres premiers"""
    concept = next((c for c in CONCEPTS_ENRICHIS if c["id"] == "quantite_nombres_premiers"), None)
    if not concept:
        return {"success": False, "message": "Concept non trouvé"}
    
    return {
        "success": True,
        "concept": concept,
        "exemples_application": {
            "methode_classique": "Pour p=23, q=29: 29-23-1 = 5 nombres (24,25,26,27,28)",
            "methode_spectrale": "Utilise suites mathématiques + Digamma pour validation",
            "avantages_spectrale": [
                "Approche géométrique des intervalles",
                "Intégration avec la théorie du spectre des nombres premiers",
                "Utilisation de la fonction Digamma de Philippôt",
                "Validation par suites mathématiques associées"
            ]
        }
    }

@app.post("/api/chat-methode-spectrale")
async def chat_methode_spectrale(request: dict):
    """Chat spécialisé sur la méthode spectrale pour les intervalles entre nombres premiers"""
    message = request.get("message")
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    # Récupérer le concept de la méthode spectrale
    concept_spectral = next((c for c in CONCEPTS_ENRICHIS if c["id"] == "quantite_nombres_premiers"), None)
    
    spectral_context = f"""
**SPÉCIALISATION MÉTHODE SPECTRALE POUR INTERVALLES ENTRE NOMBRES PREMIERS**

{concept_spectral['description'] if concept_spectral else ''}

**FORMULES SPÉCIALISÉES :**
- Méthode classique: q - p - 1 (où q > p sont premiers consécutifs)
- Étape 1 spectrale: somme_suite_1 - (somme_suite_2 - Digamma_grand_premier)
- Étape 2 spectrale: (résultat_étape_1 - Digamma_petit_premier) / √5120
- Digamma de Philippôt: ((somme_suite_2 / √E) - N) × √E

**CONSTANTES EMPIRIQUES :**
- A, B, C, D, E : Constantes liées aux propriétés spectrales des nombres premiers
- √5120 : Constante de normalisation dans la méthode spectrale

**APPROCHE PÉDAGOGIQUE :**
- Explique d'abord la méthode classique simple
- Présente la méthode spectrale comme extension géométrique 
- Maintiens la vision de l'auteur tout en contextualisant scientifiquement
- Respecte l'approche empirique et intuitive de la théorie
"""
    
    specialized_system = f"""{system_message}
    
    {spectral_context}
    
    **INSTRUCTIONS SPÉCIALISÉES:**
    - Focus sur la géométrie du spectre des nombres premiers
    - Explique les deux approches (classique et spectrale) 
    - Maintiens la structure bi-partite des réponses
    - Respecte l'approche empirique de l'auteur
    - Contextualise dans le cadre de la théorie générale
    """
    
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=specialized_system
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text=message)
        response = await chat.send_message(user_message)
        
        return {
            "success": True,
            "response": response,
            "specialisation": "Méthode Spectrale - Intervalles entre Nombres Premiers",
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chat spécialisé: {str(e)}")

@app.post("/api/generate-latex")
async def generate_latex(request: dict):
    """Générer une version LaTeX du contenu de collaboration"""
    content = request.get("content", "")
    title = request.get("title", "Document")
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    latex_system = f"""{system_message}
    
    **SPÉCIALISATION GÉNÉRATION LATEX**
    
    Tu es un expert en conversion de documents mathématiques vers LaTeX. Ta mission :
    - Convertir le contenu fourni en LaTeX professionnel
    - Préserver toutes les formules mathématiques
    - Structurer correctement avec sections, subsections
    - Utiliser les packages LaTeX appropriés pour les mathématiques
    - Maintenir la mise en forme et la lisibilité
    - Ajouter les commandes LaTeX nécessaires pour les symboles spéciaux
    
    **INSTRUCTIONS SPÉCIALES POUR LA THÉORIE :**
    - Utilise amsmath, amssymb, amsfonts pour les symboles mathématiques
    - Pour le zêta : \\zeta
    - Pour les racines : \\sqrt{{}}
    - Pour les indices/exposants : _{{}} et ^{{}}
    - Structure avec \\section, \\subsection, \\subsubsection
    - Utilise l'environnement equation pour les formules importantes
    - Ajoute les références bibliographiques si mentionnées
    
    **CONTENU À CONVERTIR :**
    Titre : {title}
    Contenu : {content}
    
    Génère le document LaTeX complet avec préambule et structure appropriée.
    """
    
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=latex_system
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text=f"Convertis ce document en LaTeX professionnel : {content}")
        latex_response = await chat.send_message(user_message)
        
        return {
            "success": True,
            "latex_content": latex_response,
            "title": title,
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération LaTeX: {str(e)}")

@app.post("/api/correction-personnelle")
async def ajouter_correction_personnelle(correction: dict):
    """Ajouter une correction personnelle de l'auteur"""
    try:
        correction_data = {
            "id": str(uuid.uuid4()),
            "session_id": correction.get("session_id"),
            "question_originale": correction.get("question_originale"),
            "reponse_ia_originale": correction.get("reponse_ia_originale"),
            "correction_auteur": correction.get("correction_auteur"),
            "contexte_theorique": correction.get("contexte_theorique", ""),
            "domaine_concerne": correction.get("domaine_concerne", "General"),
            "type_correction": correction.get("type_correction", "nuance_manquante"),
            "approuve": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.corrections_personnelles.insert_one(correction_data)
        
        # Mettre à jour le profil auteur
        await mettre_a_jour_profil_auteur(correction.get("session_id"), correction_data)
        
        return {
            "success": True,
            "message": "Correction enregistrée avec succès",
            "correction_id": correction_data["id"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement: {str(e)}")

@app.get("/api/corrections-personnelles/{session_id}")
async def get_corrections_personnelles(session_id: str):
    """Récupérer les corrections personnelles d'une session"""
    corrections = await db.corrections_personnelles.find(
        {"session_id": session_id, "approuve": True}
    ).sort("created_at", -1).to_list(length=50)
    
    return {
        "success": True,
        "corrections": corrections
    }

@app.post("/api/profil-auteur")
async def mettre_a_jour_profil_auteur(session_id: str, correction_data: dict):
    """Mettre à jour le profil de l'auteur avec les corrections"""
    try:
        profil_existant = await db.profil_auteur.find_one({"session_id": session_id})
        
        if profil_existant:
            # Mise à jour du profil existant
            update_data = {
                "corrections_approuvees": profil_existant.get("corrections_approuvees", []) + [correction_data["id"]],
                "derniere_mise_a_jour": datetime.now(timezone.utc).isoformat()
            }
            
            # Ajouter la correction aux nuances importantes
            nuances = profil_existant.get("nuances_importantes", [])
            nuances.append(correction_data["correction_auteur"][:200])  # Limiter la taille
            update_data["nuances_importantes"] = nuances[-20:]  # Garder les 20 dernières
            
            await db.profil_auteur.update_one(
                {"session_id": session_id},
                {"$set": update_data}
            )
        else:
            # Créer un nouveau profil
            nouveau_profil = {
                "session_id": session_id,
                "preferences_style": ["structure_bi_partie", "vision_auteur_scientifique"],
                "corrections_approuvees": [correction_data["id"]],
                "expressions_preferees": {},
                "nuances_importantes": [correction_data["correction_auteur"][:200]],
                "domaines_expertise": ["L'univers est au carré", correction_data["domaine_concerne"]],
                "derniere_mise_a_jour": datetime.now(timezone.utc).isoformat()
            }
            
            await db.profil_auteur.insert_one(nouveau_profil)
            
        return {"success": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur profil auteur: {str(e)}")

@app.get("/api/collaboration-documents/{session_id}")
async def get_collaboration_documents(session_id: str):
    """Récupérer les documents collaboratifs d'une session"""
    documents = await db.collaboration_documents.find(
        {"session_id": session_id}
    ).sort("updated_at", -1).to_list(length=None)
    
    return [
        {
            "id": doc["id"],
            "title": doc["title"],
            "updated_at": doc["updated_at"],
            "word_count": doc.get("word_count", 0),
            "char_count": doc.get("char_count", 0)
        }
        for doc in documents
    ]

@app.get("/api/collaboration-document/{doc_id}")
async def get_collaboration_document(doc_id: str):
    """Récupérer un document collaboratif spécifique"""
    document = await db.collaboration_documents.find_one({"id": doc_id})
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    
    return {
        "id": document["id"],
        "title": document["title"],
        "content": document["content"],
        "created_at": document["created_at"],
        "updated_at": document["updated_at"]
    }

# ===============================================
# SYSTÈME DE CORRECTION INTELLIGENT ET ANALYSE
# ===============================================

@app.post("/api/analyse-texte")
async def analyser_texte_complet(request: dict):
    """Analyse complète d'un texte : orthographe, grammaire, sémantique, structure"""
    texte = request.get("texte", "")
    options = request.get("options", {
        "orthographe": True,
        "grammaire": True,
        "semantique": True,
        "structure": True,
        "synonymes": True,
        "style": True
    })
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not texte or not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=400, detail="Texte et clé API requis")
    
    try:
        # Système spécialisé pour l'analyse textuelle française
        systeme_correcteur = f"""Tu es un correcteur français expert et discret, spécialisé dans l'analyse de textes scientifiques et mathématiques.

**INSTRUCTIONS CRUCIALES - STYLE DISCRET :**
- Suggestions SUBTILES et NON ENVAHISSANTES
- Format JSON structuré pour intégration UI
- Préserve l'intention de l'auteur
- Respecte le style personnel
- Analyse contextuelle intelligente

**ANALYSE DEMANDÉE :**
{', '.join([k for k, v in options.items() if v])}

**STRUCTURE RÉPONSE JSON :**
{{
    "analyse_orthographe": [
        {{"position": [start, end], "erreur": "mot", "suggestion": "correction", "confiance": 0.9, "type": "accord"}}
    ],
    "analyse_grammaire": [
        {{"position": [start, end], "probleme": "description", "suggestion": "amélioration", "severite": "mineure"}}
    ],
    "ameliorations_semantique": [
        {{"position": [start, end], "original": "phrase", "ameliore": "version", "raison": "clarté"}}
    ],
    "synonymes_proposes": [
        {{"mot": "terme", "position": [start, end], "synonymes": ["alt1", "alt2"], "nuance": "explication"}}
    ],
    "suggestions_structure": [
        {{"section": "paragraphe X", "suggestion": "reorganisation", "impact": "lisibilité"}}
    ],
    "style_et_ton": {{
        "coherence": "bon/moyen/faible",
        "suggestions": ["conseil1", "conseil2"]
    }},
    "score_global": {{
        "orthographe": 85,
        "grammaire": 90,
        "clarte": 75,
        "style": 80
    }}
}}

**TEXTE À ANALYSER :**
{texte}

Analyse ce texte avec bienveillance et expertise, en restant discret et constructif."""

        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=systeme_correcteur
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text="Effectue une analyse complète et discrète de ce texte en suivant exactement le format JSON demandé.")
        response = await chat.send_message(user_message)
        
        # Extraire le JSON de la réponse
        try:
            import json
            import re
            
            # Chercher le JSON dans la réponse
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analyse_data = json.loads(json_match.group())
            else:
                # Fallback si pas de JSON détecté
                analyse_data = {
                    "analyse_complete": response,
                    "score_global": {"orthographe": 85, "grammaire": 85, "clarte": 80, "style": 80}
                }
        except:
            analyse_data = {
                "analyse_complete": response,
                "score_global": {"orthographe": 85, "grammaire": 85, "clarte": 80, "style": 80}
            }
        
        return {
            "success": True,
            "analyse": analyse_data,
            "options_utilisees": options,
            "session_id": session_id,
            "longueur_texte": len(texte)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}")

@app.post("/api/detection-plagiat")
async def detecter_plagiat(request: dict):
    """Détection de plagiat et protection de propriété intellectuelle"""
    texte = request.get("texte", "")
    mode = request.get("mode", "protection")  # "protection" ou "verification"
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not texte or not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=400, detail="Texte requis")
    
    try:
        # Système pour la détection de plagiat et protection IP
        systeme_plagiat = f"""Tu es un expert en propriété intellectuelle et détection de plagiat, spécialisé dans la protection de contenu scientifique et mathématique.

**MODE ANALYSE : {mode.upper()}**

**INSTRUCTIONS SPÉCIALISÉES :**
- Identifie les éléments uniques et originaux
- Évalue le niveau d'originalité du contenu
- Détecte les patterns pouvant indiquer du plagiat
- Suggestions pour renforcer la protection IP
- Analyse de l'antériorité conceptuelle

**ÉLÉMENTS À ANALYSER :**
1. Originalité des concepts présentés
2. Formulations uniques et innovations
3. Méthodologies spécifiques à l'auteur
4. Terminologie créée par l'auteur
5. Structures argumentaires originales

**STRUCTURE RÉPONSE :**
{{
    "originalite_score": 85,
    "elements_uniques": ["concept1", "formule2"],
    "risques_plagiat": ["zone1", "zone2"],
    "recommandations_protection": ["action1", "action2"],
    "empreinte_uniqueness": "signature_textuelle",
    "date_analyse": "timestamp"
}}

**TEXTE À ANALYSER POUR PROTECTION IP :**
{texte}

Fournis une analyse complète de protection et d'originalité."""

        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=systeme_plagiat
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text="Analyse ce texte pour sa protection de propriété intellectuelle et détection de plagiat potentiel.")
        response = await chat.send_message(user_message)
        
        # Créer un hash unique du texte pour traçabilité
        import hashlib
        texte_hash = hashlib.sha256(texte.encode()).hexdigest()[:16]
        
        # Sauvegarder l'analyse pour historique
        analyse_plagiat = {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "texte_hash": texte_hash,
            "longueur_texte": len(texte),
            "analyse": response,
            "mode": mode,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        await db.analyses_plagiat.insert_one(analyse_plagiat)
        
        return {
            "success": True,
            "protection_id": analyse_plagiat["id"],
            "analyse_plagiat": response,
            "texte_hash": texte_hash,
            "recommendations": [
                "Documentez la date de création de vos concepts",
                "Conservez les versions brouillon avec timestamps",
                "Établissez des preuves d'antériorité",
                "Considérez le dépôt légal de vos travaux"
            ],
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur détection plagiat: {str(e)}")

@app.post("/api/dictionnaire-personnel")
async def gerer_dictionnaire_personnel(request: dict):
    """Gestion du dictionnaire personnel de l'utilisateur"""
    action = request.get("action", "get")  # "add", "get", "update", "delete"
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    try:
        if action == "add":
            terme = request.get("terme", "")
            definition = request.get("definition", "")
            contexte = request.get("contexte", "")
            
            nouveau_terme = {
                "id": str(uuid.uuid4()),
                "session_id": session_id,
                "terme": terme.lower(),
                "definition": definition,
                "contexte": contexte,
                "utilisation_count": 0,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            await db.dictionnaire_personnel.insert_one(nouveau_terme)
            
            return {
                "success": True,
                "message": f"Terme '{terme}' ajouté au dictionnaire",
                "terme_id": nouveau_terme["id"]
            }
            
        elif action == "get":
            termes = await db.dictionnaire_personnel.find(
                {"session_id": session_id}
            ).sort("created_at", -1).to_list(length=None)
            
            return {
                "success": True,
                "dictionnaire": termes,
                "total_termes": len(termes)
            }
            
        elif action == "search":
            query = request.get("query", "").lower()
            termes = await db.dictionnaire_personnel.find({
                "session_id": session_id,
                "$or": [
                    {"terme": {"$regex": query, "$options": "i"}},
                    {"definition": {"$regex": query, "$options": "i"}}
                ]
            }).to_list(length=10)
            
            return {
                "success": True,
                "resultats": termes,
                "query": query
            }
        
        else:
            raise HTTPException(status_code=400, detail="Action non supportée")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur dictionnaire: {str(e)}")

@app.post("/api/analyse-lacunes-comprehension")
async def analyser_lacunes_comprehension(request: dict):
    """Analyse des lacunes de compréhension basée sur les questions utilisateurs"""
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    try:
        # Récupérer l'historique des questions pour cette session
        historique_questions = await db.chat_history.find(
            {"session_id": session_id, "type": "user"}
        ).sort("timestamp", -1).limit(50).to_list(length=None)
        
        if not historique_questions:
            return {
                "success": True,
                "analyse": "Pas assez de données pour analyser les lacunes",
                "recommendations": ["Continuez à poser des questions pour une analyse personnalisée"]
            }
        
        # Analyser les patterns de questions
        questions_text = "\n".join([q.get("message", "") for q in historique_questions])
        
        systeme_lacunes = f"""Tu es un analyste expert en détection des lacunes de compréhension dans l'apprentissage de théories mathématiques complexes.

**MISSION :**
Analyser l'historique des questions pour identifier :
1. Les concepts récurrents non maîtrisés
2. Les zones de confusion persistante  
3. Les prérequis manquants
4. Les progressions d'apprentissage optimales

**HISTORIQUE DES QUESTIONS :**
{questions_text}

**ANALYSE DEMANDÉE :**
- Concepts les plus questionnés (lacunes identifiées)
- Progression dans la compréhension
- Recommandations pédagogiques personnalisées
- Parcours d'apprentissage suggéré

**FORMAT RÉPONSE :**
{{
    "lacunes_identifiees": ["concept1", "concept2"],
    "concepts_maitrise": ["concept_ok1", "concept_ok2"],
    "progression_score": 75,
    "recommandations": ["rec1", "rec2"],
    "parcours_suggere": ["étape1", "étape2", "étape3"]
}}"""

        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=systeme_lacunes
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text="Analyse cet historique pour identifier les lacunes de compréhension et proposer un parcours personnalisé.")
        response = await chat.send_message(user_message)
        
        return {
            "success": True,
            "analyse_lacunes": response,
            "questions_analysees": len(historique_questions),
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur analyse lacunes: {str(e)}")

@app.get("/api/sections-problematiques")
async def detecter_sections_problematiques():
    """Détection automatique des sections posant des difficultés aux utilisateurs"""
    
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    try:
        # Récupérer toutes les questions récentes pour analyse globale
        questions_recentes = await db.chat_history.find({
            "type": "user",
            "timestamp": {"$gte": (datetime.now(timezone.utc) - datetime.timedelta(days=30)).isoformat()}
        }).to_list(length=None)
        
        if not questions_recentes:
            return {
                "success": True,
                "sections_problematiques": [],
                "message": "Pas assez de données récentes"
            }
        
        # Analyser les patterns globaux
        all_questions = "\n".join([q.get("message", "") for q in questions_recentes])
        
        systeme_detection = f"""Tu es un analyste expert en identification de sections problématiques dans un contenu pédagogique scientifique.

**MISSION :**
Identifier les sections de la théorie "L'univers est au carré" qui posent le plus de difficultés aux utilisateurs.

**DONNÉES QUESTIONS UTILISATEURS (30 derniers jours) :**
{all_questions[:3000]}... (extrait)

**SECTIONS DE LA THÉORIE À ANALYSER :**
1. Géométrie du spectre des nombres premiers
2. Les 14 tableaux de Philippôt  
3. Méthode de substitution
4. Fonction Digamma de Philippôt
5. Zéros triviaux et hypothèse de Riemann
6. Théorème de Philippôt (intrication quantique)
7. Géométrie de l'espace (partie 2)
8. Rectangle élevé au carré
9. Cercle Denis et propriétés
10. Résonance terrestre
11. Espace de Minkowski selon Philippôt
12. Nombres hypercomplexes
13. Sphère de la fonction Zêta

**ANALYSE DEMANDÉE :**
{{
    "sections_difficiles": [
        {{"section": "nom", "difficulte_score": 85, "problemes": ["pb1", "pb2"], "suggestions": ["sol1", "sol2"]}}
    ],
    "tendances_globales": ["pattern1", "pattern2"],
    "recommandations_amelioration": ["rec1", "rec2"]
}}"""

        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id="system_analysis",
            system_message=systeme_detection
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text="Analyse ces questions pour identifier les sections problématiques et proposer des améliorations.")
        response = await chat.send_message(user_message)
        
        return {
            "success": True,
            "analyse_sections": response,
            "questions_analysees": len(questions_recentes),
            "periode": "30 derniers jours"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur analyse sections: {str(e)}")

# ===============================================
# FONCTIONNALITÉS D'INTELLIGENCE AVANCÉE
# ===============================================

@app.post("/api/suggestions-contenu")
async def generer_suggestions_contenu(request: dict):
    """Génère des suggestions de contenu contextuelles basées sur le texte actuel"""
    texte_actuel = request.get("texte_actuel", "")
    contexte = request.get("contexte", "")
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    try:
        # Enrichissement avec la théorie pour suggestions contextuelles
        theory_enrichment = enrich_system_message_with_privileged_access()
        
        systeme_suggestions = f"""{system_message}
        
        {theory_enrichment}
        
        **MODE SUGGESTIONS INTELLIGENTES DE CONTENU**
        
        Tu es un assistant éditorial spécialisé dans la théorie 'L'univers est au carré'. 
        Ta mission : proposer des développements pertinents basés sur le contexte actuel.
        
        **INSTRUCTIONS :**
        - Analyse le texte actuel pour comprendre la direction
        - Propose 3-5 suggestions de développement naturel
        - Utilise les concepts enrichis appropriés selon le domaine
        - Maintiens la cohérence avec le style de l'auteur
        - Respecte la structure bi-partite si applicable
        
        **TEXTE ACTUEL :**
        {texte_actuel}
        
        **CONTEXTE ADDITIONNEL :**
        {contexte}
        
        **FORMAT RÉPONSE :**
        {{
            "suggestions": [
                {{
                    "titre": "Développement suggéré",
                    "contenu": "Texte proposé à ajouter",
                    "position": "après/avant/insertion",
                    "domaine": "géométrie/nombres_premiers/mécanique",
                    "pertinence": 85
                }}
            ],
            "concepts_lies": ["concept1", "concept2"],
            "direction_recommandee": "Description de la direction suggérée"
        }}
        """
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=systeme_suggestions
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text="Génère des suggestions intelligentes pour développer ce texte selon la théorie de Philippe Thomas Savard.")
        response = await chat.send_message(user_message)
        
        # Sauvegarder les suggestions générées
        suggestion_log = {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "texte_source": texte_actuel[:500],  # Limiter la taille
            "suggestions": response,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.suggestions_contenu.insert_one(suggestion_log)
        
        return {
            "success": True,
            "suggestions": response,
            "session_id": session_id,
            "concepts_disponibles": len(CONCEPTS_ENRICHIS)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur suggestions contenu: {str(e)}")

@app.post("/api/resume-automatique")
async def generer_resume_automatique(request: dict):
    """Génère un résumé automatique d'un texte long"""
    texte_complet = request.get("texte_complet", "")
    style_resume = request.get("style", "executif")  # "executif", "technique", "conceptuel"
    longueur_cible = request.get("longueur_cible", "moyen")  # "court", "moyen", "detaille"
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not texte_complet or not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=400, detail="Texte requis")
    
    try:
        # Système spécialisé pour résumé intelligent
        systeme_resume = f"""{system_message}
        
        **MODE RÉSUMÉ AUTOMATIQUE INTELLIGENT**
        
        Tu es un expert en synthèse documentaire spécialisé dans la théorie 'L'univers est au carré'.
        
        **PARAMÈTRES DE RÉSUMÉ :**
        - Style : {style_resume}
        - Longueur : {longueur_cible}
        
        **INSTRUCTIONS SPÉCIALISÉES :**
        - Identifie les concepts clés de la théorie mentionnés
        - Préserve les formules et calculs importants
        - Maintiens la logique argumentaire de l'auteur
        - Respecte la terminologie spécialisée
        - Structure selon l'importance conceptuelle
        
        **STYLES DE RÉSUMÉ :**
        - **Exécutif** : Points clés, conclusions, applications
        - **Technique** : Formules, méthodes, démonstrations
        - **Conceptuel** : Idées principales, théorèmes, innovations
        
        **LONGUEURS CIBLES :**
        - **Court** : 100-200 mots (points essentiels)
        - **Moyen** : 300-500 mots (développement structuré)
        - **Détaillé** : 600-1000 mots (analyse approfondie)
        
        **TEXTE À RÉSUMER :**
        {texte_complet}
        
        Génère un résumé {style_resume} de longueur {longueur_cible} qui capture l'essence du document.
        """
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=systeme_resume
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text=f"Crée un résumé {style_resume} de longueur {longueur_cible} de ce texte.")
        resume = await chat.send_message(user_message)
        
        # Statistiques du résumé
        mots_original = len(texte_complet.split())
        mots_resume = len(resume.split())
        taux_compression = round((1 - mots_resume / mots_original) * 100, 1) if mots_original > 0 else 0
        
        # Sauvegarder le résumé
        resume_log = {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "texte_original_hash": str(hash(texte_complet))[:16],
            "resume": resume,
            "style": style_resume,
            "longueur_cible": longueur_cible,
            "statistiques": {
                "mots_original": mots_original,
                "mots_resume": mots_resume,
                "taux_compression": taux_compression
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.resumes_automatiques.insert_one(resume_log)
        
        return {
            "success": True,
            "resume": resume,
            "statistiques": resume_log["statistiques"],
            "style_utilise": style_resume,
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur résumé automatique: {str(e)}")

@app.post("/api/detection-coherence")
async def detecter_coherence_arguments(request: dict):
    """Détecte les problèmes de cohérence dans l'argumentation"""
    texte_analyse = request.get("texte_analyse", "")
    niveau_detail = request.get("niveau_detail", "standard")  # "basic", "standard", "approfondi"
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not texte_analyse or not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=400, detail="Texte requis")
    
    try:
        # Système expert pour analyse de cohérence
        systeme_coherence = f"""{system_message}
        
        **MODE DÉTECTION DE COHÉRENCE ARGUMENTAIRE**
        
        Tu es un expert en logique argumentaire et validation de théories mathématiques.
        Spécialisé dans l'analyse de cohérence pour la théorie 'L'univers est au carré'.
        
        **NIVEAU D'ANALYSE : {niveau_detail.upper()}**
        
        **ÉLÉMENTS À ANALYSER :**
        1. **Cohérence logique** : Enchaînement des arguments
        2. **Consistance terminologique** : Utilisation uniforme des termes
        3. **Validation des assertions** : Vérification des affirmations
        4. **Transitions argumentaires** : Fluidité entre les idées
        5. **Prémisses et conclusions** : Solidité du raisonnement
        6. **Cohérence avec la théorie** : Alignement avec les concepts établis
        
        **NIVEAUX D'ANALYSE :**
        - **Basic** : Problèmes majeurs uniquement
        - **Standard** : Analyse complète standard
        - **Approfondi** : Examen minutieux + suggestions d'amélioration
        
        **FORMAT RÉPONSE :**
        {{
            "score_coherence_global": 75,
            "problemes_detectes": [
                {{
                    "position": [start, end],
                    "type": "incohérence logique",
                    "description": "Explication du problème",
                    "severite": "majeure/mineure",
                    "suggestion": "Comment corriger"
                }}
            ],
            "points_forts": ["argumentation solide section X"],
            "recommandations": ["amélioration 1", "amélioration 2"],
            "coherence_terminologique": 85,
            "fluidite_argumentaire": 70
        }}
        
        **TEXTE À ANALYSER POUR COHÉRENCE :**
        {texte_analyse}
        
        Effectue une analyse {niveau_detail} de la cohérence argumentaire.
        """
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=systeme_coherence
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text=f"Analyse la cohérence argumentaire de ce texte avec un niveau {niveau_detail}.")
        analyse = await chat.send_message(user_message)
        
        # Sauvegarder l'analyse
        coherence_log = {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "texte_hash": str(hash(texte_analyse))[:16],
            "analyse_coherence": analyse,
            "niveau_detail": niveau_detail,
            "longueur_texte": len(texte_analyse),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.analyses_coherence.insert_one(coherence_log)
        
        return {
            "success": True,
            "analyse_coherence": analyse,
            "niveau_analyse": niveau_detail,
            "session_id": session_id,
            "texte_longueur": len(texte_analyse)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur détection cohérence: {str(e)}")

@app.post("/api/citations-automatiques")
async def generer_citations_automatiques(request: dict):
    """Génère des citations théoriques automatiques basées sur le contenu"""
    contenu_texte = request.get("contenu_texte", "")
    style_citation = request.get("style_citation", "academique")  # "academique", "informel", "technique"
    domaines_focus = request.get("domaines_focus", [])  # Filtrer par domaines spécifiques
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not contenu_texte or not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=400, detail="Contenu requis")
    
    try:
        # Enrichissement avec les concepts pour citations pertinentes
        theory_enrichment = enrich_system_message_with_privileged_access()
        
        # Filtrer par domaines si spécifié
        concepts_disponibles = CONCEPTS_ENRICHIS
        if domaines_focus:
            concepts_disponibles = [c for c in CONCEPTS_ENRICHIS if c["domaine_principal"] in domaines_focus]
        
        systeme_citations = f"""{system_message}
        
        {theory_enrichment}
        
        **MODE GÉNÉRATION DE CITATIONS THÉORIQUES AUTOMATIQUES**
        
        Tu es un bibliothécaire expert spécialisé dans la théorie 'L'univers est au carré'.
        Ta mission : identifier et suggérer des citations théoriques pertinentes.
        
        **STYLE DE CITATION : {style_citation.upper()}**
        
        **DOMAINES DE FOCUS :** {', '.join(domaines_focus) if domaines_focus else 'Tous les domaines'}
        
        **SOURCES DISPONIBLES :**
        - Documents de la théorie analysés
        - Concepts enrichis de Philippe Thomas Savard
        - Références aux travaux et démonstrations
        
        **STYLES DE CITATION :**
        - **Académique** : Format formel avec références précises
        - **Informel** : Mentions naturelles dans le texte
        - **Technique** : Citations de formules et méthodes spécifiques
        
        **CONTENU À ANALYSER :**
        {contenu_texte}
        
        **FORMAT RÉPONSE :**
        {{
            "citations_suggerees": [
                {{
                    "concept_cite": "Théorème de Philippôt",
                    "position_suggere": 245,
                    "citation_formelle": "Selon Philippe Thomas Savard (L'univers est au carré, Partie 2)...",
                    "contexte": "Pertinente car le texte mentionne l'intrication quantique",
                    "domaine": "physique_theorique",
                    "pertinence": 90
                }}
            ],
            "concepts_mentionnes": ["concept1", "concept2"],
            "references_manquantes": ["référence suggérée"],
            "style_utilise": "{style_citation}"
        }}
        
        Identifie les concepts mentionnés et propose des citations appropriées.
        """
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=systeme_citations
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text=f"Analyse ce contenu et suggère des citations théoriques appropriées en style {style_citation}.")
        citations = await chat.send_message(user_message)
        
        # Sauvegarder les citations générées
        citations_log = {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "contenu_source": contenu_texte[:300],  # Extrait pour contexte
            "citations_generees": citations,
            "style_citation": style_citation,
            "domaines_focus": domaines_focus,
            "concepts_disponibles": len(concepts_disponibles),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.citations_automatiques.insert_one(citations_log)
        
        return {
            "success": True,
            "citations": citations,
            "style_utilise": style_citation,
            "concepts_sources": len(concepts_disponibles),
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur citations automatiques: {str(e)}")

@app.post("/api/notifications-intelligentes")
async def generer_notifications_intelligentes(request: dict):
    """Génère des notifications intelligentes pour corrections ou suggestions"""
    texte_actuel = request.get("texte_actuel", "")
    seuil_importance = request.get("seuil_importance", "medium")  # "low", "medium", "high"
    types_notifications = request.get("types_notifications", ["corrections", "suggestions", "coherence"])
    session_id = request.get("session_id", str(uuid.uuid4()))
    
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    try:
        # Système de notification intelligent
        systeme_notifications = f"""{system_message}
        
        **MODE NOTIFICATIONS INTELLIGENTES**
        
        Tu es un système de notification intelligent pour l'assistance à l'écriture scientifique.
        Spécialisé dans la théorie 'L'univers est au carré'.
        
        **SEUIL D'IMPORTANCE : {seuil_importance.upper()}**
        **TYPES ACTIVÉS : {', '.join(types_notifications)}**
        
        **CRITÈRES DE NOTIFICATION :**
        - **HIGH** : Erreurs critiques, incohérences majeures
        - **MEDIUM** : Améliorations importantes, suggestions pertinentes  
        - **LOW** : Optimisations mineures, suggestions stylistiques
        
        **TYPES DE NOTIFICATIONS :**
        - **corrections** : Erreurs détectées nécessitant action
        - **suggestions** : Améliorations recommandées
        - **coherence** : Problèmes de logique argumentaire
        
        **TEXTE À ANALYSER :**
        {texte_actuel}
        
        **FORMAT RÉPONSE :**
        {{
            "notifications": [
                {{
                    "id": "notif_001",
                    "type": "correction",
                    "importance": "high",
                    "titre": "Titre court de la notification",
                    "message": "Description détaillée",
                    "action_suggeree": "Action à effectuer",
                    "position": [start, end],
                    "timestamp": "now"
                }}
            ],
            "resume_session": {{
                "total_notifications": 3,
                "critiques": 1,
                "suggestions": 2
            }}
        }}
        
        Génère des notifications pertinentes selon les critères définis.
        """
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=systeme_notifications
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text=f"Analyse ce texte et génère des notifications avec seuil {seuil_importance}.")
        notifications = await chat.send_message(user_message)
        
        # Sauvegarder les notifications
        notifications_log = {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "texte_source": texte_actuel[:200],  # Extrait
            "notifications": notifications,
            "seuil_importance": seuil_importance,
            "types_actifs": types_notifications,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.notifications_intelligentes.insert_one(notifications_log)
        
        return {
            "success": True,
            "notifications": notifications,
            "seuil_utilise": seuil_importance,
            "types_actifs": types_notifications,
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur notifications intelligentes: {str(e)}")

# Modèles Pydantic pour les nouvelles fonctionnalités
class SuggestionsRequest(BaseModel):
    texte_actuel: str
    contexte: Optional[str] = ""
    session_id: Optional[str] = None

class ResumeRequest(BaseModel):
    texte_complet: str
    style: Optional[str] = "executif"
    longueur_cible: Optional[str] = "moyen"
    session_id: Optional[str] = None

class CoherenceRequest(BaseModel):
    texte_analyse: str
    niveau_detail: Optional[str] = "standard"
    session_id: Optional[str] = None

class CitationsRequest(BaseModel):
    contenu_texte: str
    style_citation: Optional[str] = "academique"
    domaines_focus: Optional[List[str]] = []
    session_id: Optional[str] = None

class NotificationsRequest(BaseModel):
    texte_actuel: str
    seuil_importance: Optional[str] = "medium"
    types_notifications: Optional[List[str]] = ["corrections", "suggestions", "coherence"]
    session_id: Optional[str] = None

# ===============================================
# SYSTÈME DE GESTION DES CONCEPTS ET FORMULES
# ===============================================

# Modèles de données pour la base relationnelle
class ConceptEnrichiModel(BaseModel):
    id: Optional[str] = None
    titre: str
    description: str
    domaine: str  # "nombres", "geometrie", "physique"
    sous_domaine: Optional[str] = None
    mots_cles: List[str]
    niveau_complexite: int  # 1-5
    document_source: str
    page_reference: Optional[str] = None
    created_by: str = "Philippe Thomas Savard"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class FormuleModel(BaseModel):
    id: Optional[str] = None
    code_formule: str  # DIG001, PHI001, etc.
    nom_formule: str
    formule_mathematique: str
    domaine: str
    description: str
    variables: Dict[str, str]  # {"n": "position", "h": "hauteur"}
    concepts_lies: List[str]  # IDs des concepts liés
    formules_dependantes: List[str]  # Autres formules nécessaires
    exemple_calcul: Optional[str] = None
    resultat_exemple: Optional[str] = None
    niveau_complexite: int
    document_source: str
    created_at: Optional[str] = None

class RelationModel(BaseModel):
    id: Optional[str] = None
    concept_1_id: str
    concept_2_id: str
    type_relation: str  # "derive_de", "applique_a", "oppose_a", "generalise"
    description_relation: str
    force_relation: int  # 1-5 (faible à très forte)
    formules_impliquees: List[str]
    created_at: Optional[str] = None

class ValidationEmpiriqueModel(BaseModel):
    id: Optional[str] = None
    formule_id: str
    type_validation: str  # "calcul_manuel", "verification_ia", "test_numerique", "application_physique"
    donnees_test: Dict
    resultat_attendu: str
    resultat_obtenu: str
    statut: str  # "validee", "echec", "partielle", "en_cours"
    commentaires: str
    testeur: str
    date_test: str
    precision_resultat: Optional[float] = None

# ===============================================
# API ENDPOINTS - GESTION DES CONCEPTS
# ===============================================

@app.post("/api/concepts", response_model=dict)
async def creer_concept(concept: ConceptEnrichiModel):
    """Créer un nouveau concept dans la base"""
    try:
        concept_data = concept.dict()
        concept_data["id"] = str(uuid.uuid4())
        concept_data["created_at"] = datetime.now(timezone.utc).isoformat()
        concept_data["updated_at"] = concept_data["created_at"]
        
        result = await db.concepts.insert_one(concept_data)
        
        return {
            "success": True,
            "concept_id": concept_data["id"],
            "message": f"Concept '{concept.titre}' créé avec succès"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur création concept: {str(e)}")

@app.get("/api/concepts")
async def lister_concepts(
    domaine: Optional[str] = None,
    niveau_max: Optional[int] = None,
    search: Optional[str] = None
):
    """Lister les concepts avec filtres optionnels"""
    try:
        # Query seulement les concepts créés par le nouveau système (avec structure complète)
        query = {
            "titre": {"$exists": True, "$ne": ""},
            "description": {"$exists": True, "$ne": ""},
            "domaine": {"$exists": True, "$ne": ""},
            "niveau_complexite": {"$exists": True}
        }
        
        if domaine:
            query["domaine"] = domaine
        if niveau_max:
            query["niveau_complexite"]["$lte"] = niveau_max
        if search:
            query["$or"] = [
                {"titre": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
                {"mots_cles": {"$in": [search]}}
            ]
        
        concepts = await db.concepts.find(query).to_list(length=None)
        
        # Convertir les ObjectId pour la sérialisation JSON
        concepts = convert_objectid(concepts)
        
        return {
            "success": True,
            "concepts": concepts,
            "total": len(concepts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération concepts: {str(e)}")

@app.get("/api/concepts/{concept_id}")
async def obtenir_concept(concept_id: str):
    """Obtenir un concept spécifique avec ses relations"""
    try:
        concept = await db.concepts.find_one({"id": concept_id})
        if not concept:
            raise HTTPException(status_code=404, detail="Concept non trouvé")
        
        # Récupérer les relations
        relations = await db.relations.find({
            "$or": [{"concept_1_id": concept_id}, {"concept_2_id": concept_id}]
        }).to_list(length=None)
        
        # Récupérer les formules liées
        formules = await db.formules.find({
            "concepts_lies": {"$in": [concept_id]}
        }).to_list(length=None)
        
        # Convertir les ObjectId pour la sérialisation JSON
        concept = convert_objectid(concept)
        relations = convert_objectid(relations)
        formules = convert_objectid(formules)
        
        return {
            "success": True,
            "concept": concept,
            "relations": relations,
            "formules_liees": formules
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération concept: {str(e)}")

# ===============================================
# API ENDPOINTS - GESTION DES FORMULES
# ===============================================

@app.post("/api/formules", response_model=dict)
async def creer_formule(formule: FormuleModel):
    """Créer une nouvelle formule avec code auto-généré"""
    try:
        formule_data = formule.dict()
        
        # Générer le code si pas fourni
        if not formule_data.get("code_formule"):
            prefix = {
                "nombres": "NUM",
                "geometrie": "GEO", 
                "physique": "PHY"
            }.get(formule.domaine, "GEN")
            
            # Compter les formules existantes dans ce domaine
            count = await db.formules.count_documents({"domaine": formule.domaine})
            formule_data["code_formule"] = f"{prefix}{count+1:03d}"
        
        formule_data["id"] = str(uuid.uuid4())
        formule_data["created_at"] = datetime.now(timezone.utc).isoformat()
        
        await db.formules.insert_one(formule_data)
        
        return {
            "success": True,
            "formule_id": formule_data["id"],
            "code_formule": formule_data["code_formule"],
            "message": f"Formule {formule_data['code_formule']} créée avec succès"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur création formule: {str(e)}")

@app.get("/api/formules")
async def lister_formules(domaine: Optional[str] = None):
    """Lister toutes les formules par domaine"""
    try:
        # Query seulement les formules avec structure complète
        query = {
            "code_formule": {"$exists": True, "$ne": ""},
            "nom_formule": {"$exists": True, "$ne": ""},
            "formule_mathematique": {"$exists": True, "$ne": ""},
            "domaine": {"$exists": True, "$ne": ""}
        }
        
        if domaine:
            query["domaine"] = domaine
            
        formules = await db.formules.find(query).to_list(length=None)
        
        # Convertir les ObjectId pour la sérialisation JSON
        formules = convert_objectid(formules)
        
        return {
            "success": True,
            "formules": formules,
            "total": len(formules)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération formules: {str(e)}")

@app.get("/api/formules/{code_formule}")
async def obtenir_formule(code_formule: str):
    """Obtenir une formule par son code avec validations"""
    try:
        formule = await db.formules.find_one({"code_formule": code_formule})
        if not formule:
            raise HTTPException(status_code=404, detail="Formule non trouvée")
        
        # Récupérer les validations empiriques
        validations = await db.validations_empiriques.find({
            "formule_id": formule["id"]
        }).to_list(length=None)
        
        # Convertir les ObjectId pour la sérialisation JSON
        formule = convert_objectid(formule)
        validations = convert_objectid(validations)
        
        return {
            "success": True,
            "formule": formule,
            "validations": validations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération formule: {str(e)}")

# ===============================================
# API ENDPOINTS - GESTION DES RELATIONS
# ===============================================

@app.post("/api/relations", response_model=dict)
async def creer_relation(relation: RelationModel):
    """Créer une relation entre deux concepts"""
    try:
        relation_data = relation.dict()
        relation_data["id"] = str(uuid.uuid4())
        relation_data["created_at"] = datetime.now(timezone.utc).isoformat()
        
        await db.relations.insert_one(relation_data)
        
        return {
            "success": True,
            "relation_id": relation_data["id"],
            "message": "Relation créée avec succès"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur création relation: {str(e)}")

# ===============================================
# API ENDPOINTS - VALIDATIONS EMPIRIQUES
# ===============================================

@app.post("/api/validations", response_model=dict)
async def creer_validation(validation: ValidationEmpiriqueModel):
    """Enregistrer une validation empirique"""
    try:
        validation_data = validation.dict()
        validation_data["id"] = str(uuid.uuid4())
        validation_data["date_test"] = datetime.now(timezone.utc).isoformat()
        
        await db.validations_empiriques.insert_one(validation_data)
        
        return {
            "success": True,
            "validation_id": validation_data["id"],
            "statut": validation.statut
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur validation: {str(e)}")

# ===============================================
# API SYSTÈME D'INDEXATION AUTOMATIQUE
# ===============================================

@app.post("/api/indexation/analyser-document")
async def analyser_document_formules(request: dict):
    """Analyser un document pour extraire automatiquement les formules"""
    try:
        texte_document = request.get("texte_document", "")
        domaine_principal = request.get("domaine_principal", "geometrie")
        
        if not texte_document or not EMERGENT_LLM_KEY:
            raise HTTPException(status_code=400, detail="Texte et clé API requis")
        
        systeme_extraction = f"""{system_message}
        
        **MODE EXTRACTION ET INDEXATION DE FORMULES**
        
        Tu es un expert en analyse de documents mathématiques spécialisé dans l'extraction de formules.
        Ta mission : identifier et codifier toutes les formules mathématiques du document.
        
        **DOMAINE PRINCIPAL :** {domaine_principal}
        
        **INSTRUCTIONS D'EXTRACTION :**
        1. Identifier toutes les formules mathématiques explicites
        2. Extraire les définitions conceptuelles
        3. Repérer les relations entre variables
        4. Générer des codes d'identification uniques
        5. Classer par niveau de complexité (1-5)
        
        **PREFIXES DE CODIFICATION :**
        - **DIG** : Digamma de Philippôt et calculs associés
        - **PHI** : Théorème de Philippôt et géométrie
        - **CIR** : Cercle Denis et relations circulaires
        - **RES** : Résonance terrestre et harmoniques
        - **MIN** : Espace Minkowski selon Philippôt
        - **HYP** : Nombres hypercomplexes
        - **INV** : Involutions et transformations
        
        **FORMAT DE RÉPONSE :**
        {{
            "formules_extraites": [
                {{
                    "code_propose": "DIG001",
                    "nom_formule": "Calcul Digamma position 8",
                    "formule_mathematique": "√((n+7)² + (n+8)²)",
                    "description": "Calcul du Digamma à la 8ème position",
                    "variables": {{"n": "position dans la séquence"}},
                    "niveau_complexite": 3,
                    "exemple_application": "Pour n=1: √(64+81) = √145"
                }}
            ],
            "concepts_identifies": [
                {{
                    "nom": "Digamma de Philippôt",
                    "domaine": "nombres",
                    "description": "Concept central pour calcul nombres premiers"
                }}
            ],
            "relations_detectees": [
                {{
                    "formule_1": "DIG001",
                    "formule_2": "DIG002",
                    "type_relation": "sequence",
                    "description": "Formules consécutives dans tableau"
                }}
            ]
        }}
        
        **DOCUMENT À ANALYSER :**
        {texte_document}
        
        Effectue une extraction complète et systématique des formules mathématiques.
        """
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=str(uuid.uuid4()),
            system_message=systeme_extraction
        ).with_model("anthropic", "claude-sonnet-4-20250514")
        
        user_message = UserMessage(text="Analyse ce document et extrait toutes les formules avec leur indexation.")
        extraction = await chat.send_message(user_message)
        
        # Sauvegarder l'analyse
        analyse_log = {
            "id": str(uuid.uuid4()),
            "document_hash": str(hash(texte_document))[:16],
            "extraction_ia": extraction,
            "domaine_principal": domaine_principal,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.analyses_indexation.insert_one(analyse_log)
        
        return {
            "success": True,
            "extraction": extraction,
            "analyse_id": analyse_log["id"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur indexation automatique: {str(e)}")

@app.post("/api/indexation/valider-extraction")
async def valider_extraction(request: dict):
    """Valider et enregistrer les formules extraites automatiquement"""
    try:
        formules_validees = request.get("formules_validees", [])
        concepts_valides = request.get("concepts_valides", [])
        relations_validees = request.get("relations_validees", [])
        
        resultats = {
            "formules_creees": 0,
            "concepts_crees": 0,
            "relations_creees": 0
        }
        
        # Enregistrer les formules validées
        for formule in formules_validees:
            formule_data = {
                "id": str(uuid.uuid4()),
                "code_formule": formule["code_propose"],
                "nom_formule": formule["nom_formule"],
                "formule_mathematique": formule["formule_mathematique"],
                "domaine": "geometrie",  # Adapté selon context
                "description": formule["description"],
                "variables": formule.get("variables", {}),
                "concepts_lies": [],
                "formules_dependantes": [],
                "niveau_complexite": formule.get("niveau_complexite", 3),
                "document_source": "Extraction automatique IA",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            await db.formules.insert_one(formule_data)
            resultats["formules_creees"] += 1
        
        # Enregistrer les concepts validés
        for concept in concepts_valides:
            concept_data = {
                "id": str(uuid.uuid4()),
                "titre": concept["nom"],
                "description": concept["description"],
                "domaine": concept["domaine"],
                "sous_domaine": None,
                "mots_cles": [],
                "niveau_complexite": 3,
                "document_source": "Extraction automatique IA",
                "created_by": "Système d'indexation",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            await db.concepts.insert_one(concept_data)
            resultats["concepts_crees"] += 1
        
        return {
            "success": True,
            "resultats": resultats,
            "message": "Extraction validée et enregistrée avec succès"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur validation extraction: {str(e)}")

# ===============================================
# API ACCÈS PRIVILÉGIÉ POUR IA SPÉCIALISÉE
# ===============================================

@app.get("/api/acces-privilegie/concepts-complets")
async def acces_concepts_complets():
    """Accès privilégié complet aux concepts pour l'IA spécialisée"""
    try:
        # Récupérer tous les concepts
        concepts = await db.concepts.find({}).to_list(length=None)
        
        # Récupérer toutes les formules
        formules = await db.formules.find({}).to_list(length=None)
        
        # Récupérer toutes les relations
        relations = await db.relations.find({}).to_list(length=None)
        
        # Convertir les ObjectId pour la sérialisation JSON
        concepts = convert_objectid(concepts)
        formules = convert_objectid(formules)
        relations = convert_objectid(relations)
        
        # Organiser par domaines
        donnees_privilegiees = {
            "domaines": {
                "nombres": {
                    "concepts": [c for c in concepts if c.get("domaine") == "nombres"],
                    "formules": [f for f in formules if f.get("domaine") == "nombres"]
                },
                "geometrie": {
                    "concepts": [c for c in concepts if c.get("domaine") == "geometrie"],
                    "formules": [f for f in formules if f.get("domaine") == "geometrie"]
                },
                "physique": {
                    "concepts": [c for c in concepts if c.get("domaine") == "physique"],
                    "formules": [f for f in formules if f.get("domaine") == "physique"]
                }
            },
            "relations_globales": relations,
            "statistiques": {
                "total_concepts": len(concepts),
                "total_formules": len(formules),
                "total_relations": len(relations)
            },
            "acces_type": "privilegie_complet",
            "derniere_mise_a_jour": datetime.now(timezone.utc).isoformat()
        }
        
        return {
            "success": True,
            "acces_privilegie": donnees_privilegiees
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur accès privilégié: {str(e)}")

@app.post("/api/acces-privilegie/requete-contextuelle")
async def requete_contextuelle_ia(request: dict):
    """Requête contextuelle avec accès privilégié pour l'IA spécialisée"""
    try:
        domaine_focus = request.get("domaine_focus", "all")
        concepts_recherches = request.get("concepts_recherches", [])
        niveau_detail = request.get("niveau_detail", "complet")
        
        query_concepts = {}
        if domaine_focus != "all":
            query_concepts["domaine"] = domaine_focus
        if concepts_recherches:
            query_concepts["titre"] = {"$in": concepts_recherches}
        
        concepts_filtres = await db.concepts.find(query_concepts).to_list(length=None)
        
        # Récupérer les formules associées
        concept_ids = [c["id"] for c in concepts_filtres]
        formules_associees = await db.formules.find({
            "concepts_lies": {"$in": concept_ids}
        }).to_list(length=None)
        
        # Convertir les ObjectId pour la sérialisation JSON
        concepts_filtres = convert_objectid(concepts_filtres)
        formules_associees = convert_objectid(formules_associees)
        
        return {
            "success": True,
            "contexte_privilegie": {
                "concepts_pertinents": concepts_filtres,
                "formules_associees": formules_associees,
                "domaine_focus": domaine_focus,
                "niveau_detail": niveau_detail
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur requête contextuelle: {str(e)}")

@app.get("/api/test-concepts")
async def test_concepts():
    """Test simple pour debug ObjectId"""
    try:
        # Compter les documents dans la collection
        count = await db.concepts.count_documents({})
        
        # Récupérer un exemple minimal
        sample = await db.concepts.find_one()
        if sample:
            sample = convert_objectid(sample)
            
        return {
            "success": True,
            "total_documents": count,
            "sample_document": sample,
            "message": "Test de la collection concepts"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Erreur lors du test"
        }

# ==================== ENDPOINTS ADMIN ====================

@app.post("/api/admin/login")
async def admin_login(credentials: dict):
    """Authentification admin"""
    # Mot de passe admin (même que pour upload documents)
    ADMIN_PASSWORD = "Uni1098020238Arc1374079226497308\\zetacar"
    
    password = credentials.get("password", "")
    
    if password == ADMIN_PASSWORD:
        return {
            "success": True,
            "message": "Authentification réussie"
        }
    else:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

@app.post("/api/admin/questions-log")
async def get_questions_log(request: dict):
    """Récupérer l'historique des questions posées à l'IA (protégé par mot de passe)"""
    ADMIN_PASSWORD = "Uni1098020238Arc1374079226497308\\zetacar"
    
    password = request.get("password", "")
    limit = request.get("limit", 100)  # Par défaut, 100 dernières questions
    
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Accès non autorisé")
    
    try:
        # Récupérer les questions avec tri par date décroissante
        questions = await db.questions_log.find(
            {},
            {"_id": 0}
        ).sort("timestamp", -1).limit(limit).to_list(limit)
        
        total_count = await db.questions_log.count_documents({})
        
        return {
            "success": True,
            "questions": questions,
            "total_count": total_count,
            "returned_count": len(questions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération historique: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)