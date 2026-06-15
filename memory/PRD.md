# L'univers est au carré - Product Requirements Document

## Problème Original
Application web pour explorer la théorie mathématique "L'univers est au carré" de Philippe Thomas Savard.

## Architecture Technique
- **Frontend**: React.js + Tailwind CSS + Shadcn/UI + Recharts (graphiques)
- **Backend**: FastAPI (Python)
- **Base de données**: MongoDB
- **IA**: Claude Sonnet 4.5 via Emergent LLM Key

## Fonctionnalités Implémentées

### Modules IA
1. **IA Spécialisée** (`/chat`) - Base de connaissances GitHub (~250k car.)
2. **IA Évolutive** (`/ia-evolutif`) - Banque Q&R synchronisée (127+ Q&R)
3. **IA Socratique** (`/ia-socratique`) - Challenge du raisonnement
4. **Gabriel** (`/gabriel`) - Assistant HOL spécialisé géométrie du spectre des nombres premiers
   - Moteur de calcul spectral: SA/SB, digamma, vérification premiers, rapports RSP, écarts
   - **Nombres premiers négatifs** (n ≤ -1): SA_neg = 3.25×2^n-2, SB_neg = 6.5×2^n-66
   - **4 graphiques spectraux** automatiques sous les réponses (Recharts):
     - Suites SA/SB (log10), Digamma, RSP convergence vers 1/2, Écarts entre premiers
   - Détection automatique des calculs (reconstruct, reconstruct_neg, analyze, range, ratio, gap)
   - Composants visuels dans `/app/frontend/src/visuel-gabriel-isabelle/`

### Synchronisation GitHub
- Dépôt: Theorie-mathematique-philippe-thomas-savard-2026
- Contenu IA + Banque Q&R (106 GitHub + 21 originales = 127 total)
- Sync auto horaire + bouton manuel dans Admin

### Système Admin
- Accès: 🔑 + Ctrl+Alt+W + mot de passe → `/admin-questions`
- Onglets: Historique Questions + Sync GitHub

## Fichiers Clés
- `/app/backend/modules/gabriel/spectral_engine.py` - Moteur calcul spectral (positif + négatif)
- `/app/backend/modules/gabriel/gabriel_service.py` - Service Gabriel (détection + LLM)
- `/app/frontend/src/visuel-gabriel-isabelle/SpectralVisualizer.jsx` - 4 graphiques
- `/app/backend/server.py` - API principale
- `/app/backend/github_sync.py` - Sync GitHub

## API Endpoints
- `POST /api/gabriel/ask` - Question Gabriel (calcul + LLM)
- `POST /api/gabriel/compute` - Calcul spectral direct
- `GET /api/gabriel/visualize` - Données pour graphiques
- `POST /api/chat`, `/api/ia-evolutif/dialoguer`, `/api/ia-socratique/challenger`
- `POST /api/github/sync`, `GET /api/github/status`

## Credentials
- **Admin**: `Uni1098020238ARC1374079226497308zetacar`
- **Phrase Auteur**: `je suis l'auteur de la théorie:1374079226497308`

## Backlog
1. Refactorisation App.js (P2) — reportée
2. Projet Fusion LaTeX + CAO (P3)

## Dernière Mise à Jour
- **Date**: 4 mai 2026
- **Changements**: Ajout support nombres premiers négatifs (n ≤ -1) + 4 graphiques spectraux automatiques (suites, digamma, RSP, écarts) dans Gabriel
