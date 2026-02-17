theory methode_de_philippot
  imports Main "HOL.Rat"
begin

section \<open>Géométrie du spectre premier – methode de Philippot.\<close>

text \<open>(**************************************************************)
(* SECTION : Suites négatives – équations spectrales          *)
(**************************************************************)

section "Suites negatives : equations spectrales"

definition SA_neg_eq :: "real => real" where
  "SA_neg_eq n = 3.25 * (2 powr n) - 2"

definition SB_neg_eq :: "real => real" where
  "SB_neg_eq n = 6.5 * (2 powr n) - 66"

definition digamma_neg_calc :: "real => real => real" where
  "digamma_neg_calc n p = SB_neg_eq n - 64 * p"

lemma digamma_neg_calc_equation_alt:
  "digamma_neg_calc n p = (SB_neg_eq n / 64 - p) * 64"
  unfolding digamma_neg_calc_def SB_neg_eq_def
  by (simp add: field_simps)


(**************************************************************)
(* SECTION : Rapport spectral 1/2 négatif (axiomatisation)    *)
(**************************************************************)

section "Rapport spectral 1/2 negatif"

definition RsP_neg :: "real => real => real" where
  "RsP_neg n1 n2 =
     (SA_neg_eq n1 - SA_neg_eq n2) /
     (SB_neg_eq n1 - SB_neg_eq n2)"

axiomatization where
  spectral_ratio_neg_un_demi:
    "\<lbrakk> n1 \<le> -1; n2 \<le> -1; n1 \<noteq> n2 \<rbrakk> \<Longrightarrow> RsP_neg n1 n2 = 1/2"

lemma RsP_neg_un_demi_general:
  assumes "n1 \<le> -1" "n2 \<le> -1" "n1 \<noteq> n2"
  shows "RsP_neg n1 n2 = 1/2"
  using spectral_ratio_neg_un_demi assms by blast


(**************************************************************)
(* SECTION : Géométrie Spectrale — Asymétrie Ordonnée/Chaotique *)
(**************************************************************)

section "Geometrie spectrale : asymetries"

definition indice_valide :: "int \<Rightarrow> bool" where
  "indice_valide n \<longleftrightarrow> (n \<ge> 1 \<or> n \<le> -1)"

definition liste_strictement_croissante :: "int list \<Rightarrow> bool" where
  "liste_strictement_croissante xs \<longleftrightarrow>
     (\<forall>i j. i < j \<and> j < length xs \<longrightarrow> xs ! i < xs ! j)"

definition asymetrique_ordonnee :: "int list \<Rightarrow> int list \<Rightarrow> bool" where
  "asymetrique_ordonnee A_indices B_indices \<longleftrightarrow>
     (\<forall>n \<in> set A_indices. indice_valide n) \<and>
     (\<forall>n \<in> set B_indices. indice_valide n) \<and>
     liste_strictement_croissante A_indices \<and>
     liste_strictement_croissante B_indices \<and>
     A_indices \<noteq> [] \<and>
     B_indices \<noteq> [] \<and>
     last A_indices < hd B_indices \<and>
     length B_indices = length A_indices + 1"

definition asymetrique_chaotique :: "int list \<Rightarrow> int list \<Rightarrow> bool" where
  "asymetrique_chaotique A_indices B_indices \<longleftrightarrow>
     (\<forall>n \<in> set A_indices. indice_valide n) \<and>
     (\<forall>n \<in> set B_indices. indice_valide n) \<and>
     length A_indices \<noteq> length B_indices \<and>
     \<not> asymetrique_ordonnee A_indices B_indices"

lemma asymetrie_implique_indices_valides :
  assumes "asymetrique_ordonnee A_indices B_indices \<or>
           asymetrique_chaotique A_indices B_indices"
  shows "(\<forall>n \<in> set A_indices. indice_valide n) \<and>
         (\<forall>n \<in> set B_indices. indice_valide n)"
proof -
  from assms
  show ?thesis
  proof
    assume h1: "asymetrique_ordonnee A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_ordonnee_def by auto
  next
    assume h2: "asymetrique_chaotique A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_chaotique_def by auto
  qed
qed


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

fun etape1_general :: "nat =>rat list" where
  "etape1_general n =
     (if n < 3 then []
      else
        let
          base = map (\<lambda>i. 1 / (2 ^ i)) [1 ..< n - 1];
          avant = (1 / (2 ^ (n - 2))) * (2/3);
          dernier = avant / 2
        in base @ [avant, dernier])"

definition suite_reglementaire_etape1 :: "nat =>rat list =>bool" where
  "suite_reglementaire_etape1 n xs \<longleftrightarrow>
     length xs = n \<and>
     n \<ge> 3 \<and>
     (\<forall>i. 1 \<le> i \<and> i \<le> n - 2 \<longrightarrow> xs ! (i - 1) = 1 / (2 ^ i)) \<and>
     xs ! (n - 2) = xs ! (n - 3) * (2/3) \<and>
     xs ! (n - 1) = xs ! (n - 2) / 2"


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

definition pos_substitution_petit :: "nat \<Rightarrow> nat" where
  "pos_substitution_petit n =
     (if n = 3 then 1
      else if n = 4 then 2
      else if n = 5 then 3
      else if n = 6 then 4
      else if n = 7 then 5
      else 0)"

definition suite_reglementaire_etape2_petit ::
  "nat=>rat list =>bool" where
  "suite_reglementaire_etape2_petit n xs \<longleftrightarrow>
     length xs = n \<and> 3 \<le> n \<and> n \<le> 7 \<and>
     xs ! (n - 2) = xs ! (n - 3) * (2/3) \<and>
     sum_list xs = 1 - xs ! (pos_substitution_petit n - 1)"

definition pos_substitution_grand :: "nat \<Rightarrow> nat" where
  "pos_substitution_grand n = (if n \<ge> 8 then 6 else 0)"

definition suite_reglementaire_etape2_grand ::
  "nat =>rat list =>bool" where
  "suite_reglementaire_etape2_grand n xs \<longleftrightarrow>
     length xs = n \<and> n \<ge> 8 \<and>
     xs ! (n - 2) = xs ! (n - 3) * (2/3) \<and>
     pos_substitution_grand n = 6 \<and>
     sum_list xs = 1 - (1/64)"


subsection \<open>Étape 3 : suites explicites pour 7 termes et moins\<close>

text \<open>
  L'étape 3 répète exactement le mécanisme de l'étape 2 :
  une position est substituée, et une valeur compensatoire est ajoutée
  de l'autre côté de l'égalité. À chaque étape supplémentaire, la position
  substituée est multipliée par 1/2, et la valeur substituée elle-même
  est également multipliée par 1/2 par rapport à l'étape précédente.
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

definition pos_substitution_etape3 :: "nat \<Rightarrow> nat" where
  "pos_substitution_etape3 n =
     (if n = 3 then 1
      else if n = 4 then 1
      else if n = 5 then 1
      else if n = 6 then 1
      else if n = 7 then 1
      else 0)"

definition valeur_substituee_etape3 :: "nat \<Rightarrow> rat" where
  "valeur_substituee_etape3 n =
     (if n = 3 then 1/2 + 1/4
      else if n = 4 then 1/4 + 1/8
      else if n = 5 then 1/8 + 1/16
      else if n = 6 then 1/16 + 1/32
      else if n = 7 then 1/32 + 1/64
      else 0)"

definition suite_reglementaire_etape3 ::
  "nat =>rat list =>bool" where
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

definition pos_substitution_etape3_grand :: "nat \<Rightarrow> nat" where
  "pos_substitution_etape3_grand n =
     (if n \<ge> 8 then 6 else 0)"

definition valeur_substituee_etape3_grand :: "rat" where
  "valeur_substituee_etape3_grand = (1/64 + 1/128)"

definition suite_reglementaire_etape3_grand ::
  "nat =>rat list =>bool" where
  "suite_reglementaire_etape3_grand n xs \<longleftrightarrow>
     length xs = n \<and> n \<ge> 8 \<and>
     pos_substitution_etape3_grand n = 6 \<and>
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

end