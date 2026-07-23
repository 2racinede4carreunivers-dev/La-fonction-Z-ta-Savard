import React, { useState, useEffect } from 'react';

const AdminPanel = ({ onBack, sessionToken }) => {
  const [activeTab, setActiveTab] = useState('stats');
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [users, setUsers] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  const fetchData = async (endpoint) => {
    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        headers: { 'X-Session-Token': sessionToken }
      });
      if (!response.ok) throw new Error('Erreur de chargement');
      return await response.json();
    } catch (err) {
      setError(err.message);
      return null;
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      const [statsData, historyData, usersData, suggestionsData] = await Promise.all([
        fetchData('/api/admin/stats'),
        fetchData('/api/admin/history?limit=50'),
        fetchData('/api/admin/users?limit=50'),
        fetchData('/api/suggestions?limit=50')
      ]);
      
      if (statsData) setStats(statsData);
      if (historyData) setHistory(historyData);
      if (usersData) setUsers(usersData);
      if (suggestionsData) setSuggestions(suggestionsData);
      
      setLoading(false);
    };
    loadData();
  }, [sessionToken]);

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleString('fr-FR');
  };

  const tabStyle = (isActive) => ({
    padding: '12px 20px',
    backgroundColor: isActive ? '#ffd700' : 'transparent',
    color: isActive ? '#1a1a2e' : '#a0aec0',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontWeight: isActive ? 'bold' : 'normal',
    transition: 'all 0.3s'
  });

  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center', color: '#ffd700' }}>
        Chargement du panneau administrateur...
      </div>
    );
  }

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#1a1a2e',
      padding: '20px'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
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

        <h1 style={{ color: '#ffd700', marginBottom: '30px' }}>
          🔐 Panneau Administrateur
        </h1>

        {error && (
          <div style={{
            padding: '15px',
            backgroundColor: 'rgba(245, 101, 101, 0.2)',
            borderRadius: '8px',
            color: '#fc8181',
            marginBottom: '20px'
          }}>
            {error}
          </div>
        )}

        {/* Tabs */}
        <div style={{
          display: 'flex',
          gap: '10px',
          marginBottom: '20px',
          flexWrap: 'wrap'
        }}>
          <button style={tabStyle(activeTab === 'stats')} onClick={() => setActiveTab('stats')}>
            📊 Statistiques
          </button>
          <button style={tabStyle(activeTab === 'history')} onClick={() => setActiveTab('history')}>
            📝 Historique Questions
          </button>
          <button style={tabStyle(activeTab === 'users')} onClick={() => setActiveTab('users')}>
            👥 Utilisateurs
          </button>
          <button style={tabStyle(activeTab === 'suggestions')} onClick={() => setActiveTab('suggestions')}>
            💡 Suggestions
          </button>
        </div>

        {/* Content */}
        <div style={{
          backgroundColor: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '15px',
          padding: '25px',
          border: '1px solid rgba(255, 215, 0, 0.2)'
        }}>
          {/* Stats Tab */}
          {activeTab === 'stats' && stats && (
            <div>
              <h2 style={{ color: '#ffd700', marginTop: 0 }}>Statistiques Globales</h2>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '20px',
                marginBottom: '30px'
              }}>
                <div style={{
                  backgroundColor: 'rgba(255, 215, 0, 0.1)',
                  padding: '20px',
                  borderRadius: '10px',
                  textAlign: 'center'
                }}>
                  <div style={{ fontSize: '36px', color: '#ffd700', fontWeight: 'bold' }}>
                    {stats.total_users}
                  </div>
                  <div style={{ color: '#a0aec0' }}>Utilisateurs</div>
                </div>
                <div style={{
                  backgroundColor: 'rgba(72, 187, 120, 0.1)',
                  padding: '20px',
                  borderRadius: '10px',
                  textAlign: 'center'
                }}>
                  <div style={{ fontSize: '36px', color: '#68d391', fontWeight: 'bold' }}>
                    {stats.total_questions}
                  </div>
                  <div style={{ color: '#a0aec0' }}>Questions posées</div>
                </div>
                <div style={{
                  backgroundColor: 'rgba(99, 179, 237, 0.1)',
                  padding: '20px',
                  borderRadius: '10px',
                  textAlign: 'center'
                }}>
                  <div style={{ fontSize: '36px', color: '#63b3ed', fontWeight: 'bold' }}>
                    {stats.total_suggestions}
                  </div>
                  <div style={{ color: '#a0aec0' }}>Suggestions</div>
                </div>
              </div>

              {stats.questions_by_module && Object.keys(stats.questions_by_module).length > 0 && (
                <>
                  <h3 style={{ color: '#e2e8f0' }}>Questions par module IA</h3>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '15px' }}>
                    {Object.entries(stats.questions_by_module).map(([module, count]) => (
                      <div key={module} style={{
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        padding: '10px 20px',
                        borderRadius: '8px'
                      }}>
                        <span style={{ color: '#ffd700' }}>{module}</span>
                        <span style={{ color: '#a0aec0', marginLeft: '10px' }}>{count}</span>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}

          {/* History Tab */}
          {activeTab === 'history' && (
            <div>
              <h2 style={{ color: '#ffd700', marginTop: 0 }}>Historique des Questions</h2>
              {history.length === 0 ? (
                <p style={{ color: '#a0aec0' }}>Aucune question enregistrée</p>
              ) : (
                <div style={{ overflowX: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ borderBottom: '1px solid rgba(255, 215, 0, 0.3)' }}>
                        <th style={{ padding: '12px', textAlign: 'left', color: '#ffd700' }}>Date</th>
                        <th style={{ padding: '12px', textAlign: 'left', color: '#ffd700' }}>Email</th>
                        <th style={{ padding: '12px', textAlign: 'left', color: '#ffd700' }}>Module</th>
                        <th style={{ padding: '12px', textAlign: 'left', color: '#ffd700' }}>Question</th>
                      </tr>
                    </thead>
                    <tbody>
                      {history.map((item, index) => (
                        <tr key={index} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
                          <td style={{ padding: '12px', color: '#a0aec0', fontSize: '13px' }}>
                            {formatDate(item.timestamp)}
                          </td>
                          <td style={{ padding: '12px', color: '#e2e8f0', fontSize: '13px' }}>
                            {item.user_email}
                          </td>
                          <td style={{ padding: '12px', color: '#ffd700', fontSize: '13px' }}>
                            {item.ia_module}
                          </td>
                          <td style={{ padding: '12px', color: '#e2e8f0', fontSize: '13px', maxWidth: '400px' }}>
                            {item.question?.substring(0, 100)}{item.question?.length > 100 ? '...' : ''}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* Users Tab */}
          {activeTab === 'users' && (
            <div>
              <h2 style={{ color: '#ffd700', marginTop: 0 }}>Utilisateurs Enregistrés</h2>
              {users.length === 0 ? (
                <p style={{ color: '#a0aec0' }}>Aucun utilisateur enregistré</p>
              ) : (
                <div style={{ overflowX: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ borderBottom: '1px solid rgba(255, 215, 0, 0.3)' }}>
                        <th style={{ padding: '12px', textAlign: 'left', color: '#ffd700' }}>Email</th>
                        <th style={{ padding: '12px', textAlign: 'left', color: '#ffd700' }}>Première visite</th>
                        <th style={{ padding: '12px', textAlign: 'left', color: '#ffd700' }}>Dernière visite</th>
                        <th style={{ padding: '12px', textAlign: 'left', color: '#ffd700' }}>Visites</th>
                        <th style={{ padding: '12px', textAlign: 'left', color: '#ffd700' }}>Questions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {users.map((user, index) => (
                        <tr key={index} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
                          <td style={{ padding: '12px', color: '#e2e8f0' }}>{user.email}</td>
                          <td style={{ padding: '12px', color: '#a0aec0', fontSize: '13px' }}>
                            {formatDate(user.first_visit)}
                          </td>
                          <td style={{ padding: '12px', color: '#a0aec0', fontSize: '13px' }}>
                            {formatDate(user.last_visit)}
                          </td>
                          <td style={{ padding: '12px', color: '#68d391' }}>{user.total_visits}</td>
                          <td style={{ padding: '12px', color: '#63b3ed' }}>{user.total_questions}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* Suggestions Tab */}
          {activeTab === 'suggestions' && (
            <div>
              <h2 style={{ color: '#ffd700', marginTop: 0 }}>Suggestions des Utilisateurs</h2>
              {suggestions.length === 0 ? (
                <p style={{ color: '#a0aec0' }}>Aucune suggestion reçue</p>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                  {suggestions.map((item, index) => (
                    <div key={index} style={{
                      backgroundColor: 'rgba(255, 255, 255, 0.05)',
                      padding: '15px',
                      borderRadius: '10px',
                      border: '1px solid rgba(255, 215, 0, 0.1)'
                    }}>
                      <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        marginBottom: '10px',
                        fontSize: '13px'
                      }}>
                        <span style={{ color: '#ffd700' }}>{item.user_email}</span>
                        <span style={{ color: '#718096' }}>{formatDate(item.timestamp)}</span>
                      </div>
                      <p style={{ color: '#e2e8f0', margin: 0, lineHeight: '1.6' }}>
                        {item.suggestion}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;
