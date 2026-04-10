import React from 'react';

export default function ImpactPanel({ data={}, basePrediction=0 }) {
  const entries = Object.entries(data);
  if (entries.length === 0) return null;

  const getImpactLevel = (value) => {
    const abs = Math.abs(Number(value || 0));
    if (abs >= 0.08) return 'high';
    if (abs >= 0.04) return 'medium';
    return 'low';
  };

  return (
    <div className="dashboard-panel impact-panel">
      <h3>
        Simulation: Maximize Inputs
        <span className="info-tooltip" title="Shows how much score changes if improved.">
          ⓘ
        </span>
      </h3>
      <p className="description">What happens if we max out a single feature?</p>
      <p className="description">Impact shows how much score improves if a feature is maximized.</p>
      
      <ul className="impact-list">
        {entries.map(([feature, difference], idx) => {
          const isPositive = difference > 0;
          const level = getImpactLevel(difference);
          return (
            <li key={idx}>
              <div className="impact-header-row">
                <div className="feature-name">{feature.replace(/_/g, ' ')}</div>
                <span className={`impact-level ${level}`}>
                  {level === 'high' ? 'High Impact' : level === 'medium' ? 'Medium Impact' : 'Low Impact'}
                </span>
              </div>
              <div className="impact-delta">
                {Math.abs(Number(difference || 0)) < 0.005 ? (
                  <span className="neutral">No significant impact</span>
                ) : (
                  <span className={isPositive ? 'positive' : 'negative'}>
                    {isPositive ? '+' : ''}{difference.toFixed(2)} pts
                  </span>
                )}
                <span className="base-comparison">
                  ({Number(basePrediction || 0).toFixed(2)} → {(Number(basePrediction || 0) + Number(difference || 0)).toFixed(2)})
                </span>
              </div>
              <div className="progress-bar">
                <div 
                  className={isPositive ? 'progress-fill positive' : 'progress-fill negative'} 
                  style={{ width: `${Math.min(Math.abs(difference) * 50, 100)}%` }}
                />
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
