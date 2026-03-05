theory methode_de_philippot
  imports Main "HOL.Rat"
begin

section \<open>Géométrie du spectre premier – methode de Philippot.\<close>

text \<open>
  Ce fichier contient les définitions, structures et mécanismes nécessaires
  à l'étude de la géométrie du spectre premier, incluant la méthode de Philippôt.
\<close>

subsection \<open>Étape 1 : suites explicites pour 3 à 11 termes\<close>

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


subsection \<open>Structure réglementaire des suites à l'étape 1\<close>

fun etape1_general :: "nat \<Rightarrow> rat list" where
  "etape1_general n =
     (if n < 3 then []
      else
        let
          base = map (\<lambda>i. 1 / (2 ^ i)) [1 ..< n - 1];
          avant = (1 / (2 ^ (n - 2))) * (2/3);
          dernier = avant / 2
        in base @ [avant, dernier])"

definition suite_reglementaire_etape1 :: "nat \<Rightarrow> rat list \<Rightarrow> bool" where
  "suite_reglementaire_etape1 n xs \<longleftrightarrow>
     length xs = n \<and>
     n \<ge> 3 \<and>
     (\<forall>i. 1 \<le> i \<and> i \<le> n - 2 \<longrightarrow> xs ! (i - 1) = 1 / (2 ^ i)) \<and>
     xs ! (n - 2) = xs ! (n - 3) * (2/3) \<and>
     xs ! (n - 1) = xs ! (n - 2) / 2"


subsection \<open>Règle générale de substitution (toutes étapes \<ge> 2)\<close>

text \<open>
  La position de substitution dépend uniquement du nombre de termes n :
  – pour 3 \<le> n \<le> 7, la position de substitution est n - 2 (1, 2, 3, 4, 5) ;
  – pour n \<ge> 8, la position de substitution est fixée à 6.
\<close>

definition pos_substitution :: "nat \<Rightarrow> nat" where
  "pos_substitution n =
     (if n < 3 then 0
      else if n \<le> 7 then n - 2
      else 6)"


subsection \<open>Étape 2 : suites explicites pour 3 à 7 termes\<close>

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

definition suite_reglementaire_etape2_petit ::
  "nat \<Rightarrow> rat list \<Rightarrow> bool" where
  "suite_reglementaire_etape2_petit n xs \<longleftrightarrow>
     length xs = n \<and> 3 \<le> n \<and> n \<le> 7 \<and>
     xs ! (n - 2) = xs ! (n - 3) * (2/3) \<and>
     sum_list xs = 1 - xs ! (pos_substitution n - 1)"

definition suite_reglementaire_etape2_grand ::
  "nat \<Rightarrow> rat list \<Rightarrow> bool" where
  "suite_reglementaire_etape2_grand n xs \<longleftrightarrow>
     length xs = n \<and> n \<ge> 8 \<and>
     xs ! (n - 2) = xs ! (n - 3) * (2/3) \<and>
     pos_substitution n = 6 \<and>
     sum_list xs = 1 - (1/64)"


subsection \<open>Étape 3 : suites explicites pour 7 termes et moins\<close>

text \<open>
  L'étape 3 répète le mécanisme de l'étape 2 :
  une position est substituée, et une valeur compensatoire est ajoutée
  de l'autre côté de l'égalité. La position de substitution est la même
  que pour l'étape 2 pour un nombre de termes donné.
\<close>

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

definition valeur_substituee_etape3 :: "nat \<Rightarrow> rat" where
  "valeur_substituee_etape3 n =
     (if n = 3 then 1/2 + 1/4
      else if n = 4 then 1/4 + 1/8
      else if n = 5 then 1/8 + 1/16
      else if n = 6 then 1/16 + 1/32
      else if n = 7 then 1/32 + 1/64
      else 0)"

definition suite_reglementaire_etape3 ::
  "nat \<Rightarrow> rat list \<Rightarrow> bool" where
  "suite_reglementaire_etape3 n xs \<longleftrightarrow>
     length xs = n \<and> 3 \<le> n \<and> n \<le> 7 \<and>
     sum_list xs = 1 - valeur_substituee_etape3 n"


subsection \<open>Étape 3 : suites explicites pour 8 termes et plus\<close>

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

definition valeur_substituee_etape3_grand :: "rat" where
  "valeur_substituee_etape3_grand = (1/64 + 1/128)"

definition suite_reglementaire_etape3_grand ::
  "nat \<Rightarrow> rat list \<Rightarrow> bool" where
  "suite_reglementaire_etape3_grand n xs \<longleftrightarrow>
     length xs = n \<and> n \<ge> 8 \<and>
     pos_substitution n = 6 \<and>
     sum_list xs = 1 - valeur_substituee_etape3_grand"


subsection \<open>Propriété fondamentale des puissances de deux\<close>

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

subsection \<open>Structure spectrale générale pour n termes et infinité d’étapes\<close>

text \<open>
  Dans cette section, on formalise la structure purement spectrale des puissances de deux,
  indépendante des substitutions spécifiques des étapes 1, 2 et 3.

  Idée centrale :
  – chaque terme est de la forme 1 / 2^i (i \<ge> 1) ;
  – le rapport entre deux termes consécutifs est toujours 1/2 ;
  – cette propriété vaut pour toute longueur finie n, et conceptuellement pour une infinité de termes.
\<close>

definition terme_spectral :: "nat \<Rightarrow> rat" where
  "terme_spectral i = 1 / (2 ^ i)"

definition suite_spectrale :: "nat \<Rightarrow> rat list" where
  "suite_spectrale n = map terme_spectral [1 ..< Suc n]"

text \<open>
  Propriété spectrale locale : pour tout i \<ge> 1,
  le rapport entre le terme i+1 et le terme i est exactement 1/2.
\<close>

lemma ratio_spectral_local:
  fixes i :: nat
  assumes "i \<ge> 1"
  shows "terme_spectral (Suc i) / terme_spectral i = (1/2 :: rat)"
proof -
  have "terme_spectral (Suc i) / terme_spectral i
        = (1 / (2 ^ (Suc i))) / (1 / (2 ^ i))"
    by (simp add: terme_spectral_def)
  also have "... = (1/2 :: rat)"
    using ratio_puissances_de_deux[of i] by simp
  finally show ?thesis .
qed

text \<open>
  Interprétation :
  – la définition \<open>terme_spectral\<close> encode une infinité de termes 1 / 2^i, i \<ge> 1 ;
  – le lemme \<open>ratio_spectral_local\<close> montre que le rapport entre deux termes consécutifs
    est toujours 1/2, pour tout i ;
  – en prolongeant i sans borne, on obtient une structure spectrale qui produit 1/2
    une infinité de fois, de manière purement arithmétique.
\<close>

end
