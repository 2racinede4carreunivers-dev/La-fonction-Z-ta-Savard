# Géométrie du spectre des nombres premiers
Projet conceptuel et formel de Philippe Thomas Savard

Ce dépôt présente un projet d’analyse conceptuelle lié à la conjecture de la fonction zêta de Bernhard Riemann. L’approche développée ici, appelée géométrie du spectre des nombres premiers, propose un outil dynamique permettant d’examiner la structure des nombres premiers et leur relation avec les propriétés analytiques de la fonction zêta.

Le projet repose sur deux méthodes validées par des scripts Isabelle/HOL, accompagnées de documents LaTeX explicatifs en français et en anglais. L’ensemble du contenu est distribué sous licence Apache 2.0.

---

## 1. Présentation générale

L’objectif du projet est d’explorer la conjecture de Riemann à travers une approche personnelle et conceptuelle. Deux scripts Isabelle/HOL structurent cette démarche :

- `methode_de_philippot.thy`
- `methode_spectral.thy`

Ces fichiers sont validés par Isabelle/HOL et inclus dans le dépôt. Les documents LaTeX associés détaillent les méthodes, les exemples de calculs et les fondements conceptuels.

---

## 2. Méthode de Philippôt

La méthode de Philippôt constitue le premier chapitre du projet. Elle vise à vérifier qu’il est cohérent de poser la question de la conjecture de Riemann avant d’en entreprendre l’analyse.

Les idées principales sont les suivantes :

- Les zéros non triviaux de la fonction zêta sont infinis.
- Les nombres premiers sont également infinis.
- La conjecture affirme que tous les zéros non triviaux ont une partie réelle égale à \(1/2\).
- La méthode explore, par des suites rationnelles et des opérations itératives, la possibilité de générer indéfiniment la valeur \(1/2\).
- Si cette génération s’était révélée impossible, la conjecture aurait été infirmée par l’absurde.

Le fichier `methode_de_philippot.thy` formalise cette méthode et en assure la validité logique.

---

## 3. Méthode spectrale

Le second chapitre, formalisé dans `methode_spectral.thy`, présente la méthode spectrale, cœur de la géométrie du spectre des nombres premiers.

Cette méthode repose sur l’idée que :

> Pour tout entier \(n \ge 1\) ou \(n \le -1\), chaque valeur de \(n\) correspond à un nombre premier \(P\). Les suites \(A\) et \(B\) déterminent la valeur de \(n\), et le rapport spectral \(1/k\) est numériquement valide mais algébriquement incohérent.

Le fichier détaille notamment :

- la construction des suites \(A\) et \(B\),
- la substitution liée à la lettre grecque zêta et au digamma,
- les équations généralisées pour déterminer les suites,
- des exemples de calculs (29, 31, 37, 41),
- le rôle particulier du digamma,
- la détermination des nombres premiers à partir de \(n\),
- les rapports spectraux \(1/2\), \(1/3\), \(1/4\),
- les écarts entre nombres premiers selon ces rapports,
- l’axiomatisation reliant :
  - la fonction zêta,
  - le rapport spectral,
  - la valeur de \(n\),
  - la densité des zéros sur la droite critique.

---

## 4. Documents LaTeX

Deux documents LaTeX (français et anglais) accompagnent les scripts Isabelle/HOL. Ils présentent :

- des explications détaillées des deux méthodes,
- des exemples de calculs,
- des illustrations conceptuelles,
- des démonstrations textuelles rédigées par l’auteur.

Ces documents servent de guide pour les utilisateurs souhaitant comprendre ou modifier le projet.

---

## 5. Référence au code Lean consulté

Pour la section portant sur l’axiomatisation de la fonction zêta et de la conjecture, du code Lean provenant du dépôt suivant a été consulté et adapté conformément à la licence Apache 2.0 :

Dépôt Lean (mathlib3) :  
https://github.com/leanprover-community/mathlib3.git

Ce dépôt contient la formalisation Lean de la fonction zêta, des L‑fonctions et d’éléments liés à l’hypothèse de Riemann.

---

## Certification de compilation

![Isabelle/HOL](https://img.shields.io/badge/Isabelle2025--2-Build%20Passing-brightgreen)
![LaTeX](https://img.shields.io/badge/LaTeX-PDF%20OK-brightgreen)

**État de certification :**  
Tous les fichiers Isabelle/HOL et LaTeX de ce dépôt ont été compilés avec succès  
le **3 mars 2026**, sous l’environnement suivant :

- **Isabelle2025‑2** (`isabelle build -D .`)
- **MiKTeX** (`pdflatex`)

Cette certification atteste uniquement que la version officielle du dépôt compile à cette date.

## 6. Licence

Ce projet est distribué sous licence Apache 2.0. Les utilisateurs peuvent consulter, utiliser, modifier et redistribuer le contenu selon les termes de la licence incluse dans le dépôt.