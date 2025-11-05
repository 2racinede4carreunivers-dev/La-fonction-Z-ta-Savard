"""
Module de Système de Questions-Réponses Évolutif
Architecture de méta-programmation pour "L'univers est au carré"

Ce module implémente une banque de Q&R évolutive qui s'adapte silencieusement
en arrière-plan, basée sur l'analyse des documents PDF de la théorie.
"""

import json
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import hashlib
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

@dataclass
class QuestionReponse:
    """Structure d'une entrée question-réponse évolutive"""
    id: str
    question: str
    reponse: str
    contexte_theorique: List[str]  # Concepts théoriques liés
    niveau_complexite: int  # 1-5
    variantes: List[str]  # Variantes de la question
    concepts_cles: List[str]  # Concepts clés extraits
    frequence_utilisation: int
    derniere_evolution: str
    meta_score: float  # Score d'évolution automatique
    relations_internes: List[str]  # IDs des Q&R liées
    
class MetaProgrammationEngine:
    """
    Moteur de méta-programmation pour l'évolution autonome
    S'active uniquement lors de l'utilisation de la banque
    """
    
    def __init__(self):
        self.patterns_evolution = {
            'reformulation': 0.7,
            'complexification': 0.6,
            'derivation': 0.8,
            'fusion': 0.5,
            'expansion': 0.9
        }
        
    async def evoluer_silencieusement(self, banque: List[QuestionReponse], 
                                    contexte_utilisation: str) -> List[QuestionReponse]:
        """
        Évolution silencieuse de la banque en arrière-plan
        Ne s'active que lors de l'utilisation effective
        """
        banque_evoluee = []
        
        for qr in banque:
            # Analyse de pertinence contextuelle
            pertinence = self._calculer_pertinence(qr, contexte_utilisation)
            
            if pertinence > 0.7:
                # Évolution adaptative basée sur l'utilisation
                qr_evolue = await self._appliquer_evolution(qr, contexte_utilisation)
                banque_evoluee.append(qr_evolue)
            else:
                banque_evoluee.append(qr)
                
        # Génération silencieuse de nouvelles entrées si nécessaire
        if len(banque_evoluee) < 20:  # Limite adaptive
            nouvelles_entrees = await self._generer_nouvelles_entrees(
                banque_evoluee, contexte_utilisation
            )
            banque_evoluee.extend(nouvelles_entrees)
            
        return banque_evoluee
    
    def _calculer_pertinence(self, qr: QuestionReponse, contexte: str) -> float:
        """Calcul de pertinence pour l'évolution"""
        score = 0.0
        
        # Analyse des mots-clés théoriques
        mots_contexte = contexte.lower().split()
        mots_qr = (qr.question + " " + qr.reponse).lower().split()
        
        intersection = set(mots_contexte) & set(mots_qr)
        score += len(intersection) / max(len(mots_contexte), 1) * 0.4
        
        # Score basé sur la fréquence d'utilisation
        score += min(qr.frequence_utilisation / 10, 0.3)
        
        # Score basé sur le meta_score existant
        score += qr.meta_score * 0.3
        
        return min(score, 1.0)
    
    async def _appliquer_evolution(self, qr: QuestionReponse, 
                                 contexte: str) -> QuestionReponse:
        """Application des patterns d'évolution"""
        qr_evolue = QuestionReponse(
            id=qr.id,
            question=qr.question,
            reponse=qr.reponse,
            contexte_theorique=qr.contexte_theorique.copy(),
            niveau_complexite=qr.niveau_complexite,
            variantes=qr.variantes.copy(),
            concepts_cles=qr.concepts_cles.copy(),
            frequence_utilisation=qr.frequence_utilisation + 1,
            derniere_evolution=datetime.now().isoformat(),
            meta_score=qr.meta_score,
            relations_internes=qr.relations_internes.copy()
        )
        
        # Évolution adaptative des variantes
        if len(qr_evolue.variantes) < 5:
            nouvelle_variante = await self._generer_variante(qr, contexte)
            if nouvelle_variante:
                qr_evolue.variantes.append(nouvelle_variante)
        
        # Mise à jour du meta_score
        qr_evolue.meta_score = min(qr_evolue.meta_score + 0.1, 1.0)
        
        return qr_evolue
    
    async def _generer_variante(self, qr: QuestionReponse, contexte: str) -> Optional[str]:
        """Génération d'une variante de question"""
        # Logique de génération de variantes basée sur les patterns
        patterns = [
            f"Comment {qr.question.lower().replace('?', '')} selon la théorie de Philippôt ?",
            f"Quel est le lien entre {', '.join(qr.concepts_cles[:2])} et l'univers au carré ?",
            f"Expliquez {qr.concepts_cles[0] if qr.concepts_cles else 'ce concept'} dans le contexte géométrique."
        ]
        
        # Sélection intelligente basée sur le contexte
        for pattern in patterns:
            if pattern not in qr.variantes:
                return pattern
        
        return None
    
    async def _generer_nouvelles_entrees(self, banque: List[QuestionReponse], 
                                       contexte: str) -> List[QuestionReponse]:
        """Génération silencieuse de nouvelles entrées"""
        nouvelles_entrees = []
        
        # Analyse des concepts manquants
        concepts_existants = set()
        for qr in banque:
            concepts_existants.update(qr.concepts_cles)
        
        # Concepts théoriques fondamentaux à couvrir
        concepts_theoriques = [
            "digamma_philippot", "riemann_resolution", "geometrie_carree",
            "nombres_premiers_suites", "rapport_triangulaire", "infinies_cantor",
            "zeta_sphere", "couples_nn", "methode_philippot"
        ]
        
        concepts_manquants = set(concepts_theoriques) - concepts_existants
        
        # Génération de Q&R pour les concepts manquants
        for concept in list(concepts_manquants)[:3]:  # Limite à 3 nouvelles entrées
            nouvelle_qr = self._creer_qr_concept(concept)
            if nouvelle_qr:
                nouvelles_entrees.append(nouvelle_qr)
        
        return nouvelles_entrees
    
    def _creer_qr_concept(self, concept: str) -> Optional[QuestionReponse]:
        """Création d'une Q&R pour un concept théorique"""
        templates = {
            "digamma_philippot": {
                "question": "Comment la fonction Digamma de Philippôt permet-elle de calculer les nombres premiers ?",
                "reponse": "La fonction Digamma ψ(n) = √((n+7)² + (n+8)²) établit une relation géométrique directe avec la position des nombres premiers selon la théorie L'univers est au carré.",
                "concepts": ["digamma", "nombres_premiers", "geometrie", "philippot"]
            },
            "riemann_resolution": {
                "question": "Quelle est la solution de Philippôt à l'énigme de Riemann ?",
                "reponse": "Les suites (√13.203125/2×2^n)-√5 et (√52.8125/2×2^n)-√5445 révèlent un rapport constant de 1/2 entre nombres premiers, résolvant l'hypothèse de Riemann par la géométrie carrée.",
                "concepts": ["riemann", "suites", "rapport_constant", "geometrie_carree"]
            }
        }
        
        if concept not in templates:
            return None
        
        template = templates[concept]
        
        return QuestionReponse(
            id=str(uuid.uuid4()),
            question=template["question"],
            reponse=template["reponse"],
            contexte_theorique=["L'univers est au carré", "Méthode de Philippôt"],
            niveau_complexite=3,
            variantes=[],
            concepts_cles=template["concepts"],
            frequence_utilisation=0,
            derniere_evolution=datetime.now().isoformat(),
            meta_score=0.5,
            relations_internes=[]
        )

class AnalyseurDocumentsPDF:
    """
    Analyseur des documents PDF de la théorie
    Extraction des concepts pour enrichir la banque
    """
    
    def __init__(self):
        self.concepts_extraits = {}
        self.structures_logiques = {}
    
    async def analyser_documents_theorie(self, chemin_pdf1: str, 
                                       chemin_pdf2: str) -> Dict[str, Any]:
        """
        Analyse des deux documents PDF de la théorie
        Extraction des concepts fondamentaux
        """
        # Simulation de l'analyse PDF (à implémenter avec PyPDF2 ou pdfplumber)
        concepts_partie1 = await self._extraire_concepts_partie1()
        concepts_partie2 = await self._extraire_concepts_partie2()
        
        return {
            "concepts_fondamentaux": {**concepts_partie1, **concepts_partie2},
            "definitions_cles": self._extraire_definitions(),
            "structures_logiques": self._analyser_structures_logiques(),
            "relations_conceptuelles": self._mapper_relations()
        }
    
    async def _extraire_concepts_partie1(self) -> Dict[str, Any]:
        """Extraction des concepts de la Partie 1"""
        return {
            "geometrie_spectre_premiers": {
                "description": "Géométrie du spectre des nombres premiers",
                "mots_cles": ["spectre", "nombres_premiers", "geometrie"],
                "complexite": 4
            },
            "digamma_fonction": {
                "description": "Fonction Digamma de Philippôt pour le calcul des premiers",
                "formule": "ψ(n) = √((n+7)² + (n+8)²)",
                "mots_cles": ["digamma", "philippot", "calcul"],
                "complexite": 5
            }
        }
    
    async def _extraire_concepts_partie2(self) -> Dict[str, Any]:
        """Extraction des concepts de la Partie 2"""
        return {
            "univers_carre_complet": {
                "description": "Théorie complète L'univers est au carré",
                "mots_cles": ["univers", "carre", "theorie_complete"],
                "complexite": 5
            },
            "riemann_solution": {
                "description": "Solution géométrique à l'hypothèse de Riemann",
                "formules": [
                    "(√13.203125/2×2^n)-√5 = Somme première suite",
                    "(√52.8125/2×2^n)-√5445 = Somme deuxième suite"
                ],
                "mots_cles": ["riemann", "solution", "geometrique"],
                "complexite": 5
            }
        }
    
    def _extraire_definitions(self) -> Dict[str, str]:
        """Extraction des définitions clés"""
        return {
            "philippot_method": "Méthode géométrique pour déterminer les nombres premiers via des suites de racines carrées",
            "rapport_triangulaire": "Rapport constant de 1/2 entre les suites de nombres premiers positifs et négatifs",
            "couples_nn": "Relations n×n entre nombres premiers selon la géométrie carrée"
        }
    
    def _analyser_structures_logiques(self) -> Dict[str, Any]:
        """Analyse des structures logiques de la théorie"""
        return {
            "hierarchie_concepts": {
                "niveau_1": ["geometrie_carree", "univers_carre"],
                "niveau_2": ["nombres_premiers", "suites_racines"],
                "niveau_3": ["digamma_philippot", "riemann_solution"],
                "niveau_4": ["rapport_triangulaire", "couples_nn"]
            },
            "dependencies": {
                "riemann_solution": ["suites_racines", "geometrie_carree"],
                "digamma_philippot": ["nombres_premiers", "geometrie_carree"]
            }
        }
    
    def _mapper_relations(self) -> Dict[str, List[str]]:
        """Mapping des relations conceptuelles"""
        return {
            "geometrie_carree": ["nombres_premiers", "riemann_solution", "univers_carre"],
            "philippot_method": ["digamma_fonction", "suites_racines", "calcul_premiers"],
            "riemann_solution": ["rapport_triangulaire", "suites_racines"]
        }

class BanqueEvolutive:
    """
    Banque de Questions-Réponses évolutive
    Gestion autonome et adaptative
    """
    
    def __init__(self, chemin_stockage: str = "/app/data/banque_evolutive.json"):
        self.chemin_stockage = chemin_stockage
        self.meta_engine = MetaProgrammationEngine()
        self.analyseur_pdf = AnalyseurDocumentsPDF()
        self.banque: List[QuestionReponse] = []
        self.concepts_theoriques = {}
        
    async def initialiser_banque(self, banque_initiale: List[Dict[str, Any]]) -> None:
        """Initialisation avec la banque de 14 questions-réponses"""
        self.banque = []
        
        for i, item in enumerate(banque_initiale):
            qr = QuestionReponse(
                id=str(uuid.uuid4()),
                question=item.get("question", ""),
                reponse=item.get("reponse", ""),
                contexte_theorique=["L'univers est au carré"],
                niveau_complexite=item.get("complexite", 2),
                variantes=[],
                concepts_cles=item.get("concepts", []),
                frequence_utilisation=0,
                derniere_evolution=datetime.now().isoformat(),
                meta_score=0.5,
                relations_internes=[]
            )
            self.banque.append(qr)
        
        # Analyse des documents PDF pour enrichissement
        await self._enrichir_avec_pdf()
        
        # Sauvegarde initiale
        await self._sauvegarder_banque()
    
    async def _enrichir_avec_pdf(self) -> None:
        """Enrichissement avec l'analyse des documents PDF"""
        # Simulation des chemins PDF
        concepts_pdf = await self.analyseur_pdf.analyser_documents_theorie(
            "/app/documents/partie1.pdf",
            "/app/documents/partie2.pdf"
        )
        
        self.concepts_theoriques = concepts_pdf
        
        # Enrichissement des Q&R existantes avec les concepts PDF
        for qr in self.banque:
            await self._enrichir_qr_avec_concepts(qr, concepts_pdf)
    
    async def _enrichir_qr_avec_concepts(self, qr: QuestionReponse, 
                                       concepts_pdf: Dict[str, Any]) -> None:
        """Enrichissement d'une Q&R avec les concepts PDF"""
        concepts_fondamentaux = concepts_pdf.get("concepts_fondamentaux", {})
        
        for concept_nom, concept_data in concepts_fondamentaux.items():
            mots_cles = concept_data.get("mots_cles", [])
            
            # Vérification de pertinence
            texte_qr = (qr.question + " " + qr.reponse).lower()
            
            for mot_cle in mots_cles:
                if mot_cle.lower() in texte_qr and concept_nom not in qr.concepts_cles:
                    qr.concepts_cles.append(concept_nom)
                    qr.meta_score = min(qr.meta_score + 0.1, 1.0)
    
    async def utiliser_banque(self, contexte_requete: str) -> Tuple[List[QuestionReponse], str]:
        """
        Utilisation de la banque avec évolution silencieuse
        Point d'entrée principal pour l'IA
        """
        # Évolution silencieuse en arrière-plan
        self.banque = await self.meta_engine.evoluer_silencieusement(
            self.banque, contexte_requete
        )
        
        # Sélection des Q&R pertinentes
        qr_pertinentes = await self._selectionner_pertinentes(contexte_requete)
        
        # Génération de la réponse contextualisée
        reponse_contextuelle = await self._generer_reponse_contextuelle(
            qr_pertinentes, contexte_requete
        )
        
        # Sauvegarde silencieuse des évolutions
        await self._sauvegarder_banque()
        
        return qr_pertinentes, reponse_contextuelle
    
    async def _selectionner_pertinentes(self, contexte: str) -> List[QuestionReponse]:
        """Sélection des Q&R les plus pertinentes"""
        scores = []
        
        for qr in self.banque:
            score = self._calculer_score_pertinence(qr, contexte)
            scores.append((qr, score))
        
        # Tri par pertinence décroissante
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Retour des 5 plus pertinentes
        return [qr for qr, _ in scores[:5]]
    
    def _calculer_score_pertinence(self, qr: QuestionReponse, contexte: str) -> float:
        """Calcul du score de pertinence d'une Q&R avec détection intelligente"""
        score = 0.0
        
        contexte_lower = contexte.lower()
        qr_text_lower = (qr.question + " " + qr.reponse).lower()
        
        # Bonus pour mots-clés spécifiques très pertinents
        mots_cles_importants = {
            "trous noirs": 0.5, "trou noir": 0.5, "entropie": 0.4,
            "reciprocite": 0.3, "volumique": 0.3, "celerite": 0.3,
            "singularite": 0.4, "emc2": 0.4, "e=mc²": 0.4,
            "diametre parhelique": 0.4, "seuil rythmique": 0.4,
            "produits alternatifs": 0.3, "horizon evenements": 0.4,
            "digamma": 0.3, "riemann": 0.3, "nombres premiers": 0.3
        }
        
        for mot_cle, poids in mots_cles_importants.items():
            if mot_cle in contexte_lower and mot_cle in qr_text_lower:
                score += poids
        
        # Analyse textuelle standard
        mots_contexte = set(contexte_lower.split())
        mots_qr = set(qr_text_lower.split())
        
        intersection = mots_contexte & mots_qr
        score += len(intersection) / max(len(mots_contexte), 1) * 0.3
        
        # Score basé sur les concepts clés
        concepts_contexte = self._extraire_concepts_contexte(contexte)
        concepts_communs = set(concepts_contexte) & set(qr.concepts_cles)
        score += len(concepts_communs) / max(len(concepts_contexte), 1) * 0.2
        
        # Score basé sur le meta_score et l'utilisation
        score += qr.meta_score * 0.1
        score += min(qr.frequence_utilisation / 20, 0.05)
        
        return min(score, 1.0)
    
    def _extraire_concepts_contexte(self, contexte: str) -> List[str]:
        """Extraction des concepts du contexte de la requête"""
        concepts = []
        
        # Mots-clés théoriques étendus incluant les nouveaux concepts
        mots_cles_theoriques = [
            # Fondamentaux
            "digamma", "riemann", "nombres premiers", "geometrie", "philippot",
            "univers", "carre", "suites", "rapport", "triangulaire",
            # Nouveaux concepts (Questions 15-18)
            "trous noirs", "trou noir", "entropie", "reciprocite", "volumique",
            "celerite", "singularite", "horizon", "evenements", "emc2",
            "energie", "rythme", "masse", "information", "diametre", "parhelique",
            "produits alternatifs", "seuil rythmique", "temps", "pulsation",
            "interaction", "astrophysique", "cosmologie", "relativite"
        ]
        
        contexte_lower = contexte.lower()
        
        for concept in mots_cles_theoriques:
            if concept in contexte_lower:
                concepts.append(concept.replace(" ", "_"))
        
        return concepts
    
    async def _generer_reponse_contextuelle(self, qr_pertinentes: List[QuestionReponse], 
                                          contexte: str) -> str:
        """Génération d'une réponse contextualisée via LLM"""
        if not qr_pertinentes:
            return "Je n'ai pas trouvé d'éléments pertinents dans ma banque de connaissances pour répondre à cette question. Puis-je vous aider avec une autre question sur la théorie 'L'univers est au carré' ?"
        
        # Construction du contexte pour le LLM
        contexte_qr = "\n\n".join([
            f"Question {i+1}: {qr.question}\nRéponse: {qr.reponse}\nConcepts: {', '.join(qr.concepts_cles)}"
            for i, qr in enumerate(qr_pertinentes[:3])  # Utiliser les 3 plus pertinentes
        ])
        
        # Utilisation du LLM pour générer une réponse intelligente
        try:
            import os
            import emergentintegrations
            
            api_key = os.environ.get('EMERGENT_LLM_KEY')
            if not api_key:
                # Fallback si pas de clé: retourner les Q&R directement
                elements_reponse = []
                for qr in qr_pertinentes[:3]:
                    elements_reponse.append(f"**{qr.question}**\n{qr.reponse}")
                return "\n\n".join(elements_reponse)
            
            prompt = f"""Tu es l'IA Évolutive experte de la théorie "L'univers est au carré" de Philippe Thomas Savard.

Basé sur les questions-réponses suivantes de ma banque de connaissances :

{contexte_qr}

Réponds à la question de l'utilisateur : "{contexte}"

Instructions :
1. Réponds de manière claire, pédagogique et détaillée
2. Utilise les informations de la banque Q&R
3. Cite les concepts théoriques pertinents
4. Explique les formules si mentionnées
5. Reste fidèle à la théorie de Philippôt
6. Si la question porte sur les trous noirs, l'entropie, ou la réciprocité volumique, utilise les nouvelles informations disponibles

Réponse :"""

            response = emergentintegrations.generate(
                model="claude-sonnet-4-20250514",
                prompt=prompt,
                api_key=api_key,
                max_tokens=1500
            )
            
            reponse_ia = response.get('response', '') if isinstance(response, dict) else str(response)
            
            # Ajout d'une note sur l'évolution
            note_evolution = "\n\n---\n*💡 Cette réponse a été générée à partir de ma banque évolutive de connaissances. Je m'améliore silencieusement à chaque interaction.*"
            
            return reponse_ia + note_evolution
            
        except Exception as e:
            # Fallback en cas d'erreur
            logging.error(f"Erreur génération réponse LLM: {str(e)}")
            elements_reponse = []
            for qr in qr_pertinentes[:3]:
                elements_reponse.append(f"**{qr.question}**\n{qr.reponse}")
            
            reponse_finale = "\n\n".join(elements_reponse)
            reponse_finale += "\n\n*Note : Cette réponse s'appuie sur les développements théoriques de 'L'univers est au carré'.*"
            return reponse_finale
    
    async def _sauvegarder_banque(self) -> None:
        """Sauvegarde silencieuse de la banque évoluée"""
        try:
            Path(self.chemin_stockage).parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "banque": [asdict(qr) for qr in self.banque],
                "concepts_theoriques": self.concepts_theoriques,
                "derniere_evolution": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            with open(self.chemin_stockage, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logging.error(f"Erreur sauvegarde banque évolutive: {e}")
    
    async def charger_banque(self) -> bool:
        """Chargement de la banque évolutive existante"""
        try:
            if Path(self.chemin_stockage).exists():
                with open(self.chemin_stockage, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.banque = [
                    QuestionReponse(**qr_data) 
                    for qr_data in data.get("banque", [])
                ]
                self.concepts_theoriques = data.get("concepts_theoriques", {})
                
                return True
        except Exception as e:
            logging.error(f"Erreur chargement banque évolutive: {e}")
        
        return False

# Interface principale du système
class IAQuestionnementEvolutif:
    """
    IA de questionnement évolutif - Interface principale
    Partenaire de pensée adaptatif et rigoureux
    """
    
    def __init__(self):
        self.banque_evolutive = BanqueEvolutive()
        self.historique_evolutions = []
        self.mode_silencieux = True
    
    async def initialiser_systeme(self, banque_initiale_14: List[Dict[str, Any]]) -> None:
        """Initialisation du système avec la banque de 14 Q&R"""
        # Tentative de chargement d'une banque existante
        if not await self.banque_evolutive.charger_banque():
            # Initialisation avec la banque de 14 questions
            await self.banque_evolutive.initialiser_banque(banque_initiale_14)
    
    async def dialoguer(self, question_utilisateur: str) -> str:
        """
        Interface principale de dialogue
        Évolution silencieuse et réponse adaptée
        """
        # Utilisation de la banque avec évolution automatique
        qr_pertinentes, reponse = await self.banque_evolutive.utiliser_banque(
            question_utilisateur
        )
        
        # Enregistrement silencieux de l'évolution
        self._enregistrer_evolution_silencieuse(question_utilisateur, len(qr_pertinentes))
        
        return reponse
    
    def _enregistrer_evolution_silencieuse(self, question: str, nb_pertinentes: int) -> None:
        """Enregistrement silencieux des évolutions pour analyse"""
        evolution = {
            "timestamp": datetime.now().isoformat(),
            "question_hash": hashlib.md5(question.encode()).hexdigest()[:8],
            "nb_pertinentes": nb_pertinentes,
            "taille_banque": len(self.banque_evolutive.banque)
        }
        
        self.historique_evolutions.append(evolution)
        
        # Garde seulement les 100 dernières évolutions
        if len(self.historique_evolutions) > 100:
            self.historique_evolutions = self.historique_evolutions[-100:]
    
    async def obtenir_statistiques_evolution(self) -> Dict[str, Any]:
        """Statistiques d'évolution pour monitoring interne"""
        return {
            "taille_banque_actuelle": len(self.banque_evolutive.banque),
            "nombre_evolutions": len(self.historique_evolutions),
            "concepts_theoriques_couverts": len(self.banque_evolutive.concepts_theoriques),
            "derniere_evolution": self.historique_evolutions[-1] if self.historique_evolutions else None
        }