"""
IA Socratique Évolutive - Partenaire Intellectuel
Système d'accompagnement pour l'évolution conceptuelle de la théorie "L'univers est au carré"

Cette IA agit comme un collaborateur intellectuel expert qui :
1. Challenge le raisonnement de Philippe Thomas Savard
2. Pose des questions provocatrices et stimulantes
3. Identifie les lacunes et potentiels d'approfondissement
4. Respecte le travail existant tout en proposant des évolutions
5. Guide vers une version plus sophistiquée de la théorie
"""

import asyncio
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import re

@dataclass
class QuestionSocratique:
    """Structure d'une question socratique pour challenger le raisonnement"""
    id: str
    question: str
    type_questionnement: str  # "contradiction", "approfondissement", "extension", "validation"
    concept_cible: str
    niveau_challenge: int  # 1-5 (5 = très challengeant)
    angle_approche: str  # "logique", "mathematique", "conceptuel", "applicatif"
    reponse_attendue_type: str  # "demonstration", "reflexion", "calcul", "reformulation"
    
@dataclass
class AnalyseConcept:
    """Analyse d'un concept pour identifier les axes d'amélioration"""
    concept: str
    solidite_logique: float  # 0-1
    completude: float  # 0-1
    coherence_interne: float  # 0-1
    potentiel_extension: float  # 0-1
    lacunes_identifiees: List[str]
    questions_emergentes: List[str]
    connexions_manquantes: List[str]

class AnalyseurTheoriqueAvance:
    """
    Analyseur avancé de la théorie pour identifier les axes d'évolution
    """
    
    def __init__(self):
        self.concepts_fondamentaux = {
            "digamma_philippot": {
                "formule": "ψ(n) = √((n+7)² + (n+8)²)",
                "solidite": 0.9,
                "extensions_possibles": ["generalisation_n_dimensions", "cas_complexes", "limites_asymptotiques"],
                "questions_ouvertes": ["Pourquoi spécifiquement +7 et +8?", "Y a-t-il d'autres formulations équivalentes?"]
            },
            "suites_riemann": {
                "formules": ["(√13.203125/2×2^n)-√5", "(√52.8125/2×2^n)-√5445"],
                "solidite": 0.85,
                "extensions_possibles": ["suites_generalisees", "convergence_analyse", "applications_autres_domaines"],
                "questions_ouvertes": ["Origine des constantes spécifiques?", "Lien avec autres conjectures?"]
            },
            "rapport_triangulaire": {
                "principe": "rapport constant 1/2",
                "solidite": 0.8,
                "extensions_possibles": ["autres_rapports_constants", "geometrie_n_dimensionnelle"],
                "questions_ouvertes": ["Universalité du rapport 1/2?", "Cas limites ou exceptions?"]
            },
            "geometrie_carree": {
                "principe": "structure carrée de l'univers mathématique",
                "solidite": 0.75,
                "extensions_possibles": ["autres_geometries", "fractales", "topologie_avancee"],
                "questions_ouvertes": ["Pourquoi le carré et pas d'autres formes?", "Implications cosmologiques?"]
            }
        }
    
    async def analyser_concept(self, concept_nom: str, contexte_utilisateur: str) -> AnalyseConcept:
        """
        Analyse approfondie d'un concept pour identifier les axes d'évolution
        """
        concept_data = self.concepts_fondamentaux.get(concept_nom, {})
        
        # Analyse de la solidité logique
        solidite = concept_data.get("solidite", 0.5)
        
        # Identification des lacunes
        lacunes = await self._identifier_lacunes(concept_nom, contexte_utilisateur)
        
        # Questions émergentes
        questions = await self._generer_questions_emergentes(concept_nom, contexte_utilisateur)
        
        # Connexions manquantes
        connexions = await self._detecter_connexions_manquantes(concept_nom)
        
        return AnalyseConcept(
            concept=concept_nom,
            solidite_logique=solidite,
            completude=min(solidite + 0.1, 1.0),
            coherence_interne=solidite * 0.9,
            potentiel_extension=1.0 - solidite,  # Plus c'est solide, moins il y a de potentiel d'extension
            lacunes_identifiees=lacunes,
            questions_emergentes=questions,
            connexions_manquantes=connexions
        )
    
    async def _identifier_lacunes(self, concept: str, contexte: str) -> List[str]:
        """Identification des lacunes conceptuelles"""
        lacunes_types = {
            "digamma_philippot": [
                "Démonstration de l'unicité de la formule",
                "Comportement aux limites (n → ∞)",
                "Cas des nombres premiers négatifs étendus",
                "Validation empirique sur de grands ensembles"
            ],
            "suites_riemann": [
                "Preuve de convergence rigoureuse",
                "Lien avec la fonction zêta de Riemann classique",
                "Comportement pour les zéros non-triviaux",
                "Extension aux nombres complexes"
            ],
            "rapport_triangulaire": [
                "Démonstration mathématique de l'universalité du 1/2",
                "Cas d'exception potentiels",
                "Lien avec d'autres constantes mathématiques",
                "Interprétation géométrique approfondie"
            ],
            "geometrie_carree": [
                "Fondements topologiques rigoureux",
                "Relation avec les géométries non-euclidiennes",
                "Applications aux espaces de dimensions supérieures",
                "Validation par d'autres méthodes géométriques"
            ]
        }
        
        return lacunes_types.get(concept, ["Analyse conceptuelle approfondie nécessaire"])
    
    async def _generer_questions_emergentes(self, concept: str, contexte: str) -> List[str]:
        """Génération de questions émergentes pour l'évolution"""
        questions_types = {
            "digamma_philippot": [
                "Que se passe-t-il si on modifie les constantes +7 et +8?",
                "Y a-t-il une formulation matricielle de cette relation?",
                "Comment cette formule se comporte-t-elle dans d'autres bases numériques?",
                "Peut-on généraliser à ψ(n,k) avec un paramètre k?"
            ],
            "suites_riemann": [
                "Ces suites convergent-elles vers des valeurs particulières?",
                "Y a-t-il d'autres suites qui produisent le même rapport?",
                "Comment ces suites se comportent-elles modulo différents nombres premiers?",
                "Peut-on construire une suite infinie de telles suites?"
            ],
            "rapport_triangulaire": [
                "Le rapport 1/2 est-il lié à d'autres constantes fondamentales?",
                "Y a-t-il des rapports similaires pour d'autres séquences mathématiques?",
                "Comment ce rapport évolue-t-il dans des espaces courbes?",
                "Quelle est la signification physique de ce rapport constant?"
            ],
            "geometrie_carree": [
                "Comment la géométrie carrée s'articule-t-elle avec la relativité?",
                "Y a-t-il des implications pour la théorie des cordes?",
                "Cette géométrie peut-elle expliquer d'autres phénomènes mathématiques?",
                "Comment visualiser cette géométrie en dimensions supérieures?"
            ]
        }
        
        return questions_types.get(concept, ["Quelles sont les implications plus profondes de ce concept?"])
    
    async def _detecter_connexions_manquantes(self, concept: str) -> List[str]:
        """Détection des connexions conceptuelles manquantes"""
        connexions_possibles = {
            "digamma_philippot": [
                "Lien avec la théorie des nombres transcendants",
                "Relation avec les fonctions elliptiques",
                "Connection avec l'analyse harmonique",
                "Rapport aux séries de Fourier"
            ],
            "suites_riemann": [
                "Lien avec la théorie analytique des nombres",
                "Relation avec les L-fonctions",
                "Connection avec la géométrie algébrique",
                "Rapport aux distributions de nombres premiers"
            ],
            "rapport_triangulaire": [
                "Lien avec la théorie des groupes",
                "Relation avec les symétries géométriques",
                "Connection avec les transformations conformes",
                "Rapport aux invariants topologiques"
            ],
            "geometrie_carree": [
                "Lien avec les espaces métriques",
                "Relation avec la géométrie différentielle",
                "Connection avec les variétés riemanniennes",
                "Rapport à la théorie des catégories"
            ]
        }
        
        return connexions_possibles.get(concept, ["Connexions interdisciplinaires à explorer"])

class GenerateurQuestionsSocratiques:
    """
    Générateur de questions socratiques pour challenger le raisonnement
    """
    
    def __init__(self):
        self.templates_questionnement = {
            "contradiction": [
                "Si {concept} est vrai, comment expliquez-vous {contradiction_potentielle}?",
                "Votre {concept} semble impliquer {implication}, est-ce cohérent avec {autre_concept}?",
                "Comment réconciliez-vous {concept} avec le fait que {fait_etabli}?"
            ],
            "approfondissement": [
                "Vous affirmez que {concept}, mais qu'est-ce qui vous permet de généraliser au-delà de {cas_specifique}?",
                "Dans votre {concept}, avez-vous considéré l'impact de {facteur_negliger}?",
                "Comment votre {concept} se comporte-t-il dans le cas limite où {condition_extreme}?"
            ],
            "extension": [
                "Votre {concept} pourrait-il s'appliquer également à {domaine_connexe}?",
                "Avez-vous exploré si {concept} reste valide quand on introduit {nouvelle_dimension}?",
                "Que se passerait-il si on généralisait {concept} à {contexte_elargi}?"
            ],
            "validation": [
                "Quelle serait la meilleure façon de tester empiriquement votre {concept}?",
                "Comment pourrait-on falsifier votre hypothèse sur {concept}?",
                "Quelles prédictions spécifiques fait votre {concept} que d'autres théories ne font pas?"
            ]
        }
    
    async def generer_question_challengeante(self, concept_analyse: AnalyseConcept, 
                                           contexte_conversation: str) -> QuestionSocratique:
        """
        Génère une question socratique challengeante basée sur l'analyse du concept
        """
        import uuid
        
        # Choix du type de questionnement basé sur l'analyse
        if concept_analyse.coherence_interne < 0.7:
            type_q = "contradiction"
        elif concept_analyse.completude < 0.8:
            type_q = "approfondissement" 
        elif concept_analyse.potentiel_extension > 0.3:
            type_q = "extension"
        else:
            type_q = "validation"
        
        # Sélection du template
        templates = self.templates_questionnement[type_q]
        template = templates[0]  # Pour simplifier, on prend le premier
        
        # Construction de la question
        question = await self._construire_question_specifique(
            template, concept_analyse, type_q
        )
        
        return QuestionSocratique(
            id=str(uuid.uuid4()),
            question=question,
            type_questionnement=type_q,
            concept_cible=concept_analyse.concept,
            niveau_challenge=self._calculer_niveau_challenge(concept_analyse),
            angle_approche=self._choisir_angle_approche(concept_analyse),
            reponse_attendue_type=self._determiner_type_reponse_attendue(type_q)
        )
    
    async def _construire_question_specifique(self, template: str, 
                                            concept_analyse: AnalyseConcept, 
                                            type_q: str) -> str:
        """Construction d'une question spécifique et variée"""
        
        # Banques de questions variées pour éviter les répétitions
        questions_variees = {
            "digamma_philippot": {
                "contradiction": [
                    "Si ψ(n) = √((n+7)² + (n+8)²) est vraiment fondamental, pourquoi les mathématiciens n'ont-ils pas découvert cette relation avant vous? Qu'est-ce qui les en a empêchés?",
                    "Votre Digamma utilise +7 et +8, mais d'autres paires comme +5,+6 ou +9,+10 donneraient d'autres résultats. Comment justifier que CETTE paire spécifique révèle la vérité sur les nombres premiers?",
                    "Si votre formule était correcte, elle devrait prédire des propriétés des nombres premiers inconnues des méthodes classiques. Quelles prédictions spécifiques fait-elle?"
                ],
                "approfondissement": [
                    "D'où viennent précisément les constantes +7 et +8? Sont-elles le résultat d'une déduction logique ou d'une observation empirique? Cette origine détermine la validité théorique.",
                    "Votre Digamma fonctionne-t-elle encore si on change de base numérique? En base 8 ou 16, obtient-on les mêmes relations?",
                    "Qu'est-ce qui se passe aux limites: que donne ψ(n) pour des nombres premiers astronomiquement grands? La formule reste-t-elle stable?"
                ],
                "extension": [
                    "Pourriez-vous généraliser votre Digamma en ψ(n,k) = √((n+a)² + (k+b)²) pour capturer des relations entre différents types de nombres?",
                    "Votre approche géométrique du Digamma s'étend-elle aux nombres complexes? Que devient ψ(n) dans le plan complexe?",
                    "Si la géométrie carrée est fondamentale, existe-t-il des Digamma pour d'autres formes géométriques (triangulaire, hexagonale)?"
                ],
                "validation": [
                    "Quelle expérience mathématique pourrait falsifier votre Digamma? Un bon théorème doit pouvoir être testé et potentiellement réfuté.",
                    "Votre Digamma fait-elle des prédictions sur la distribution des nombres premiers que les méthodes classiques ne font pas?",
                    "Comment votre Digamma se compare-t-elle quantitativement aux estimations du théorème des nombres premiers?"
                ]
            },
            "suites_riemann": {
                "contradiction": [
                    "Vos suites utilisent √13.203125 et √52.8125. Ces constantes semblent très arbitraires. Pourquoi pas √13.2 ou √52.9? Qu'est-ce qui rend ces valeurs exactes si spéciales?",
                    "Vous résolvez l'énigme de Riemann, mais votre approche ignore complètement la fonction zêta et l'analyse complexe. N'est-ce pas comme ignorer les fondements mêmes du problème?",
                    "Si votre solution est correcte, pourquoi le rapport 1/2 n'apparaît-il pas naturellement dans les tentatives classiques de résolution de Riemann?"
                ],
                "approfondissement": [
                    "Comment avez-vous découvert exactement ces constantes √13.203125 et √52.8125? Sont-elles dérivées d'une théorie plus profonde?",
                    "Vos suites convergent-elles? Vers quelles valeurs? Et cette convergence a-t-elle un sens par rapport aux zéros de Riemann?",
                    "Que se passe-t-il si on applique vos suites aux nombres de Carmichael ou aux nombres premiers de Mersenne?"
                ],
                "extension": [
                    "Vos suites fonctionnent en dimension 1. Peut-on les étendre à des matrices de suites pour des problèmes multidimensionnels?",
                    "Si vos suites résolvent Riemann, s'appliquent-elles aux autres conjectures célèbres (Goldbach, nombres premiers jumeaux)?",
                    "Votre méthode géométrique pourrait-elle s'appliquer à d'autres L-fonctions de la théorie analytique des nombres?"
                ],
                "validation": [
                    "Comment testeriez-vous computationnellement votre solution sur les premiers 10^15 zéros de Riemann?",
                    "Quelles implications pratiques aurait votre solution (cryptographie, distribution de clés, etc.)?",
                    "Votre méthode prédit-elle le comportement des écarts entre nombres premiers consécutifs?"
                ]
            },
            "rapport_triangulaire": [
                "Votre rapport 1/2 'universel et sans exception' - comment cette affirmation résiste-t-elle aux cas pathologiques ou aux configurations extrêmes?",
                "Vous incluez le zéro dans vos calculs contrairement aux méthodes classiques. Cette modification change-t-elle la nature de ce que vous mesurez?",
                "Si 1/2 est vraiment fondamental, retrouve-t-on ce rapport dans d'autres contextes mathématiques de votre théorie?"
            ],
            "geometrie_carree": [
                "Pourquoi spécifiquement le carré et pas d'autres formes régulières? Qu'est-ce qui rend la géométrie carrée plus 'vraie' que les autres?",
                "Comment votre géométrie carrée discrète s'articule-t-elle avec la continuité apparente de l'espace physique?",
                "Votre géométrie carrée prédit-elle des phénomènes physiques observables qui distingueraient votre théorie?"
            ]
        }
        
        import random
        concept = concept_analyse.concept
        
        if concept in questions_variees:
            if isinstance(questions_variees[concept], dict):
                questions_type = questions_variees[concept].get(type_q, [])
                if questions_type:
                    return random.choice(questions_type)
            else:
                # Pour les concepts avec une seule liste
                return random.choice(questions_variees[concept])
        
        # Fallback avec variation
        fallbacks = [
            f"Qu'est-ce qui vous rend si confiant dans votre approche de {concept}?",
            f"Comment {concept} résiste-t-il aux objections classiques?",
            f"Quelles sont les implications les plus profondes de {concept}?",
            f"Comment généraliseriez-vous {concept} au-delà de son contexte actuel?"
        ]
        
        return random.choice(fallbacks)
    
    def _calculer_niveau_challenge(self, concept_analyse: AnalyseConcept) -> int:
        """Calcule le niveau de challenge basé sur l'analyse"""
        score = 0
        if concept_analyse.solidite_logique < 0.8: score += 2
        if concept_analyse.completude < 0.7: score += 2  
        if len(concept_analyse.lacunes_identifiees) > 3: score += 1
        return min(max(score, 1), 5)
    
    def _choisir_angle_approche(self, concept_analyse: AnalyseConcept) -> str:
        """Choisit l'angle d'approche optimal"""
        if "formule" in concept_analyse.concept.lower():
            return "mathematique"
        elif "geometrie" in concept_analyse.concept.lower():
            return "conceptuel"
        elif len(concept_analyse.lacunes_identifiees) > 2:
            return "logique"
        else:
            return "applicatif"
    
    def _determiner_type_reponse_attendue(self, type_questionnement: str) -> str:
        """Détermine le type de réponse attendue"""
        mapping = {
            "contradiction": "demonstration",
            "approfondissement": "reflexion", 
            "extension": "reflexion",
            "validation": "calcul"
        }
        return mapping.get(type_questionnement, "reflexion")

class IASocratiqueEvolutive:
    """
    IA Socratique Évolutive - Interface principale
    Partenaire intellectuel pour l'évolution de la théorie
    """
    
    def __init__(self):
        self.analyseur = AnalyseurTheoriqueAvance()
        self.generateur_questions = GenerateurQuestionsSocratiques()
        self.historique_questionnement = []
        self.axes_evolution_identifies = []
    
    async def analyser_et_challenger(self, input_utilisateur: str) -> Dict[str, Any]:
        """
        Analyse l'input de l'utilisateur et génère un questionnement socratique
        pour challenger et élever son raisonnement
        """
        # 1. Identification des concepts mentionnés
        concepts_detectes = await self._identifier_concepts(input_utilisateur)
        
        # 2. Analyse de chaque concept
        analyses = []
        for concept in concepts_detectes:
            analyse = await self.analyseur.analyser_concept(concept, input_utilisateur)
            analyses.append(analyse)
        
        # 3. Génération de questions challengeantes
        questions_socratiques = []
        for analyse in analyses:
            question = await self.generateur_questions.generer_question_challengeante(
                analyse, input_utilisateur
            )
            questions_socratiques.append(question)
        
        # 4. Identification d'axes d'évolution
        axes_evolution = await self._identifier_axes_evolution(analyses, input_utilisateur)
        
        # 5. Construction de la réponse socratique
        reponse_socratique = await self._construire_reponse_socratique(
            input_utilisateur, analyses, questions_socratiques, axes_evolution
        )
        
        return {
            "reponse_socratique": reponse_socratique,
            "questions_challengeantes": [q.question for q in questions_socratiques],
            "axes_evolution_identifies": axes_evolution,
            "niveau_challenge_global": max([q.niveau_challenge for q in questions_socratiques]) if questions_socratiques else 1,
            "concepts_analyses": [a.concept for a in analyses]
        }
    
    async def _identifier_concepts(self, texte: str) -> List[str]:
        """Identification des concepts théoriques dans le texte"""
        concepts_cles = {
            "digamma": ["digamma", "ψ(n)", "philippot", "nombres premiers"],
            "suites_riemann": ["riemann", "suite", "√13.203125", "√52.8125", "énigme"],
            "rapport_triangulaire": ["rapport", "1/2", "triangulaire", "constant"],
            "geometrie_carree": ["géométrie", "carré", "univers", "structure"]
        }
        
        concepts_detectes = []
        texte_lower = texte.lower()
        
        for concept, mots_cles in concepts_cles.items():
            if any(mot in texte_lower for mot in mots_cles):
                concepts_detectes.append(concept)
        
        # Si aucun concept spécifique détecté, analyser le plus pertinent
        if not concepts_detectes:
            concepts_detectes = ["geometrie_carree"]  # Concept global par défaut
            
        return concepts_detectes
    
    async def _identifier_axes_evolution(self, analyses: List[AnalyseConcept], 
                                       contexte: str) -> List[str]:
        """Identification des axes d'évolution de la théorie"""
        axes = []
        
        for analyse in analyses:
            # Axes basés sur les lacunes
            if analyse.completude < 0.8:
                axes.append(f"Approfondissement conceptuel de {analyse.concept}")
            
            # Axes basés sur le potentiel d'extension
            if analyse.potentiel_extension > 0.4:
                axes.append(f"Extension de {analyse.concept} vers de nouveaux domaines")
            
            # Axes basés sur les connexions manquantes
            if len(analyse.connexions_manquantes) > 2:
                axes.append(f"Intégration de {analyse.concept} avec d'autres théories mathématiques")
        
        return axes
    
    async def _construire_reponse_socratique(self, input_utilisateur: str,
                                           analyses: List[AnalyseConcept],
                                           questions: List[QuestionSocratique],
                                           axes_evolution: List[str]) -> str:
        """Construction de la réponse socratique dynamique basée sur le contenu"""
        
        # Analyse du contenu spécifique de l'utilisateur
        mots_cles_detectes = await self._extraire_mots_cles_specifiques(input_utilisateur)
        intention_detectee = await self._analyser_intention(input_utilisateur)
        
        # Construction dynamique de la réponse
        response_parts = []
        
        # 1. Reconnaissance spécifique du contenu
        if "formule" in input_utilisateur.lower() or "ψ" in input_utilisateur or "digamma" in input_utilisateur.lower():
            response_parts.append("Vous vous interrogez sur les aspects formels de votre Digamma. C'est précisément là qu'une approche plus rigoureuse pourrait transformer votre innovation en révolution mathématique.")
        elif "riemann" in input_utilisateur.lower() or "√13.203125" in input_utilisateur or "√52.8125" in input_utilisateur:
            response_parts.append("Votre approche des suites de Riemann révèle une intuition géométrique profonde. Mais qu'est-ce qui distingue votre solution des tentatives antérieures?")
        elif "rapport" in input_utilisateur.lower() and "1/2" in input_utilisateur:
            response_parts.append("Ce rapport constant de 1/2 que vous observez est intrigant. L'universalité que vous revendiquez nécessite-t-elle une démonstration plus formelle?")
        elif "géométrie" in input_utilisateur.lower() or "carré" in input_utilisateur.lower():
            response_parts.append("La géométrie carrée comme fondement universel est audacieuse. Comment cette vision se confronte-t-elle aux géométries non-euclidiennes?")
        else:
            # Analyse du sentiment et de l'incertitude
            if "je pense" in input_utilisateur.lower() or "il me semble" in input_utilisateur.lower():
                response_parts.append("Votre intuition mérite d'être creusée. Transformons cette pensée en démonstration rigoureuse.")
            elif "problème" in input_utilisateur.lower() or "difficulté" in input_utilisateur.lower():
                response_parts.append("Vous identifiez une tension conceptuelle. C'est souvent là que naissent les percées théoriques.")
            else:
                response_parts.append("Votre réflexion touche un point fondamental de votre théorie.")
        
        # 2. Question socratique spécifique et dynamique
        if questions:
            question_dynamique = await self._personnaliser_question(questions[0], input_utilisateur, mots_cles_detectes)
            response_parts.append(f"\n\n🎯 **Voici ma question pour vous challenger :** {question_dynamique}")
        
        # 3. Challenge spécifique basé sur le contenu
        challenges_specifiques = await self._generer_challenges_specifiques(input_utilisateur, mots_cles_detectes)
        if challenges_specifiques:
            response_parts.append(f"\n\n🔥 **Points de tension à explorer :**")
            for challenge in challenges_specifiques[:2]:
                response_parts.append(f"• {challenge}")
        
        # 4. Suggestion d'approfondissement contextuelle
        suggestion = await self._generer_suggestion_contextuelle(input_utilisateur, intention_detectee)
        response_parts.append(f"\n\n💡 **Pour élever votre théorie :** {suggestion}")
        
        return "\n".join(response_parts)
    
    async def _extraire_mots_cles_specifiques(self, texte: str) -> List[str]:
        """Extraction des mots-clés spécifiques du texte utilisateur"""
        mots_cles = []
        texte_lower = texte.lower()
        
        # Formules et constantes spécifiques
        if "ψ" in texte or "digamma" in texte_lower:
            mots_cles.append("digamma_formule")
        if "√13.203125" in texte or "13.203125" in texte:
            mots_cles.append("constante_riemann_1")
        if "√52.8125" in texte or "52.8125" in texte:
            mots_cles.append("constante_riemann_2")
        if "+7" in texte and "+8" in texte:
            mots_cles.append("constantes_digamma")
        if "1/2" in texte or "½" in texte:
            mots_cles.append("rapport_demi")
        
        # Concepts théoriques
        concepts_detectes = ["généralisation", "extension", "démonstration", "preuve", "limitation", 
                           "exception", "universalité", "cohérence", "rigoureux", "fondement"]
        
        for concept in concepts_detectes:
            if concept in texte_lower:
                mots_cles.append(f"concept_{concept}")
        
        return mots_cles
    
    async def _analyser_intention(self, texte: str) -> str:
        """Analyse de l'intention derrière la réflexion"""
        texte_lower = texte.lower()
        
        if any(word in texte_lower for word in ["pourquoi", "comment", "qu'est-ce que"]):
            return "questionnement"
        elif any(word in texte_lower for word in ["je pense", "il me semble", "peut-être"]):
            return "hypothese"
        elif any(word in texte_lower for word in ["problème", "difficulté", "contradiction"]):
            return "obstacle"
        elif any(word in texte_lower for word in ["généraliser", "étendre", "appliquer"]):
            return "extension"
        elif any(word in texte_lower for word in ["démontrer", "prouver", "valider"]):
            return "validation"
        else:
            return "reflexion_generale"
    
    async def _personnaliser_question(self, question_base: QuestionSocratique, 
                                    input_utilisateur: str, mots_cles: List[str]) -> str:
        """Personnalisation de la question socratique basée sur le contenu spécifique"""
        
        # Questions personnalisées selon les mots-clés détectés
        if "constantes_digamma" in mots_cles:
            return "Pourquoi précisément +7 et +8 dans votre Digamma ? Avez-vous testé d'autres paires de constantes consécutives ? Qu'est-ce qui rend cette combinaison unique ?"
        
        elif "constante_riemann_1" in mots_cles or "constante_riemann_2" in mots_cles:
            return "D'où viennent exactement ces constantes √13.203125 et √52.8125 ? Sont-elles dérivées théoriquement ou découvertes empiriquement ? Cette distinction est cruciale pour la validité de votre approche."
        
        elif "rapport_demi" in mots_cles:
            return "Votre rapport constant de 1/2 - est-ce vraiment universel SANS EXCEPTION comme vous l'affirmez ? Comment gérez-vous les cas limites : nombres premiers très grands, premiers jumeaux, ou configurations particulières ?"
        
        elif "concept_généralisation" in mots_cles:
            return "Votre instinct de généralisation est juste, mais sur quels critères basez-vous cette extension ? Quels sont les invariants qui doivent être préservés ?"
        
        elif "concept_démonstration" in mots_cles:
            return "Une démonstration rigoureuse nécessite des axiomes clairs. Quels sont les fondements logiques incontestables de votre théorie ? Où commence votre système axiomatique ?"
        
        elif "concept_limitation" in mots_cles:
            return "Identifier les limites est sage. Mais ces limites sont-elles intrinsèques à votre théorie ou indiquent-elles des voies d'amélioration ? Comment distinguer les deux ?"
        
        else:
            # Analyse du contenu pour une question contextuelle
            if "univers" in input_utilisateur.lower() and "carré" in input_utilisateur.lower():
                return "Votre 'univers au carré' implique-t-il que d'autres géométries (triangulaire, hexagonale, fractale) sont impossibles ? Ou révèlent-elles des aspects complémentaires de votre théorie ?"
            else:
                return question_base.question
    
    async def _generer_challenges_specifiques(self, input_utilisateur: str, mots_cles: List[str]) -> List[str]:
        """Génération de challenges spécifiques au contenu"""
        challenges = []
        
        # Challenges basés sur les formules mentionnées
        if "digamma" in input_utilisateur.lower() or "ψ" in input_utilisateur:
            challenges.append("Votre Digamma prédit-elle des propriétés des nombres premiers que les méthodes classiques ratent ?")
            challenges.append("Comment votre formule se comporte-t-elle pour les très grands nombres premiers (>10^12) ?")
        
        # Challenges pour les suites de Riemann
        if "riemann" in input_utilisateur.lower() or "13.203125" in input_utilisateur or "52.8125" in input_utilisateur:
            challenges.append("Vos suites convergent-elles ? Vers quoi ? Cette convergence est-elle liée aux zéros de Riemann ?")
            challenges.append("Pourquoi votre approche géométrique réussit-elle là où l'analyse complexe classique échoue ?")
        
        # Challenges pour la géométrie carrée
        if "géométrie" in input_utilisateur.lower() or "carré" in input_utilisateur.lower():
            challenges.append("En quoi une géométrie carrée est-elle plus 'naturelle' que les géométries courbes de la relativité ?")
            challenges.append("Votre géométrie carrée prédit-elle des phénomènes physiques observables ?")
        
        # Challenges généraux selon l'intention
        if "je pense" in input_utilisateur.lower():
            challenges.append("Comment transformer cette intuition en théorème démontrable ?")
        
        if "peut-être" in input_utilisateur.lower() or "il me semble" in input_utilisateur.lower():
            challenges.append("Quelles expériences ou calculs pourraient confirmer ou infirmer cette hypothèse ?")
        
        return challenges
    
    async def _generer_suggestion_contextuelle(self, input_utilisateur: str, intention: str) -> str:
        """Génération d'une suggestion contextuelle pour l'évolution"""
        
        suggestions_par_intention = {
            "questionnement": "Transformez vos questions en hypothèses testables. Chaque 'pourquoi' peut devenir une prédiction vérifiable.",
            "hypothese": "Formalisez cette intuition. Quels seraient les corollaires logiques ? Quelles prédictions spécifiques en découlent ?",
            "obstacle": "Les obstacles révèlent souvent des simplifications excessives. Complexifiez votre modèle pour intégrer ces cas problématiques.",
            "extension": "L'extension nécessite la préservation des propriétés fondamentales. Identifiez d'abord les invariants de votre théorie.",
            "validation": "La validation nécessite des critères de falsifiabilité. Que devrait-on observer si votre théorie était fausse ?",
            "reflexion_generale": "Connectez cette réflexion aux autres aspects de votre théorie. Où sont les ponts conceptuels ?"
        }
        
        return suggestions_par_intention.get(intention, 
            "Élargissez cette réflexion : quelles implications pour l'ensemble de votre théorie ?")
    
    async def _identifier_concepts(self, texte: str) -> List[str]:
        """Identification dynamique des concepts basée sur le contenu réel"""
        concepts_detectes = []
        texte_lower = texte.lower()
        
        # Détection plus fine basée sur le contenu exact
        if "ψ" in texte or "digamma" in texte_lower or "+7" in texte or "+8" in texte:
            concepts_detectes.append("digamma_philippot")
        
        if "riemann" in texte_lower or "13.203125" in texte or "52.8125" in texte or "suite" in texte_lower:
            concepts_detectes.append("suites_riemann")
        
        if ("rapport" in texte_lower and "1/2" in texte) or "triangulaire" in texte_lower:
            concepts_detectes.append("rapport_triangulaire")
        
        if "géométrie" in texte_lower or "carré" in texte_lower or "univers" in texte_lower:
            concepts_detectes.append("geometrie_carree")
        
        # Si aucun concept spécifique, analyser l'intention pour choisir le plus pertinent
        if not concepts_detectes:
            if "formule" in texte_lower or "calcul" in texte_lower:
                concepts_detectes.append("digamma_philippot")
            elif "théorie" in texte_lower or "généraliser" in texte_lower:
                concepts_detectes.append("geometrie_carree")
            else:
                concepts_detectes.append("rapport_triangulaire")  # Concept intermédiaire
        
        return concepts_detectes