import React, { useEffect, useRef } from 'react';
import './DocumentProtection.css';
import domManager from '../utils/DOMManager';

/**
 * Composant de protection des documents
 * Empêche copier-coller, clic droit, sélection de texte
 * Ajoute watermark et copyright
 */
const DocumentProtection = ({ children, showWatermark = true, documentTitle = "" }) => {
  const protectedRef = useRef(null);
  const watermarkRef = useRef(null);

  useEffect(() => {
    const protectedElement = protectedRef.current;
    if (!protectedElement) return;

    // Désactiver le clic droit (contextmenu)
    const handleContextMenu = (e) => {
      e.preventDefault();
      showCopyrightAlert("Le clic droit est désactivé pour protéger le contenu.");
      return false;
    };

    // Désactiver les raccourcis clavier de copie
    const handleKeyDown = (e) => {
      // Ctrl+C, Ctrl+S, Ctrl+P, Ctrl+A, F12 (DevTools)
      if (
        (e.ctrlKey || e.metaKey) && 
        (e.key === 'c' || e.key === 'C' || 
         e.key === 's' || e.key === 'S' || 
         e.key === 'p' || e.key === 'P' ||
         e.key === 'a' || e.key === 'A' ||
         e.key === 'u' || e.key === 'U')
      ) {
        e.preventDefault();
        showCopyrightAlert("La copie et l'enregistrement sont désactivés pour protéger le contenu.");
        return false;
      }
      
      // F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C (DevTools)
      if (
        e.key === 'F12' ||
        ((e.ctrlKey || e.metaKey) && e.shiftKey && 
         (e.key === 'I' || e.key === 'i' || 
          e.key === 'J' || e.key === 'j' ||
          e.key === 'C' || e.key === 'c'))
      ) {
        e.preventDefault();
        return false;
      }
    };

    // Désactiver la sélection par glisser-déposer
    const handleDragStart = (e) => {
      e.preventDefault();
      return false;
    };

    // Détecter les tentatives de copie
    const handleCopy = (e) => {
      e.preventDefault();
      e.clipboardData.setData('text/plain', 
        '© Tous droits réservés - Philippe Thomas Savard\nCe contenu est protégé par le droit d\'auteur.\nLa reproduction non autorisée est strictement interdite.\n\nThéorie: L\'univers est au carré\nSource: Application officielle'
      );
      showCopyrightAlert("Contenu protégé par copyright ©");
      return false;
    };

    // Désactiver la sélection
    const handleSelectStart = (e) => {
      // Permettre la sélection dans les champs de formulaire
      if (e.target.tagName === 'INPUT' || 
          e.target.tagName === 'TEXTAREA' ||
          e.target.contentEditable === 'true') {
        return true;
      }
      e.preventDefault();
      return false;
    };

    // Ajouter les écouteurs d'événements
    protectedElement.addEventListener('contextmenu', handleContextMenu);
    protectedElement.addEventListener('keydown', handleKeyDown);
    protectedElement.addEventListener('dragstart', handleDragStart);
    protectedElement.addEventListener('copy', handleCopy);
    protectedElement.addEventListener('selectstart', handleSelectStart);

    // Empêcher le print screen (limitation)
    const handleBeforePrint = () => {
      showCopyrightAlert("L'impression est désactivée pour protéger le contenu.");
    };
    window.addEventListener('beforeprint', handleBeforePrint);

    // Nettoyage
    return () => {
      if (protectedElement) {
        protectedElement.removeEventListener('contextmenu', handleContextMenu);
        protectedElement.removeEventListener('keydown', handleKeyDown);
        protectedElement.removeEventListener('dragstart', handleDragStart);
        protectedElement.removeEventListener('copy', handleCopy);
        protectedElement.removeEventListener('selectstart', handleSelectStart);
      }
      window.removeEventListener('beforeprint', handleBeforePrint);
      
      // Nettoyer tous les toasts copyright existants avec DOMManager
      const toasts = document.querySelectorAll('.copyright-toast');
      toasts.forEach(toast => {
        // Utiliser DOMManager pour supprimer de manière sécurisée
        domManager.removeChild(document.body, toast);
      });
    };
  }, []);

  // Afficher une alerte de copyright
  const showCopyrightAlert = (message) => {
    // Créer un toast notification au lieu d'une alerte bloquante
    const toast = document.createElement('div');
    const toastId = `toast-${Date.now()}-${Math.random()}`;
    toast.className = 'copyright-toast';
    toast.innerHTML = `
      <div class="copyright-toast-content">
        <strong>⚠️ Protection Copyright</strong>
        <p>${message}</p>
        <small>© Philippe Thomas Savard - Tous droits réservés</small>
      </div>
    `;
    
    // Utiliser le DOMManager pour ajouter l'élément
    domManager.appendChild(document.body, toast, toastId);
    
    // Utiliser le DOMManager pour les timers
    domManager.setTimeout(() => {
      toast.classList.add('show');
    }, 10, `${toastId}-show`);

    domManager.setTimeout(() => {
      toast.classList.remove('show');
      
      domManager.setTimeout(() => {
        // Utiliser le DOMManager pour supprimer l'élément
        domManager.removeChild(document.body, toast);
      }, 300, `${toastId}-remove`);
    }, 3000, `${toastId}-hide`);
  };

  return (
    <div className="document-protection-wrapper" ref={protectedRef}>
      {/* Watermark */}
      {showWatermark && (
        <div className="document-watermark" ref={watermarkRef}>
          <div className="watermark-content">
            <div className="watermark-text">© Philippe Thomas Savard</div>
            <div className="watermark-text">L'univers est au carré</div>
            <div className="watermark-text">Tous droits réservés</div>
            {documentTitle && (
              <div className="watermark-text">{documentTitle}</div>
            )}
          </div>
        </div>
      )}

      {/* Copyright Notice en haut */}
      <div className="copyright-notice top">
        <span className="copyright-icon">©</span>
        <span className="copyright-text">
          <strong>Philippe Thomas Savard</strong> - Tous droits réservés - 
          La reproduction, même partielle, est strictement interdite sans autorisation
        </span>
      </div>

      {/* Contenu protégé */}
      <div className="protected-content">
        {children}
      </div>

      {/* Copyright Notice en bas */}
      <div className="copyright-notice bottom">
        <div className="copyright-full">
          <h4>© Copyright et Propriété Intellectuelle</h4>
          <p>
            <strong>Tous droits réservés - Philippe Thomas Savard</strong>
          </p>
          <p>
            La théorie "L'univers est au carré" et tous les documents associés sont protégés 
            par le droit d'auteur. Toute reproduction, distribution, modification ou utilisation 
            non autorisée de ce contenu, en tout ou en partie, est strictement interdite et 
            constitue une violation des droits de propriété intellectuelle.
          </p>
          <p>
            <strong>Protections actives:</strong> Copier-coller désactivé • Clic droit désactivé • 
            Téléchargement empêché • Sélection de texte limitée • Watermark de protection
          </p>
          <p className="copyright-warning">
            ⚠️ Toute violation sera poursuivie conformément à la loi.
          </p>
        </div>
      </div>

      {/* Overlay de protection invisible (rend plus difficile l'inspection) */}
      <div className="protection-overlay"></div>
    </div>
  );
};

export default DocumentProtection;
