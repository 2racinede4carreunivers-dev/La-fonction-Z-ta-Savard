/**
 * Gestionnaire centralisé pour les manipulations DOM
 * Évite les conflits entre composants et les erreurs removeChild
 */

class DOMManager {
  constructor() {
    // Ensemble pour suivre les éléments créés
    this.trackedElements = new WeakSet();
    // Map pour suivre les timers actifs
    this.activeTimers = new Map();
  }

  /**
   * Ajoute un élément au DOM de manière sécurisée
   */
  appendChild(parent, element, elementId = null) {
    if (!parent || !element) return false;
    
    try {
      parent.appendChild(element);
      this.trackedElements.add(element);
      
      if (elementId) {
        // Stocker la référence pour cleanup ultérieur
        element.dataset.domManagerId = elementId;
      }
      
      return true;
    } catch (error) {
      console.warn('DOMManager: Erreur appendChild', error);
      return false;
    }
  }

  /**
   * Supprime un élément du DOM de manière sécurisée
   */
  removeChild(parent, element) {
    if (!parent || !element) return false;
    
    try {
      // Vérifier que l'élément est bien un enfant du parent
      if (element.parentNode === parent && this.trackedElements.has(element)) {
        parent.removeChild(element);
        this.trackedElements.delete(element);
        
        // Nettoyer les timers associés
        if (element.dataset.domManagerId) {
          this.clearTimers(element.dataset.domManagerId);
        }
        
        return true;
      }
      return false;
    } catch (error) {
      console.warn('DOMManager: Erreur removeChild', error);
      return false;
    }
  }

  /**
   * Crée un timer avec suivi automatique
   */
  setTimeout(callback, delay, timerId) {
    // Annuler le timer existant s'il y en a un
    if (timerId && this.activeTimers.has(timerId)) {
      clearTimeout(this.activeTimers.get(timerId));
    }

    const timer = setTimeout(() => {
      callback();
      if (timerId) {
        this.activeTimers.delete(timerId);
      }
    }, delay);

    if (timerId) {
      this.activeTimers.set(timerId, timer);
    }

    return timer;
  }

  /**
   * Annule un timer suivi
   */
  clearTimeout(timer, timerId = null) {
    if (timer) {
      clearTimeout(timer);
    }
    if (timerId && this.activeTimers.has(timerId)) {
      clearTimeout(this.activeTimers.get(timerId));
      this.activeTimers.delete(timerId);
    }
  }

  /**
   * Annule tous les timers associés à un ID
   */
  clearTimers(elementId) {
    if (!elementId) return;
    
    // Chercher tous les timers avec cet ID
    for (const [timerId, timer] of this.activeTimers.entries()) {
      if (timerId.startsWith(elementId)) {
        clearTimeout(timer);
        this.activeTimers.delete(timerId);
      }
    }
  }

  /**
   * Nettoie tous les éléments et timers
   */
  cleanup() {
    // Annuler tous les timers actifs
    for (const [timerId, timer] of this.activeTimers.entries()) {
      clearTimeout(timer);
    }
    this.activeTimers.clear();
    
    // Note: On ne peut pas nettoyer directement les éléments du WeakSet
    // mais ils seront garbage collectés automatiquement
  }
}

// Instance singleton
const domManager = new DOMManager();

export default domManager;
