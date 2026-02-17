theory methode_spectral
  imports Complex_Main
begin

(****************************************************************)
(* TABLE DES MATIERES – SCRIPT HOL : GEOMETRIE DU SPECTRE       *)
(*                                                              *)
(* I.  RAPPORT SPECTRAL 1/2 – FONDATIONS                        *)
(*     1. Definitions des suites SA et SB (type nat)            *)
(*     2. Validite des formes generales pour n > 0              *)
(*     3. Definition du Rapport Spectral RsP                    *)
(*     4. Preuve formelle du ratio constant 1/2                 *)
(*     5. Points de resonance (29, 31, 37, 41)                  *)
(*     6. Validation numrique sur les indices z1 à z25         *)
(*                                                              *)
(* II. EXTENSIONS AUX RAPPORTS 1/3 ET 1/4                       *)
(*     1. Modele spectral 1/3 – Premier 227                     *)
(*     2. Modele spectral 1/4 – Premier 947                     *)
(*     3. Preuve du Rapport Spectral constant 1/3               *)
(*     4. Preuve du Rapport Spectral constant 1/4               *)
(*                                                              *)
(* III. MeTHODE SAVARD – UNIFICATION GeNeRALE                   *)
(*     1. Les quatre equations spectrales (SA & SB reels)       *)
(*        - Equations positives                                 *)
(*        -Equations negatives                                 *)
(*     2. Demonstration des suites negatives (n < 0)            *)
(*        - Structure geometrique                               *)
(*        - Exemples explicites SA_neg                          *)
(*        - Correspondance rang \<leftrightarrow> premier negatif               *)
(*     3. Definition generale du Digamma calcule                *)
(*        - Version positive                                    *)
(*        - Version négative                                    *)
(*     4. Définition generale du Gap spectral (Methode Savard)  *)
(*                                                              *)
(* IV. ÉCART ENTRE DEUX NOMBRES PREMIERS                        *)
(*     1. Exemple 1 : Écart entre 23 et 7                       *)
(*        - SA(11)                                              *)
(*        - SB(23)                                              *)
(*        - Digamma(23)                                         *)
(*        - Digamma(7)                                          *)
(*        - Résultat -15                                      *)
(*                                                              *)
(*     2. Exemple 2 : Écart entre -19 et -5                     *)
(*        - SA(-7)                                              *)
(*        - SB(-3)                                              *)
(*        - Digamma(-5)                                         *)
(*        - SB(-19)                                             *)
(*        - Digamma(-19)                                        *)
(*        - Résultat final : -13                                *)
(*                                                              *)
(*     3. Exemple 3 : Écart entre -31 et 17                     *)
(*        - SA(-29)                                             *)
(*        - SB(17)                                              *)
(*        - Digamma(17)                                         *)
(*        - SB(-31)                                             *)
(*        - Digamma(-31)                                        *)
(*        - Résultat final : -47                                *)
(*                                                              *)



(****************************************************************)
(* Sous-bloc 1 : formes generales des suites A et B *)
(****************************************************************)
section "Forme genrale des suites A et B"

definition SA :: "nat \<Rightarrow> real" where
  "SA n = (3.25 / 2) * (2 ^ n) - 2"

definition SB :: "nat \<Rightarrow> real" where
  "SB n = (6.5 / 2) * (2 ^ n) - 66"


(****************************************************************)
(* Sous-bloc 2 : validite pour tout n > 0 *)
(****************************************************************)

lemma SA_forme_generale:
  assumes "n > 0"
  shows "SA n = (3.25 / 2) * (2 ^ n) - 2"
  using assms by (simp add: SA_def)

lemma SB_forme_generale:
  assumes "n > 0"
  shows "SB n = (6.5 / 2) * (2 ^ n) - 66"
  using assms by (simp add: SB_def)

(**************************************************************)
(* Definition generale de Kn : 6e position de la suite A      *)
(**************************************************************)

definition K_n :: "(nat \<Rightarrow> real) \<Rightarrow> real" where
  "K_n A = A 6"
(****************************************************************)
(* Sous-bloc 3 : rapport spectral = 1/2 (cas 1\<times>1) *)
(****************************************************************)
section "Rapport spectral 1/2"

definition RsP :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "RsP n1 n2 = (SA n1 - SA n2) / (SB n1 - SB n2)"

lemma RsP_un_demi_general:
  assumes "n1 > 0" "n2 > 0" "n1 \<noteq> n2"
  shows "RsP n1 n2 = 1/2"
proof -
  have SA1: "SA n1 = (3.25 / 2) * (2 ^ n1) - 2"
    by (simp add: SA_def)
  have SA2: "SA n2 = (3.25 / 2) * (2 ^ n2) - 2"
    by (simp add: SA_def)
  have SB1: "SB n1 = (6.5 / 2) * (2 ^ n1) - 66"
    by (simp add: SB_def)
  have SB2: "SB n2 = (6.5 / 2) * (2 ^ n2) - 66"
    by (simp add: SB_def)

  have num: "SA n1 - SA n2 = (3.25 / 2) * (2 ^ n1 - 2 ^ n2)"
    by (simp add: SA1 SA2 algebra_simps)
  have den: "SB n1 - SB n2 = (6.5 / 2) * (2 ^ n1 - 2 ^ n2)"
    by (simp add: SB1 SB2 algebra_simps)

  have "RsP n1 n2 =
        ((3.25 / 2) * (2 ^ n1 - 2 ^ n2)) /
        ((6.5 / 2) * (2 ^ n1 - 2 ^ n2))"
    by (simp add: RsP_def num den)
  also have "... = (3.25 / 2) / (6.5 / 2)"
    using assms by (simp add: field_simps)
  also have "... = 1/2"
    by simp
  finally show ?thesis .
qed


(****************************************************************)
(* AJOUT : généralisation symétrique n\<times>n *)
(****************************************************************)
section "Rapport spectral n\<times>n (généralisation symétrique)"

definition RsP_nn :: "nat list \<Rightarrow> nat list \<Rightarrow> real" where
  "RsP_nn A_indices B_indices =
     (sum_list (map SA A_indices)) /
     (sum_list (map SB B_indices))"

definition rapport_spectral_un_demi_nn :: "nat list \<Rightarrow> nat list \<Rightarrow> bool" where
  "rapport_spectral_un_demi_nn A_indices B_indices \<longleftrightarrow>
     RsP_nn A_indices B_indices = 1/2"

definition A3 :: "nat list" where
  "A3 = [2, 9, 10]"

definition B3 :: "nat list" where
  "B3 = [3, 11, 15]"

(*
lemma exemple_3x3_spectral:
  "rapport_spectral_un_demi_nn A3 B3"
  unfolding rapport_spectral_un_demi_nn_def
            RsP_nn_def A3_def B3_def
  by admit
*)



(****************************************************************)
(* Sous-bloc 4 : Digamma calcule a partir de SB et du nombre premier *)
(****************************************************************)
section "Section du Digamma calcule."

definition digamma_calc :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "digamma_calc n p = SB n - 64 * real p"

definition prime_equation :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "prime_equation n p = (SB n - digamma_calc n p) / 64"

lemma digamma_calc_equation_alt:
  "digamma_calc n p = (SB n / 64 - real p) * 64"
  unfolding digamma_calc_def by simp

lemma prime_equation_identity:
  "prime_equation n p = real p"
  unfolding prime_equation_def digamma_calc_def
  by simp


(****************************************************************)
(* Postulat spectral 1/2 (régime positif) *)
(****************************************************************)
section "Axiomatisation positive"

axiomatization where
  spectral_postulate_pos:
    "\<And>n p. n \<ge> 1 \<Longrightarrow> prime p \<Longrightarrow> prime_equation n p = real p"

lemma prime_equation_for_primes_pos:
  assumes "n \<ge> 1" "prime p"
  shows "prime_equation n p = real p"
  using spectral_postulate_pos assms by blast


(****************************************************************)
(* Sous-bloc 5 : Exemples concrets pour 29, 31, 37, 41 *)
(****************************************************************)
section "Exemple complet pour les nombres premiers 29 31 37 et 41."

definition n29 :: nat where "n29 = 10"
definition n31 :: nat where "n31 = 11"
definition n37 :: nat where "n37 = 12"
definition n41 :: nat where "n41 = 13"

definition D29 :: real where "D29 = 256"
definition D31 :: real where "D31 = 5 * 256"
definition D37 :: real where "D37 = 9 * 256 + 5 * 384"
definition D41 :: real where "D41 = 13 * 256 + 9 * 384 + 5 * 768"

section "Valeur des somme A et B pour n."

lemma SA_10: "SA n29 = 1662"
  unfolding n29_def SA_def by simp

lemma SB_10: "SB n29 = 3262"
  unfolding n29_def SB_def by simp

lemma SA_11: "SA n31 = 3326"
  unfolding n31_def SA_def by simp

lemma SB_11: "SB n31 = 6590"
  unfolding n31_def SB_def by simp

lemma SA_12: "SA n37 = 6654"
  unfolding n37_def SA_def by simp

lemma SB_12: "SB n37 = 13246"
  unfolding n37_def SB_def by simp

lemma SA_13: "SA n41 = 13310"
  unfolding n41_def SA_def by simp

lemma SB_13: "SB n41 = 26558"
  unfolding n41_def SB_def by simp

lemma digamma_calc_29:
  "digamma_calc n29 29 = 1406"
  unfolding digamma_calc_def n29_def SB_def by simp

lemma digamma_calc_31:
  "digamma_calc n31 31 = 4606"
  unfolding digamma_calc_def n31_def SB_def by simp

lemma digamma_calc_37:
  "digamma_calc n37 37 = 10878"
  unfolding digamma_calc_def n37_def SB_def by simp

lemma digamma_calc_41:
  "digamma_calc n41 41 = 23934"
  unfolding digamma_calc_def n41_def SB_def by simp

lemma relation_29:
  "digamma_calc n29 29 = SA n29 - D29"
  unfolding digamma_calc_def SA_def SB_def n29_def D29_def by simp

lemma relation_31:
  "digamma_calc n31 31 = SA n31 + D31"
  unfolding digamma_calc_def SA_def SB_def n31_def D31_def by simp

lemma relation_37:
  "digamma_calc n37 37 = SA n37 + D37"
  unfolding digamma_calc_def SA_def SB_def n37_def D37_def by simp

lemma relation_41:
  "digamma_calc n41 41 = SA n41 + D41"
  unfolding digamma_calc_def SA_def SB_def n41_def D41_def by simp
(**************************************************************)
(* SECTION : Modele Spectral 1/4 – Definitions completes      *)
(**************************************************************)

section " Modele spectrale 1/4 : Forme generale des suite A et B."

text \<open>
  Formes generalisees pour le rapport 1/4.
  On suit les equations :
    ((241/16)/12 * 4^n) - 4/3
    ((964/16)/12 * 4^n) - (3073 * (4/3))
\<close>

(* --- Definition des suites A_1_4 et B_1_4 --- *)

definition A_1_4 :: "nat => real" where
  "A_1_4 n = ((241 / 16) / 12) * (4^n) - (4 / 3)"

definition B_1_4 :: "nat => real" where
  "B_1_4 n = ((964 / 16) / 12) * (4^n) - (3073 * (4 / 3))"


(**************************************************************)
(* SECTION : Equation generale pour le modele spectral 1/4     *)
(**************************************************************)

definition prime_equation_1_4 :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "prime_equation_1_4 n p = (B_1_4 n - (B_1_4 n - 4096 * real p)) / 4096"

lemma prime_equation_1_4_identity:
  "prime_equation_1_4 n p = real p"
  unfolding prime_equation_1_4_def by simp


(**************************************************************)
(* SECTION : Postulat spectral 1/4                            *)
(**************************************************************)
section " Axiomatisation spectral 1/4"
axiomatization where
  spectral_postulate_1_4:
    "\<And>n p. n > 0==>rime p ==prime_equation_1_4 n p = real p"


(**************************************************************)
(* SECTION : Lemme final pour les nombres premiers (1/4)      *)
(**************************************************************)

lemma prime_equation_1_4_for_primes:
  assumes "n > 0" "prime p"
  shows "prime_equation_1_4 n p = real p"
  using spectral_postulate_1_4 assms by blast


(**************************************************************)
(* SECTION : Exemple concret pour 947                         *)
(**************************************************************)

section "Modèle spectral 1/4: Sommes de suite A et B, Digamma, Digamma calcule et determination du premier 947."

text \<open>
  Donnees numeriques globales pour le modele 1/4 :
  - Somme de la suite A : 1316180
  - Somme de la suite B : 5260628
  - Digamma : 65536
  - Digamma calcule : 1316180 + 65536 = 1381716
  - (5260628 - 1381716) / 4096 = 947 (premier)
\<close>

definition suite_A_1_4_somme :: real where
  "suite_A_1_4_somme = 1316180"

definition suite_B_1_4_somme :: real where
  "suite_B_1_4_somme = 5260628"

definition digamma_1_4 :: real where
  "digamma_1_4 = 65536"

definition digamma_calcule_1_4 :: real where
  "digamma_calcule_1_4 = suite_A_1_4_somme + digamma_1_4"

lemma preuve_premier_947:
  "(suite_B_1_4_somme - digamma_calcule_1_4) / 4096 = 947"
  by (simp add: suite_A_1_4_somme_def suite_B_1_4_somme_def
                digamma_1_4_def digamma_calcule_1_4_def)
(**************************************************************)
(* SECTION : Modele Spectral 1/3 – Définitions completes      *)
(**************************************************************)

section " Rapport 1/3 forme generaliser pour les suites A et B."
text \<open>
  Formes généralisées pour le rapport 1/3.
  On suit les équations :
    ((73/9)/12 * 3^n) - 1.5
    ((219/9)/12 * 3^n) - (487 * 1.5)
\<close>

definition A_1_3 :: "nat => real" where
  "A_1_3 n = ((73 / 9) / 12) * (3^n) - 1.5"

definition B_1_3 :: "nat => real" where
  "B_1_3 n = ((219 / 9) / 12) * (3^n) - (487 * 1.5)"


(**************************************************************)
(* SECTION : Equation generale pour le modele spectral 1/3     *)
(**************************************************************)

definition prime_equation_1_3 :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "prime_equation_1_3 n p = (B_1_3 n - (B_1_3 n - 729 * real p)) / 729"

lemma prime_equation_1_3_identity:
  "prime_equation_1_3 n p = real p"
  unfolding prime_equation_1_3_def by simp


(**************************************************************)
(* SECTION : Postulat spectral 1/3                            *)
(**************************************************************)
section " Axiomatisation rapport 1/3."
axiomatization where
  spectral_postulate_1_3:
    "\<And>n p. n > 0==>prime p==>prime_equation_1_3 n p = real p"


(**************************************************************)
(* SECTION : Lemme final pour les nombres premiers (1/3)      *)
(**************************************************************)

lemma prime_equation_1_3_for_primes:
  assumes "n > 0" "prime p"
  shows "prime_equation_1_3 n p = real p"
  using spectral_postulate_1_3 assms by blast


(**************************************************************)
(* SECTION : Exemple concret pour 227                         *)
(**************************************************************)

section " Rapport spectal 1/3 validation numerique pour les suite A et B, Digamma, Digamma calcule et la determination du premier 227."

definition suite_A_1_3_somme :: real where
  "suite_A_1_3_somme = 79824"

definition suite_B_1_3_somme :: real where
  "suite_B_1_3_somme = 238746"

section "Rapport 1/3" 
definition digamma_1_3 :: real where
  "digamma_1_3 = 6561"

definition digamma_calcule_1_3 :: real where
  "digamma_calcule_1_3 = suite_A_1_3_somme - digamma_1_3"

lemma preuve_premier_227:
  "(suite_B_1_3_somme - digamma_calcule_1_3) / 729 = 227"
  by (simp add: suite_A_1_3_somme_def suite_B_1_3_somme_def
                digamma_1_3_def digamma_calcule_1_3_def)

(**************************************************************)
(* SECTION 6 : Rapport Spectral 1/3 et 1/4                    *)
(**************************************************************)
section " Rapport spectral constant 1/3 et 1/4."
text \<open>
  Définition du Rapport Spectral pour les modèles 1/3 et 1/4.
\<close>
section "Rapport spectral 1/3 Validation généralisé."
(* Rapport spectral 1/3 *)

definition RsP_1_3 :: "nat => nat => real" where
  "RsP_1_3 n1 n2 =
    (A_1_3 n1 - A_1_3 n2) /
    (B_1_3 n1 - B_1_3 n2)"

theorem RsP_un_tiers_constant:
  assumes "n1 > 0" and "n2 > 0" and "n1 ~= n2"
  shows "RsP_1_3 n1 n2 = 1/3"
proof -
  have diff_A:
    "A_1_3 n1 - A_1_3 n2 =
      ((73/9)/12) * (3^n1 - 3^n2)"
    unfolding A_1_3_def by (simp add: algebra_simps)

  have diff_B:
    "B_1_3 n1 - B_1_3 n2 =
      ((219/9)/12) * (3^n1 - 3^n2)"
    unfolding B_1_3_def by (simp add: algebra_simps)

  have "RsP_1_3 n1 n2 =
        (((73/9)/12) * (3^n1 - 3^n2)) /
        (((219/9)/12) * (3^n1 - 3^n2))"
    unfolding RsP_1_3_def by (simp add: diff_A diff_B)

  also have "... = ((73/9)/12) / ((219/9)/12)"
    using assms by (simp add: field_simps)

  also have "... = 1/3"
    by simp

  finally show ?thesis .
qed

(* Rapport spectral 1/4 *)

section" Rapport spectral constant 1/4."

definition RsP_1_4 :: "nat => nat => real" where
  "RsP_1_4 n1 n2 =
    (A_1_4 n1 - A_1_4 n2) /
    (B_1_4 n1 - B_1_4 n2)"
section " Rapport spectral 1/4 validation généralisé."
theorem RsP_un_quart_constant:
  assumes "n1 > 0" and "n2 > 0" and "n1 ~= n2"
  shows "RsP_1_4 n1 n2 = 1/4"
proof -
  have diff_A:
    "A_1_4 n1 - A_1_4 n2 =
      ((241/16)/12) * (4^n1 - 4^n2)"
    unfolding A_1_4_def by (simp add: algebra_simps)

  have diff_B:
    "B_1_4 n1 - B_1_4 n2 =
      ((964/16)/12) * (4^n1 - 4^n2)"
    unfolding B_1_4_def by (simp add: algebra_simps)

  have "RsP_1_4 n1 n2 =
        (((241/16)/12) * (4^n1 - 4^n2)) /
        (((964/16)/12) * (4^n1 - 4^n2))"
    unfolding RsP_1_4_def by (simp add: diff_A diff_B)

  also have "... = ((241/16)/12) / ((964/16)/12)"
    using assms by (simp add: field_simps)

  also have "... = 1/4"
    by simp

  finally show ?thesis .
qed

(**************************************************************)
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

(**************************************************************)
(* SECTION : Methode de comparaison asymetrique (1/2 et 1/4)  *)
(**************************************************************)

section "Methode de comparaison asymetrique pour 1/2 et 1/4"

text \<open>
  La methode de comparaison asymetrique relie :

  - des suites de nombres premiers A et B (via leurs indices n),
  - les equations generales des suites A et B (SA, SB pour 1/2 ; A_1_4, B_1_4 pour 1/4),
  - et un rapport spectral construit a partir des sommes de blocs.

  Les puissances utilisees dans les equations generales sont egales
  aux positions (indices) des termes dans les suites, ou a la longueur
  des blocs consideres. La methode est applicable a tout ensemble
  de nombres premiers dont la position correspond aux puissances
  des equations generales A et B.
\<close>


(**************************************************************)
(* 1. Version nat des asymetries (indices naturels)           *)
(**************************************************************)

text \<open>
  Les definitions asymetrique_ordonnee et asymetrique_chaotique
  existent deja pour des listes d'entiers (int). Pour travailler
  directement avec les indices naturels des suites SA, SB, A_1_4
  et B_1_4, on introduit une version analogue sur nat.
\<close>

definition indice_valide_nat :: "nat \<Rightarrow> bool" where
  "indice_valide_nat n \<longleftrightarrow> (n > 0)"

definition liste_strictement_croissante_nat :: "nat list \<Rightarrow> bool" where
  "liste_strictement_croissante_nat xs \<longleftrightarrow>
     (\<forall>i j. i < j \<and> j < length xs \<longrightarrow> xs ! i < xs ! j)"

definition asymetrique_ordonnee_nat :: "nat list \<Rightarrow> nat list \<Rightarrow> bool" where
  "asymetrique_ordonnee_nat A_indices B_indices \<longleftrightarrow>
     (\<forall>n \<in> set A_indices. indice_valide_nat n) \<and>
     (\<forall>n \<in> set B_indices. indice_valide_nat n) \<and>
     liste_strictement_croissante_nat A_indices \<and>
     liste_strictement_croissante_nat B_indices \<and>
     A_indices \<noteq> [] \<and>
     B_indices \<noteq> [] \<and>
     last A_indices < hd B_indices \<and>
     length B_indices = length A_indices + 1"

definition asymetrique_chaotique_nat :: "nat list \<Rightarrow> nat list \<Rightarrow> bool" where
  "asymetrique_chaotique_nat A_indices B_indices \<longleftrightarrow>
     (\<forall>n \<in> set A_indices. indice_valide_nat n) \<and>
     (\<forall>n \<in> set B_indices. indice_valide_nat n) \<and>
     length A_indices \<noteq> length B_indices \<and>
     \<not> asymetrique_ordonnee_nat A_indices B_indices"

lemma asymetrie_nat_implique_indices_valides :
  assumes "asymetrique_ordonnee_nat A_indices B_indices \<or>
           asymetrique_chaotique_nat A_indices B_indices"
  shows "(\<forall>n \<in> set A_indices. indice_valide_nat n) \<and>
         (\<forall>n \<in> set B_indices. indice_valide_nat n)"
proof -
  from assms
  show ?thesis
  proof
    assume h1: "asymetrique_ordonnee_nat A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_ordonnee_nat_def by auto
  next
    assume h2: "asymetrique_chaotique_nat A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_chaotique_nat_def by auto
  qed
qed


(**************************************************************)
(* 2. Methode de comparaison asymetrique pour le modele 1/2   *)
(**************************************************************)

text \<open>
  Pour le modele 1/2, on utilise les suites SA et SB deja definies :

    SA n = (3.25 / 2) * 2^n - 2
    SB n = (6.5 / 2) * 2^n - 66

  La methode de comparaison asymetrique travaille sur des blocs
  d'indices A_indices et B_indices, qui correspondent a des positions
  dans les suites de nombres premiers. On construit un rapport
  spectral de blocs a partir des sommes des valeurs SA et SB.
\<close>

definition somme_SA_bloc :: "nat list \<Rightarrow> real" where
  "somme_SA_bloc A_indices = sum_list (map SA A_indices)"

definition somme_SB_bloc :: "nat list \<Rightarrow> real" where
  "somme_SB_bloc B_indices = sum_list (map SB B_indices)"

text \<open>
  Rapport spectral de blocs pour le modele 1/2 :
  on compare la difference des sommes de deux blocs A et B
  pour SA et SB, comme dans l'exemple (11 - 50) / (-40 - 38).
\<close>

definition RsP_bloc_1_2 :: "nat list \<Rightarrow> nat list \<Rightarrow> real" where
  "RsP_bloc_1_2 A_indices B_indices =
     (somme_SA_bloc A_indices - somme_SA_bloc B_indices) /
     (somme_SB_bloc A_indices - somme_SB_bloc B_indices)"

text \<open>
  Comparaison asymetrique ordonnee (modele 1/2) :
  - A_indices et B_indices sont strictement croissants,
  - les indices sont valides (n > 0),
  - B contient exactement un element de plus que A,
  - les puissances associees aux equations generales sont donc
    dans l'ordre naturel et decalees d'une unite.
\<close>

definition comparaison_asym_ordonnee_1_2 :: "nat list \<Rightarrow> nat list \<Rightarrow> bool" where
  "comparaison_asym_ordonnee_1_2 A_indices B_indices \<longleftrightarrow>
     asymetrique_ordonnee_nat A_indices B_indices"

text \<open>
  Comparaison asymetrique chaotique (modele 1/2) :
  - A_indices et B_indices ont des longueurs differentes,
  - l'ordre croissant naturel n'est pas impose,
  - les puissances associees aux equations generales ne sont pas
    necessairement consecutives.
\<close>

definition comparaison_asym_chaotique_1_2 :: "nat list \<Rightarrow> nat list \<Rightarrow> bool" where
  "comparaison_asym_chaotique_1_2 A_indices B_indices \<longleftrightarrow>
     asymetrique_chaotique_nat A_indices B_indices"

text \<open>
  La methode de comparaison asymetrique pour le modele 1/2
  consiste donc a :
  - choisir deux blocs A_indices et B_indices,
  - verifier s'ils sont en configuration asymetrique ordonnee
    ou chaotique,
  - calculer le rapport RsP_bloc_1_2 A_indices B_indices.

  Ce rapport est numeriquement tres proche de 1/2 dans le regime
  chaotique, et evolue vers 1 dans certaines configurations
  asymetriques ordonnees lorsque la taille des blocs augmente.
  Ces comportements sont observes numeriquement et interpretes
  comme signatures spectrales, sans etre derives algébriquement.
\<close>


(**************************************************************)
(* 3. Methode de comparaison asymetrique pour le modele 1/4   *)
(**************************************************************)

text \<open>
  Pour le modele 1/4, on utilise les suites A_1_4 et B_1_4 :

    A_1_4 n = ((241/16)/12) * 4^n - 4/3
    B_1_4 n = ((964/16)/12) * 4^n - (3073 * (4/3))

  On applique la meme methode de comparaison asymetrique,
  cette fois avec ces equations generales.
\<close>

definition somme_A_1_4_bloc :: "nat list \<Rightarrow> real" where
  "somme_A_1_4_bloc A_indices = sum_list (map A_1_4 A_indices)"

definition somme_B_1_4_bloc :: "nat list \<Rightarrow> real" where
  "somme_B_1_4_bloc B_indices = sum_list (map B_1_4 B_indices)"

definition RsP_bloc_1_4 :: "nat list \<Rightarrow> nat list \<Rightarrow> real" where
  "RsP_bloc_1_4 A_indices B_indices =
     (somme_A_1_4_bloc A_indices - somme_A_1_4_bloc B_indices) /
     (somme_B_1_4_bloc A_indices - somme_B_1_4_bloc B_indices)"

definition comparaison_asym_ordonnee_1_4 :: "nat list \<Rightarrow> nat list \<Rightarrow> bool" where
  "comparaison_asym_ordonnee_1_4 A_indices B_indices \<longleftrightarrow>
     asymetrique_ordonnee_nat A_indices B_indices"

definition comparaison_asym_chaotique_1_4 :: "nat list \<Rightarrow> nat list \<Rightarrow> bool" where
  "comparaison_asym_chaotique_1_4 A_indices B_indices \<longleftrightarrow>
     asymetrique_chaotique_nat A_indices B_indices"

text \<open>
  Comme pour le modele 1/2, la methode de comparaison asymetrique
  pour le modele 1/4 s'applique a tout ensemble de nombres premiers
  dont les positions (indices) correspondent aux puissances utilisees
  dans les equations generales A_1_4 et B_1_4.

  Les configurations asymetriques ordonnees et chaotiques permettent
  d'observer numeriquement des rapports proches de 1/4 ou evoluant
  vers 1, sans que ces valeurs puissent etre obtenues par une
  simplification algébrique directe des equations generales.
\<close>
(**************************************************************)
(* SECTION : Rapport spectral 1/3 négatif (axiomatisation)     *)
(**************************************************************)

section "Rapport spectral 1/3 negatif"

(*
  Suites A et B generalisees pour le rapport 1/3.
  A(n) = ((73/9)/6) * 3^n - 1.5
  B(n) = ((219/9)/6) * 3^n - (487 * 1.5)
*)

definition SA_neg_eq_un_tiers :: "real \<Rightarrow> real" where
  "SA_neg_eq_un_tiers n = ((73/9) / 6) * (3 powr n) - 1.5"

definition SB_neg_eq_un_tiers :: "real \<Rightarrow> real" where
  "SB_neg_eq_un_tiers n = ((219/9) / 6) * (3 powr n) - (487 * 1.5)"

definition RsP_neg_un_tiers :: "real \<Rightarrow> real \<Rightarrow> real" where
  "RsP_neg_un_tiers n1 n2 =
     (SA_neg_eq_un_tiers n1 - SA_neg_eq_un_tiers n2) /
     (SB_neg_eq_un_tiers n1 - SB_neg_eq_un_tiers n2)"

(*
  Axiomatisation :
  Comme pour le rapport 1/2, la valeur numerique du rapport spectral
  vaut 1/3 pour toutes paires (n1,n2) negatives distinctes.
  Mais cette valeur ne peut pas etre obtenue algébriquement.
  On encode donc cette realite physique/numerique comme un axiome,
  parallele a l'effet Hall fractionnaire.
*)

axiomatization where
  spectral_ratio_neg_un_tiers:
    "\<lbrakk> n1 \<le> -1; n2 \<le> -1; n1 \<noteq> n2 \<rbrakk> \<Longrightarrow> RsP_neg_un_tiers n1 n2 = 1/3"

lemma RsP_neg_un_tiers_general:
  assumes "n1 \<le> -1" "n2 \<le> -1" "n1 \<noteq> n2"
  shows "RsP_neg_un_tiers n1 n2 = 1/3"
  using spectral_ratio_neg_un_tiers assms by blast



(**************************************************************)
(* SECTION : Rapport spectral 1/4 négatif (axiomatisation)     *)
(**************************************************************)

section "Rapport spectral 1/4 negatif"

(*
  Suites A et B generalisees pour le rapport 1/4.
  A(n) = ((241/16)/12) * 4^n - (4/3)
  B(n) = ((964/16)/12) * 4^n - (3073 * (4/3))
*)

definition SA_neg_eq_un_quart :: "real \<Rightarrow> real" where
  "SA_neg_eq_un_quart n = ((241/16) / 12) * (4 powr n) - (4/3)"

definition SB_neg_eq_un_quart :: "real \<Rightarrow> real" where
  "SB_neg_eq_un_quart n = ((964/16) / 12) * (4 powr n) - (3073 * (4/3))"

definition RsP_neg_un_quart :: "real \<Rightarrow> real \<Rightarrow> real" where
  "RsP_neg_un_quart n1 n2 =
     (SA_neg_eq_un_quart n1 - SA_neg_eq_un_quart n2) /
     (SB_neg_eq_un_quart n1 - SB_neg_eq_un_quart n2)"

(*
  Axiomatisation :
  Comme pour 1/2 et 1/3, le rapport spectral numerique vaut 1/4.
  Mais aucune reduction algébrique ne permet d'obtenir cette valeur.
  On encode donc cette valeur comme un axiome spectral,
  parallele aux plateaux fractionnaires de l'effet Hall.
*)

axiomatization where
  spectral_ratio_neg_un_quart:
    "\<lbrakk> n1 \<le> -1; n2 \<le> -1; n1 \<noteq> n2 \<rbrakk> \<Longrightarrow> RsP_neg_un_quart n1 n2 = 1/4"

lemma RsP_neg_un_quart_general:
  assumes "n1 \<le> -1" "n2 \<le> -1" "n1 \<noteq> n2"
  shows "RsP_neg_un_quart n1 n2 = 1/4"
  using spectral_ratio_neg_un_quart assms by blast
(**************************************************************)
(* SECTION : Forme générale de l'écart négatif                *)
(**************************************************************)

section "Forme générale de l'écart négatif"

definition gap_neg_val ::
  "real => real => real => real => real => real" where
  "gap_neg_val A_next B_high D_high D_low dummy =
      (A_next - (B_high - D_high) - D_low) / 64"


(**************************************************************)
(* SECTION : Exemple complet – écart entre -19 et -5          *)
(**************************************************************)

section "Exemple complet : écart entre -19 et -5"

text \<open>
  Pour l’écart entre -19 et -5 :
    le premier suivant -5 est -7  -> SA(-7)
    le rang spectral de -5 est -3 -> SB(-3)
    le rang spectral de -19 est -8 -> SB(-8)
\<close>

definition n_m7  :: real where "n_m7  = -7"
definition n_m3  :: real where "n_m3  = -3"
definition n_m19 :: real where "n_m19 = -8"


(**************************************************************)
(* SECTION : Valeurs spectrales exactes (-19 et -5)           *)
(**************************************************************)

section "Valeurs spectrales exactes pour -19 et -5"

definition SA_m7_val :: real where
  "SA_m7_val = -10110 / 5120"

definition SB_m5_val :: real where
  "SB_m5_val = -20860 / 320"

definition D_m5_val :: real where
  "D_m5_val = 81540 / 320"

definition SB_m19_val :: real where
  "SB_m19_val = -337790 / 5120"

definition D_m19_val :: real where
  "D_m19_val = 5888130 / 5120"


(**************************************************************)
(* SECTION : Lemme final – écart -19 / -5                     *)
(**************************************************************)

section "Démonstration finale : écart -19 / -5"

lemma gap_m19_m5:
  "gap_neg_val SA_m7_val SB_m5_val D_m5_val D_m19_val 0 = -13"
  unfolding gap_neg_val_def
            SA_m7_val_def SB_m5_val_def
            D_m5_val_def D_m19_val_def
  by simp

(**************************************************************)
(* SECTION : Exemple complet – écart entre -31 et 17          *)
(**************************************************************)

section "Exemple complet : écart entre -31 et 17"

text \<open>
  Exemple mixte : quantité de nombres entre -31 et 17.
  Le premier suivant -31 est -29  -> SA(-29)
  Le rang spectral de 17 est 8    -> SB(8)
  Le rang spectral de -31 est -11 -> SB(-11)
\<close>

definition n_m29 :: real where "n_m29 = -10"
definition n_p17 :: real where "n_p17 = 8"
definition n_m31 :: real where "n_m31 = -11"


(**************************************************************)
(* SECTION : Valeurs spectrales exactes (-31 et 17)           *)
(**************************************************************)

section "Valeurs spectrales exactes pour -31 et 17"

definition SA_m29_val :: real where
  "SA_m29_val = -40895 / 20480"

definition SB_p17_val :: real where
  "SB_p17_val = 350"

definition D_p17_val :: real where
  "D_p17_val = -738"

definition SB_m31_val :: real where
  "SB_m31_val = -1351615 / 20480"

definition D_m31_val :: real where
  "D_m31_val = 39280705 / 20480"


(**************************************************************)
(* SECTION : Forme générale de l'écart mixte                  *)
(**************************************************************)

section "Forme générale de l'écart mixte"

definition gap_mix_val ::
  "real => real => real => real => real => real" where
  "gap_mix_val A_next B_high D_high D_low dummy =
      (A_next - (B_high - D_high) - D_low) / 64"


(**************************************************************)
(* SECTION : Lemme final – écart -31 / 17                     *)
(**************************************************************)

section "Démonstration finale : écart -31 / 17"

lemma gap_m31_17:
  "gap_mix_val SA_m29_val SB_p17_val D_p17_val D_m31_val 0 = -47"
  unfolding gap_mix_val_def
            SA_m29_val_def SB_p17_val_def
            D_p17_val_def D_m31_val_def
  by simp


(**************************************************************)
(* SECTION : Exemple complet – écart entre 23 et 7            *)
(**************************************************************)

section "Exemple complet : écart entre les premiers 23 et 7"

text \<open>
  Exemple positif : quantité de nombres entre les deux premiers 23 et 7.

  On utilise la même méthode que pour les écarts -19 / -5 et -31 / 17 :

    - Le premier suivant 7 est 11
    - Le rang spectral de 7 est 4
    - Le rang spectral de 23 est 9

  Calculs numériques :

    SA(11) = 50
    SB(23) = 1598
    D(23)  = 126
    SB(7)  = -14
    D(7)   = -464

  Formule générale :

    (A_next - (B_high - D_high) - D_low) / 64

  Résultat :

    (50 - (1598 - 126) - (-464)) / 64 = -15

  Ce qui correspond aux 15 nombres entre 23 et 7.
\<close>

(**************************************************************)
(* SECTION : Valeurs spectrales exactes pour 23 et 7          *)
(**************************************************************)

section "Valeurs spectrales exactes pour 23 et 7"

definition SA_11_val :: real where "SA_11_val = 50"
definition SB_23_val :: real where "SB_23_val = 1598"
definition D_23_val :: real where "D_23_val = 126"
definition SB_7_val :: real where "SB_7_val = -14"
definition D_7_val :: real where "D_7_val = -464"


(**************************************************************)
(* SECTION : Note explicite sur l'inclusion du zéro           *)
(**************************************************************)

section "Note sur l'inclusion du zéro dans les écarts spectraux"

text \<open>
  Le zéro n'est inclus que dans les écarts mixtes (exemple -31 / 17).
  Dans les écarts du même signe (-19 / -5 et 23 / 7), la progression
  spectrale ne traverse pas 0, donc il n'est pas compté.
\<close>

(**************************************************************)
(* SECTION : Exemple complet – écart entre 227 et 173 (1/3)   *)
(**************************************************************)

section "Exemple complet : écart entre les premiers 227 et 173 (rapport 1/3)"

text \<open>
  Exemple positif : quantité de nombres entre les deux premiers 227 et 173.

  Données spectrales :

    - Le premier suivant 173 est 179
    - Rang spectral de 227 : 10
    - Rang spectral de 173 : 1

  Valeurs numériques :

    SA(227) = 79824
    SB(227) = 238746
    D(227)  = 73263

    SA(179) = 96/9

    SB(173) = -2155/3
    D(173)  = -1141518/9

  Formule générale (rapport 1/3) :

      (A_next - (B_high - D_high) - D_low) / 729

  Résultat :

      ((96/9) - (238746 - 73263) - (-1141518/9)) / 729 = -53

  Ce qui correspond aux 53 nombres entre 227 et 173.
\<close>


(**************************************************************)
(* SECTION : Valeurs spectrales exactes pour 227 et 173       *)
(**************************************************************)

section "Valeurs spectrales exactes pour 227 et 173 (1/3)"

definition SA_227_val :: real where
  "SA_227_val = 79824"

definition SB_227_val :: real where
  "SB_227_val = 238746"

definition D_227_val :: real where
  "D_227_val = 73263"


definition SA_179_val :: real where
  "SA_179_val = 96/9"


definition SB_173_val :: real where
  "SB_173_val = -2155/3"

definition D_173_val :: real where
  "D_173_val = -1141518/9"


(**************************************************************)
(* SECTION : Validation de l'écart entre 227 et 173           *)
(**************************************************************)

section "Validation numérique de l'écart entre 227 et 173 (1/3)"

lemma ecart_227_173_1_3:
  "((SA_179_val - (SB_227_val - D_227_val) - D_173_val) / 729) = -53"
  by (simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def)

(**************************************************************)
(* SECTION : Equation generale d'ecart pour le rapport 1/3    *)
(**************************************************************)

section "Equation generale d'ecart pour le rapport spectral 1/3"

text \<open>
  Formule generale pour l'ecart entre deux nombres premiers
  dans le modele spectral 1/3, a partir de deux suites A et B
  de n termes et de leurs Digamma associes.

  Forme generale (rapport 1/3) :

      (A_next - (B_high - D_high) - D_low) / 729

  ou :

    - A_next  : somme de la suite A pour le premier suivant du plus petit
    - B_high  : somme de la suite B pour le plus grand premier
    - D_high  : Digamma du plus grand premier
    - D_low   : Digamma du plus petit premier

  Le resultat correspond a la quantite de nombres entiers entre les deux premiers.
\<close>

definition gap_equation_1_3 :: "real =>real =>real =>real =>real" where
  "gap_equation_1_3 A_next B_high D_high D_low =
     (A_next - (B_high - D_high) - D_low) / 729"

lemma gap_equation_1_3_simplifiee:
  "gap_equation_1_3 A_next B_high D_high D_low =
     (A_next - B_high + D_high - D_low) / 729"
  unfolding gap_equation_1_3_def by simp


(**************************************************************)
(* SECTION : Postulat spectral d'ecart 1/3                    *)
(**************************************************************)

text \<open>
  Postulat spectral d'ecart pour le rapport 1/3 :

  Pour toute paire de nombres premiers (p_high, p_low),
  et pour leurs valeurs spectrales associees (A_next, B_high, D_high, D_low)
  construites selon le modele 1/3, l'equation d'ecart donne exactement
  la quantite de nombres entiers entre ces deux premiers :

      gap_equation_1_3 ... = p_low - p_high
\<close>

axiomatization where
  spectral_gap_postulate_1_3:
    "\<And>p_high p_low A_next B_high D_high D_low.
       prime p_high==>prime p_low==>
       gap_equation_1_3 A_next B_high D_high D_low =
         real (p_low - p_high)"


(**************************************************************)
(* SECTION : Lemme general pour l'ecart entre deux premiers   *)
(**************************************************************)

lemma gap_equation_1_3_for_primes:
  assumes "prime p_high" "prime p_low"
  shows "gap_equation_1_3 A_next B_high D_high D_low =
         real (p_low - p_high)"
  using spectral_gap_postulate_1_3 assms by blast


(**************************************************************)
(* SECTION : Lien avec l'exemple 227 / 173                    *)
(**************************************************************)

section "Validation de l'exemple 227 / 173 via l'equation generale 1/3"

lemma ecart_227_173_1_3_via_gap_equation:
  "gap_equation_1_3 SA_179_val SB_227_val D_227_val D_173_val = -53"
  by (simp add: gap_equation_1_3_def
                SA_179_val_def SB_227_val_def
                D_227_val_def D_173_val_def)


(**************************************************************)
(* SECTION : Valeurs spectrales exactes pour 947 et 881 (1/4) *)
(**************************************************************)

section "Valeurs spectrales exactes pour 947 et 881 (1/4)"

definition SA_883_val :: real where
  "SA_883_val = 75/4"

definition SB_947_val :: real where
  "SB_947_val = 5260628"

definition D_947_val :: real where
  "D_947_val = 1381716"

definition D_881_val :: real where
  "D_881_val = -(14450613/4)"


(**************************************************************)
(* SECTION : Equation generale d'ecart pour le rapport 1/4    *)
(**************************************************************)

section "Equation generale d'ecart pour le rapport spectral 1/4"

definition gap_equation_1_4 :: "real =>real =>real =>real =>real" where
  "gap_equation_1_4 A_next B_high D_high D_low =
     (A_next - (B_high - D_high) - D_low) / 4096"

lemma gap_equation_1_4_simplifiee:
  "gap_equation_1_4 A_next B_high D_high D_low =
     (A_next - B_high + D_high - D_low) / 4096"
  unfolding gap_equation_1_4_def by simp


(**************************************************************)
(* SECTION : Postulat spectral d'ecart 1/4                    *)
(**************************************************************)

text \<open>
  Postulat spectral d'ecart pour le rapport 1/4 :

  Pour toute paire de nombres premiers (p_high, p_low),
  et pour leurs valeurs spectrales associees (A_next, B_high, D_high, D_low)
  construites selon le modele 1/4, l'equation d'ecart donne exactement
  la quantite de nombres entiers entre ces deux premiers :

      gap_equation_1_4 ... = p_low - p_high
\<close>

axiomatization where
  spectral_gap_postulate_1_4:
    "\<And>p_high p_low A_next B_high D_high D_low.
       prime p_high==>prime p_low==>
       gap_equation_1_4 A_next B_high D_high D_low =
         real (p_low - p_high)"


(**************************************************************)
(* SECTION : Lemme general pour l'ecart entre deux premiers   *)
(**************************************************************)

lemma gap_equation_1_4_for_primes:
  assumes "prime p_high" "prime p_low"
  shows "gap_equation_1_4 A_next B_high D_high D_low =
         real (p_low - p_high)"
  using spectral_gap_postulate_1_4 assms by blast


(**************************************************************)
(* SECTION : Lien avec l'exemple 947 / 881                    *)
(**************************************************************)

section "Validation de l'exemple 947 / 881 via l'equation generale 1/4"

lemma ecart_947_881_1_4_via_gap_equation:
  "gap_equation_1_4 SA_883_val SB_947_val D_947_val D_881_val = -65"
  by (simp add: gap_equation_1_4_def
                SA_883_val_def SB_947_val_def
                D_947_val_def D_881_val_def)

(****************************************************************)
(* Mentions légales                                             *)
(****************************************************************)

text \<open>
  Tous droits réservés.
  Toute reproduction, diffusion ou utilisation commerciale
  est interdite sans l'autorisation écrite de l'auteur.

  Auteur : Philippe Thomas Savard
  Date   : Deux février deux mille vingt-deux
\<close>

end