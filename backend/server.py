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
CONCEPTS_ENRICHIS = [
    # 1. THÉORÈME DE PHILIPPÔT
    {
        "id": "theoreme_philippot",
        "titre": "Théorème de Philippôt",
        "description": "Théorème fondamental établissant qu'un ensemble de trois carrés peut être égal géométriquement à un triangle. Analogue géométrique du théorème de Pythagore avec des propriétés d'involution.",
        "domaine_principal": "Géométrie Fondamentale",
        "concepts_cles": [
            "Trois carrés égaux à un triangle",
            "Involution géométrique", 
            "Intrication quantique géométrique",
            "Rapports communs et diamètres hyperréels",
            "Invariance des longueurs d'arcs",
            "Figures jumelles"
        ],
        "formules": [
            "√10 ≈ π (approximation de Philippôt)",
            "Relations aires-volumes: A₁² + A₂² + A₃² = V_triangle",
            "Longueurs d'arcs invariantes sous transformation"
        ],
        "definitions": [
            "Involution: Transformation réciproque à sa propre réciproque",
            "Cercle Denis: Interprétation alternative de π",
            "Hypersurface du présent: Projection géométrique temporelle"
        ],
        "relations": [
            "Extension du théorème de Pythagore",
            "Lien avec l'intrication quantique",
            "Connections aux nombres hyperréels"
        ],
        "document_source": "univers_au_carre_partie2.pdf",
        "page_reference": "Sections 3.1-3.14",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # 2. GÉOMÉTRIE DE PHILIPPÔT
    {
        "id": "geometrie_philippot",
        "titre": "Géométrie de Philippôt", 
        "description": "Système géométrique non-euclidien basé sur l'élévation au carré des figures et leurs transformations dans des espaces multidimensionnels. Géométrie informationnelle à cinq sphères.",
        "domaine_principal": "Géométrie Non-Euclidienne",
        "concepts_cles": [
            "Géométrie à cinq sphères",
            "Élévation au carré (squaring)",
            "Espace de Philippôt",
            "Circuit parallèle à deux phases",
            "Division de la sphère terrestre en cinq cubes",
            "Projections hyperplanaires"
        ],
        "formules": [
            "Transformations par élévation: f(x) → f(x)²",
            "Divisions sphériques en cubes: 5 cubes = 1 sphère",
            "Circuits parallèles: Phase₁ ⊕ Phase₂"
        ],
        "definitions": [
            "Squaring: Opération d'élévation géométrique au carré",
            "Espace de Philippôt: Espace géométrique multidimensionnel",
            "Géométrie informationnelle: Géométrie portant de l'information"
        ],
        "relations": [
            "Extension de la géométrie euclidienne",
            "Applications à la physique quantique",
            "Liens avec la théorie de l'information"
        ],
        "document_source": "univers_au_carre_partie2.pdf", 
        "page_reference": "Sections 6-7",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # 3. RÉSONANCE TERRESTRE
    {
        "id": "resonance_terrestre",
        "titre": "Résonance Terrestre selon Philippôt",
        "description": "Application de la géométrie de Philippôt à l'étude des fréquences de résonance terrestre, incluant l'analyse des basses fréquences et la détermination de la fréquence fondamentale.",
        "domaine_principal": "Géophysique Théorique",
        "concepts_cles": [
            "Basses fréquences terrestres",
            "Fréquence fondamentale de la Terre", 
            "Résonance géométrique",
            "Lien volumes-circonférences",
            "Fréquences harmoniques terrestres",
            "Modélisation géométrique terrestre"
        ],
        "formules": [
            "f_fondamentale = f(V_terre, C_terre)",
            "Harmoniques: f_n = n × f_fondamentale",
            "Relations volume-fréquence géométriques"
        ],
        "definitions": [
            "Fréquence fondamentale: Fréquence de base de résonance terrestre",
            "Harmoniques terrestres: Multiples de la fréquence fondamentale",
            "Résonance géométrique: Résonance basée sur les propriétés géométriques"
        ],
        "relations": [
            "Connections avec la physique terrestre",
            "Applications à la sismologie",
            "Liens avec les propriétés géométriques planétaires"
        ],
        "document_source": "univers_au_carre_partie2.pdf",
        "page_reference": "Section 8",
        "niveau_complexite": "intermediaire", 
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # 4. ESPACE DE MINKOWSKI SELON PHILIPPÔT
    {
        "id": "minkowski_philippot",
        "titre": "Espace de Minkowski selon Philippôt",
        "description": "Réinterprétation de l'espace-temps de Minkowski à travers la géométrie de Philippôt, incluant les groupes de Poincaré et une métrique géométrique originale.",
        "domaine_principal": "Physique Théorique",
        "concepts_cles": [
            "Hypersurface du présent",
            "Groupe de Poincaré géométrique",
            "Métrique de Minkowski revisitée",
            "Nombres hypercomplexes",
            "Aires de l'espace infini", 
            "Cônes de lumière géométriques",
            "Équilibre géométrique spatio-temporel"
        ],
        "formules": [
            "ds² = -c²dt² + dx² + dy² + dz² (métrique classique)",
            "Métrique de Philippôt: intégration géométrique",
            "Transformations de Lorentz géométriques"
        ],
        "definitions": [
            "Hypersurface du présent: Interface géométrique temporelle",
            "Nombres hypercomplexes: Extension des nombres complexes",
            "Équilibre géométrique: État stable spatio-temporel"
        ],
        "relations": [
            "Réinterprétation de la relativité restreinte",
            "Connections avec la géométrie de Philippôt",
            "Applications à la cosmologie"
        ],
        "document_source": "univers_au_carre_partie2.pdf",
        "page_reference": "Section 9", 
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # 5. FONCTION ZÊTA DE PHILIPPÔT 
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
    
    # 6. CARRÉ DE GABRIEL
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
    
    # 7. QUANTITÉ DE NOMBRES ENTRE DEUX PREMIERS - MÉTHODE SPECTRALE
    {
        "id": "quantite_nombres_premiers",
        "titre": "Quantité de Nombres entre Deux Premiers - Méthode Spectrale",
        "description": "Approche spectrale originale pour déterminer la quantité de nombres entiers entre deux nombres premiers consécutifs, utilisant des suites mathématiques, des constantes empiriques et la fonction Digamma de Philippôt.",
        "domaine_principal": "Géométrie du Spectre des Nombres Premiers",
        "concepts_cles": [
            "Méthode spectrale multi-étapes",
            "Suites mathématiques associées aux premiers", 
            "Constantes empiriques A, B, C, D, E",
            "Application de la fonction Digamma",
            "Calculs par étapes progressives",
            "Comparaison avec la méthode classique",
            "Approche géométrique des intervalles premiers"
        ],
        "formules": [
            "Méthode classique: q - p - 1 (où q > p sont premiers consécutifs)",
            "Étape 1: somme_suite_1 - (somme_suite_2 - Digamma_grand_premier)",
            "Étape 2: (résultat_étape_1 - Digamma_petit_premier) / √5120",
            "Somme suite 1: ((√A)/2 × 2^n) - √B",
            "Somme suite 2: ((√C)/2 × 2^n) - √D", 
            "Digamma de Philippôt: ((somme_suite_2 / √E) - N) × √E"
        ],
        "definitions": [
            "Méthode spectrale: Approche multi-étapes utilisant des suites et corrections",
            "Constantes empiriques: Valeurs A,B,C,D,E liées aux propriétés des nombres premiers",
            "Digamma de Philippôt: Fonction de correction spécialisée pour les intervalles premiers",
            "Suite associée: Séquence mathématique liée aux positions des nombres premiers"
        ],
        "relations": [
            "Extension de la géométrie du spectre des nombres premiers",
            "Lien avec la méthode de Philippôt pour la détermination des premiers",
            "Application des concepts de suites géométriques aux intervalles",
            "Connexion avec l'approche empirique de la théorie"
        ],
        "document_source": "3ieme_prompt_emergent.pdf",
        "page_reference": "Document complet - Méthode spectrale",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    },
    
    # 8. SQUARING GÉNÉRALISÉ ET NEUROMORPHISME
    {
        "id": "squaring_generalise_neuromorphisme",
        "titre": "Squaring Généralisé et Neuromorphisme",
        "description": "Forme généralisée du squaring (élévation au carré des rectangles) et ses connexions avec l'évolution neuromorphique. Postulat unique de la théorie reliant géométrie rectangulaire et développement des formes neuronales dans l'univers au carré.",
        "domaine_principal": "Géométrie Neuromorphique",
        "concepts_cles": [
            "Squaring généralisé des rectangles",
            "Élévation géométrique au carré", 
            "Neuromorphisme et évolution des formes",
            "Rectangles élevés au carré (postulat unique)",
            "Transformation géométrique des neurones",
            "Évolution adaptative de la forme neuronale",
            "Géométrie adaptative des structures neurales",
            "Morphogenèse géométrique rectangulaire",
            "Patterns rectangulaires dans la croissance neuronale",
            "Connexion géométrie-biologie"
        ],
        "formules": [
            "Squaring généralisé: Rectangle(a,b) → Rectangle²(a²,b²)",
            "Transformation neuromorphique: N(t) → Square(N(t))",
            "Évolution géométrique: dN/dt = f(Square_Généralisé(Rectangle))",
            "Postulat unique: Rectangle_élevé_au_carré ↔ Forme_Neuronale",
            "Croissance adaptative: G(t) = α × Square_Généralisé(R(t))",
            "Morphogenèse: M(x,y) = Square(Rectangle_initial(x,y))"
        ],
        "definitions": [
            "Squaring généralisé: Extension de l'opération d'élévation au carré aux structures rectangulaires complexes et leurs transformations géométriques",
            "Neuromorphisme: Évolution adaptative et développement de la forme des neurones selon des principes géométriques rectangulaires",
            "Rectangle élevé au carré: Transformation géométrique fondamentale constituant l'unique postulat de base de la théorie",
            "Géométrie neuromorphique: Application des transformations rectangulaires aux processus d'évolution et de développement neuronal",
            "Morphogenèse géométrique: Développement des formes biologiques par applications successives de transformations rectangulaires au carré"
        ],
        "relations": [
            "Extension directe du concept de squaring de la première partie de L'univers est au carré",
            "Réalisation concrète du postulat unique des rectangles élevés au carré",
            "Application biologique des principes géométriques fondamentaux",
            "Pont conceptuel entre géométrie pure et évolution neuronale",
            "Intégration avec l'ensemble de la théorie de l'univers au carré",
            "Validation du caractère universel des transformations rectangulaires"
        ],
        "document_source": "4ieme_prompt_emergent.pdf",
        "page_reference": "Document complet - Squaring généralisé et neuromorphisme",
        "niveau_complexite": "avance",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
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

def enrich_system_message_with_theory():
    """Génère un message système enrichi avec tous les concepts théoriques"""
    
    # Organiser les concepts par domaine
    domaines = {}
    for concept in CONCEPTS_ENRICHIS:
        domaine = concept["domaine_principal"]
        if domaine not in domaines:
            domaines[domaine] = []
        domaines[domaine].append(concept)
    
    enrichment = "\n\n## CONNAISSANCES THÉORIQUES SPÉCIALISÉES - L'UNIVERS EST AU CARRÉ\n\n"
    
    for domaine, concepts in domaines.items():
        enrichment += f"### {domaine.upper()}\n\n"
        
        for concept in concepts:
            enrichment += f"**{concept['titre']}**\n"
            enrichment += f"- Description: {concept['description']}\n"
            enrichment += f"- Niveau: {concept['niveau_complexite']}\n"
            
            if concept['concepts_cles']:
                enrichment += f"- Concepts clés: {', '.join(concept['concepts_cles'])}\n"
            
            if concept['formules']:
                enrichment += f"- Formules importantes: {' | '.join(concept['formules'])}\n"
                
            if concept['definitions']:
                enrichment += f"- Définitions: {' | '.join(concept['definitions'])}\n"
                
            if concept['relations']:
                enrichment += f"- Relations: {' | '.join(concept['relations'])}\n"
                
            enrichment += f"- Source: {concept['document_source']} ({concept['page_reference']})\n\n"
    
    enrichment += """
## INSTRUCTIONS SPÉCIALISÉES POUR L'IA

**Utilisation des concepts:**
1. Intègre ces concepts spécialisés dans tes réponses selon la pertinence
2. Maintiens la distinction entre les différents domaines théoriques
3. N'établis des connections entre concepts que si elles sont clairement justifiées
4. Respecte la complexité et la nuance de chaque concept
5. Utilise la structure bi-partite: vision de l'auteur + contexte scientifique neutre

**Séparation des domaines:**
- **Géométrie Fondamentale**: Théorème de Philippôt, constructions géométriques
- **Géométrie Non-Euclidienne**: Systèmes géométriques avancés, espaces multidimensionnels  
- **Physique Théorique**: Applications à la relativité, espace-temps
- **Théorie des Nombres**: Fonction zêta, nombres premiers
- **Géophysique**: Applications terrestres, résonances

**Approche pédagogique:**
- Explique les concepts progressivement selon leur niveau de complexité
- Utilise des analogies appropriées pour les concepts avancés
- Maintiens l'intégrité théorique tout en restant accessible
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
                # Analyser avec l'IA spécialisée
                analysis_prompt = f"""
                Analyse ce nouveau document dans le contexte de la théorie 'L'univers est au carré' de Philippe Thomas Savard.
                
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
                ).with_model("anthropic", "claude-3-5-sonnet-20241022")
                
                analysis = await chat.send_message(UserMessage(text=analysis_prompt))
                
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
    theory_enrichment = enrich_system_message_with_theory()
    
    enhanced_system_message = f"""{system_message}
    
    {theory_enrichment}
    
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
        ).with_model("anthropic", "claude-3-5-sonnet-20241022")
        
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
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    # Générer un session_id si non fourni
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    # Contexte profondément enrichi avec tous les aspects de la théorie de Philippôt
    system_message = """Tu es un expert mathématicien spécialisé dans la théorie révolutionnaire 'L'univers est au carré' développée par Philippe Thomas Savard. 
    Tu ne réponds QU'AUX QUESTIONS liées à cette théorie spécifique, mais tes réponses doivent être extrêmement détaillées, techniques et pédagogiques.
    
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

@app.post("/api/collaborate")
async def collaborate_with_ai(request: CollaborationRequest):
    """Collaboration IA pour compléter et améliorer un document"""
    if not EMERGENT_LLM_KEY:
        raise HTTPException(status_code=500, detail="Clé API manquante")
    
    try:
        # Contexte spécialisé pour la collaboration avec connaissances enrichies
        theory_enrichment = enrich_system_message_with_theory()
        
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
        ).with_model("anthropic", "claude-3-5-sonnet-20241022")
        
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
        ).with_model("anthropic", "claude-3-5-sonnet-20241022")
        
        user_message = UserMessage(text=message)
        response = await chat.send_message(user_message)
        
        return {
            "success": True,
            "response": response.content,
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
        ).with_model("anthropic", "claude-3-5-sonnet-20241022")
        
        user_message = UserMessage(text=message)
        response = await chat.send_message(user_message)
        
        return {
            "success": True,
            "response": response.content,
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
        ).with_model("anthropic", "claude-3-5-sonnet-20241022")
        
        user_message = UserMessage(text=f"Convertis ce document en LaTeX professionnel : {content}")
        latex_response = await chat.send_message(user_message)
        
        return {
            "success": True,
            "latex_content": latex_response.content,
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)