# L'univers est au carré - Product Requirements Document

## Problème Original
Application web complète pour explorer et interagir avec la théorie mathématique "L'univers est au carré" de Philippe Thomas Savard.

## Architecture Technique
- **Frontend**: React.js avec Tailwind CSS + Shadcn/UI
- **Backend**: FastAPI (Python)
- **Base de données**: MongoDB
- **IA**: Claude Sonnet 4.5 via Emergent LLM Key (emergentintegrations)

## Fonctionnalités Implémentées

### Modules IA
1. **IA Spécialisée** (`/chat`) - Expert de la théorie avec base de connaissances GitHub (~250k car.)
2. **IA Évolutive** (`/ia-evolutif`) - Banque Q&R synchronisée GitHub (127+ Q&R) + apprentissage utilisateurs
3. **IA Socratique** (`/ia-socratique`) - Challenge et questionnement du raisonnement
4. **Gabriel** (`/gabriel`) - **NOUVEAU** - Assistant HOL spécialisé géométrie du spectre des nombres premiers
   - Moteur de calcul spectral Python (suites SA/SB, digamma, vérification premiers, rapports spectraux 4 configurations, écarts)
   - Table de 1000 nombres premiers (2 à 7919)
   - Détection automatique des calculs nécessaires dans les questions
   - Réponses LLM enrichies par les résultats de calcul vérifiés
   - Panneau de calcul direct (analyser, position, n-ième premier)

### Synchronisation GitHub (ACTIF)
- **Dépôt**: Theorie-mathematique-philippe-thomas-savard-2026
- **Sync contenu IA**: 5 .thy + 7 .tex + 7 .md = ~250k car.
- **Sync banque Q&R**: 106 Q&R depuis SQLite -> fusionnées (127 total)
- **Sync automatique**: Toutes les heures + bouton manuel dans Admin

### Système Admin
- Accès: icône 🔑 + Ctrl+Alt+W + mot de passe
- Onglets: Historique Questions + Sync GitHub

## Fichiers Clés
- `/app/backend/server.py` - Serveur API principal
- `/app/backend/github_sync.py` - Sync GitHub
- `/app/backend/modules/gabriel/spectral_engine.py` - Moteur de calcul spectral
- `/app/backend/modules/gabriel/gabriel_service.py` - Service Gabriel (LLM + calcul)
- `/app/backend/modules/evolutionary_qa_system.py` - IA Évolutive
- `/app/frontend/src/App.js` - Frontend

## API Endpoints
- `POST /api/chat` - IA Spécialisée
- `POST /api/ia-evolutif/dialoguer` - IA Évolutive
- `POST /api/ia-socratique/challenger` - IA Socratique
- `POST /api/gabriel/ask` - Gabriel (question + calcul + LLM)
- `POST /api/gabriel/compute` - Calcul spectral direct (sans LLM)
- `POST /api/github/sync` + `GET /api/github/status` - Sync GitHub

## Credentials
- **Admin**: `Uni1098020238ARC1374079226497308zetacar`
- **Phrase Auteur**: `je suis l'auteur de la théorie:1374079226497308`

## Backlog
1. Refactorisation App.js (P2) — reportée
2. Projet Fusion LaTeX + CAO (P3)

## Dernière Mise à Jour
- **Date**: 4 mai 2026
- **Changement**: Intégration de Gabriel (agent multi-boucle HOL) comme 4ème module IA dans le logiciel web, avec moteur de calcul spectral complet et clé Emergent
