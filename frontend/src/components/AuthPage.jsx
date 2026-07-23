import React, { useState } from 'react';

const AuthPage = ({ onAuthSuccess }) => {
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [step, setStep] = useState('email'); // 'email' or 'code'
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [expiresIn, setExpiresIn] = useState(null);

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  const requestCode = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await fetch(`${API_URL}/api/auth/request-code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      const data = await response.json();

      if (data.success) {
        setStep('code');
        setMessage(data.message);
        setExpiresIn(data.expires_in_minutes);
      } else {
        setError(data.message || 'Erreur lors de l&apos;envoi du code');
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const verifyCode = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/api/auth/verify-code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, code })
      });

      const data = await response.json();

      if (data.success) {
        // Store session
        localStorage.setItem('sessionToken', data.session_token);
        localStorage.setItem('userEmail', data.email);
        localStorage.setItem('isAdmin', data.is_admin);
        onAuthSuccess(data);
      } else {
        setError(data.message || 'Code incorrect');
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setStep('email');
    setCode('');
    setMessage('');
    setError('');
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
      padding: '20px'
    }}>
      <div style={{
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        backdropFilter: 'blur(10px)',
        borderRadius: '20px',
        padding: '40px',
        maxWidth: '450px',
        width: '100%',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
        border: '1px solid rgba(255, 215, 0, 0.2)'
      }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <h1 style={{
            color: '#ffd700',
            fontSize: '28px',
            fontWeight: 'bold',
            marginBottom: '8px',
            textShadow: '0 0 20px rgba(255, 215, 0, 0.3)'
          }}>
            L'Univers est au Carré
          </h1>
          <p style={{ color: '#a0aec0', fontSize: '14px' }}>
            Géométrie du Spectre des Nombres Premiers
          </p>
        </div>

        {/* Form */}
        {step === 'email' ? (
          <form onSubmit={requestCode}>
            <div style={{ marginBottom: '20px' }}>
              <label style={{
                display: 'block',
                color: '#e2e8f0',
                marginBottom: '8px',
                fontSize: '14px'
              }}>
                Adresse email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="votre@email.com"
                required
                data-testid="email-input"
                style={{
                  width: '100%',
                  padding: '14px 16px',
                  borderRadius: '10px',
                  border: '1px solid rgba(255, 215, 0, 0.3)',
                  backgroundColor: 'rgba(0, 0, 0, 0.3)',
                  color: '#fff',
                  fontSize: '16px',
                  outline: 'none',
                  transition: 'border-color 0.3s',
                  boxSizing: 'border-box'
                }}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              data-testid="request-code-btn"
              style={{
                width: '100%',
                padding: '14px',
                borderRadius: '10px',
                border: 'none',
                backgroundColor: loading ? '#4a5568' : '#ffd700',
                color: '#1a1a2e',
                fontSize: '16px',
                fontWeight: 'bold',
                cursor: loading ? 'not-allowed' : 'pointer',
                transition: 'all 0.3s'
              }}
            >
              {loading ? 'Envoi en cours...' : 'Recevoir le code de vérification'}
            </button>
          </form>
        ) : (
          <form onSubmit={verifyCode}>
            <div style={{
              backgroundColor: 'rgba(255, 215, 0, 0.1)',
              borderRadius: '10px',
              padding: '15px',
              marginBottom: '20px',
              border: '1px solid rgba(255, 215, 0, 0.2)'
            }}>
              <p style={{ color: '#ffd700', margin: 0, fontSize: '14px' }}>
                📧 Code envoyé à <strong>{email}</strong>
              </p>
              {expiresIn && (
                <p style={{ color: '#a0aec0', margin: '5px 0 0 0', fontSize: '12px' }}>
                  Valide pendant {expiresIn} minutes
                </p>
              )}
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label style={{
                display: 'block',
                color: '#e2e8f0',
                marginBottom: '8px',
                fontSize: '14px'
              }}>
                Code de vérification (6 chiffres)
              </label>
              <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                placeholder="000000"
                required
                maxLength={6}
                data-testid="code-input"
                style={{
                  width: '100%',
                  padding: '14px 16px',
                  borderRadius: '10px',
                  border: '1px solid rgba(255, 215, 0, 0.3)',
                  backgroundColor: 'rgba(0, 0, 0, 0.3)',
                  color: '#fff',
                  fontSize: '24px',
                  fontWeight: 'bold',
                  textAlign: 'center',
                  letterSpacing: '8px',
                  outline: 'none',
                  boxSizing: 'border-box'
                }}
              />
            </div>

            <button
              type="submit"
              disabled={loading || code.length !== 6}
              data-testid="verify-code-btn"
              style={{
                width: '100%',
                padding: '14px',
                borderRadius: '10px',
                border: 'none',
                backgroundColor: (loading || code.length !== 6) ? '#4a5568' : '#ffd700',
                color: '#1a1a2e',
                fontSize: '16px',
                fontWeight: 'bold',
                cursor: (loading || code.length !== 6) ? 'not-allowed' : 'pointer',
                transition: 'all 0.3s',
                marginBottom: '10px'
              }}
            >
              {loading ? 'Vérification...' : 'Vérifier le code'}
            </button>

            <button
              type="button"
              onClick={resetForm}
              style={{
                width: '100%',
                padding: '12px',
                borderRadius: '10px',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                backgroundColor: 'transparent',
                color: '#a0aec0',
                fontSize: '14px',
                cursor: 'pointer'
              }}
            >
              ← Changer d&apos;adresse email
            </button>
          </form>
        )}

        {/* Messages */}
        {message && (
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

        {/* Footer */}
        <div style={{
          marginTop: '30px',
          paddingTop: '20px',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
          textAlign: 'center'
        }}>
          <p style={{ color: '#718096', fontSize: '12px', margin: 0 }}>
            © Philippe Thomas Savard & E1 (Emergent Labs)
          </p>
          <p style={{ color: '#4a5568', fontSize: '11px', marginTop: '5px' }}>
            www.universestaucarre.com
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
