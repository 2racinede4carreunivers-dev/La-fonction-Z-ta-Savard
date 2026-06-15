/**
 * Graphiques spectraux pour Gabriel - Assistant HOL
 * Visualisation des suites SA/SB, digamma, rapport spectral RSP et ecarts premiers
 * Dossier: /app/frontend/src/visuel-gabriel-isabelle/
 */
import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from 'recharts';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL;

const CHART_COLORS = {
  sa: '#f59e0b',
  sb: '#3b82f6',
  digamma: '#10b981',
  ratio: '#f59e0b',
  expected: '#ef4444',
  gap: '#8b5cf6',
};

const chartStyle = {
  container: {
    background: 'rgba(15, 23, 42, 0.6)',
    border: '1px solid rgba(245, 158, 11, 0.15)',
    borderRadius: '12px',
    padding: '16px',
    marginTop: '12px',
  },
  title: {
    color: '#fbbf24',
    fontSize: '13px',
    fontWeight: '600',
    marginBottom: '8px',
  },
  subtitle: {
    color: 'rgba(255,255,255,0.4)',
    fontSize: '11px',
    marginBottom: '12px',
  }
};

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload || !payload.length) return null;
  return (
    <div style={{ background: '#1e293b', border: '1px solid rgba(245,158,11,0.3)', borderRadius: '8px', padding: '10px', fontSize: '12px' }}>
      <p style={{ color: '#fbbf24', marginBottom: '4px' }}>Position n={label}</p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color, margin: '2px 0' }}>
          {entry.name}: {typeof entry.value === 'number' ? entry.value.toLocaleString('fr-FR', { maximumFractionDigits: 4 }) : entry.value}
        </p>
      ))}
    </div>
  );
};

/** Courbe SA(n) et SB(n) */
const SuiteChart = ({ data }) => {
  if (!data || data.length === 0) return null;
  const displayData = data.map(d => ({
    ...d,
    SA_log: d.SA > 0 ? Math.log10(d.SA) : 0,
    SB_log: d.SB > 0 ? Math.log10(d.SB) : 0,
  }));

  return (
    <div style={chartStyle.container}>
      <div style={chartStyle.title}>Suites spectrales SA(n) et SB(n)</div>
      <div style={chartStyle.subtitle}>Echelle logarithmique (log10) — Rapport 1/2, facteur 64</div>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={displayData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
          <XAxis dataKey="n" stroke="rgba(255,255,255,0.3)" tick={{ fontSize: 10 }} />
          <YAxis stroke="rgba(255,255,255,0.3)" tick={{ fontSize: 10 }} />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ fontSize: '11px' }} />
          <Line type="monotone" dataKey="SA_log" name="log10(SA)" stroke={CHART_COLORS.sa} dot={false} strokeWidth={2} />
          <Line type="monotone" dataKey="SB_log" name="log10(SB)" stroke={CHART_COLORS.sb} dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

/** Digamma calcule pour chaque premier */
const DigammaChart = ({ data }) => {
  if (!data || data.length === 0) return null;
  const displayData = data.map(d => ({
    ...d,
    digamma_abs: Math.abs(d.digamma),
    label: `p=${d.p}`,
  }));

  return (
    <div style={chartStyle.container}>
      <div style={chartStyle.title}>Digamma calcule par position</div>
      <div style={chartStyle.subtitle}>digamma(n, p) = SB(n) - 64 * p</div>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={displayData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
          <XAxis dataKey="n" stroke="rgba(255,255,255,0.3)" tick={{ fontSize: 10 }} />
          <YAxis stroke="rgba(255,255,255,0.3)" tick={{ fontSize: 10 }}
            tickFormatter={(v) => v >= 1000000 ? `${(v/1000000).toFixed(1)}M` : v >= 1000 ? `${(v/1000).toFixed(0)}k` : v} />
          <Tooltip content={<CustomTooltip />} />
          <Line type="monotone" dataKey="digamma" name="Digamma" stroke={CHART_COLORS.digamma} dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

/** Rapport spectral RSP — convergence vers 1/2 */
const RSPChart = ({ data }) => {
  if (!data || data.length === 0) return null;
  return (
    <div style={chartStyle.container}>
      <div style={chartStyle.title}>Rapport spectral RSP — Convergence vers 1/2</div>
      <div style={chartStyle.subtitle}>ratio_1x1(n-1, n) pour chaque position consecutive</div>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
          <XAxis dataKey="n" stroke="rgba(255,255,255,0.3)" tick={{ fontSize: 10 }} />
          <YAxis stroke="rgba(255,255,255,0.3)" tick={{ fontSize: 10 }} domain={[0.48, 0.52]} />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ fontSize: '11px' }} />
          <ReferenceLine y={0.5} stroke={CHART_COLORS.expected} strokeDasharray="6 3" label={{ value: '1/2', fill: CHART_COLORS.expected, fontSize: 10 }} />
          <Line type="monotone" dataKey="ratio" name="Ratio RSP" stroke={CHART_COLORS.ratio} dot={{ r: 2 }} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

/** Ecarts entre nombres premiers consecutifs */
const GapsChart = ({ data }) => {
  if (!data || data.length === 0) return null;
  return (
    <div style={chartStyle.container}>
      <div style={chartStyle.title}>Ecarts entre nombres premiers consecutifs</div>
      <div style={chartStyle.subtitle}>gap = p(n) - p(n-1)</div>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
          <XAxis dataKey="p" stroke="rgba(255,255,255,0.3)" tick={{ fontSize: 9 }}
            label={{ value: 'Premier p', position: 'insideBottom', offset: -2, fill: 'rgba(255,255,255,0.3)', fontSize: 10 }} />
          <YAxis stroke="rgba(255,255,255,0.3)" tick={{ fontSize: 10 }} />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="gap" name="Ecart" fill={CHART_COLORS.gap} radius={[3, 3, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

/**
 * Composant principal: affiche les 4 graphiques spectraux.
 * Props:
 *  - computationType: type de calcul effectue par Gabriel
 *  - primeAnalyzed: nombre premier analyse (optionnel)
 *  - visible: afficher ou non
 */
export const SpectralVisualizer = ({ computationType, primeAnalyzed, visible }) => {
  const [vizData, setVizData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [range, setRange] = useState({ start: 1, end: 50 });

  useEffect(() => {
    if (!visible) return;
    loadData(range.start, range.end);
  }, [visible, range]);

  const loadData = async (start, end) => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/api/gabriel/visualize?start=${start}&end=${end}`);
      setVizData(res.data);
    } catch (err) {
      console.error('Erreur chargement visualisation:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!visible) return null;

  return (
    <div data-testid="spectral-visualizer" style={{ marginTop: '16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ color: '#fbbf24', fontSize: '14px', fontWeight: '600' }}>
          Visualisation spectrale
        </span>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <span style={{ color: 'rgba(255,255,255,0.4)', fontSize: '11px' }}>Plage:</span>
          {[
            { label: '1-25', s: 1, e: 25 },
            { label: '1-50', s: 1, e: 50 },
            { label: '1-100', s: 1, e: 100 },
            { label: '50-150', s: 50, e: 150 },
          ].map(r => (
            <button
              key={r.label}
              onClick={() => setRange({ start: r.s, end: r.e })}
              style={{
                padding: '2px 8px', borderRadius: '4px', fontSize: '10px', cursor: 'pointer',
                border: range.start === r.s && range.end === r.e ? '1px solid #f59e0b' : '1px solid rgba(255,255,255,0.1)',
                background: range.start === r.s && range.end === r.e ? 'rgba(245,158,11,0.15)' : 'rgba(15,23,42,0.5)',
                color: range.start === r.s && range.end === r.e ? '#fbbf24' : 'rgba(255,255,255,0.4)',
              }}
            >
              {r.label}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div style={{ textAlign: 'center', color: 'rgba(245,158,11,0.5)', padding: '20px', fontSize: '13px' }}>
          Chargement des donnees spectrales...
        </div>
      )}

      {vizData && !loading && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          <SuiteChart data={vizData.suites} />
          <DigammaChart data={vizData.digamma} />
          <RSPChart data={vizData.rsp} />
          <GapsChart data={vizData.gaps} />
        </div>
      )}
    </div>
  );
};

export default SpectralVisualizer;
