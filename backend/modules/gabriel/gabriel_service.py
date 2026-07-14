"""
Service Gabriel - Assistant HOL specialiste Geometrie du spectre des nombres premiers.
Combine le moteur de calcul spectral avec un LLM pour des reponses detaillees.
"""
from __future__ import annotations
import os
import re
import logging

logger = logging.getLogger(__name__)

SPECTRAL_SYSTEM_PROMPT = """Tu es Gabriel, assistant HOL specialiste de la GEOMETRIE DU SPECTRE DES NOMBRES PREMIERS,
methode developpee par Philippe Thomas Savard dans sa theorie "L'univers est au carre".

=== SOURCE : methode_spectral.thy (COMPILE AVEC SUCCES - Isabelle/HOL) ===
Ce fichier .thy de 2956 lignes compile integralement. Toutes les formules ci-dessous sont PROUVEES.

=== SECTION I : RAPPORT SPECTRAL 1/2 - FONDATIONS ===

DEFINITIONS FONDAMENTALES (lignes 102-106):
  SA(n) = (3.25/2) * 2^n - 2 = (13/8) * 2^n - 2
  SB(n) = (6.5/2) * 2^n - 66 = (13/4) * 2^n - 66

RAPPORT SPECTRAL (ligne 130-131):
  RsP(n1, n2) = (SA(n1) - SA(n2)) / (SB(n1) - SB(n2))

LEMME PROUVE RsP_un_demi_general (lignes 133-163):
  Pour tout n1 >= 1, n2 >= 1, n1 != n2 : RsP(n1, n2) = 1/2 EXACTEMENT

DIGAMMA ET EQUATION DU PREMIER (lignes 165-180):
  digamma_calc(n, p) = SB(n) - 64 * p
  prime_equation(n, p) = (SB(n) - digamma_calc(n, p)) / 64 = p

LEMME PROUVE prime_equation_identity (ligne 196):
  Pour tout n >= 1 et p premier a la position n:
  (SB(n) - digamma_calc(n, p)) / 64 = p [TAUTOLOGIE PROUVEE]

TABLE DES POSITIONS (rapport 1/2):
  n=1->p=2, n=2->p=3, n=3->p=5, n=4->p=7, n=5->p=11, n=6->p=13, n=7->p=17, n=8->p=19,
  n=9->p=23, n=10->p=29, n=11->p=31, n=12->p=37, n=13->p=41, n=14->p=43, n=15->p=47,
  n=16->p=53, n=17->p=59, n=18->p=61, n=19->p=67, n=20->p=71, n=21->p=73, n=22->p=79,
  n=23->p=83, n=24->p=89, n=25->p=97, n=26->p=101, n=33->p=137

=== SECTION II-IV : MODELES SPECTRAUX 1/3 et 1/4 ===
Rapport 1/2 : facteur = 64   (modele principal, Section I)
Rapport 1/3 : facteur = 729  (Section III)
Rapport 1/4 : facteur = 4096 (Sections II et IV)

=== SECTION V-VI : NOMBRES PREMIERS NEGATIFS ===
Pour les positions negatives (n <= -1):
  SA_neg(n) = 3.25 * 2^n - 2
  SB_neg(n) = 6.5 * 2^n - 66
  digamma_neg(n, p) = SB_neg(n) - 64 * p
  Le n-ieme premier negatif = -(|n|-ieme premier positif)
  Exemples: n=-1->p=-2, n=-2->p=-3, n=-3->p=-5, n=-7->p=-17, n=-8->p=-19, n=-10->p=-29

=== SECTION VII : CONFIGURATIONS DU RAPPORT SPECTRAL ===
1. Symetrique 1*1 : (SA(n1) - SA(n2)) / (SB(n1) - SB(n2)) = 1/2 TOUJOURS
2. Symetrique n*n : sum_A / sum_B = 1/2 pour blocs de meme taille
3. Asymetrique ORDONNEE : len(B) = len(A)+1, max(A) < min(B), ordre croissant
4. Asymetrique CHAOTIQUE : longueurs differentes, ordre quelconque -> converge vers 1/2

=== ECARTS ENTRE PREMIERS (Sections V-VI du .thy) ===

FORMULE GENERALE D'ECART (gap_neg_val, ligne 1455-1458):
  gap = (A_next - (B_high - D_high) - D_low) / 64

CAS POSITIF-POSITIF (ex: 5 et 47):
  n_min=3 (p=5), n_max=15 (p=47), n_suivant_min=4 (p=7)
  SA(4)=24, SB(15)=106430, Digamma(15,47)=103422, SB(3)=-40, Digamma(3,5)=-360
  gap = (24 - (106430 - 103422) - (-360)) / 64 = -2624/64 = -41 EXACT

CAS NEGATIF-NEGATIF (ex: -19 et -5, lemme gap_m19_m5 ligne 1500-1505):
  LEMME PROUVE: gap_neg_val(...) = -13 EXACT

CAS MIXTE (ex: -31 et 17, lemme gap_m31_17 ligne 1900-1902):
  LEMME PROUVE: gap_mix_val(...) = -47 EXACT
  Note: Le zero est inclus UNIQUEMENT dans les ecarts mixtes (ligne 1926)

=== PREUVE PAR L'ABSURDE - EXCLUSION DES COMPOSES (Section apres ligne 1509) ===

THEOREME composite_not_prime_i (lignes 1535-1546):
  Pour tout compose C (non premier), pour tout i: C != prime_i(i)
  Preuve: Si C = prime_i(i), alors prime(prime_i(i)) implique prime(C), CONTRADICTION.

COROLLAIRES PROUVES:
- spectral_method_exclusively_for_primes : La MS s'applique UNIQUEMENT a P
- composite_no_reconstruction_position : Pas de reconstruction pour composes
- composite_pair_no_rsp_positions : Pas de RsP pour paires de composes

INTERPRETATION: L'echec systematique de prime_position(C) pour un compose C
est la CONTRAPOSITION EFFECTIVE du theoreme composite_not_prime_i.

=== SECTION X : PLAN TRIFOCAL (lignes 2100+) ===
Validation epipolaire avec 3 foyers: Zeta / Spectral / RH
Theoreme final: solution epipolaire validee

=== SECTION XI : REGLES DE CONSTRUCTION DES SUITES (8+ termes) ===
Definition raison_spectrale (ligne 2375): coefficient de progression
Definition avant_dernier_terme_savard (ligne 2390)
Definition dernier_terme_savard (ligne 2398)
Theoreme ecart_minimal_universel_A (ligne 2586)
Theoreme ecart_minimal_universel_B (ligne 2610)

=== REGLE ABSOLUE ===
Le resultat du moteur spectral Python est TOUJOURS EXACT. Ne jamais arrondir
ou "corriger" les valeurs calculees. Le fichier .thy COMPILE = PROUVE.

=== REGLES DE FORMATAGE DES REPONSES ===
IMPORTANT: Tu DOIS formater tes reponses avec un Markdown PROPRE et STRUCTURE:

1. UTILISE des titres avec des SAUTS DE LIGNE AVANT ET APRES:

# Titre Principal

## Sous-titre

2. SEPARE chaque section par des LIGNES VIDES:

**Donnees de base:**

- Premier: p = 59
- Position: n = 17

3. UTILISE des blocs de code pour les calculs:

```
SA(17) = 212990.0
SB(17) = 425918.0
```

4. STRUCTURE avec des listes a puces:

- Point 1
- Point 2
- Point 3

5. MET EN VALEUR les resultats importants avec du gras: **resultat = 59**

6. AJOUTE toujours une CONCLUSION claire a la fin

=== REGLES DE REPONSE ===
- TOUJOURS utiliser les calculs du moteur spectral Python quand fournis.
- TOUJOURS inclure la valeur du digamma calcule dans les reponses de reconstruction.
- TOUJOURS montrer chaque etape: SA(n), SB(n), digamma_calcule(n,p), equation du premier, verification.
- TOUJOURS distinguer "n = position" (rapport 1/2) vs "n != position" (autres rapports).
- TOUJOURS reconnaitre que la methode FONCTIONNE mathematiquement.
- Format de reconstruction: montrer SA, SB, digamma calcule = SB(n) - 64*p, puis (SB - digamma)/64 = p.
- Si donnee manquante : demander precision, JAMAIS inventer.
- Repondre en francais, avec rigueur mathematique et un vocabulaire precis et elegant.
- Utiliser un langage scientifique accessible mais rigoureux.
- Tu as acces a une table de 1000 nombres premiers (2 a 7919).
"""


def detect_computation_request(question: str) -> dict:
    """Detecte si la question necessite un calcul spectral et extrait les parametres."""
    q = question.lower()
    result = {"needs_computation": False, "type": None, "params": {}}

    # Detection de nombres - gere "19ieme", "17e", "29" etc. et aussi nombres negatifs "-41"
    prime_matches = re.findall(r'-?\d+', question)
    numbers = [int(x) for x in prime_matches if abs(int(x)) <= 8000 and int(x) != 0]
    positive_numbers = [n for n in numbers if n > 0]

    # Detection des indicateurs ordinaux (37ième, 12e, 100ème, etc.)
    # Ces patterns indiquent une demande de POSITION, pas d'analyse d'un premier
    ordinal_pattern = re.search(r'(\d+)\s*(ième|ieme|ème|eme|e|er|ère|ere)\s*(nombre\s*)?(premier|prime)?', q)
    is_ordinal_request = ordinal_pattern is not None
    
    is_negative = any(k in q for k in ["negatif", "négatif", "negative", "négative", "négatifs", "negatifs", "n<=-1", "n <= -1", "n=-"])

    # PRIORITE 0: Ecart entre premiers (V2 - supporte negatifs)
    # DOIT être avant reconstruction car "écart entre -11 et 31" ne doit pas déclencher reconstruct
    if any(k in q for k in ["ecart", "écart", "gap", "distance entre"]):
        if len(numbers) >= 2:
            result["needs_computation"] = True
            result["type"] = "gap_v2"
            result["params"]["primes"] = numbers[:2]
            return result

    # PRIORITE 1: Demande de position/reconstruction (détection ordinale)
    # "37ième nombre premier", "quel est le 100e premier", "reconstruis le 12ème"
    if is_ordinal_request or any(k in q for k in ["position", "quel est le", "n-ieme", "nieme", "n-ième", "nième", 
                                                    "combien", "reconstruire", "reconstruis", "reconstruit", 
                                                    "reconstruction", "déterminer", "determiner", "trouver le", "générer", "generer"]):
        if positive_numbers:
            result["needs_computation"] = True
            result["type"] = "reconstruct_neg" if is_negative else "reconstruct"
            result["params"]["numbers"] = positive_numbers
            return result  # Retourner immédiatement pour éviter les overrides

    # Detection directe des premiers negatifs meme sans mot-cle reconstruction
    if is_negative and positive_numbers:
        result["needs_computation"] = True
        result["type"] = "reconstruct_neg"
        result["params"]["numbers"] = positive_numbers
        return result

    # Courbe RSP (NOUVELLE FONCTIONNALITE V2)
    if any(k in q for k in ["courbe rsp", "rsp curve", "evolution du rapport", "convergence"]):
        result["needs_computation"] = True
        result["type"] = "rsp_curve"
        result["params"]["config"] = "1x1"  # Par defaut
        if "sym" in q or "symetrique" in q:
            result["params"]["config"] = "sym"
        elif "chaos" in q or "chaotique" in q:
            result["params"]["config"] = "chaos"
        elif "ord" in q or "ordonne" in q:
            result["params"]["config"] = "ord"
        result["params"]["k_max"] = 50
        for n in positive_numbers:
            if n <= 500:
                result["params"]["k_max"] = n
                break
        return result

    # Rapport spectral
    if any(k in q for k in ["rapport", "ratio", "rsp", "1/2", "1/3", "1/4"]):
        result["needs_computation"] = True
        result["type"] = "spectral_ratio"
        if positive_numbers:
            result["params"]["numbers"] = positive_numbers
        return result

    # Plage de nombres premiers
    if any(k in q for k in ["plage", "range", "liste", "premiers de", "premiers entre"]):
        if len(positive_numbers) >= 2:
            result["needs_computation"] = True
            result["type"] = "range"
            result["params"]["start"] = min(positive_numbers[:2])
            result["params"]["end"] = max(positive_numbers[:2])
        elif len(positive_numbers) == 1:
            result["needs_computation"] = True
            result["type"] = "range"
            result["params"]["start"] = 2
            result["params"]["end"] = positive_numbers[0]
        return result

    # Verification/analyse d'un premier (APRES les détections de position)
    if any(k in q for k in ["verifie", "analyse", "montre", "prouve", "calcul", "spectral", "digamma", "equation"]):
        if positive_numbers:
            result["needs_computation"] = True
            result["type"] = "analyze_prime"
            result["params"]["primes"] = positive_numbers
            return result

    # Fallback: si des nombres sont mentionnes dans un contexte math SANS indicateur ordinal
    if not result["needs_computation"] and positive_numbers and any(k in q for k in ["premier", "prime", "nombre"]):
        # Vérifier qu'il n'y a pas d'indicateur ordinal caché
        if not is_ordinal_request:
            result["needs_computation"] = True
            result["type"] = "analyze_prime"
            result["params"]["primes"] = positive_numbers[:5]

    return result


def run_computation(detection: dict) -> str:
    """Execute le calcul spectral et retourne un resume textuel."""
    from .spectral_engine import (
        analyze_prime, analyze_range, verify_prime_equation,
        compute_spectral_ratio, nth_prime, prime_position,
        is_known_prime, PRIMES, max_position,
        SA_neg, SB_neg, neg_nth_prime, verify_neg_prime_equation, analyze_neg_prime
    )

    comp_type = detection["type"]
    params = detection["params"]
    lines = []

    if comp_type == "analyze_prime":
        for p in params.get("primes", [])[:5]:
            if is_known_prime(p):
                r = analyze_prime(p)
                m = r["models"]["1/2"]
                lines.append(f"=== Premier {p} (position n={r['position']}) ===")
                lines.append(f"  SA({r['position']}) = {m['SA']}")
                lines.append(f"  SB({r['position']}) = {m['SB']}")
                lines.append(f"  Digamma calcule = {m['digamma_calc']}")
                lines.append(f"  Reconstruction: (SB - dgm) / 64 = {m['reconstructed_p']}")
                lines.append(f"  Equation valide: {m['equation_holds']}")
                if r.get("neighbors"):
                    nb = r["neighbors"]
                    if "precedent" in nb:
                        lines.append(f"  Voisin precedent: {nb['precedent']['prime']} (n={nb['precedent']['position']})")
                    if "suivant" in nb:
                        lines.append(f"  Voisin suivant: {nb['suivant']['prime']} (n={nb['suivant']['position']})")
            else:
                pos = prime_position(p)
                if pos:
                    lines.append(f"{p} est le {pos}e nombre premier")
                else:
                    lines.append(f"{p} n'est pas un nombre premier (ou hors table 2-7919)")

    elif comp_type == "position":
        for n in params.get("numbers", []):
            p = nth_prime(n)
            if p:
                lines.append(f"Le {n}e nombre premier est {p}")
                v = verify_prime_equation(n, p, "1/2")
                lines.append(f"  Verification: SA={v['SA']}, SB={v['SB']}, dgm={v['digamma_calc']}, valid={v['equation_holds']}")
            else:
                pos = prime_position(n)
                if pos:
                    lines.append(f"{n} est le {pos}e nombre premier")
                else:
                    lines.append(f"Position {n} hors table (max: {max_position()})")

    elif comp_type == "reconstruct":
        # Import du generateur HOL
        from .hol_generator import generate_hol_for_reconstruction
        from .spectral_models import get_model
        
        for n in params.get("numbers", []):
            p = nth_prime(n)
            if p:
                # Utiliser le nouveau modele spectral
                model = get_model("1/2")
                result = model.reconstruct_nth_prime(n, p)
                
                # Calcul des valeurs flottantes pour affichage
                SA_float = float(result.A_value)
                SB_float = float(result.B_value)
                digamma_float = float(result.digamma)
                
                lines.append(f"=== RECONSTRUCTION DU {n}e NOMBRE PREMIER ===")
                lines.append(f"  Position: n = {n}")
                lines.append(f"  Premier reconstruit: p = {p}")
                lines.append(f"")
                lines.append(f"  Suite A positive: SA({n}) = (13/8) * 2^{n} - 2 = {SA_float}")
                lines.append(f"  Suite B positive: SB({n}) = (13/4) * 2^{n} - 66 = {SB_float}")
                lines.append(f"")
                lines.append(f"  Digamma calcule: digamma({n}, {p}) = SB({n}) - 64 * {p} = {SB_float} - {64 * p} = {digamma_float}")
                lines.append(f"")
                lines.append(f"  Equation du premier:")
                lines.append(f"    prime_equation = (SB({n}) - digamma_calcule) / 64")
                lines.append(f"                   = ({SB_float} - {digamma_float}) / 64")
                lines.append(f"                   = {SB_float - digamma_float} / 64")
                lines.append(f"                   = {int(result.reconstructed_prime)}")
                lines.append(f"")
                lines.append(f"  Equation valide: {result.is_exact}")
                lines.append(f"  Le {n}e nombre premier est bien {p}")
                lines.append(f"")
                lines.append(f"INVARIANT (ratio 1/2): position = n = number_of_terms = {n}")
                lines.append(f"SA_sum={SA_float:.6f}, SB_sum={SB_float:.6f}, digamma={digamma_float:.6f}")
                
                # Generer le fragment HOL
                hol_code = generate_hol_for_reconstruction(
                    n=n, p=p,
                    SA_value=SA_float,
                    SB_value=SB_float,
                    digamma_value=digamma_float,
                    model="1/2"
                )
                lines.append(f"")
                lines.append(f"=== FRAGMENT HOL GENERE ===")
                lines.append(hol_code)
            else:
                pos = prime_position(n)
                if pos:
                    lines.append(f"{n} est un nombre premier (position {pos})")
                    v = verify_prime_equation(pos, n, "1/2")
                    lines.append(f"  SA({pos}) = {v['SA']}")
                    lines.append(f"  SB({pos}) = {v['SB']}")
                    lines.append(f"  Digamma calcule = {v['digamma_calc']}")
                    lines.append(f"  Reconstruction: {v['reconstructed_p']}")
                    lines.append(f"  Equation valide: {v['equation_holds']}")
                else:
                    lines.append(f"Position {n} hors table (max: {max_position()})")

    elif comp_type == "reconstruct_neg":
        for n in params.get("numbers", []):
            neg_n = -abs(n)
            p_neg = neg_nth_prime(neg_n)
            if p_neg is not None:
                v = verify_neg_prime_equation(neg_n, p_neg)
                lines.append(f"=== RECONSTRUCTION DU {abs(neg_n)}e NOMBRE PREMIER NEGATIF ===")
                lines.append(f"  Position negative: n = {neg_n}")
                lines.append(f"  Premier negatif: p = {p_neg}")
                lines.append(f"")
                lines.append(f"  Equations pour n <= -1:")
                lines.append(f"  SA_neg({neg_n}) = 3.25 * 2^({neg_n}) - 2 = {v['SA_neg']}")
                lines.append(f"  SB_neg({neg_n}) = 6.5 * 2^({neg_n}) - 66 = {v['SB_neg']}")
                lines.append(f"")
                lines.append(f"  Digamma calcule: digamma({neg_n}, {p_neg}) = SB_neg({neg_n}) - 64 * ({p_neg})")
                lines.append(f"                 = {v['SB_neg']} - {64 * p_neg} = {v['digamma_calc']}")
                lines.append(f"")
                lines.append(f"  Equation du premier negatif:")
                lines.append(f"    prime_equation = (SB_neg({neg_n}) - digamma_calcule) / 64")
                lines.append(f"                   = ({v['SB_neg']} - {v['digamma_calc']}) / 64")
                lines.append(f"                   = {v['SB_neg'] - v['digamma_calc']} / 64")
                lines.append(f"                   = {v['reconstructed_p']}")
                lines.append(f"")
                lines.append(f"  Equation valide: {v['equation_holds']}")
                lines.append(f"  Le {abs(neg_n)}e nombre premier negatif est bien {p_neg}")
            else:
                lines.append(f"Position {n} hors table (max: {max_position()})")

    elif comp_type == "range":
        start = params.get("start", 2)
        end = min(params.get("end", 100), 200)
        results = analyze_range(start, end)
        lines.append(f"=== Nombres premiers de {start} a {end} ({len(results)} premiers) ===")
        for r in results[:20]:
            m = r["models"]["1/2"]
            lines.append(f"  p={r['prime']:>4} (n={r['position']:>3}) | SA={m['SA']:>12.0f} | SB={m['SB']:>12.0f} | dgm={m['digamma_calc']:>12.0f} | OK={m['equation_holds']}")
        if len(results) > 20:
            lines.append(f"  ... ({len(results) - 20} premiers supplementaires omis)")

    elif comp_type == "spectral_ratio":
        numbers = params.get("numbers", [])
        if len(numbers) >= 2:
            positions = []
            for n in numbers:
                pos = prime_position(n)
                if pos:
                    positions.append(pos)
            if len(positions) >= 2:
                mid = len(positions) // 2
                A_idx = positions[:mid] if mid > 0 else positions[:1]
                B_idx = positions[mid:]
                r = compute_spectral_ratio(A_idx, B_idx, "1/2")
                lines.append(f"=== Rapport spectral ===")
                lines.append(f"  Configuration: {r['configuration']}")
                lines.append(f"  A_indices: {r['A_indices']} | B_indices: {r['B_indices']}")
                lines.append(f"  Ratio: {r['ratio']}")
                lines.append(f"  Attendu: {r['expected']}")
                lines.append(f"  Correspond: {r['matches_expected']}")

    elif comp_type == "gap":
        primes = params.get("primes", [])
        if len(primes) >= 2:
            p1, p2 = sorted(primes[:2])
            pos1 = prime_position(p1)
            pos2 = prime_position(p2)
            if pos1 and pos2:
                v1 = verify_prime_equation(pos1, p1, "1/2")
                v2 = verify_prime_equation(pos2, p2, "1/2")
                lines.append(f"=== Ecart entre {p1} et {p2} ===")
                lines.append(f"  {p1}: n={pos1}, SB={v1['SB']}, dgm={v1['digamma_calc']}")
                lines.append(f"  {p2}: n={pos2}, SB={v2['SB']}, dgm={v2['digamma_calc']}")
                lines.append(f"  Ecart arithmetique: {p2 - p1}")
                lines.append(f"  Entiers entre eux: {p2 - p1 - 1}")

    elif comp_type == "gap_v2":
        # NOUVELLE FORMULE V2 - Supporte positifs, negatifs et mixtes
        from .gap_solver import compute_gap as gap_compute
        primes = params.get("primes", [])
        if len(primes) >= 2:
            p1, p2 = primes[0], primes[1]
            result = gap_compute(p1, p2)
            if result and "error" not in result:
                lines.append(f"=== ECART SPECTRAL V2 (Formule corrigee) ===")
                lines.append(f"  Type d'ecart: {result['gap_type']}")
                lines.append(f"")
                lines.append(f"  IMPORTANT: Les valeurs ci-dessous sont les NOMBRES PREMIERS eux-memes,")
                lines.append(f"  PAS leurs positions. La position est entre parentheses.")
                lines.append(f"")
                lines.append(f"  Nombre premier 1: p = {result['p1']} (se trouve a la position n={result['position_p1']})")
                lines.append(f"  Nombre premier 2: p = {result['p2']} (se trouve a la position n={result['position_p2']})")
                lines.append(f"")
                lines.append(f"  Calculs spectraux:")
                lines.append(f"    Position suivant min: n={result['position_suivant_min']}")
                lines.append(f"    SA(n_suivant_min) = {result['SA_suivant_min']:.6f}")
                lines.append(f"    SB(n_min) = {result['SB_min']:.6f}")
                lines.append(f"    Digamma(n_min) = {result['digamma_min']:.6f}")
                lines.append(f"    SB(n_max) = {result['SB_max']:.6f}")
                lines.append(f"    Digamma(n_max) = {result['digamma_max']:.6f}")
                lines.append(f"")
                lines.append(f"  Formule: {result['formula_used']}")
                lines.append(f"  Ecart spectral calcule: {result['gap_float']:.4f} ~ {result['gap_count']}")
                if "arithmetic_gap" in result.get("validation", {}):
                    arith = result['validation']['arithmetic_gap']
                    lines.append(f"  Ecart arithmetique reel: {result['p2']} - ({result['p1']}) = {arith}")
                lines.append(f"")
                lines.append(f"  RESUME: L'ecart entre les nombres premiers {result['p1']} et {result['p2']} est {result['validation'].get('arithmetic_gap', 'N/A')} (arithmetique)")
            else:
                error_msg = result.get("error", "Erreur inconnue") if result else "Calcul impossible"
                lines.append(f"Erreur calcul ecart: {error_msg}")

    elif comp_type == "rsp_curve":
        # NOUVELLE FONCTIONNALITE - Courbe RSP
        from .rsp_curve import generate_rsp_viz_data
        config = params.get("config", "1x1")
        k_max = params.get("k_max", 50)
        result = generate_rsp_viz_data(config, k_max)
        lines.append(f"=== COURBE RSP (Configuration: {config}, k=1 a {k_max}) ===")
        lines.append(f"")
        lines.append(result["ascii_curve"])
        lines.append(f"")
        lines.append(f"=== RESUME STATISTIQUE ===")
        lines.append(result["summary"])

    if not lines:
        return "(Aucun calcul spectral applicable pour ces parametres)"

    return "\n".join(lines)


async def gabriel_ask(question: str, session_id: str, conversation_history: list = None) -> dict:
    """Point d'entree principal de Gabriel: detecte les calculs necessaires,
    execute le moteur spectral, puis utilise le LLM pour formuler la reponse.
    
    NOUVEAU (v7): Detecte les nombres composes et retourne une preuve par l'absurde
    pedagogique expliquant pourquoi la Methode Spectrale ne s'applique qu'aux premiers.
    
    IMPORTANT: La detection des composes ne s'applique QUE lorsque l'utilisateur
    demande explicitement d'analyser un nombre comme premier (ecart, analyse),
    PAS pour les positions/indices (reconstruction du n-ieme premier).
    """
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    from .composite_absurdity_prover import get_composite_rejection_response
    
    detection = detect_computation_request(question)
    
    # NOUVEAU: Verifier si des nombres composes sont presents
    # MAIS seulement pour les types de calcul ou le nombre EST le premier a analyser
    # PAS pour reconstruction (ou le nombre est une POSITION, pas un premier)
    composite_check_types = ["gap_v2", "analyze_prime", "spectral_ratio"]
    
    if detection["needs_computation"] and detection["type"] in composite_check_types:
        # Extraire les nombres qui sont les SUJETS du calcul (premiers a analyser)
        numbers_to_check = []
        if detection["type"] == "gap_v2":
            numbers_to_check = detection["params"].get("primes", [])
        elif detection["type"] == "analyze_prime":
            numbers_to_check = detection["params"].get("primes", [])
        elif detection["type"] == "spectral_ratio":
            numbers_to_check = detection["params"].get("numbers", [])
        
        if numbers_to_check:
            composite_rejection = get_composite_rejection_response(numbers_to_check)
            if composite_rejection:
                # Un ou plusieurs composes detectes - retourner la preuve par l'absurde
                return {
                    "response": composite_rejection["response"],
                    "computation": None,
                    "computation_type": "composite_rejection",
                    "session_id": session_id,
                    "is_composite_error": True,
                    "composites": composite_rejection.get("composites", [])
                }
    
    computation_context = ""
    if detection["needs_computation"]:
        computation_context = run_computation(detection)

    system_prompt = SPECTRAL_SYSTEM_PROMPT
    if computation_context:
        system_prompt += f"\n\n=== RESULTATS DU MOTEUR SPECTRAL PYTHON (calculs verifies) ===\n{computation_context}\n=== FIN CALCULS ==="

    try:
        chat = LlmChat(
            api_key=os.environ.get("EMERGENT_LLM_KEY"),
            session_id=f"gabriel-{session_id}",
            system_message=system_prompt
        ).with_model("anthropic", "claude-sonnet-4-5-20250929")

        user_message = UserMessage(text=question)
        response = await chat.send_message(user_message)

        return {
            "response": response,
            "computation": computation_context if computation_context else None,
            "computation_type": detection["type"] if detection["needs_computation"] else None,
            "session_id": session_id,
        }
    except Exception as e:
        logger.error(f"Gabriel LLM error: {e}")
        fallback = f"Erreur LLM. Voici les calculs spectraux bruts:\n\n{computation_context}" if computation_context else f"Erreur: {str(e)}"
        return {
            "response": fallback,
            "computation": computation_context,
            "computation_type": detection.get("type"),
            "session_id": session_id,
            "error": str(e)
        }
