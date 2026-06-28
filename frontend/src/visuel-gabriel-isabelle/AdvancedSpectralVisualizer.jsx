/**
 * Graphiques spectraux avances pour Gabriel
 * 1. Digamma calcule pour n=1 a n=200
 * 2. Rapport Spectral Asymetrique Ordonne (100 paires)
 */
import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, ReferenceLine, ComposedChart, Bar
} from 'recharts';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL;

const COLORS = {
  digamma: '#10b981',
  sumSA_A: '#f59e0b',
  sumSB_A: '#3b82f6',
  sumSA_B: '#f97316',
  sumSB_B: '#06b6d4',
  ratio: '#8b5cf6',
  expected: '#ef4444',
};

const chartStyle = {
  container: {
    background: 'rgba(15, 23, 42, 0.6)',
    border: '1px solid rgba(16, 185, 129, 0.2)',
    borderRadius: '12px',
    padding: '16px',
    marginTop: '16px',
  },
  title: {
    color: '#10b981',
    fontSize: '14px',
    fontWeight: '600',
    marginBottom: '6px',
  },
  subtitle: {
    color: 'rgba(255,255,255,0.5)',
    fontSize: '12px',
    marginBottom: '12px',
  },
  stats: {
    display: 'flex',
    gap: '16px',
    marginTop: '12px',
    padding: '10px',
    background: 'rgba(0,0,0,0.2)',
    borderRadius: '8px',
  },
  statItem: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: '11px',
  },
  statValue: {
    color: '#10b981',
    fontWeight: '600',
  },
};

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload || !payload.length) return null;
  return (
    <div style={{ 
      background: '#1e293b', 
      border: '1px solid rgba(16,185,129,0.3)', 
      borderRadius: '8px', 
      padding: '12px', 
      fontSize: '12px',
      maxWidth: '300px'
    }}>
      <p style={{ color: '#10b981', marginBottom: '6px', fontWeight: '600' }}>
        {payload[0]?.payload?.pair_index ? `Paire k=${label}` : `Position n=${label}`}
      </p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color, margin: '3px 0' }}>
          {entry.name}: {typeof entry.value === 'number' 
            ? entry.value.toLocaleString('fr-FR', { maximumFractionDigits: 6 }) 
            : entry.value}
        </p>
      ))}
      {payload[0]?.payload?.block_A_str && (
        <div style={{ marginTop: '8px', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '8px' }}>
          <p style={{ color: '#f59e0b', fontSize: '10px' }}>Bloc A: [{payload[0].payload.block_A_str}]</p>
          <p style={{ color: '#3b82f6', fontSize: '10px' }}>Bloc B: [{payload[0].payload.block_B_str}]</p>
        </div>
      )}
    </div>
  );
};

/**
 * GRAPHIQUE 1: Courbe du Digamma calcule (n=1 a n=200)
 */
export const DigammaCurveChart = ({ onLoad }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [range, setRange] = useState({ start: 1, end: 200 });

  useEffect(() => {
    loadData();
  }, [range]);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await axios.get(
        `${API_URL}/api/gabriel/digamma-curve?n_start=${range.start}&n_end=${range.end}`
      );
      setData(res.data);
      if (onLoad) onLoad(res.data);
    } catch (err) {
      console.error('Erreur chargement digamma curve:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={chartStyle.container}>
        <div style={{ textAlign: 'center', color: 'rgba(16,185,129,0.5)', padding: '40px' }}>
          Chargement de la courbe Digamma...
        </div>
      </div>
    );
  }

  if (!data || !data.data) return null;

  return (
    <div style={chartStyle.container} data-testid="digamma-curve-chart">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <div style={chartStyle.title}>📈 Courbe du Digamma Calculé</div>
          <div style={chartStyle.subtitle}>
            {data.formula} — pour n={range.start} à n={range.end}
          </div>
        </div>
        <div style={{ display: 'flex', gap: '6px' }}>
          {[
            { label: '1-50', s: 1, e: 50 },
            { label: '1-100', s: 1, e: 100 },
            { label: '1-200', s: 1, e: 200 },
          ].map(r => (
            <button
              key={r.label}
              onClick={() => setRange({ start: r.s, end: r.e })}
              style={{
                padding: '4px 10px', borderRadius: '6px', fontSize: '11px', cursor: 'pointer',
                border: range.end === r.e ? '1px solid #10b981' : '1px solid rgba(255,255,255,0.1)',
                background: range.end === r.e ? 'rgba(16,185,129,0.15)' : 'transparent',
                color: range.end === r.e ? '#10b981' : 'rgba(255,255,255,0.4)',
              }}
            >
              {r.label}
            </button>
          ))}
        </div>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data.data}>
          <defs>
            <linearGradient id="digammaGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={COLORS.digamma} stopOpacity={0.3}/>
              <stop offset="95%" stopColor={COLORS.digamma} stopOpacity={0.05}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
          <XAxis 
            dataKey="n" 
            stroke="rgba(255,255,255,0.3)" 
            tick={{ fontSize: 10 }}
            label={{ value: 'Position n', position: 'insideBottom', offset: -5, fill: 'rgba(255,255,255,0.4)', fontSize: 11 }}
          />
          <YAxis 
            stroke="rgba(255,255,255,0.3)" 
            tick={{ fontSize: 10 }}
            tickFormatter={(v) => {
              if (Math.abs(v) >= 1e12) return `${(v/1e12).toFixed(1)}T`;
              if (Math.abs(v) >= 1e9) return `${(v/1e9).toFixed(1)}G`;
              if (Math.abs(v) >= 1e6) return `${(v/1e6).toFixed(1)}M`;
              if (Math.abs(v) >= 1e3) return `${(v/1e3).toFixed(0)}k`;
              return v;
            }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area 
            type="monotone" 
            dataKey="digamma" 
            name="Digamma calculé" 
            stroke={COLORS.digamma} 
            fill="url(#digammaGradient)"
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>

      <div style={chartStyle.stats}>
        <div style={chartStyle.statItem}>
          Valeurs: <span style={chartStyle.statValue}>{data.stats?.count || 0}</span>
        </div>
        <div style={chartStyle.statItem}>
          Min: <span style={chartStyle.statValue}>{data.stats?.digamma_min?.toLocaleString('fr-FR', {maximumFractionDigits: 0})}</span>
        </div>
        <div style={chartStyle.statItem}>
          Max: <span style={chartStyle.statValue}>{data.stats?.digamma_max?.toLocaleString('fr-FR', {maximumFractionDigits: 0})}</span>
        </div>
      </div>
    </div>
  );
};

/**
 * GRAPHIQUE 2: Rapport Spectral Asymetrique Ordonne
 */
export const AsymmetricOrderedChart = ({ onLoad }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [numPairs, setNumPairs] = useState(100);
  const [viewMode, setViewMode] = useState('ratio'); // 'ratio' ou 'sums'

  useEffect(() => {
    loadData();
  }, [numPairs]);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await axios.get(
        `${API_URL}/api/gabriel/asymmetric-ordered?num_pairs=${numPairs}`
      );
      setData(res.data);
      if (onLoad) onLoad(res.data);
    } catch (err) {
      console.error('Erreur chargement asymmetric ordered:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={chartStyle.container}>
        <div style={{ textAlign: 'center', color: 'rgba(139,92,246,0.5)', padding: '40px' }}>
          Calcul des {numPairs} paires asymétriques...
        </div>
      </div>
    );
  }

  if (!data || !data.data) return null;

  return (
    <div style={{...chartStyle.container, border: '1px solid rgba(139,92,246,0.2)'}} data-testid="asymmetric-ordered-chart">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
        <div>
          <div style={{...chartStyle.title, color: '#8b5cf6'}}>📊 Rapport Spectral Asymétrique Ordonné</div>
          <div style={chartStyle.subtitle}>
            Bloc B = Bloc A + 1 terme — Convergence vers 1/2
          </div>
        </div>
        <div style={{ display: 'flex', gap: '6px', flexDirection: 'column', alignItems: 'flex-end' }}>
          <div style={{ display: 'flex', gap: '6px' }}>
            {[50, 100].map(n => (
              <button
                key={n}
                onClick={() => setNumPairs(n)}
                style={{
                  padding: '4px 10px', borderRadius: '6px', fontSize: '11px', cursor: 'pointer',
                  border: numPairs === n ? '1px solid #8b5cf6' : '1px solid rgba(255,255,255,0.1)',
                  background: numPairs === n ? 'rgba(139,92,246,0.15)' : 'transparent',
                  color: numPairs === n ? '#8b5cf6' : 'rgba(255,255,255,0.4)',
                }}
              >
                {n} paires
              </button>
            ))}
          </div>
          <div style={{ display: 'flex', gap: '6px' }}>
            {['ratio', 'sums'].map(mode => (
              <button
                key={mode}
                onClick={() => setViewMode(mode)}
                style={{
                  padding: '3px 8px', borderRadius: '4px', fontSize: '10px', cursor: 'pointer',
                  border: viewMode === mode ? '1px solid #8b5cf6' : '1px solid rgba(255,255,255,0.1)',
                  background: viewMode === mode ? 'rgba(139,92,246,0.1)' : 'transparent',
                  color: viewMode === mode ? '#a78bfa' : 'rgba(255,255,255,0.3)',
                }}
              >
                {mode === 'ratio' ? 'Ratio RsP' : 'Sommes'}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Exemples de paires */}
      <div style={{ 
        background: 'rgba(0,0,0,0.2)', 
        padding: '10px', 
        borderRadius: '8px', 
        marginBottom: '12px',
        fontSize: '11px',
        color: 'rgba(255,255,255,0.6)'
      }}>
        <span style={{ color: '#a78bfa', fontWeight: '600' }}>Configuration:</span> 
        {' '}A=[2] vs B=[3,5] → A=[2,3] vs B=[5,7,11] → A=[2,3,5] vs B=[7,11,13,17] → ...
      </div>

      {viewMode === 'ratio' ? (
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={data.data}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis 
              dataKey="pair_index" 
              stroke="rgba(255,255,255,0.3)" 
              tick={{ fontSize: 10 }}
              label={{ value: 'Index de paire k', position: 'insideBottom', offset: -5, fill: 'rgba(255,255,255,0.4)', fontSize: 11 }}
            />
            <YAxis 
              stroke="rgba(255,255,255,0.3)" 
              tick={{ fontSize: 10 }}
              domain={[0.49, 0.51]}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ fontSize: '11px' }} />
            <ReferenceLine 
              y={0.5} 
              stroke={COLORS.expected} 
              strokeDasharray="6 3" 
              label={{ value: '1/2', fill: COLORS.expected, fontSize: 10, position: 'right' }} 
            />
            <Line 
              type="monotone" 
              dataKey="ratio" 
              name="Ratio RsP" 
              stroke={COLORS.ratio} 
              dot={{ r: 2, fill: COLORS.ratio }} 
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <ResponsiveContainer width="100%" height={280}>
          <ComposedChart data={data.data}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis 
              dataKey="pair_index" 
              stroke="rgba(255,255,255,0.3)" 
              tick={{ fontSize: 10 }}
            />
            <YAxis 
              stroke="rgba(255,255,255,0.3)" 
              tick={{ fontSize: 10 }}
              tickFormatter={(v) => {
                if (Math.abs(v) >= 1e15) return `${(v/1e15).toFixed(1)}P`;
                if (Math.abs(v) >= 1e12) return `${(v/1e12).toFixed(1)}T`;
                if (Math.abs(v) >= 1e9) return `${(v/1e9).toFixed(1)}G`;
                if (Math.abs(v) >= 1e6) return `${(v/1e6).toFixed(1)}M`;
                return v;
              }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ fontSize: '10px' }} />
            <Line type="monotone" dataKey="sum_SA_A" name="∑SA(A)" stroke={COLORS.sumSA_A} dot={false} strokeWidth={2} />
            <Line type="monotone" dataKey="sum_SB_A" name="∑SB(A)" stroke={COLORS.sumSB_A} dot={false} strokeWidth={2} />
            <Line type="monotone" dataKey="sum_SA_B" name="∑SA(B)" stroke={COLORS.sumSA_B} dot={false} strokeWidth={1} strokeDasharray="4 2" />
            <Line type="monotone" dataKey="sum_SB_B" name="∑SB(B)" stroke={COLORS.sumSB_B} dot={false} strokeWidth={1} strokeDasharray="4 2" />
          </ComposedChart>
        </ResponsiveContainer>
      )}

      <div style={{...chartStyle.stats, background: 'rgba(139,92,246,0.1)'}}>
        <div style={chartStyle.statItem}>
          Paires: <span style={{...chartStyle.statValue, color: '#a78bfa'}}>{data.stats?.num_pairs || 0}</span>
        </div>
        <div style={chartStyle.statItem}>
          Ratio moyen: <span style={{...chartStyle.statValue, color: '#a78bfa'}}>{data.stats?.ratio_mean?.toFixed(6) || 'N/A'}</span>
        </div>
        <div style={chartStyle.statItem}>
          Convergées (δ&lt;0.001): <span style={{...chartStyle.statValue, color: '#a78bfa'}}>
            {data.stats?.converged_count || 0} ({((data.stats?.convergence_rate || 0) * 100).toFixed(1)}%)
          </span>
        </div>
      </div>
    </div>
  );
};

/**
 * GRAPHIQUE 3: Rapport Spectral Asymetrique Chaotique
 */
export const ChaoticComparisonChart = ({ onLoad }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/api/gabriel/chaotic-comparison?num_pairs=10`);
      setData(res.data);
      if (onLoad) onLoad(res.data);
    } catch (err) {
      console.error('Erreur chargement chaotic comparison:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={chartStyle.container}>
        <div style={{ textAlign: 'center', color: 'rgba(249,115,22,0.5)', padding: '40px' }}>
          Calcul des comparaisons chaotiques...
        </div>
      </div>
    );
  }

  if (!data || !data.data) return null;

  return (
    <div style={{...chartStyle.container, border: '1px solid rgba(249,115,22,0.3)'}} data-testid="chaotic-comparison-chart">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
        <div>
          <div style={{...chartStyle.title, color: '#f97316'}}>🌀 Rapport Spectral Asymétrique Chaotique</div>
          <div style={chartStyle.subtitle}>
            Configuration désordonnée — Convergence surprenante vers 1/2
          </div>
        </div>
      </div>

      {/* Pattern chaotique */}
      <div style={{ 
        background: 'rgba(249,115,22,0.1)', 
        padding: '10px', 
        borderRadius: '8px', 
        marginBottom: '12px',
        fontSize: '11px',
        color: 'rgba(255,255,255,0.7)'
      }}>
        <span style={{ color: '#fb923c', fontWeight: '600' }}>Pattern chaotique:</span> 
        <br />
        <span style={{ fontFamily: 'monospace', fontSize: '10px' }}>
          k=1: (3)-(5,2) | k=2: (5,7)-(11,2,3) | k=3: (7,11,13)-(17,2,3,5) | ...
        </span>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data.data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
          <XAxis 
            dataKey="k" 
            stroke="rgba(255,255,255,0.3)" 
            tick={{ fontSize: 10 }}
            label={{ value: 'Index k', position: 'insideBottom', offset: -5, fill: 'rgba(255,255,255,0.4)', fontSize: 11 }}
          />
          <YAxis 
            stroke="rgba(255,255,255,0.3)" 
            tick={{ fontSize: 10 }}
            domain={[-0.2, 0.6]}
          />
          <Tooltip 
            content={({ active, payload }) => {
              if (!active || !payload || !payload.length) return null;
              const d = payload[0].payload;
              return (
                <div style={{ 
                  background: '#1e293b', 
                  border: '1px solid rgba(249,115,22,0.3)', 
                  borderRadius: '8px', 
                  padding: '12px', 
                  fontSize: '11px',
                  maxWidth: '350px'
                }}>
                  <p style={{ color: '#f97316', fontWeight: '600', marginBottom: '6px' }}>
                    Paire k={d.k}
                  </p>
                  <p style={{ color: '#fb923c', margin: '2px 0', fontFamily: 'monospace', fontSize: '10px' }}>
                    A=[{d.bloc_A_str}]
                  </p>
                  <p style={{ color: '#fdba74', margin: '2px 0', fontFamily: 'monospace', fontSize: '10px' }}>
                    B=[{d.bloc_B_str}]
                  </p>
                  <p style={{ color: '#10b981', margin: '6px 0 2px' }}>
                    Ratio: <strong>{d.ratio?.toFixed(10)}</strong>
                  </p>
                  <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: '10px' }}>
                    Delta: {d.delta?.toFixed(10)} | {d.is_converged ? '✓ Convergé' : '○ En cours'}
                  </p>
                </div>
              );
            }}
          />
          <Legend wrapperStyle={{ fontSize: '11px' }} />
          <ReferenceLine 
            y={0.5} 
            stroke={COLORS.expected} 
            strokeDasharray="6 3" 
            label={{ value: '1/2', fill: COLORS.expected, fontSize: 10, position: 'right' }} 
          />
          <ReferenceLine y={0} stroke="rgba(255,255,255,0.2)" />
          <Line 
            type="monotone" 
            dataKey="ratio" 
            name="Ratio Chaotique" 
            stroke="#f97316" 
            dot={{ r: 4, fill: '#f97316', strokeWidth: 2 }} 
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>

      <div style={{...chartStyle.stats, background: 'rgba(249,115,22,0.1)'}}>
        <div style={chartStyle.statItem}>
          Paires: <span style={{...chartStyle.statValue, color: '#fb923c'}}>{data.stats?.num_pairs || 0}</span>
        </div>
        <div style={chartStyle.statItem}>
          Ratio moyen: <span style={{...chartStyle.statValue, color: '#fb923c'}}>{data.stats?.ratio_mean?.toFixed(6) || 'N/A'}</span>
        </div>
        <div style={chartStyle.statItem}>
          Convergées (δ&lt;0.05): <span style={{...chartStyle.statValue, color: '#fb923c'}}>
            {data.stats?.converged_count || 0} ({((data.stats?.convergence_rate || 0) * 100).toFixed(1)}%)
          </span>
        </div>
      </div>

      {/* Observation */}
      <div style={{ 
        marginTop: '12px',
        padding: '10px', 
        background: 'rgba(16,185,129,0.1)',
        borderRadius: '8px',
        borderLeft: '3px solid #10b981',
        fontSize: '11px',
        color: 'rgba(255,255,255,0.8)'
      }}>
        <strong style={{ color: '#10b981' }}>Observation remarquable:</strong> {data.observation || 'Convergence vers 1/2 malgré le désordre'}
      </div>
    </div>
  );
};

/**
 * Composant combine pour afficher les deux graphiques avances
 */
export const AdvancedSpectralVisualizer = ({ visible }) => {
  if (!visible) return null;

  return (
    <div data-testid="advanced-spectral-visualizer" style={{ marginTop: '20px' }}>
      <div style={{ 
        color: '#10b981', 
        fontSize: '15px', 
        fontWeight: '600', 
        marginBottom: '12px',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
      }}>
        <span>🔬</span>
        <span>Visualisations Spectrales Avancées</span>
      </div>
      
      <DigammaCurveChart />
      <AsymmetricOrderedChart />
      <ChaoticComparisonChart />
    </div>
  );
};

export default AdvancedSpectralVisualizer;
