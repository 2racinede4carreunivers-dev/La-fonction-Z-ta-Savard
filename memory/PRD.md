# L'univers est au carré - Product Requirements Document

## Problème Original
Application web complète pour explorer et interagir avec la théorie mathématique personnelle "L'univers est au carré" de Philippe Thomas Savard, concernant la géométrie du spectre premier et l'hypothèse de Riemann.

## Architecture Technique
- **Frontend**: React.js avec Tailwind CSS
- **Backend**: FastAPI (Python)
- **Base de données**: MongoDB
- **IA**: Claude Sonnet 4.5 via Emergent LLM Key

## Fonctionnalités Implémentées

### Modules IA
1. **IA Spécialisée** - Expert de la théorie avec base de connaissances GitHub (contexte 250k car.)
2. **IA Évolutive** - Banque Q&R synchronisée GitHub (124+ Q&R) + apprentissage utilisateurs
3. **IA Socratique** - Challenge et questionnement du raisonnement

### Synchronisation GitHub (ACTIF)
- **Dépôt**: https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026
- **Sync contenu IA**: 5 .thy + 7 .tex (nettoyés) + 7 .md = ~250k car.
- **Sync banque Q&R**: 106 Q&R depuis SQLite (`qa_bank/qa_bank.db`) -> fusionnées avec la banque logiciel (21 originales) = 127 total
- **Sync automatique**: Toutes les heures (contenu + Q&R)
- **Sync manuelle**: Bouton dans Admin > Sync GitHub
- **Endpoints**: `POST /api/github/sync`, `GET /api/github/status`

### Système Admin
- Accès: icône 🔑 (bas gauche) + Ctrl+Alt+W + mot de passe
- Page `/admin-questions` avec onglets:
  - **Historique Questions**: log des questions posées aux IA
  - **Sync GitHub**: statut, taille contexte, banque Q&R, bouton sync manuelle

### Documents et Preuves Formelles
- Upload de documents avec protection par mot de passe
- Support des fichiers Isabelle HOL (.thy)

## Fichiers Clés
- `/app/backend/server.py` - Serveur API principal
- `/app/backend/github_sync.py` - Sync GitHub: contenu IA + banque Q&R
- `/app/backend/modules/evolutionary_qa_system.py` - IA Évolutive avec banque fusionnée
- `/app/frontend/src/App.js` - Frontend monolithique (>12k lignes)
- `/app/data/banque_evolutive.json` - Banque Q&R fusionnée (GitHub + logiciel)

## Intégrations Tierces
- Anthropic Claude via `emergentintegrations`

## Mots de Passe et Codes Secrets
- **Admin/Upload**: `Uni1098020238ARC1374079226497308zetacar`
- **Phrase Auteur**: `je suis l'auteur de la théorie:1374079226497308`

## Backlog
1. **Refactorisation App.js** (P2) - Découper en composants plus petits (reporté)
2. **Projet Fusion** (P3) - Fusion avec applications LaTeX et CAO

## Dernière Mise à Jour
- **Date**: 4 mai 2026
- **Changement**: Synchronisation bidirectionnelle banque Q&R entre dépôt GitHub (106 Q&R SQLite) et logiciel web (21 Q&R originales). L'IA Évolutive bénéficie désormais de 124+ Q&R.
