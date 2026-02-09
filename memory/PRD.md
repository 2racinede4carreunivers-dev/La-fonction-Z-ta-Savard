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
- **NOUVEAU (Feb 2025)**: Intégration de 2 scripts Isabelle HOL validés:
  - `geometrie_spectre_premier.thy` - Fondations du rapport spectral 1/2, 1/3, 1/4, suites négatives, calcul d'écart entre premiers
  - `geometrie_spectre_premier_second_chapitre.thy` - Méthode de Philippôt généralisée pour n termes

## Intégrations Tierces
- Anthropic Claude via `emergentintegrations`

## Fichiers Clés
- `/app/backend/server.py` - Serveur API principal
- `/app/frontend/src/App.js` - Frontend monolithique (>12,000 lignes)
- `/app/data/isabelle_proofs/` - Scripts Isabelle HOL formels

## Mots de Passe Secrets
- **Admin/Upload**: `Uni1098020238Arc1374079226497308\zetacar`
- **Phrase Auteur**: `Bonjour? Je souhaite discuter de ta compréhension de la théorie moi l'auteur Philippôt Uni#109802038Arc1374079226497308\zetacar`

## Backlog (P2/P3)
1. **Refactorisation App.js** - Découper en composants plus petits
2. **Projet Fusion** - Fusion avec applications LaTeX et CAO

## Dernière Mise à Jour
- **Date**: 9 février 2025
- **Changement**: Ajout des 2 scripts Isabelle HOL dans la base de connaissances de l'IA
