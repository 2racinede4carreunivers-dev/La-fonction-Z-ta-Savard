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
EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY", "sk-emergent-c20D27d2bDa5755870")

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
        ).with_model("anthropic", "claude-3-5-sonnet-20241022")
        
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