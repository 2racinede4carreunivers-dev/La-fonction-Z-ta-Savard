#!/usr/bin/env python3
"""
Système de synchronisation GitHub pour "L'univers est au carré"
Dépôt: https://github.com/2racinede4carreunivers-dev/L-univers-est-au-carre.git

Ce module gère:
- La synchronisation périodique avec le dépôt GitHub
- L'extraction du contenu des fichiers (PDF, TEX, THY, MD)
- La mise à jour de la base de connaissances de l'IA
"""

import os
import subprocess
import hashlib
from datetime import datetime
import PyPDF2

GITHUB_REPO_URL = "https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git"
LOCAL_REPO_PATH = "/app/data/Theorie-mathematique-philippe-thomas-savard-2026"
SYNC_LOG_PATH = "/app/data/github_sync_log.txt"

def log_sync(message):
    """Enregistre un message de synchronisation"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    print(log_entry.strip())
    try:
        with open(SYNC_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except:
        pass

def get_repo_hash():
    """Obtient le hash du dernier commit"""
    try:
        result = subprocess.run(
            ["git", "-C", LOCAL_REPO_PATH, "rev-parse", "HEAD"],
            capture_output=True, text=True
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

def sync_repository():
    """Synchronise le dépôt GitHub local"""
    old_hash = get_repo_hash()
    
    try:
        if os.path.exists(LOCAL_REPO_PATH):
            # Pull les dernières modifications
            result = subprocess.run(
                ["git", "-C", LOCAL_REPO_PATH, "pull", "--ff-only"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                # Si pull échoue, re-cloner
                subprocess.run(["rm", "-rf", LOCAL_REPO_PATH])
                subprocess.run(["git", "clone", "--depth", "1", GITHUB_REPO_URL, LOCAL_REPO_PATH])
                log_sync("Dépôt re-cloné (pull échoué)")
            else:
                log_sync("Dépôt mis à jour (git pull)")
        else:
            # Cloner le dépôt
            subprocess.run(["git", "clone", "--depth", "1", GITHUB_REPO_URL, LOCAL_REPO_PATH])
            log_sync("Dépôt cloné pour la première fois")
        
        new_hash = get_repo_hash()
        
        if old_hash != new_hash:
            log_sync(f"Nouveau contenu détecté: {old_hash[:8] if old_hash else 'N/A'} -> {new_hash[:8] if new_hash else 'N/A'}")
            return True
        else:
            log_sync("Aucun changement détecté")
            return False
            
    except Exception as e:
        log_sync(f"Erreur sync: {str(e)}")
        return False

def extract_pdf_text(pdf_path, max_chars=80000):
    """Extrait le texte d'un PDF"""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            if len(text) > max_chars:
                text = text[:max_chars] + "\n\n[... Document tronqué ...]"
            
            return text
    except Exception as e:
        return f"[Erreur extraction PDF: {str(e)}]"

def load_all_content():
    """Charge tout le contenu du dépôt pour l'IA - Version optimisée"""
    content = ""
    
    # En-tête
    content += """
================================================================================
BASE DE CONNAISSANCES EXCLUSIVE - "L'UNIVERS EST AU CARRÉ"
Dépôt GitHub: https://github.com/2racinede4carreunivers-dev/L-univers-est-au-carre
Auteur: Philippe Thomas Savard
Certification: SLSA Build Level 3 - Isabelle2025-2 - LaTeX
================================================================================
"""
    
    repo_path = LOCAL_REPO_PATH
    
    # 1. Charger le README principal (PRIORITÉ HAUTE)
    readme_path = os.path.join(repo_path, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content += f"\n\n{'='*80}\n=== README PRINCIPAL ===\n{'='*80}\n"
            content += f.read()
    
    # 2. Charger tous les fichiers .thy (Isabelle/HOL) - PRIORITÉ HAUTE
    hol_dir = os.path.join(repo_path, "src/hol")
    if os.path.exists(hol_dir):
        content += f"\n\n{'='*80}\n=== PREUVES FORMELLES ISABELLE/HOL (Certifiées SLSA) ===\n{'='*80}\n"
        for thy_file in sorted(os.listdir(hol_dir)):
            if thy_file.endswith('.thy'):
                thy_path = os.path.join(hol_dir, thy_file)
                with open(thy_path, 'r', encoding='utf-8') as f:
                    content += f"\n\n--- {thy_file} ---\n"
                    content += f.read()
    
    # 3. Charger les guides de la documentation (PRIORITÉ MOYENNE)
    docs_dir = os.path.join(repo_path, "docs")
    if os.path.exists(docs_dir):
        content += f"\n\n{'='*80}\n=== DOCUMENTATION ET GUIDES ===\n{'='*80}\n"
        for root, dirs, files in os.walk(docs_dir):
            for md_file in sorted(files):
                if md_file.endswith('.md'):
                    md_path = os.path.join(root, md_file)
                    with open(md_path, 'r', encoding='utf-8') as f:
                        rel_path = os.path.relpath(md_path, docs_dir)
                        content += f"\n\n--- {rel_path} ---\n"
                        file_content = f.read()
                        # Limiter chaque fichier md à 30000 caractères
                        if len(file_content) > 30000:
                            file_content = file_content[:30000] + "\n[... Document tronqué ...]"
                        content += file_content
    
    # 4. Charger les PDFs (extraits texte) - LIMITÉS pour éviter le dépassement
    pdf_dir = os.path.join(repo_path, "src/pdf")
    if os.path.exists(pdf_dir):
        content += f"\n\n{'='*80}\n=== DOCUMENTS PDF (Compilés et Certifiés) - Résumés ===\n{'='*80}\n"
        for pdf_file in sorted(os.listdir(pdf_dir)):
            if pdf_file.endswith('.pdf'):
                pdf_path = os.path.join(pdf_dir, pdf_file)
                # Limiter l'extraction des PDFs à 25000 caractères chacun
                text = extract_pdf_text(pdf_path, max_chars=25000)
                content += f"\n\n--- {pdf_file} ---\n"
                content += text
    
    # 5. NE PAS charger les fichiers .tex complets (redondants avec les PDFs)
    # Les .tex sont la source, les PDFs sont la version compilée
    
    log_sync(f"Contenu chargé (optimisé): {len(content)} caractères")
    return content

def get_last_sync_info():
    """Retourne les informations de la dernière synchronisation"""
    try:
        if os.path.exists(SYNC_LOG_PATH):
            with open(SYNC_LOG_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    return lines[-1].strip()
        return "Aucune synchronisation enregistrée"
    except:
        return "Erreur lecture log"

if __name__ == "__main__":
    print("=== Test du système de synchronisation ===")
    sync_repository()
    content = load_all_content()
    print(f"Contenu total: {len(content)} caractères")
