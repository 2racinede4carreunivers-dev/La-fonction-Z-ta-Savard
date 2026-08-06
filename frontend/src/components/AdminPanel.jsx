import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const AdminPanel = ({ onBack, sessionToken }) => {
  const [activeTab, setActiveTab] = useState('analytics');
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [users, setUsers] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Analytics state
  const [analyticsSummary, setAnalyticsSummary] = useState(null);
  const [analyticsCountry, setAnalyticsCountry] = useState([]);
  const [analyticsCity, setAnalyticsCity] = useState([]);
  const [analyticsTimeline, setAnalyticsTimeline] = useState([]);
  const [analyticsDevices, setAnalyticsDevices] = useState({});
  const [analyticsPages, setAnalyticsPages] = useState([]);
  const [analyticsMonthly, setAnalyticsMonthly] = useState([]);
  const [analyticsPeriod, setAnalyticsPeriod] = useState(30);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  const fetchData = async (endpoint) => {
    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        headers: { 'X-Session-Token': sessionToken },
        credentials: 'include'
      });
      if (!response.ok) throw new Error('Erreur de chargement');
      return await response.json();
    } catch (err) {
      console.error('Fetch error:', err);
      return null;
    }
  };

  const loadAnalytics = async (days = 30) => {
    setAnalyticsLoading(true);
    try {
      const [summary, country, city, timeline, devices, pages, monthly] = await Promise.all([
        fetchData('/api/admin/analytics/summary'),
        fetchData(`/api/admin/analytics/by-country?days=${days}`),
        fetchData(`/api/admin/analytics/by-city?days=${days}`),
        fetchData(`/api/admin/analytics/timeline?days=${days}`),
        fetchData(`/api/admin/analytics/devices?days=${days}`),
        fetchData(`/api/admin/analytics/top-pages?days=${days}`),
        fetchData('/api/admin/analytics/monthly?months=12')
      ]);
      
      if (summary) setAnalyticsSummary(summary);
      if (country?.data) setAnalyticsCountry(country.data);
      if (city?.data) setAnalyticsCity(city.data);
      if (timeline?.data) setAnalyticsTimeline(timeline.data);
      if (devices?.data) setAnalyticsDevices(devices.data);
      if (pages?.data) setAnalyticsPages(pages.data);
      if (monthly?.data) setAnalyticsMonthly(monthly.data);
    } catch (err) {
      console.error('Analytics error:', err);
    }
    setAnalyticsLoading(false);
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
      
      // Load analytics
      await loadAnalytics(30);
      
      setLoading(false);
    };
    loadData();
  }, [sessionToken]);

  const handlePeriodChange = async (days) => {
    setAnalyticsPeriod(days);
    await loadAnalytics(days);
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleString('fr-FR');
  };

  const COLORS = ['#ffd700', '#68d391', '#63b3ed', '#fc8181', '#b794f4', '#f6ad55', '#4fd1c5', '#f687b3'];

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

  const StatCard = ({ value, label, color = '#ffd700' }) => (
    <div style={{
      backgroundColor: `${color}15`,
      padding: '20px',
      borderRadius: '12px',
      textAlign: 'center',
      border: `1px solid ${color}30`
    }}>
      <div style={{ fontSize: '32px', color, fontWeight: 'bold' }}>{value}</div>
      <div style={{ color: '#a0aec0', fontSize: '14px', marginTop: '5px' }}>{label}</div>
    </div>
  );

  if (loading) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        backgroundColor: '#1a1a2e', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center' 
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '50px',
            height: '50px',
            border: '3px solid rgba(255, 215, 0, 0.3)',
            borderTopColor: '#ffd700',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 20px'
          }} />
          <p style={{ color: '#ffd700' }}>Chargement du panneau administrateur...</p>
          <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#1a1a2e',
      padding: '20px'
    }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
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
          ← Retour à l'application
        </button>

        <h1 style={{ color: '#ffd700', marginBottom: '30px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <span>🔐</span> Panneau Administrateur
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
          <button style={tabStyle(activeTab === 'analytics')} onClick={() => setActiveTab('analytics')}>
            📈 Analytics Visiteurs
          </button>
          <button style={tabStyle(activeTab === 'stats')} onClick={() => setActiveTab('stats')}>
            📊 Statistiques App
          </button>
          <button style={tabStyle(activeTab === 'history')} onClick={() => setActiveTab('history')}>
            📝 Historique
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
          
          {/* ANALYTICS TAB */}
          {activeTab === 'analytics' && (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px', flexWrap: 'wrap', gap: '15px' }}>
                <h2 style={{ color: '#ffd700', margin: 0 }}>📈 Analytics des Visiteurs</h2>
                <div style={{ display: 'flex', gap: '10px' }}>
                  {[7, 30, 90].map(days => (
                    <button
                      key={days}
                      onClick={() => handlePeriodChange(days)}
                      style={{
                        padding: '8px 16px',
                        borderRadius: '6px',
                        border: 'none',
                        backgroundColor: analyticsPeriod === days ? '#ffd700' : 'rgba(255,255,255,0.1)',
                        color: analyticsPeriod === days ? '#1a1a2e' : '#a0aec0',
                        cursor: 'pointer',
                        fontWeight: analyticsPeriod === days ? 'bold' : 'normal'
                      }}
                    >
                      {days} jours
                    </button>
                  ))}
                </div>
              </div>

              {analyticsLoading ? (
                <div style={{ textAlign: 'center', padding: '40px', color: '#a0aec0' }}>
                  Chargement des analytics...
                </div>
              ) : (
                <>
                  {/* Summary Cards */}
                  {analyticsSummary && (
                    <div style={{
                      display: 'grid',
                      gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
                      gap: '15px',
                      marginBottom: '30px'
                    }}>
                      <StatCard value={analyticsSummary.visits_today} label="Visites aujourd'hui" color="#ffd700" />
                      <StatCard value={analyticsSummary.visits_7_days} label="7 derniers jours" color="#68d391" />
                      <StatCard value={analyticsSummary.visits_30_days} label="30 derniers jours" color="#63b3ed" />
                      <StatCard value={analyticsSummary.total_visits} label="Total visites" color="#b794f4" />
                      <StatCard value={analyticsSummary.unique_visitors_today} label="Uniques aujourd'hui" color="#f6ad55" />
                      <StatCard value={analyticsSummary.unique_visitors_30_days} label="Uniques 30 jours" color="#4fd1c5" />
                    </div>
                  )}

                  {/* Timeline Chart */}
                  {analyticsTimeline.length > 0 && (
                    <div style={{ marginBottom: '30px' }}>
                      <h3 style={{ color: '#e2e8f0', marginBottom: '15px' }}>📅 Visites par jour</h3>
                      <div style={{ backgroundColor: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '20px' }}>
                        <ResponsiveContainer width="100%" height={250}>
                          <LineChart data={analyticsTimeline}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                            <XAxis dataKey="date" stroke="#a0aec0" tick={{ fontSize: 11 }} />
                            <YAxis stroke="#a0aec0" />
                            <Tooltip 
                              contentStyle={{ backgroundColor: '#2d3748', border: 'none', borderRadius: '8px' }}
                              labelStyle={{ color: '#ffd700' }}
                            />
                            <Legend />
                            <Line type="monotone" dataKey="visits" stroke="#ffd700" strokeWidth={2} name="Visites" dot={false} />
                            <Line type="monotone" dataKey="unique_visitors" stroke="#68d391" strokeWidth={2} name="Uniques" dot={false} />
                          </LineChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  )}

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '20px', marginBottom: '30px' }}>
                    {/* Country Chart */}
                    {analyticsCountry.length > 0 && (
                      <div>
                        <h3 style={{ color: '#e2e8f0', marginBottom: '15px' }}>🌍 Par Pays</h3>
                        <div style={{ backgroundColor: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '20px' }}>
                          <ResponsiveContainer width="100%" height={250}>
                            <BarChart data={analyticsCountry.slice(0, 10)} layout="vertical">
                              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                              <XAxis type="number" stroke="#a0aec0" />
                              <YAxis dataKey="country" type="category" stroke="#a0aec0" width={100} tick={{ fontSize: 11 }} />
                              <Tooltip contentStyle={{ backgroundColor: '#2d3748', border: 'none', borderRadius: '8px' }} />
                              <Bar dataKey="visits" fill="#ffd700" name="Visites" radius={[0, 4, 4, 0]} />
                            </BarChart>
                          </ResponsiveContainer>
                        </div>
                      </div>
                    )}

                    {/* City Chart */}
                    {analyticsCity.length > 0 && (
                      <div>
                        <h3 style={{ color: '#e2e8f0', marginBottom: '15px' }}>🏙️ Par Ville</h3>
                        <div style={{ backgroundColor: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '20px' }}>
                          <ResponsiveContainer width="100%" height={250}>
                            <BarChart data={analyticsCity.slice(0, 10)} layout="vertical">
                              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                              <XAxis type="number" stroke="#a0aec0" />
                              <YAxis dataKey="city" type="category" stroke="#a0aec0" width={100} tick={{ fontSize: 11 }} />
                              <Tooltip contentStyle={{ backgroundColor: '#2d3748', border: 'none', borderRadius: '8px' }} />
                              <Bar dataKey="visits" fill="#68d391" name="Visites" radius={[0, 4, 4, 0]} />
                            </BarChart>
                          </ResponsiveContainer>
                        </div>
                      </div>
                    )}
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
                    {/* Devices Pie Chart */}
                    {Object.keys(analyticsDevices).length > 0 && (
                      <div>
                        <h3 style={{ color: '#e2e8f0', marginBottom: '15px' }}>📱 Appareils</h3>
                        <div style={{ backgroundColor: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '20px' }}>
                          <ResponsiveContainer width="100%" height={200}>
                            <PieChart>
                              <Pie
                                data={Object.entries(analyticsDevices).map(([name, value]) => ({ name, value }))}
                                cx="50%"
                                cy="50%"
                                innerRadius={40}
                                outerRadius={70}
                                paddingAngle={5}
                                dataKey="value"
                                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                              >
                                {Object.keys(analyticsDevices).map((entry, index) => (
                                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                              </Pie>
                              <Tooltip contentStyle={{ backgroundColor: '#2d3748', border: 'none', borderRadius: '8px' }} />
                            </PieChart>
                          </ResponsiveContainer>
                        </div>
                      </div>
                    )}

                    {/* Top Pages */}
                    {analyticsPages.length > 0 && (
                      <div>
                        <h3 style={{ color: '#e2e8f0', marginBottom: '15px' }}>📄 Pages populaires</h3>
                        <div style={{ 
                          backgroundColor: 'rgba(0,0,0,0.2)', 
                          borderRadius: '10px', 
                          padding: '15px',
                          maxHeight: '200px',
                          overflowY: 'auto'
                        }}>
                          {analyticsPages.slice(0, 10).map((page, index) => (
                            <div key={index} style={{
                              display: 'flex',
                              justifyContent: 'space-between',
                              padding: '8px 0',
                              borderBottom: index < 9 ? '1px solid rgba(255,255,255,0.1)' : 'none'
                            }}>
                              <span style={{ color: '#a0aec0', fontSize: '13px', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                {page.path}
                              </span>
                              <span style={{ color: '#ffd700', fontWeight: 'bold', marginLeft: '10px' }}>
                                {page.visits}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Monthly Stats */}
                    {analyticsMonthly.length > 0 && (
                      <div>
                        <h3 style={{ color: '#e2e8f0', marginBottom: '15px' }}>📆 Par Mois</h3>
                        <div style={{ backgroundColor: 'rgba(0,0,0,0.2)', borderRadius: '10px', padding: '20px' }}>
                          <ResponsiveContainer width="100%" height={200}>
                            <BarChart data={analyticsMonthly}>
                              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                              <XAxis dataKey="period" stroke="#a0aec0" tick={{ fontSize: 10 }} />
                              <YAxis stroke="#a0aec0" />
                              <Tooltip contentStyle={{ backgroundColor: '#2d3748', border: 'none', borderRadius: '8px' }} />
                              <Bar dataKey="visits" fill="#b794f4" name="Visites" radius={[4, 4, 0, 0]} />
                            </BarChart>
                          </ResponsiveContainer>
                        </div>
                      </div>
                    )}
                  </div>
                </>
              )}
            </div>
          )}

          {/* Stats Tab */}
          {activeTab === 'stats' && stats && (
            <div>
              <h2 style={{ color: '#ffd700', marginTop: 0 }}>📊 Statistiques Application</h2>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '20px',
                marginBottom: '30px'
              }}>
                <StatCard value={stats.total_users} label="Utilisateurs" color="#ffd700" />
                <StatCard value={stats.total_questions} label="Questions posées" color="#68d391" />
                <StatCard value={stats.total_suggestions} label="Suggestions" color="#63b3ed" />
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
              <h2 style={{ color: '#ffd700', marginTop: 0 }}>📝 Historique des Questions</h2>
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
              <h2 style={{ color: '#ffd700', marginTop: 0 }}>👥 Utilisateurs Enregistrés</h2>
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
              <h2 style={{ color: '#ffd700', marginTop: 0 }}>💡 Suggestions des Utilisateurs</h2>
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
