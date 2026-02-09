(*============================================================
   TABLE DES MATIÈRES — geometrie_spectre_premier_second_chapitre.thy
============================================================

0. Informations générales
1. Étape 1 — Suites explicites (3 à 11 termes)
2. Étape 1 — Structure réglementaire générale
3. Étape 2 — Suites explicites (3 à 7 termes)
4. Étape 2 — Structure réglementaire (petit et grand)
5. Étape 3 — Suites explicites (<= 7 termes)
6. Étape 3 — Suites explicites (>= 8 termes)
7. Étape 3 — Structure réglementaire (petit et grand)
8. Propriété fondamentale des puissances de deux
9. Exemples concrets de ratios = 1/2

============================================================
*)

theory geometrie_spectre_premier_second_chapitre
  imports Main "HOL.Rat"
begin

section "Geometrie du spectre premier – Second chapitre"

text "
  Ce fichier contient les definitions, structures et mecanismes necessaires
  a l'etude de la geometrie du spectre premier, incluant la methode de Philippot.
"

subsection "Etape 1 : suites explicites pour 3 a 11 termes"

definition etape1_3 :: "rat list" where
  "etape1_3 = [1/2, 1/3, 1/6]"

definition etape1_4 :: "rat list" where
  "etape1_4 = [1/2, 1/4, 1/6, 1/12]"

definition etape1_5 :: "rat list" where
  "etape1_5 = [1/2, 1/4, 1/8, 1/12, 1/24]"

definition etape1_6 :: "rat list" where
  "etape1_6 = [1/2, 1/4, 1/8, 1/16, 1/24, 1/48]"

definition etape1_7 :: "rat list" where
  "etape1_7 = [1/2, 1/4, 1/8, 1/16, 1/32, 1/48, 1/96]"

definition etape1_8 :: "rat list" where
  "etape1_8 = [1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/96, 1/192]"

definition etape1_9 :: "rat list" where
  "etape1_9 = [1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/128, 1/192, 1/384]"

definition etape1_10 :: "rat list" where
  "etape1_10 = [1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/128, 1/256, 1/384, 1/768]"

definition etape1_11 :: "rat list" where
  "etape1_11 = [1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/128, 1/256, 1/512, 1/768, 1/1536]"


subsection "Structure reglementaire des suites a l'etape 1"

fun etape1_general :: "nat => rat list" where
  "etape1_general n =
     (if n < 3 then []
      else
        let
          base = map (%i. 1 / (2 ^ i)) [1 ..< n - 1];
          avant = (1 / (2 ^ (n - 2))) * (2/3);
          dernier = avant / 2
        in base @ [avant, dernier])"

definition suite_reglementaire_etape1 :: "nat => rat list => bool" where
  "suite_reglementaire_etape1 n xs =
     (length xs = n &
      n >= 3 &
      (ALL i. 1 <= i & i <= n - 2 --> xs ! (i - 1) = 1 / (2 ^ i)) &
      xs ! (n - 2) = xs ! (n - 3) * (2/3) &
      xs ! (n - 1) = xs ! (n - 2) / 2)"


subsection "Etape 2 : suites explicites pour 3 a 7 termes"

definition etape2_3 :: "rat list" where
  "etape2_3 = [1/4, 1/6, 1/12]"

definition etape2_4 :: "rat list" where
  "etape2_4 = [1/2, 1/8, 1/12, 1/24]"

definition etape2_5 :: "rat list" where
  "etape2_5 = [1/2, 1/4, 1/16, 1/24, 1/48]"

definition etape2_6 :: "rat list" where
  "etape2_6 = [1/2, 1/4, 1/8, 1/32, 1/48, 1/96]"

definition etape2_7 :: "rat list" where
  "etape2_7 = [1/2, 1/4, 1/8, 1/16, 1/64, 1/96, 1/192]"

definition pos_substitution_petit :: "nat => nat" where
  "pos_substitution_petit n =
     (if n = 3 then 1
      else if n = 4 then 2
      else if n = 5 then 3
      else if n = 6 then 4
      else if n = 7 then 5
      else 0)"

definition suite_reglementaire_etape2_petit ::
  "nat => rat list => bool" where
  "suite_reglementaire_etape2_petit n xs =
     (length xs = n &
      3 <= n & n <= 7 &
      xs ! (n - 2) = xs ! (n - 3) * (2/3) &
      sum_list xs = 1 - xs ! (pos_substitution_petit n - 1))"

definition pos_substitution_grand :: "nat => nat" where
  "pos_substitution_grand n = (if n >= 8 then 6 else 0)"

definition suite_reglementaire_etape2_grand ::
  "nat => rat list => bool" where
  "suite_reglementaire_etape2_grand n xs =
     (length xs = n &
      n >= 8 &
      xs ! (n - 2) = xs ! (n - 3) * (2/3) &
      pos_substitution_grand n = 6 &
      sum_list xs = 1 - (1/64))"


subsection "Etape 3 : suites explicites pour 7 termes et moins"

definition etape3_3 :: "rat list" where
  "etape3_3 = [1/24, 1/12, 1/8]"

definition etape3_4 :: "rat list" where
  "etape3_4 = [1/48, 1/24, 1/16, 1/2]"

definition etape3_5 :: "rat list" where
  "etape3_5 = [1/96, 1/48, 1/32, 1/4, 1/2]"

definition etape3_6 :: "rat list" where
  "etape3_6 = [1/192, 1/96, 1/64, 1/8, 1/4, 1/2]"

definition etape3_7 :: "rat list" where
  "etape3_7 = [1/192, 1/96, 1/128, 1/16, 1/8, 1/4, 1/2]"

definition pos_substitution_etape3 :: "nat => nat" where
  "pos_substitution_etape3 n =
     (if n = 3 then 1
      else if n = 4 then 1
      else if n = 5 then 1
      else if n = 6 then 1
      else if n = 7 then 1
      else 0)"

definition valeur_substituee_etape3 :: "nat => rat" where
  "valeur_substituee_etape3 n =
     (if n = 3 then 1/2 + 1/4
      else if n = 4 then 1/4 + 1/8
      else if n = 5 then 1/8 + 1/16
      else if n = 6 then 1/16 + 1/32
      else if n = 7 then 1/32 + 1/64
      else 0)"

definition suite_reglementaire_etape3 ::
  "nat => rat list => bool" where
  "suite_reglementaire_etape3 n xs =
     (length xs = n &
      3 <= n & n <= 7 &
      sum_list xs = 1 - valeur_substituee_etape3 n)"


subsection "Etape 3 : suites explicites pour 8 termes et plus"

definition etape3_8 :: "rat list" where
  "etape3_8 =
     [1/384, 1/192, 1/128, 1/32, 1/16, 1/8, 1/4, 1/2]"

definition etape3_9 :: "rat list" where
  "etape3_9 =
     [1/768, 1/384, 1/256, 1/128, 1/32, 1/16, 1/8, 1/4, 1/2]"

definition etape3_10 :: "rat list" where
  "etape3_10 =
     [1/1536, 1/768, 1/512, 1/256, 1/128, 1/32, 1/16, 1/8, 1/4, 1/2]"

definition etape3_11 :: "rat list" where
  "etape3_11 =
     [1/3072, 1/1536, 1/1024, 1/512, 1/256, 1/128, 1/32, 1/16, 1/8, 1/4, 1/2]"

definition pos_substitution_etape3_grand :: "nat => nat" where
  "pos_substitution_etape3_grand n =
     (if n >= 8 then 6 else 0)"

definition valeur_substituee_etape3_grand :: "rat" where
  "valeur_substituee_etape3_grand = (1/64 + 1/128)"

definition suite_reglementaire_etape3_grand ::
  "nat => rat list => bool" where
  "suite_reglementaire_etape3_grand n xs =
     (length xs = n &
      n >= 8 &
      pos_substitution_etape3_grand n = 6 &
      sum_list xs = 1 - valeur_substituee_etape3_grand)"


subsection "Propriete fondamentale des puissances de deux"

lemma ratio_puissances_de_deux:
  fixes n :: nat
  shows "(1 / (2 ^ (Suc n)) :: rat) / (1 / (2 ^ n)) = 1 / 2"
  by (simp add: field_simps)

lemma exemples_ratio_puissances_de_deux:
  shows "(1/128 :: rat) / (1/64) = 1/2"
    and "(1/64 :: rat) / (1/32) = 1/2"
    and "(1/32 :: rat) / (1/16) = 1/2"
    and "(1/16 :: rat) / (1/8) = 1/2"
    and "(1/8 :: rat) / (1/4) = 1/2"
    and "(1/4 :: rat) / (1/2) = 1/2"
  by (simp_all add: ratio_puissances_de_deux)


(*
============================================================
   MENTIONS LÉGALES ET CRÉDITS
============================================================

Ce fichier Isabelle/HOL constitue une formalisation mathématique
de la méthode de Philippôt appliquée à la géométrie du spectre premier.

Encodé le : 8 février 2026
Lieu : Chaudière-Appalaches, Lévis, Québec, Canada
Auteur : Philippe Thomas Savard

Tous droits réservés.
============================================================
*)

end
