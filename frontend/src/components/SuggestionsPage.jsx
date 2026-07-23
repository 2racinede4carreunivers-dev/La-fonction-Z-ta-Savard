import React, { useState } from 'react';

const SuggestionsPage = ({ onBack, sessionToken }) => {
  const [suggestion, setSuggestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const API_URL = process.env.REACT_APP_BACKEND_URL;
  const maxLength = 350;
  const remaining = maxLength - suggestion.length;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (suggestion.trim().length < 10) {
      setError('La suggestion doit contenir au moins 10 caractères.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/api/suggestions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Session-Token': sessionToken
        },
        body: JSON.stringify({ suggestion: suggestion.trim() })
      });

      const data = await response.json();

      if (data.success) {
        setMessage(data.message);
        setSubmitted(true);
        setSuggestion('');
      } else {
        setError(data.message || data.detail || 'Erreur lors de l\'envoi');
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#1a1a2e',
      padding: '20px'
    }}>
      <div style={{
        maxWidth: '700px',
        margin: '0 auto',
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        borderRadius: '15px',
        padding: '30px',
        border: '1px solid rgba(255, 215, 0, 0.2)'
      }}>
        <button
          onClick={onBack}
          style={{
            background: 'transparent',
            border: '1px solid rgba(255, 215, 0, 0.3)',
            color: '#ffd700',
            padding: '8px 16px',
            borderRadius: '8px',
            cursor: 'pointer',
            marginBottom: '20px'
          }}
        >
          ← Retour
        </button>

        <h1 style={{ color: '#ffd700', marginBottom: '10px' }}>
          💡 Vos Suggestions
        </h1>
        <p style={{ color: '#a0aec0', marginBottom: '30px' }}>
          Partagez vos idées pour améliorer l'application (maximum 350 caractères)
        </p>

        {submitted ? (
          <div style={{
            textAlign: 'center',
            padding: '40px 20px'
          }}>
            <div style={{
              fontSize: '60px',
              marginBottom: '20px'
            }}>
              ✅
            </div>
            <h2 style={{ color: '#68d391', marginBottom: '15px' }}>
              Merci pour votre contribution !
            </h2>
            <p style={{ color: '#a0aec0', marginBottom: '30px' }}>
              Votre suggestion sera examinée par l'administrateur.
            </p>
            <button
              onClick={() => setSubmitted(false)}
              style={{
                padding: '12px 24px',
                borderRadius: '8px',
                border: 'none',
                backgroundColor: '#ffd700',
                color: '#1a1a2e',
                fontWeight: 'bold',
                cursor: 'pointer'
              }}
            >
              Soumettre une autre suggestion
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '15px' }}>
              <textarea
                value={suggestion}
                onChange={(e) => setSuggestion(e.target.value.slice(0, maxLength))}
                placeholder="Décrivez votre suggestion, idée d'amélioration ou commentaire..."
                rows={6}
                data-testid="suggestion-input"
                style={{
                  width: '100%',
                  padding: '15px',
                  borderRadius: '10px',
                  border: '1px solid rgba(255, 215, 0, 0.3)',
                  backgroundColor: 'rgba(0, 0, 0, 0.3)',
                  color: '#fff',
                  fontSize: '16px',
                  resize: 'vertical',
                  outline: 'none',
                  boxSizing: 'border-box'
                }}
              />
            </div>

            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '20px'
            }}>
              <span style={{
                color: remaining < 50 ? '#fc8181' : '#718096',
                fontSize: '14px'
              }}>
                {remaining} caractères restants
              </span>
              <span style={{ color: '#718096', fontSize: '14px' }}>
                Minimum 10 caractères
              </span>
            </div>

            <button
              type="submit"
              disabled={loading || suggestion.trim().length < 10}
              data-testid="submit-suggestion-btn"
              style={{
                width: '100%',
                padding: '14px',
                borderRadius: '10px',
                border: 'none',
                backgroundColor: (loading || suggestion.trim().length < 10) ? '#4a5568' : '#ffd700',
                color: '#1a1a2e',
                fontSize: '16px',
                fontWeight: 'bold',
                cursor: (loading || suggestion.trim().length < 10) ? 'not-allowed' : 'pointer',
                transition: 'all 0.3s'
              }}
            >
              {loading ? 'Envoi en cours...' : 'Envoyer ma suggestion'}
            </button>
          </form>
        )}

        {message && !submitted && (
          <div style={{
            marginTop: '20px',
            padding: '12px',
            borderRadius: '8px',
            backgroundColor: 'rgba(72, 187, 120, 0.2)',
            border: '1px solid rgba(72, 187, 120, 0.3)',
            color: '#68d391'
          }}>
            {message}
          </div>
        )}

        {error && (
          <div style={{
            marginTop: '20px',
            padding: '12px',
            borderRadius: '8px',
            backgroundColor: 'rgba(245, 101, 101, 0.2)',
            border: '1px solid rgba(245, 101, 101, 0.3)',
            color: '#fc8181'
          }}>
            {error}
          </div>
        )}

        {/* Info */}
        <div style={{
          marginTop: '30px',
          padding: '15px',
          backgroundColor: 'rgba(255, 215, 0, 0.1)',
          borderRadius: '10px',
          border: '1px solid rgba(255, 215, 0, 0.2)'
        }}>
          <p style={{ color: '#a0aec0', margin: 0, fontSize: '13px' }}>
            💡 Vos suggestions nous aident à améliorer l'application. 
            N'hésitez pas à partager vos idées, remarques ou fonctionnalités souhaitées.
          </p>
        </div>
      </div>
    </div>
  );
};

export default SuggestionsPage;
