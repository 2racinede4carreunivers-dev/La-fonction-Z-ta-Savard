# guide_methode_de_philippot.md
# Guide méthodologique de la méthode de Philippôt

Ce document présente la méthodologie opérationnelle permettant d’appliquer la **méthode de Philippôt**, telle qu’encodée dans le fichier HOL `methode_de_philippot.thy`.

Le fichier HOL limite volontairement :
- les **suites** à des longueurs de **3 à 11 termes**,  
- et les **étapes** à **3 niveaux** (étape 1, étape 2, étape 3),

afin de rendre la lecture et la vérification plus accessibles.  
Mais la méthode elle-même est **générale**, et s’applique à :
- des suites de **3 termes jusqu’à l’infini**,  
- un nombre d’étapes **illimité**,  
- produisant une **infinité de rapports 1/2**.

Ce guide explique comment appliquer la méthode dans sa forme complète.

---

# 1. Règles fondamentales pour appliquer la méthode de Philippôt

Pour utiliser correctement la méthode, l’utilisateur doit respecter les règles suivantes :

1. **Les suites peuvent avoir de 3 termes jusqu’à l’infini.**  
   Le fichier HOL montre seulement les cas 3–11 pour illustrer la structure.

2. **Il peut y avoir une infinité d’étapes.**  
   Chaque étape applique une substitution à une position précise.

3. **Toutes les suites, à toutes les étapes, suivent la même structure générale :**  
   - tous les termes sauf les deux derniers sont obtenus par multiplication successive par **1/2**,  
   - l’avant‑dernier terme est obtenu par multiplication par **2/3**,  
   - le dernier terme est obtenu par multiplication par **1/2**.

4. **La substitution ne s’applique jamais à l’étape 1.**  
   Elle commence **à l’étape 2**.

5. **Il existe deux types de substitution :**
   - **Substitution A** : pour les suites de **3 à 7 termes**,  
   - **Substitution B** : pour les suites de **8 termes et plus**.

6. **La position de substitution dépend uniquement du nombre de termes :**
   - 3 termes → position 1  
   - 4 termes → position 2  
   - 5 termes → position 3  
   - 6 termes → position 4  
   - 7 termes → position 5  
   - 8 termes et plus → position **6** (fixe)

7. **À partir de l’étape 2, la valeur substituée est soustraite à 1**,  
   puis **s’additionne** à la valeur substituée précédente, créant une suite infinie de valeurs compensatoires.

8. **Le rapport entre deux valeurs substituées successives est toujours 1/2.**  
   C’est la mécanique centrale de la méthode :  
   > une machine produisant une infinité de 1/2.

---

# 2. Structure générale des suites (toutes longueurs)

Pour une suite de longueur \(n\), les règles sont :

- Pour les positions 1 à \(n-3\) :  
  \[
  x_{i+1} = x_i \cdot \frac{1}{2}
  \]

- Avant‑dernier terme :  
  \[
  x_{n-1} = x_{n-2} \cdot \frac{2}{3}
  \]

- Dernier terme :  
  \[
  x_n = x_{n-1} \cdot \frac{1}{2}
  \]

Exemple pour **5 termes** :  
\[
\frac12,\ \frac14,\ \frac18,\ \frac{1}{12},\ \frac{1}{24}
\]

- \(1/2 → 1/4 → 1/8\) (multiplication par 1/2)  
- \(1/8 × 2/3 = 1/12\) (avant‑dernier)  
- \(1/12 × 1/2 = 1/24\) (dernier)

---

# 3. Étape 1 : construction initiale des suites

L’étape 1 construit la suite réglementaire pour un nombre de termes donné.

Le fichier HOL fournit les cas explicites pour 3 à 11 termes, par exemple :

- 3 termes : `[1/2, 1/3, 1/6]`
- 5 termes : `[1/2, 1/4, 1/8, 1/12, 1/24]`
- 8 termes : `[1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/96, 1/192]`

La définition générale est :

\[
x_i = \frac{1}{2^i} \quad \text{pour } 1 \le i \le n-2
\]
\[
x_{n-1} = x_{n-2} \cdot \frac{2}{3}
\]
\[
x_n = x_{n-1} \cdot \frac{1}{2}
\]

Cette étape **ne contient aucune substitution**.

---

# 4. Étape 2 : première substitution

À partir de l’étape 2, une substitution est appliquée à une position précise.

## 4.1 Substitution A (3 à 7 termes)

Position de substitution :

| Nombre de termes | Position substituée |
|------------------|---------------------|
| 3                | 1                   |
| 4                | 2                   |
| 5                | 3                   |
| 6                | 4                   |
| 7                | 5                   |

La substitution modifie le terme à cette position, et la somme totale devient :

\[
\text{Somme} = 1 - \text{valeur substituée}
\]

## 4.2 Substitution B (8 termes et plus)

- La position substituée est **toujours la position 6**.
- La valeur substituée à l’étape 2 est **toujours** :
  \[
  \frac{1}{64}
  \]
- La somme devient :
  \[
  \text{Somme} = 1 - \frac{1}{64}
  \]

---

# 5. Étape 3 : seconde substitution

L’étape 3 répète le mécanisme de l’étape 2 :

- même position de substitution que l’étape 2,
- nouvelle valeur substituée,
- la somme devient :
  \[
  1 - (\text{valeur substituée étape 2} + \text{valeur substituée étape 3})
  \]

Pour les suites de 3 à 7 termes, les valeurs substituées sont explicites dans le fichier HOL.

Pour les suites de 8 termes et plus :

- position = 6,
- valeur substituée = \(1/64 + 1/128\).

---

# 6. Mécanique infinie des substitutions

À partir de l’étape 2, chaque nouvelle étape :

1. substitue une nouvelle valeur à la même position,
2. soustrait cette valeur à 1,
3. ajoute cette valeur à la somme des substitutions précédentes.

On obtient une suite infinie :

\[
s_1,\ s_2,\ s_3,\ \ldots
\]

où :

\[
\frac{s_{k+1}}{s_k} = \frac{1}{2}
\]

C’est la **machine à produire des 1/2**.

---

# 7. Structure spectrale générale (infinité de termes)

La méthode encode une structure fondamentale :

\[
x_i = \frac{1}{2^i}
\]

et :

\[
\frac{x_{i+1}}{x_i} = \frac{1}{2}
\]

Cette propriété :

- vaut pour toute longueur finie,
- se prolonge conceptuellement à l’infini,
- garantit que la méthode produit une infinité de rapports 1/2.

---

# 8. Algorithme complet de la méthode de Philippôt

Voici l’algorithme général, applicable à toute longueur et tout nombre d’étapes.

## 8.1 Entrée
- un nombre de termes \(n \ge 3\),
- un nombre d’étapes \(k \ge 1\).

## 8.2 Étape 1 : construction initiale
Construire la suite :

1. \(x_1 = 1/2\)
2. \(x_{i+1} = x_i / 2\) pour \(2 \le i \le n-3\)
3. \(x_{n-1} = x_{n-2} \cdot 2/3\)
4. \(x_n = x_{n-1} / 2\)

## 8.3 Détermination de la position de substitution
Si \(3 \le n \le 7\) :
\[
p = n - 2
\]
Si \(n \ge 8\) :
\[
p = 6
\]

## 8.4 Étape 2
- substituer la valeur \(s_1\) à la position \(p\),
- recalculer la somme :
  \[
  \text{Somme} = 1 - s_1
  \]

## 8.5 Étape 3
- substituer la valeur \(s_2\) à la même position,
- recalculer la somme :
  \[
  \text{Somme} = 1 - (s_1 + s_2)
  \]

## 8.6 Étapes suivantes (k ≥ 4)
Pour chaque étape \(j\) :

1. substituer \(s_j\) à la position \(p\),
2. mettre à jour :
   \[
   S_j = S_{j-1} + s_j
   \]
3. la somme devient :
   \[
   1 - S_j
   \]

## 8.7 Propriété fondamentale
Pour toute étape :

\[
\frac{s_{j+1}}{s_j} = \frac{1}{2}
\]

---

# 9. Conclusion

La méthode de Philippôt est une **mécanique spectrale** fondée sur :

- la structure des puissances de deux,
- une substitution répétée à une position fixe,
- une suite infinie de valeurs compensatoires,
- et une production automatique d’une infinité de rapports 1/2.

Le fichier HOL illustre cette mécanique sur 3 étapes et 3–11 termes,  
mais la méthode complète s’étend naturellement à l’infini.

---