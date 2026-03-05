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
1. **IA Spécialisée** - Expert de la théorie avec base de connaissances enrichie
2. **IA Évolutive** - Apprentissage continu basé sur les conversations
3. **IA Socratique** - Challenge et questionnement du raisonnement

### Galerie de Schémas
- 22 images de visualisation de la théorie
- Section "Schémas & Visualisations" dans l'interface

### Système Admin
- Page secrète `/admin-questions` pour historique des questions
- Accès via icône 🔑 + Ctrl+Shift+A
- Protection par mot de passe
- Logging des questions posées à l'IA Spécialisée

### Documents et Preuves Formelles
- Upload de documents avec protection par mot de passe
- Support des fichiers Isabelle HOL (.thy) via le bouton "Ajouter document"
- **NOUVEAU**: Intégration complète du dépôt GitHub de Philippe Thomas Savard:
  - URL: https://github.com/2racinede4carreunivers-dev/analyse-de-la-conjecture-zeta-riemann-savard
  - Fichiers Isabelle HOL (67,419 caractères): `methode_spectral.thy`, `methode_de_philippot.thy`
  - Guides méthodologiques (24,493 caractères): `README.md`, `guide_methode_de_philippot.md`, `guide_methode_spectrale.md`
  - Certification: Isabelle2025-2 Build Passing, LaTeX PDF OK (3 mars 2026)
  - Licence: Apache 2.0

## Intégrations Tierces
- Anthropic Claude via `emergentintegrations`

## Fichiers Clés
- `/app/backend/server.py` - Serveur API principal
- `/app/frontend/src/App.js` - Frontend monolithique (>12,000 lignes)
- `/app/data/isabelle_proofs/methode_spectral.thy` - Preuves spectrales (rapport 1/2, 1/3, 1/4, asymétries)
- `/app/data/isabelle_proofs/methode_de_philippot.thy` - Méthode de Philippôt généralisée

## Mots de Passe et Codes Secrets
- **Admin/Upload**: `Uni1098020238ARC1374079226497308zetacar`
- **Phrase Auteur** (pour toutes les IAs): `Bonjour je m'appelle Philippe Thomas Savard, je suis l'auteur de la théorie:1374079226497308.`

## Backlog (P2/P3)
1. **Refactorisation App.js** - Découper en composants plus petits
2. **Projet Fusion** - Fusion avec applications LaTeX et CAO

## Dernière Mise à Jour
- **Date**: 9 février 2025
- **Changement**: Ajout des 2 scripts Isabelle HOL dans la base de connaissances de l'IA
