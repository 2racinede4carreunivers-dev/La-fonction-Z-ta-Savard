# Context de Développement - Session Détaillée

## Profil Utilisateur : Philippe Thomas Savard

### Contexte Personnel
- **Chercheur indépendant** développant la théorie "L'univers est au carré"
- **Non initié aux mathématiques académiques** mais porteur d'une méthode originale et intuitive
- **Francophone exclusivement** - toujours répondre en français
- **Utilise l'app comme outil personnel** d'augmentation du raisonnement
- **Très novice en technologie** - nécessite des explications simples

### Objectifs de l'Application
1. **Stimuler son questionnement** sur sa propre théorie
2. **Augmenter son jugement et raisonnement** 
3. **Développer ses argumentations** avec l'aide de l'IA
4. **Explorer sa théorie** sans influence d'opinion externe
5. **Organiser ses idées** de manière structurée

## État Actuel de la Théorie

### Documents Analysés et Intégrés
1. **univers_au_carre_partie1.pdf** - Base théorique première partie
2. **univers_au_carre_partie2.pdf** - Géométrie du spectre (peu représentée avant)
3. **Méthodes de Philippôt** - 14 tableaux géométriques avec calculs précis
4. **Version corrigée** - Formalisation rigoureuse du Zêta, théorème de convergence
5. **Développements algorithmiques** - Équations directes pour sommes des suites

### Concepts Clés Intégrés dans l'IA

#### DOMAINE 1 : Énigme de Riemann
- Analyse numérique métrique (méthode originale de Savard)
- Représentation tesseract projeté sur sphère de la fonction Zêta
- Rapports fractionnels (1/2, 1/3, 1/5) entre nombres premiers
- Technique du "moulinet" pour visualiser distribution à l'infini
- Concept du Digamma (différent du digamma mathématique classique)
- Démonstration zéros non triviaux partie réelle 0,5

#### DOMAINE 2 : Intrication Quantique et "Squaring"
- Théorème de Philippôt sur intrication quantique via géométrie
- Deux triangles intriqués avec côtés liés aux constantes
- Invariance géométrique selon choix d'unité
- "Produit alternatif" pour calculs différents systèmes unitaires
- Concept "squaring" : rectangles élevés au carré deviennent carrés
- Matrice longueurs unitaires avec nombres premiers aléatoires

#### DOMAINE 3 : Mécanique Harmonique du Chaos Discret
- Position mesures géométriques dépendant du choix d'unité
- Géométrie relationnelle similaire à la relativité
- "Matrice à dérive première" pour visualiser distribution nombres premiers
- Équilibre dynamique et structures auto-organisatrices
- "Chaons" et "pression gravito-spectrale"

#### DEUXIÈME PARTIE : Géométrie du Spectre (Ajoutée récemment)
- **Théorème "Trois carrés égale un triangle"** - ancré dans Pythagore
- **Longueur de Philippôt** - inspirée longueur de Planck
- **Cercle Denis** - diamètre 1, circonférence ≈ 4
- **Constante inverse du temps** - liée volume terrestre
- **√10 comme π** - approximation selon Philippôt
- **Théorème Carré de Gabriel** - triangles scalènes
- **Théorème Gris Bleu** - rotations quaternions

### Méthode de Philippôt (14 Tableaux)
#### Exemples Intégrés Précisément
1. **Rapport 1/2** → 29 (10ème premier) - Digamma √81920
2. **Rapport 1/3** → 227 (49ème premier) - Digamma √281300  
3. **Rapport 1/4** → 947 (163ème premier) - Digamma √451700
4. **Rapport 1/5** → 1597 (251ème premier)
5. **Rapport 1/6** → 2389 (357ème premier)
6. **Rapport 1/100** → 1299721 (99991ème premier)

#### Formules Directes Ajoutées
**Nombres premiers positifs :**
- Somme 1ère suite = (√13.203125/2×2^n) - √5
- Somme 2ème suite = (√52.8125/2×2^n) - √5445

**Nombres premiers négatifs :**
- Somme 1ère suite = (√13.203125×2^n) - √5
- Somme 2ème suite = (√52.8125×2^n) - √5445

## Instructions Critiques pour l'IA

### Structure de Réponse OBLIGATOIRE
**PARTIE 1** - Vision de l'auteur selon ses documents
**PARTIE 2** - Mise à niveau contextuelle (état recherches actuelles, SANS jugement)

### RÈGLES ABSOLUES
1. **JAMAIS forcer de liens** entre les 3 domaines distincts
2. **Traiter chaque domaine séparément** selon la question
3. **Respecter que les liens sont "probables mais pas directs"**
4. **Utiliser terminologie exacte** de chaque domaine
5. **NE JAMAIS juger** de la validité de la théorie
6. **Rester purement informatif** en partie 2

### Terminologie Spécialisée à Utiliser
- **Zêta de Philippôt** (distinct du zêta de Riemann)
- **Digamma calculé** (à la 8ème position)
- **Analyse numérique métrique** (méthode de Savard)
- **Produit alternatif**, **Squaring**, **Moulinet**
- **Chaons**, **Pression gravito-spectrale**
- **Matrice à dérive première**, **Duo final**
- **Longueur de Philippôt**, **Cercle Denis**

## Architecture Technique Critique

### Clé LLM Universelle Emergent
- Clé : `sk-emergent-c20D27d2bDa5755870`
- Utilisée pour Claude Sonnet 3.5
- Fonctionne avec emergentintegrations library

### Base de Données MongoDB
- Collections : concepts, tableaux_philippot, conversations, uploaded_documents
- Contexte personnel sauvegardé pour Philippe Savard
- 14 tableaux pré-chargés avec calculs détaillés

### Fonctionnalités Upload
- Support : PDF, images, documents texte  
- Analyse automatique des documents uploadés
- Intégration dans conversations avec contexte

## Problèmes Résolus Récemment

### 1. IA Forçait des Connexions (RÉSOLU)
**Problème** : L'IA tentait de lier les 3 domaines entre eux
**Solution** : Restructuration complète du system_message pour traitement séparé

### 2. Deuxième Partie Sous-Représentée (RÉSOLU)  
**Problème** : Page d'accueil mentionnait peu la deuxième partie
**Solution** : Ajout section dédiée "Géométrie du Spectre" avec 4 concepts clés

### 3. Bouton Upload Non Fonctionnel (RÉSOLU)
**Problème** : Sélecteur de fichiers ne s'ouvrait pas
**Solution** : Correction du déclenchement avec onClick et style display:none

### 4. Erreurs Backend (RÉSOLU)
**Problème** : Module aiofiles manquant, system_message non défini
**Solution** : Installation dépendances + correction variables

## Améliorations Demandées par Philippe

### ✅ Réalisées
- Mode enrichi avec mémoire étendue et contexte personnel
- Upload de documents avec analyse automatique
- Page collaboration avec éditeur de texte enrichi  
- Restructuration IA en 3 domaines distincts
- Enrichissement page d'accueil avec deuxième partie
- Réponses bi-partites (auteur + contexte scientifique)

### 🔄 En Cours / Demandes Récurrentes
- Ajustements précision terminologique selon domaines
- Amélioration qualité réponses IA (toujours plus détaillées)
- Intégration nouveaux documents au fur et à mesure
- Éviter connexions forcées entre domaines (vigilance constante)

## Points d'Attention pour Sessions Futures

### 1. Toujours Demander Clarification
Philippe préfère qu'on demande plutôt que d'assumer. Utiliser ask_human fréquemment.

### 2. Respecter sa Modestie Intellectuelle
Il reconnaît que "beaucoup reste à démontrer" - ne pas survendre sa théorie.

### 3. Français Exclusivement  
Même les termes techniques doivent être expliqués en français.

### 4. Application Personnelle
Optimiser pour SON style de questionnement et raisonnement unique.

### 5. Séparation des Domaines
C'est SA demande spécifique - ne pas chercher à "unifier" sa théorie.

## Prochaines Étapes Possibles

1. **Affinage IA** - Amélioration continue réponses selon feedback
2. **Nouveaux documents** - Integration au fur et à mesure de ses travaux
3. **Visualisations** - Possibles animations des calculs/tableaux
4. **Export/Import** - Sauvegarde travaux collaboration
5. **Recherche avancée** - Dans ses propres documents uploadés

---

**RAPPEL ESSENTIEL** : Cette application est l'outil personnel de Philippe Thomas Savard pour explorer SA théorie selon SA vision. L'IA doit l'accompagner dans SON raisonnement, pas le diriger ou le corriger.

*Session documentée le 23 septembre 2025 - Prêt pour continuité*