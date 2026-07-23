import React, { useState, useEffect } from 'react';

const LicencePage = ({ onBack }) => {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetch(`${API_URL}/api/pages/licence`)
      .then(res => res.json())
      .then(data => {
        setContent(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [API_URL]);

  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: '#ffd700' }}>
        Chargement...
      </div>
    );
  }

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#1a1a2e',
      padding: '20px'
    }}>
      <div style={{
        maxWidth: '800px',
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

        <h1 style={{ color: '#ffd700', marginBottom: '20px' }}>
          📜 {content?.title || 'Licence d\'utilisation'}
        </h1>

        <pre style={{
          color: '#e2e8f0',
          whiteSpace: 'pre-wrap',
          fontFamily: 'inherit',
          lineHeight: '1.8',
          fontSize: '14px'
        }}>
          {content?.content}
        </pre>
      </div>
    </div>
  );
};

export default LicencePage;
