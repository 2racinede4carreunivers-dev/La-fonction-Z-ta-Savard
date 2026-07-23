import React, { useState, useEffect } from 'react';

const GuidePage = ({ onBack }) => {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetch(`${API_URL}/api/pages/guide`)
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
        maxWidth: '900px',
        margin: '0 auto'
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

        <h1 style={{ color: '#ffd700', marginBottom: '30px', textAlign: 'center' }}>
          📖 {content?.title || 'Guide d\'utilisation'}
        </h1>

        {/* Sections */}
        {content?.sections?.map((section, index) => (
          <div key={index} style={{
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            borderRadius: '15px',
            padding: '25px',
            marginBottom: '20px',
            border: '1px solid rgba(255, 215, 0, 0.2)'
          }}>
            <h2 style={{ 
              color: '#ffd700', 
              marginTop: 0,
              marginBottom: '15px',
              fontSize: '20px'
            }}>
              {section.title}
            </h2>
            <p style={{
              color: '#e2e8f0',
              lineHeight: '1.8',
              whiteSpace: 'pre-wrap',
              margin: 0
            }}>
              {section.content}
            </p>
          </div>
        ))}

        {/* Important Notice */}
        {content?.important_notice && (
          <div style={{
            backgroundColor: 'rgba(245, 101, 101, 0.1)',
            borderRadius: '15px',
            padding: '25px',
            border: '1px solid rgba(245, 101, 101, 0.3)',
            marginTop: '30px'
          }}>
            <h2 style={{ 
              color: '#fc8181', 
              marginTop: 0,
              marginBottom: '15px',
              fontSize: '18px'
            }}>
              ⚠️ Avertissement Important
            </h2>
            <p style={{
              color: '#e2e8f0',
              lineHeight: '1.8',
              whiteSpace: 'pre-wrap',
              margin: 0
            }}>
              {content.important_notice}
            </p>
          </div>
        )}

        {/* Footer */}
        <div style={{
          textAlign: 'center',
          marginTop: '40px',
          padding: '20px',
          color: '#718096',
          fontSize: '14px'
        }}>
          © Philippe Thomas Savard & E1 (Emergent Labs)<br />
          www.universestaucarre.com
        </div>
      </div>
    </div>
  );
};

export default GuidePage;
