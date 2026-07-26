import React, { useEffect, useRef, useState } from 'react';

/**
 * Page d'authentification Google OAuth pour L'Univers est au Carré
 * REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
 */
const AuthPage = ({ onAuthSuccess }) => {
  
  const handleGoogleLogin = () => {
    // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    const redirectUrl = window.location.origin + '/auth/callback';
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
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
        border: '1px solid rgba(255, 215, 0, 0.2)',
        textAlign: 'center'
      }}>
        {/* Header */}
        <div style={{ marginBottom: '40px' }}>
          <h1 style={{
            color: '#ffd700',
            fontSize: '32px',
            fontWeight: 'bold',
            marginBottom: '12px',
            textShadow: '0 0 20px rgba(255, 215, 0, 0.3)'
          }}>
            L'Univers est au Carré
          </h1>
          <p style={{ color: '#a0aec0', fontSize: '16px', marginBottom: '8px' }}>
            Géométrie du Spectre des Nombres Premiers
          </p>
          <p style={{ color: '#718096', fontSize: '14px' }}>
            par Philippe Thomas Savard
          </p>
        </div>

        {/* Divider */}
        <div style={{
          height: '1px',
          background: 'linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.3), transparent)',
          marginBottom: '40px'
        }} />

        {/* Login Section */}
        <div style={{ marginBottom: '30px' }}>
          <p style={{ color: '#e2e8f0', marginBottom: '20px', fontSize: '15px' }}>
            Connectez-vous pour accéder à l'application
          </p>
          
          <button
            onClick={handleGoogleLogin}
            data-testid="google-login-btn"
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '12px',
              width: '100%',
              padding: '14px 24px',
              borderRadius: '12px',
              border: 'none',
              backgroundColor: '#ffffff',
              color: '#1a1a2e',
              fontSize: '16px',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)'
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.3)';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.2)';
            }}
          >
            {/* Google Icon */}
            <svg width="20" height="20" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Se connecter avec Google
          </button>
        </div>

        {/* Info */}
        <div style={{
          backgroundColor: 'rgba(255, 215, 0, 0.1)',
          borderRadius: '10px',
          padding: '15px',
          marginBottom: '30px',
          border: '1px solid rgba(255, 215, 0, 0.2)'
        }}>
          <p style={{ color: '#a0aec0', margin: 0, fontSize: '13px', lineHeight: '1.6' }}>
            🔒 Connexion sécurisée via Google OAuth.<br />
            Vos données restent confidentielles.
          </p>
        </div>

        {/* Footer */}
        <div style={{
          paddingTop: '20px',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)'
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

/**
 * Composant AuthCallback pour traiter le retour de Google OAuth
 * REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
 */
export const AuthCallback = ({ onAuthSuccess }) => {
  const hasProcessed = useRef(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Prevent double processing in StrictMode
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processAuth = async () => {
      // Check for OAuth errors in URL (hash or query params)
      const hash = window.location.hash;
      const searchParams = new URLSearchParams(window.location.search);
      
      // Check for error in query params (consent denied, access denied, etc.)
      const errorParam = searchParams.get('error');
      const errorDescription = searchParams.get('error_description');
      
      // Also check hash for errors
      const hashErrorMatch = hash.match(/error=([^&]+)/);
      const hashErrorDescMatch = hash.match(/error_description=([^&]+)/);
      
      if (errorParam || hashErrorMatch) {
        const errorType = errorParam || (hashErrorMatch ? decodeURIComponent(hashErrorMatch[1]) : 'unknown');
        const errorDesc = errorDescription || (hashErrorDescMatch ? decodeURIComponent(hashErrorDescMatch[1]) : '');
        
        console.log('OAuth cancelled or denied:', errorType, errorDesc);
        
        // Show friendly message briefly, then redirect
        if (errorType === 'access_denied' || errorType === 'consent_denied') {
          setError('Connexion annulée. Redirection vers la page de connexion...');
        } else {
          setError(`Erreur d'authentification. Redirection...`);
        }
        
        setTimeout(() => {
          window.location.href = '/';
        }, 2000);
        return;
      }
      
      // Extract session_id from URL fragment
      const sessionIdMatch = hash.match(/session_id=([^&]+)/);
      
      if (!sessionIdMatch) {
        console.error('No session_id found in URL');
        setError('Session invalide. Redirection...');
        setTimeout(() => {
          window.location.href = '/';
        }, 2000);
        return;
      }

      const sessionId = sessionIdMatch[1];

      try {
        // Exchange session_id for session_token
        const API_URL = process.env.REACT_APP_BACKEND_URL;
        const response = await fetch(`${API_URL}/api/auth/session`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ session_id: sessionId })
        });

        if (!response.ok) {
          throw new Error('Session exchange failed');
        }

        const data = await response.json();
        
        if (data.success && data.user) {
          // Store user info in localStorage for quick access
          localStorage.setItem('user', JSON.stringify(data.user));
          
          // Notify parent and redirect
          if (onAuthSuccess) {
            onAuthSuccess(data.user);
          }
          
          // Redirect to main app (remove hash)
          window.location.href = '/';
        } else {
          throw new Error('Invalid response');
        }
      } catch (error) {
        console.error('Auth error:', error);
        localStorage.removeItem('user');
        setError('Erreur de connexion. Redirection...');
        setTimeout(() => {
          window.location.href = '/';
        }, 2000);
      }
    };

    processAuth();
  }, [onAuthSuccess]);

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)'
    }}>
      <div style={{ textAlign: 'center' }}>
        {error ? (
          <>
            <div style={{
              width: '50px',
              height: '50px',
              backgroundColor: 'rgba(255, 215, 0, 0.2)',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 20px',
              fontSize: '24px'
            }}>
              ↩️
            </div>
            <p style={{ color: '#ffd700', fontSize: '18px', marginBottom: '10px' }}>{error}</p>
            <p style={{ color: '#a0aec0', fontSize: '14px' }}>Vous serez redirigé automatiquement</p>
          </>
        ) : (
          <>
            <div style={{
              width: '50px',
              height: '50px',
              border: '3px solid rgba(255, 215, 0, 0.3)',
              borderTopColor: '#ffd700',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
              margin: '0 auto 20px'
            }} />
            <p style={{ color: '#ffd700', fontSize: '18px' }}>Connexion en cours...</p>
          </>
        )}
        <style>{`
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    </div>
  );
};

export default AuthPage;
