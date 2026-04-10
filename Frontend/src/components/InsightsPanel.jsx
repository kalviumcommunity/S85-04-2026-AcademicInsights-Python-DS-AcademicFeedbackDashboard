function toLabel(feature = '') {
  return feature
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (m) => m.toUpperCase());
}

function getBaseDomain(feature = '') {
  const domains = ['teaching', 'course', 'exam', 'lab', 'library', 'extra'];
  return domains.find((d) => feature.toLowerCase().includes(d)) || '';
}

function getCurrentRatingFromForm(feature, formData) {
  const domain = getBaseDomain(feature);
  if (!domain) return null;
  const key = `${domain}_rating`;
  return typeof formData[key] === 'number' ? Number(formData[key]) : null;
}

export default function InsightsPanel({
  topFeatures = {},
  impactAnalysis = {},
  formData = {},
  sentimentImpact,
}) {
  const sortedTop = Object.entries(topFeatures).sort((a, b) => b[1] - a[1]);
  const strengthFeature = sortedTop[0]?.[0] || 'lab_rating';
  const strengthValue = Number(sortedTop[0]?.[1] || 0);

  const impactEntries = Object.entries(impactAnalysis)
    .filter(([feature]) => !feature.includes('sentiment') && !feature.includes('comment'))
    .map(([feature, impact]) => ({
      feature,
      impact: Number(impact || 0),
      currentScore: getCurrentRatingFromForm(feature, formData),
    }))
    .filter((item) => item.impact > 0)
    .sort((a, b) => {
      const aScore = a.currentScore ?? 99;
      const bScore = b.currentScore ?? 99;
      if (aScore !== bScore) return aScore - bScore;
      return b.impact - a.impact;
    });

  const improvement = impactEntries[0] || {
    feature: Object.entries(impactAnalysis).sort((a, b) => b[1] - a[1])[0]?.[0] || 'extra_rating',
    impact: Number(Object.entries(impactAnalysis).sort((a, b) => b[1] - a[1])[0]?.[1] || 0),
    currentScore: null,
  };

  const nonDuplicateImprovement =
    impactEntries.find((item) => item.feature !== strengthFeature) || improvement;

  const strengthText = `${toLabel(strengthFeature)} is the strongest driver of satisfaction due to highest model importance.`;
  const improvementText = `Improving ${toLabel(nonDuplicateImprovement.feature)} can significantly increase overall satisfaction.`;

  const topImpact = Object.entries(impactAnalysis).sort((a, b) => b[1] - a[1])[0] || ['lab_rating', 0];
  const secondImpact = Object.entries(impactAnalysis).sort((a, b) => b[1] - a[1])[1] || ['teaching_rating', 0];

  return (
    <div className="dashboard-panel insights-panel">
      <h3>Smart Recommendations</h3>
      <div className="insights-list">
        <div className="insight-item">
          <span className="icon">🔥</span>
          <p className="text"><strong>Strength:</strong> {strengthText}</p>
        </div>
        <div className="insight-item">
          <span className="icon">⚠️</span>
          <p className="text"><strong>Improvement:</strong> {improvementText}</p>
        </div>
        <div className="insight-item">
          <span className="icon">🧠</span>
          <p className="text">This is not an average calculator. The AI model learns weighted, non-linear relationships and converts them into decision-focused guidance.</p>
        </div>
      </div>

      <div className="sentiment-alert decision-insight-panel">
        <h4>Actionable Insight</h4>
        <p className="text">Improving {toLabel(topImpact[0])} will increase satisfaction the most (+{Number(topImpact[1] || 0).toFixed(2)}).</p>
        <p className="text">Best ROI candidate: {toLabel(nonDuplicateImprovement.feature)} based on current score and impact potential.</p>
        <p className="text">{toLabel(secondImpact[0])} has moderate influence (+{Number(secondImpact[1] || 0).toFixed(2)}), useful as a secondary intervention.</p>
      </div>

      {sentimentImpact && (
        <div className="sentiment-alert">
          <h4>Text Sentiment Impact</h4>
          <p className="text fade-in">
            Free-text reviews shift predictions by <span className="delta">
              {sentimentImpact.difference > 0 ? '+' : ''}
              {sentimentImpact.difference.toFixed(2)} pts
            </span>.
            ({sentimentImpact.sentiment_score > 0 ? 'Positive' : 'Negative'} sentiment)
          </p>
        </div>
      )}
    </div>
  );
}
