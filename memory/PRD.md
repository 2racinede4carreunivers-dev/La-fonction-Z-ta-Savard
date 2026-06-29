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
2. **IA Évolutive** (`/ia-evolutif`) - Banque Q&R synchronisée (179 Q&R)
3. **IA Socratique** (`/ia-socratique`) - Challenge du raisonnement
4. **Gabriel V2** (`/gabriel`) - Assistant HOL spécialisé géométrie du spectre des nombres premiers
   - Moteur de calcul spectral V2: SA/SB, digamma, vérification premiers, rapports RSP, écarts
   - **Formule d'écart CORRIGÉE** (gap_solver_final): Supporte (+,+), (-,-), et mixte (-,+)
   - **Nombres premiers négatifs** (n ≤ -1): SA_neg = 3.25×2^n-2, SB_neg = 6.5×2^n-66
   - **Courbes RSP** avec configurations: 1x1, sym, chaos, ord
   - **4 graphiques spectraux** automatiques sous les réponses (Recharts)
   - Détection automatique des calculs (reconstruct, reconstruct_neg, analyze, range, ratio, gap_v2, rsp_curve)
   - Composants visuels dans `/app/frontend/src/visuel-gabriel-isabelle/`

### Synchronisation GitHub
- Dépôt principal: Theorie-mathematique-philippe-thomas-savard-2026
- Dépôt Gabriel local: agent-multiloop-Gabriel-local (analysé pour mise à jour V2)
- Contenu IA: .thy + .tex + .md + documentation Gabriel (Ia_geo_spec_prem_app_deplo)
- Banque Q&R: 179 Q&R fusionnées
- Sync auto horaire + bouton manuel dans Admin

### Système Admin
- Accès: 🔑 + Ctrl+Alt+W + mot de passe → `/admin-questions`
- Onglets: Historique Questions + Sync GitHub

## Fichiers Clés Gabriel V2
- `/app/backend/modules/gabriel/spectral_engine.py` - Moteur calcul spectral V2 (positif + négatif)
- `/app/backend/modules/gabriel/gabriel_service.py` - Service Gabriel (détection + LLM)
- `/app/backend/modules/gabriel/gap_solver.py` - **NOUVEAU** Formule d'écart V2 corrigée
- `/app/backend/modules/gabriel/rsp_curve.py` - **NOUVEAU** Courbes RSP avec rendu ASCII
- `/app/frontend/src/visuel-gabriel-isabelle/SpectralVisualizer.jsx` - 4 graphiques
- `/app/backend/server.py` - API principale
- `/app/backend/github_sync.py` - Sync GitHub (inclut maintenant Ia_geo_spec_prem_app_deplo)

## API Endpoints Gabriel V2
- `POST /api/gabriel/ask` - Question Gabriel (calcul + LLM)
- `POST /api/gabriel/compute` - Calcul spectral direct
- `GET /api/gabriel/visualize` - Données pour graphiques
- `POST /api/gabriel/gap` - **NOUVEAU** Écart spectral V2 (positifs, négatifs, mixtes)
- `GET /api/gabriel/rsp-curve` - **NOUVEAU** Courbe RSP (config=1x1|sym|chaos|ord)

## Autres API Endpoints
- `POST /api/chat`, `/api/ia-evolutif/dialoguer`, `/api/ia-socratique/challenger`
- `POST /api/github/sync`, `GET /api/github/status`

## Credentials
- **Admin**: `Uni1098020238ARC1374079226497308zetacar`
- **Phrase Auteur**: `je suis l'auteur de la théorie:1374079226497308`

## Backlog
1. Refactorisation App.js (P2) — reportée (>12,000 lignes)
2. Projet Fusion LaTeX + CAO (P3)

## Dernière Mise à Jour
- **Date**: Décembre 2025
- **Changements**:
  - **BUG FIX CRITIQUE**: Erreur 500 sur calcul d'écarts mixtes (ex: -7 et 29)
    - Root cause: `gap_solver.py` retournait `pos_min/pos_max` mais `gabriel_service.py` attendait `position_p1/position_p2`
    - Correction: Ajout des clés attendues dans `GapResult.to_dict()` + sous-dict `validation`
    - Tous les cas testés passent: (+,+), (-,-), (-,+)
  - **Tests mis à jour**: `test_gabriel_v2.py` aligné avec le comportement corrigé
  - **20/20 tests passent** (test_gabriel_v2.py + test_gabriel_gap_fix.py)

### Historique Antérieur
- **Git pull Gabriel v6.x** depuis le dépôt local mis à jour (v6.0, v6.1, v6.2)
- **Nouveaux graphiques avancés implémentés**:
  - **Courbe Digamma Calculé** (n=1 à n=200) avec formule digamma_calc(n,p) = SB(n) - 64×p
  - **Rapport Spectral Asymétrique Ordonné** (100 paires) avec blocs A et B croissants
- **Nouveaux fichiers backend**:
  - `advanced_visualizations.py` - Génération des données pour les graphiques avancés
  - `spectral_models.py` - 3 modèles spectraux (1/2, 1/3, 1/4) avec `Fraction` exacte
  - `hol_generator.py` - Générateur de preuves HOL/Isabelle formelles
- **Nouveau composant frontend**:
  - `AdvancedSpectralVisualizer.jsx` - Affichage des graphiques avancés
- **Nouveaux endpoints API**:
  - `GET /api/gabriel/digamma-curve` - Courbe digamma n=1 à n=200
  - `GET /api/gabriel/asymmetric-ordered` - Rapport asymétrique ordonné
  - `GET /api/gabriel/asymmetric-sums` - Sommes des blocs A et B
- Reconstruction avec fragment HOL généré automatiquement
- **FIX**: Détection prioritaire "écart" vs "reconstruction"
- **FIX**: Détection ordinale ("37ième" → reconstruct n=37)
