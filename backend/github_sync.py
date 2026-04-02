#!/usr/bin/env python3
"""
Synchronisation GitHub pour "L'univers est au carre"
Depot: https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git

Charge les fichiers .thy, .tex et .md du depot dans le contexte IA.
Les .tex sont nettoyes des commandes LaTeX et des blocs HOL embarques
(deja couverts par les .thy officiels).
"""

import os
import re
import subprocess
from datetime import datetime

GITHUB_REPO_URL = "https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git"
LOCAL_REPO_PATH = "/app/data/Theorie-mathematique-philippe-thomas-savard-2026"
SYNC_LOG_PATH = "/app/data/github_sync_log.txt"

# Limites par type de fichier
MAX_TEX_CHARS_PER_FILE = 18000
MAX_MD_CHARS_PER_FILE = 12000
MAX_TOTAL_CHARS = 250000


def log_sync(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(log_entry.strip())
    try:
        with open(SYNC_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception:
        pass


def get_repo_hash():
    try:
        result = subprocess.run(
            ["git", "-C", LOCAL_REPO_PATH, "rev-parse", "HEAD"],
            capture_output=True, text=True
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def sync_repository():
    old_hash = get_repo_hash()
    try:
        if os.path.exists(LOCAL_REPO_PATH):
            result = subprocess.run(
                ["git", "-C", LOCAL_REPO_PATH, "pull", "--ff-only"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                subprocess.run(["rm", "-rf", LOCAL_REPO_PATH])
                subprocess.run(["git", "clone", "--depth", "1", GITHUB_REPO_URL, LOCAL_REPO_PATH])
                log_sync("Depot re-clone (pull echoue)")
            else:
                log_sync("Depot mis a jour (git pull)")
        else:
            subprocess.run(["git", "clone", "--depth", "1", GITHUB_REPO_URL, LOCAL_REPO_PATH])
            log_sync("Depot clone pour la premiere fois")

        new_hash = get_repo_hash()
        if old_hash != new_hash:
            log_sync(f"Nouveau contenu: {old_hash[:8] if old_hash else 'N/A'} -> {new_hash[:8] if new_hash else 'N/A'}")
            return True
        else:
            log_sync("Aucun changement detecte")
            return False
    except Exception as e:
        log_sync(f"Erreur sync: {str(e)}")
        return False


def strip_latex(text):
    """Extrait le texte lisible d'un fichier .tex en retirant les commandes LaTeX
    et les blocs de code HOL embarques (deja disponibles via les .thy officiels)."""

    # Retirer tout avant \begin{document}
    doc_match = re.search(r'\\begin\{document\}', text)
    if doc_match:
        text = text[doc_match.end():]

    # Retirer \end{document}
    text = re.sub(r'\\end\{document\}', '', text)

    # Retirer les blocs holcode/lstlisting complets (code .thy embarque)
    text = re.sub(
        r'\\begin\{holcode\}.*?\\end\{holcode\}',
        '\n[Code HOL omis - voir fichiers .thy officiels]\n',
        text, flags=re.DOTALL
    )
    text = re.sub(
        r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}',
        '\n[Code omis]\n',
        text, flags=re.DOTALL
    )
    # Retirer les blocs minted
    text = re.sub(
        r'\\begin\{minted\}(\[[^\]]*\])?\{[^}]*\}.*?\\end\{minted\}',
        '\n[Code HOL omis - voir fichiers .thy officiels]\n',
        text, flags=re.DOTALL
    )
    # Retirer les blocs verbatim (licence Apache, etc.)
    text = re.sub(
        r'\\begin\{verbatim\}.*?\\end\{verbatim\}',
        '\n[Bloc verbatim omis]\n',
        text, flags=re.DOTALL
    )

    # Convertir les titres LaTeX en texte lisible
    for cmd in ['title', 'chapter', 'section', 'subsection', 'subsubsection']:
        text = re.sub(rf'\\{cmd}\*?\{{([^}}]*)\}}', rf'\n=== \1 ===\n', text)

    # Convertir textbf, textit, emph
    text = re.sub(r'\\textbf\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textcolor\{[^}]*\}\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\underline\{([^}]*)\}', r'\1', text)

    # Retirer les environnements de mise en page mais garder le contenu
    for env in ['center', 'minipage', 'titlepage', 'quote', 'itemize',
                'enumerate', 'description', 'abstract', 'figure', 'table',
                'tabular', 'equation', 'align', 'gather']:
        text = re.sub(rf'\\begin\{{{env}\}}(\[.*?\])?', '', text)
        text = re.sub(rf'\\end\{{{env}\}}', '', text)

    # Convertir \item en tiret
    text = re.sub(r'\\item\s*', '- ', text)

    # Retirer les commandes LaTeX restantes simples
    text = re.sub(r'\\(clearpage|newpage|vfill|noindent|maketitle|tableofcontents|centering|raggedright|small|large|Large|LARGE|huge|Huge|normalsize|footnotesize|tiny|vspace\*?\{[^}]*\}|hspace\*?\{[^}]*\}|addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}|label\{[^}]*\}|ref\{[^}]*\}|cite\{[^}]*\}|pagenumbering\{[^}]*\}|setlength\{[^}]*\}\{[^}]*\}|setcounter\{[^}]*\}\{[^}]*\}|includegraphics(\[[^\]]*\])?\{[^}]*\}|usepackage(\[[^\]]*\])?\{[^}]*\}|geometry\{[^}]*\}|hypersetup\{[^}]*\})', '', text)

    # Retirer les commentaires LaTeX
    text = re.sub(r'%.*$', '', text, flags=re.MULTILINE)

    # Retirer les commandes LaTeX generiques restantes (\cmd{...} ou \cmd)
    text = re.sub(r'\\[a-zA-Z]+\*?(\{[^}]*\})*', '', text)

    # Nettoyer les accolades orphelines et caracteres speciaux LaTeX
    text = text.replace('{', '').replace('}', '')
    text = text.replace('\\\\', '\n')
    text = text.replace('\\', '')
    text = re.sub(r'~', ' ', text)
    text = re.sub(r'\$([^$]*)\$', r'\1', text)

    # Nettoyer les lignes vides multiples
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

    return text.strip()


def load_all_content():
    """Charge tout le contenu du depot pour l'IA avec deduplication .thy/.tex"""
    sections = []
    stats = {"thy": 0, "tex": 0, "md": 0, "thy_chars": 0, "tex_chars": 0, "md_chars": 0}
    repo = LOCAL_REPO_PATH

    # En-tete
    header = """
================================================================================
BASE DE CONNAISSANCES EXCLUSIVE - "L'UNIVERS EST AU CARRE"
Depot: https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026
Auteur: Philippe Thomas Savard
Certification: SLSA Build Level 3 - Isabelle2025-2 - LaTeX
================================================================================
INSTRUCTIONS: Ce contexte constitue la BASE EXCLUSIVE de connaissances.
Les fichiers .thy sont les preuves formelles OFFICIELLES en Isabelle/HOL.
Les fichiers .tex sont les documents theoriques (texte extrait, code HOL omis car identique aux .thy).
"""
    sections.append(header)

    # 1. Fichiers .thy (PRIORITE MAXIMALE - charges en entier)
    hol_dir = os.path.join(repo, "src/hol")
    if os.path.exists(hol_dir):
        thy_section = f"\n{'='*80}\n=== PREUVES FORMELLES ISABELLE/HOL (Certifiees SLSA) ===\n{'='*80}\n"
        for thy_file in sorted(os.listdir(hol_dir)):
            if thy_file.endswith('.thy'):
                thy_path = os.path.join(hol_dir, thy_file)
                try:
                    with open(thy_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    thy_section += f"\n--- {thy_file} ({len(content)} car.) ---\n"
                    thy_section += content + "\n"
                    stats["thy"] += 1
                    stats["thy_chars"] += len(content)
                except Exception as e:
                    thy_section += f"\n--- {thy_file} [Erreur: {e}] ---\n"
        sections.append(thy_section)

    # 2. Fichiers .tex (texte extrait, blocs HOL retires)
    tex_dir = os.path.join(repo, "src/tex")
    if os.path.exists(tex_dir):
        tex_section = f"\n{'='*80}\n=== DOCUMENTS THEORIQUES (.tex - texte extrait) ===\n{'='*80}\n"
        tex_section += "(Les blocs de code HOL sont omis ci-dessous car identiques aux .thy officiels ci-dessus)\n"
        for tex_file in sorted(os.listdir(tex_dir)):
            if tex_file.endswith('.tex'):
                tex_path = os.path.join(tex_dir, tex_file)
                try:
                    with open(tex_path, 'r', encoding='utf-8') as f:
                        raw = f.read()
                    cleaned = strip_latex(raw)
                    if len(cleaned) > MAX_TEX_CHARS_PER_FILE:
                        cleaned = cleaned[:MAX_TEX_CHARS_PER_FILE] + "\n\n[... Document tronque ...]"
                    tex_section += f"\n--- {tex_file} ({len(cleaned)} car. apres nettoyage) ---\n"
                    tex_section += cleaned + "\n"
                    stats["tex"] += 1
                    stats["tex_chars"] += len(cleaned)
                except Exception as e:
                    tex_section += f"\n--- {tex_file} [Erreur: {e}] ---\n"
        sections.append(tex_section)

    # 3. Documentation Markdown
    docs_paths = [
        ("charge.md", os.path.join(repo, "charge.md")),
        ("CHANGELOG.md", os.path.join(repo, "CHANGELOG.md")),
    ]
    docs_dir = os.path.join(repo, "docs")
    if os.path.exists(docs_dir):
        for root, _, files in os.walk(docs_dir):
            for md_file in sorted(files):
                if md_file.endswith('.md'):
                    rel = os.path.relpath(os.path.join(root, md_file), repo)
                    docs_paths.append((rel, os.path.join(root, md_file)))

    md_section = f"\n{'='*80}\n=== DOCUMENTATION ET GUIDES ===\n{'='*80}\n"
    for label, md_path in docs_paths:
        if os.path.exists(md_path):
            try:
                with open(md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if not content.strip():
                    continue
                if len(content) > MAX_MD_CHARS_PER_FILE:
                    content = content[:MAX_MD_CHARS_PER_FILE] + "\n\n[... Document tronque ...]"
                md_section += f"\n--- {label} ({len(content)} car.) ---\n"
                md_section += content + "\n"
                stats["md"] += 1
                stats["md_chars"] += len(content)
            except Exception:
                pass
    sections.append(md_section)

    # Assembler et respecter la limite totale
    full_content = "".join(sections)
    if len(full_content) > MAX_TOTAL_CHARS:
        full_content = full_content[:MAX_TOTAL_CHARS] + "\n\n[... Contenu total tronque a 250k caracteres ...]"

    log_sync(
        f"Contenu charge: {stats['thy']} .thy ({stats['thy_chars']} car.) + "
        f"{stats['tex']} .tex ({stats['tex_chars']} car.) + "
        f"{stats['md']} .md ({stats['md_chars']} car.) = {len(full_content)} car. total"
    )
    return full_content


def get_last_sync_info():
    try:
        if os.path.exists(SYNC_LOG_PATH):
            with open(SYNC_LOG_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    return lines[-1].strip()
        return "Aucune synchronisation enregistree"
    except Exception:
        return "Erreur lecture log"


if __name__ == "__main__":
    print("=== Test du systeme de synchronisation ===")
    sync_repository()
    content = load_all_content()
    print(f"Contenu total: {len(content)} caracteres")
