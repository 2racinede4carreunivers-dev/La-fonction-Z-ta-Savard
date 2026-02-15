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
(*        - Equations negatives                                 *)
(*     2. Demonstration des suites negatives (n < 0)            *)
(*        - Structure geometrique                               *)
(*        - Exemples explicites SA_neg                          *)
(*        - Correspondance rang ↔ premier negatif               *)
(*     3. Definition generale du Digamma calcule                *)
(*        - Version positive                                    *)
(*        - Version négative                                    *)
(*     4. Définition generale du Gap spectral (Methode Savard)  *)
(*                                                              *)
(* IV. ÉCART ENTRE DEUX NOMBRES PREMIERS                        *)
(*     1. Exemple 1 : Écart entre 23 et 7                       *)
(*     2. Exemple 2 : Écart entre -19 et -5                     *)
(*     3. Exemple 3 : Écart entre -31 et 17                     *)
(*     4. Exemple 4 : Écart entre 227 et 173 (rapport 1/3)      *)
(*     5. Exemple 5 : Écart entre 947 et 881 (rapport 1/4)      *)
(****************************************************************)

(****************************************************************)
(* Sous-bloc 1 : formes generales des suites A et B             *)
(****************************************************************)
section "Forme genrale des suites A et B"

definition SA :: "nat \<Rightarrow> real" where
  "SA n = (3.25 / 2) * (2 ^ n) - 2"

definition SB :: "nat \<Rightarrow> real" where
  "SB n = (6.5 / 2) * (2 ^ n) - 66"


(****************************************************************)
(* Sous-bloc 2 : validite pour tout n > 0                       *)
(****************************************************************)

lemma SA_forme_generale:
  assumes "n > 0"
  shows "SA n = (3.25 / 2) * (2 ^ n) - 2"
  using assms by (simp add: SA_def)

lemma SB_forme_generale:
  assumes "n > 0"
  shows "SB n = (6.5 / 2) * (2 ^ n) - 66"
  using assms by (simp add: SB_def)


(****************************************************************)
(* Sous-bloc 3 : rapport spectral = 1/2 (cas 1×1)               *)
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
(* AJOUT : généralisation symétrique n×n                        *)
(****************************************************************)
section "Rapport spectral n×n (généralisation symétrique)"

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


(****************************************************************)
(* Sous-bloc 4 : Digamma calcule                                *)
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
(* Postulat spectral 1/2 (régime positif)                       *)
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
(* Sous-bloc 5 : Exemples concrets pour 29, 31, 37, 41          *)
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

section "Modele spectrale 1/4 : Forme generale des suite A et B."

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
section "Axiomatisation spectral 1/4"
axiomatization where
  spectral_postulate_1_4:
    "\<And>n p. n > 0 \<Longrightarrow> prime p \<Longrightarrow> prime_equation_1_4 n p = real p"


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

section "Rapport 1/3 forme generaliser pour les suites A et B."

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
section "Axiomatisation rapport 1/3."
axiomatization where
  spectral_postulate_1_3:
    "\<And>n p. n > 0 \<Longrightarrow> prime p \<Longrightarrow> prime_equation_1_3 n p = real p"


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

section "Rapport spectal 1/3 validation numerique pour les suite A et B, Digamma, Digamma calcule et la determination du premier 227."

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
(* SECTION 6 : Rapport Spectral 1/3 et 1/4 constant           *)
(**************************************************************)
section "Rapport spectral constant 1/3 et 1/4."

section "Rapport spectral 1/3 Validation généralisé."

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

section "Rapport spectral constant 1/4."

definition RsP_1_4 :: "nat => nat => real" where
  "RsP_1_4 n1 n2 =
    (A_1_4 n1 - A_1_4 n2) /
    (B_1_4 n1 - B_1_4 n2)"

section "Rapport spectral 1/4 validation généralisé."
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
(* SECTION : Forme générale de l'écart                        *)
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

definition n_m7  :: real where "n_m7  = -7"
definition n_m3  :: real where "n_m3  = -3"
definition n_m19 :: real where "n_m19 = -8"

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

definition n_m29 :: real where "n_m29 = -10"
definition n_p17 :: real where "n_p17 = 8"
definition n_m31 :: real where "n_m31 = -11"

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

section "Forme générale de l'écart mixte"

definition gap_mix_val ::
  "real => real => real => real => real => real" where
  "gap_mix_val A_next B_high D_high D_low dummy =
      (A_next - (B_high - D_high) - D_low) / 64"

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

section "Valeurs spectrales exactes pour 23 et 7"

definition SA_11_val :: real where "SA_11_val = 50"
definition SB_23_val :: real where "SB_23_val = 1598"
definition D_23_val :: real where "D_23_val = 126"
definition SB_7_val :: real where "SB_7_val = -14"
definition D_7_val :: real where "D_7_val = -464"

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

section "Validation numérique de l'écart entre 227 et 173 (1/3)"

lemma ecart_227_173_1_3:
  "((SA_179_val - (SB_227_val - D_227_val) - D_173_val) / 729) = -53"
  by (simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def)


(**************************************************************)
(* SECTION : Equation generale d'ecart pour le rapport 1/3    *)
(**************************************************************)

section "Equation generale d'ecart pour le rapport spectral 1/3"

definition gap_equation_1_3 :: "real => real => real => real => real" where
  "gap_equation_1_3 A_next B_high D_high D_low =
     (A_next - (B_high - D_high) - D_low) / 729"

lemma gap_equation_1_3_simplifiee:
  "gap_equation_1_3 A_next B_high D_high D_low =
     (A_next - B_high + D_high - D_low) / 729"
  unfolding gap_equation_1_3_def by simp


(**************************************************************)
(* SECTION : Postulat spectral d'ecart 1/3                    *)
(**************************************************************)

axiomatization where
  spectral_gap_postulate_1_3:
    "\<And>p_high p_low A_next B_high D_high D_low.
       prime p_high \<Longrightarrow> prime p_low \<Longrightarrow>
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

definition gap_equation_1_4 :: "real => real => real => real => real" where
  "gap_equation_1_4 A_next B_high D_high D_low =
     (A_next - (B_high - D_high) - D_low) / 4096"

lemma gap_equation_1_4_simplifiee:
  "gap_equation_1_4 A_next B_high D_high D_low =
     (A_next - B_high + D_high - D_low) / 4096"
  unfolding gap_equation_1_4_def by simp


(**************************************************************)
(* SECTION : Postulat spectral d'ecart 1/4                    *)
(**************************************************************)

axiomatization where
  spectral_gap_postulate_1_4:
    "\<And>p_high p_low A_next B_high D_high D_low.
       prime p_high \<Longrightarrow> prime p_low \<Longrightarrow>
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
