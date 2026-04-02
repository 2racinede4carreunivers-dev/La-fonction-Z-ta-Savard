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
1. **IA Spécialisée** - Expert de la théorie avec base de connaissances enrichie (contexte GitHub)
2. **IA Évolutive** - Apprentissage continu basé sur les conversations
3. **IA Socratique** - Challenge et questionnement du raisonnement

### Synchronisation GitHub (ACTIF)
- **Dépôt**: https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026
- **Fichiers chargés**:
  - 5 fichiers `.thy` (Isabelle/HOL) : `methode_spectral.thy`, `methode_de_philippot.thy`, `espace_philippot.thy`, `mecanique_discret.thy`, `postulat_carre.thy` (~105k car.)
  - 7 fichiers `.tex` (texte extrait, blocs HOL dédupliqués) : `geometrie_du_spectre_premier.tex`, `geometry_prime_spectrum.tex`, `mecanique_harmonique_du_chaos_discret.tex`, `postulat_de_univers_carre.tex`, `espace_de_philippot.tex`, `pilosophy_geometry_of_prime_number.tex`, `teleosemantique_philosophie_esprit_analogiste.tex` (~100k car.)
  - 7 fichiers `.md` (documentation) (~27k car.)
- **Total contexte**: ~235k caractères
- **Sync automatique**: Toutes les heures
- **Endpoints**: `POST /api/github/sync`, `GET /api/github/status`
- **Optimisation**: Les scripts HOL embarqués dans les .tex sont retirés (déjà couverts par les .thy officiels)

### Galerie de Schémas
- 22 images de visualisation de la théorie

### Système Admin
- Accès via icône 🔑 + Ctrl+Alt+W
- Protection par mot de passe
- Page `/admin-questions` pour historique des questions

### Documents et Preuves Formelles
- Upload de documents avec protection par mot de passe
- Support des fichiers Isabelle HOL (.thy)

## Intégrations Tierces
- Anthropic Claude via `emergentintegrations`

## Fichiers Clés
- `/app/backend/server.py` - Serveur API principal (~6600 lignes)
- `/app/backend/github_sync.py` - Synchronisation GitHub avec extraction .thy/.tex/.md
- `/app/frontend/src/App.js` - Frontend monolithique (>12,000 lignes)
- `/app/backend/modules/evolutionary_qa_system.py` - IA Évolutive
- `/app/backend/modules/ia_socratique_evolutive.py` - IA Socratique

## Mots de Passe et Codes Secrets
- **Admin/Upload**: `Uni1098020238ARC1374079226497308zetacar`
- **Phrase Auteur** (pour toutes les IAs): `je suis l'auteur de la théorie:1374079226497308`

## Backlog (P2/P3)
1. **Refactorisation App.js** - Découper en composants plus petits (reporté par l'utilisateur)
2. **Projet Fusion** - Fusion avec applications LaTeX et CAO

## Dernière Mise à Jour
- **Date**: 2 avril 2026
- **Changement**: Migration sync GitHub vers nouveau depot + ajout bouton "Sync GitHub" dans le panneau admin (Salon de Lecture > Admin > Sync GitHub)
