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

=== METHODE SPECTRALE - FORMULES FONDAMENTALES ===
SOMME SUITE A POSITIVE = (3.25/2 * 2^n) - 2
SOMME SUITE B POSITIVE = (6.5/2  * 2^n) - 66
digamma_calcule(n, p) = SB(n) - 64 * p
prime_equation(n, p) = (SB(n) - digamma_calcule) / 64 = p

--- RAPPORTS SPECTRAUX ---
Rapport 1/2 : facteur = 64   (modele principal)
Rapport 1/3 : facteur = 729
Rapport 1/4 : facteur = 4096

--- REGLE FONDAMENTALE ---
Pour le RAPPORT 1/2 : n = position du nombre premier = quantite de termes dans A et B
  n=1->p=2, n=2->p=3, n=3->p=5, n=4->p=7, n=5->p=11, n=6->p=13, n=7->p=17, n=8->p=19,
  n=9->p=23, n=10->p=29, n=11->p=31, n=12->p=37, n=13->p=41, n=14->p=43, n=15->p=47,
  n=16->p=53, n=17->p=59, n=18->p=61, n=19->p=67, n=20->p=71, n=21->p=73, n=22->p=79,
  n=23->p=83, n=24->p=89, n=25->p=97, n=26->p=101

--- 4 CONFIGURATIONS DU RAPPORT SPECTRAL ---
1. Symetrique 1*1 : (SA(n1) - SA(n2)) / (SB(n1) - SB(n2)) = 1/k
2. Symetrique n*n : sum_A / sum_B = 1/k
3. Asymetrique ordonnee : len(B) = len(A)+1, decalage chronologique
4. Asymetrique chaotique : longueurs differentes, pas d'ordre impose

--- ECARTS ENTRE PREMIERS ---
gap = (A_next - (B_high - D_high) - D_low) / facteur

=== REGLES DE REPONSE ===
- TOUJOURS utiliser les calculs du moteur spectral Python quand fournis.
- TOUJOURS inclure la valeur du digamma calcule dans les reponses de reconstruction.
- TOUJOURS montrer chaque etape: SA(n), SB(n), digamma_calcule(n,p), equation du premier, verification.
- TOUJOURS distinguer "n = position" (rapport 1/2) vs "n != position" (autres rapports).
- TOUJOURS reconnaitre que la methode FONCTIONNE mathematiquement.
- Format de reconstruction: montrer SA, SB, digamma calcule = SB(n) - 64*p, puis (SB - digamma)/64 = p.
- Si donnee manquante : demander precision, JAMAIS inventer.
- Repondre en francais, avec rigueur mathematique.
- Tu as acces a une table de 1000 nombres premiers (2 a 7919).
"""


def detect_computation_request(question: str) -> dict:
    """Detecte si la question necessite un calcul spectral et extrait les parametres."""
    q = question.lower()
    result = {"needs_computation": False, "type": None, "params": {}}

    # Detection de nombres - gere "19ieme", "17e", "29" etc.
    prime_matches = re.findall(r'(\d+)', question)
    numbers = [int(x) for x in prime_matches if 1 < int(x) <= 8000]

    # Verification/analyse d'un premier
    if any(k in q for k in ["verifie", "analyse", "montre", "prouve", "calcul", "spectral", "digamma", "equation"]):
        if numbers:
            result["needs_computation"] = True
            result["type"] = "analyze_prime"
            result["params"]["primes"] = numbers

    # Rapport spectral
    if any(k in q for k in ["rapport", "ratio", "rsp", "1/2", "1/3", "1/4"]):
        result["needs_computation"] = True
        result["type"] = "spectral_ratio"
        if numbers:
            result["params"]["numbers"] = numbers

    # Ecart entre premiers
    if any(k in q for k in ["ecart", "gap", "distance", "entre"]):
        if len(numbers) >= 2:
            result["needs_computation"] = True
            result["type"] = "gap"
            result["params"]["primes"] = numbers[:2]

    # Plage de nombres premiers
    if any(k in q for k in ["plage", "range", "liste", "premiers de", "premiers entre"]):
        if len(numbers) >= 2:
            result["needs_computation"] = True
            result["type"] = "range"
            result["params"]["start"] = min(numbers[:2])
            result["params"]["end"] = max(numbers[:2])
        elif len(numbers) == 1:
            result["needs_computation"] = True
            result["type"] = "range"
            result["params"]["start"] = 2
            result["params"]["end"] = numbers[0]

    # Position d'un premier / reconstruction
    if any(k in q for k in ["position", "quel est le", "n-ieme", "nieme", "combien", "reconstruire", "reconstruis", "reconstruit", "reconstruction"]):
        if numbers:
            result["needs_computation"] = True
            result["type"] = "reconstruct"
            result["params"]["numbers"] = numbers

    # Fallback: si des nombres sont mentionnes dans un contexte math
    if not result["needs_computation"] and numbers and any(k in q for k in ["premier", "prime", "nombre"]):
        result["needs_computation"] = True
        result["type"] = "analyze_prime"
        result["params"]["primes"] = numbers[:5]

    return result


def run_computation(detection: dict) -> str:
    """Execute le calcul spectral et retourne un resume textuel."""
    from .spectral_engine import (
        analyze_prime, analyze_range, verify_prime_equation,
        compute_spectral_ratio, nth_prime, prime_position,
        is_known_prime, PRIMES, max_position
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
        for n in params.get("numbers", []):
            p = nth_prime(n)
            if p:
                v = verify_prime_equation(n, p, "1/2")
                lines.append(f"=== RECONSTRUCTION DU {n}e NOMBRE PREMIER ===")
                lines.append(f"  Position: n = {n}")
                lines.append(f"  Premier reconstruit: p = {p}")
                lines.append(f"")
                lines.append(f"  Suite A positive: SA({n}) = (13/8) * 2^{n} - 2 = {v['SA']}")
                lines.append(f"  Suite B positive: SB({n}) = (13/4) * 2^{n} - 66 = {v['SB']}")
                lines.append(f"")
                lines.append(f"  Digamma calcule: digamma({n}, {p}) = SB({n}) - 64 * {p} = {v['SB']} - {64 * p} = {v['digamma_calc']}")
                lines.append(f"")
                lines.append(f"  Equation du premier:")
                lines.append(f"    prime_equation = (SB({n}) - digamma_calcule) / 64")
                lines.append(f"                   = ({v['SB']} - {v['digamma_calc']}) / 64")
                lines.append(f"                   = {v['SB'] - v['digamma_calc']} / 64")
                lines.append(f"                   = {v['reconstructed_p']}")
                lines.append(f"")
                lines.append(f"  Equation valide: {v['equation_holds']}")
                lines.append(f"  Le {n}e nombre premier est bien {p}")
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

    if not lines:
        return "(Aucun calcul spectral applicable pour ces parametres)"

    return "\n".join(lines)


async def gabriel_ask(question: str, session_id: str, conversation_history: list = None) -> dict:
    """Point d'entree principal de Gabriel: detecte les calculs necessaires,
    execute le moteur spectral, puis utilise le LLM pour formuler la reponse."""
    from emergentintegrations.llm.chat import LlmChat, UserMessage

    detection = detect_computation_request(question)
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
        ).with_model("anthropic", "claude-sonnet-4-20250514")

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
