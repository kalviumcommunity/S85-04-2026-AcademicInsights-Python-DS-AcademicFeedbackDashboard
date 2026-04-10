import React from 'react';

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

function normalizeRatingToUnit(rating) {
  if (typeof rating !== 'number' || Number.isNaN(rating)) return null;
  return (rating - 1) / 4;
}

function areAllCoreRatingsMax(formData) {
  const keys = [
    'teaching_rating',
    'course_rating',
    'exam_rating',
    'lab_rating',
    'library_rating',
    'extra_rating',
  ];
  return keys.every((k) => Number(formData?.[k]) >= 5);
}

function areAllCoreRatingsMin(formData) {
  const keys = [
    'teaching_rating',
    'course_rating',
    'exam_rating',
    'lab_rating',
    'library_rating',
    'extra_rating',
  ];
  return keys.every((k) => Number(formData?.[k]) <= 1);
}

export default function InsightsPanel({
  topFeatures = {},
  impactAnalysis = {},
  formData = {},
  sentimentImpact,
  strengthFeature,
}) {
  const sentimentDelta =
    typeof sentimentImpact === 'number'
      ? Number(sentimentImpact)
      : Number(sentimentImpact?.difference ?? 0);

  const sentimentScore =
    typeof sentimentImpact === 'object' && sentimentImpact !== null
      ? Number(sentimentImpact.sentiment_score ?? 0)
      : null;

  const hasSentimentImpact = Number.isFinite(sentimentDelta) && Math.abs(sentimentDelta) > 0;

  const sortedTop = Object.entries(topFeatures).sort((a, b) => b[1] - a[1]);
  const defaultStrengthFeature = strengthFeature || sortedTop[0]?.[0] || 'lab_score';

  const coreDomains = ['teaching', 'course', 'exam', 'lab', 'library', 'extra'];
  const ratedFeatures = coreDomains
    .map((domain) => ({
      feature: `${domain}_score`,
      rating: Number(formData?.[`${domain}_rating`]),
    }))
    .filter((x) => Number.isFinite(x.rating));

  const maxRating = ratedFeatures.length
    ? Math.max(...ratedFeatures.map((x) => x.rating))
    : null;

  const topRatedFeatures = maxRating === null
    ? []
    : ratedFeatures
        .filter((x) => x.rating === maxRating)
        .map((x) => x.feature);

  const contributionEntries = sortedTop
    .map(([feature, importance]) => {
      const rating = getCurrentRatingFromForm(feature, formData);
      const unit = normalizeRatingToUnit(rating);
      const contribution = Number(importance || 0) * Number(unit ?? 0);
      return { feature, contribution };
    })
    .sort((a, b) => b.contribution - a.contribution);

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

  const resolvedStrengthFeature = (() => {
    if (topRatedFeatures.length > 0) {
      const sortedByModelSignal = [...topRatedFeatures].sort((a, b) => {
        const impDiff = Number(topFeatures?.[b] || 0) - Number(topFeatures?.[a] || 0);
        if (impDiff !== 0) return impDiff;
        return Number(impactAnalysis?.[b] || 0) - Number(impactAnalysis?.[a] || 0);
      });
      return sortedByModelSignal[0];
    }
    return contributionEntries[0]?.feature || defaultStrengthFeature;
  })();

  const nonDuplicateImprovement =
    impactEntries.find((item) => item.feature !== resolvedStrengthFeature) || improvement;

  const allLow = areAllCoreRatingsMin(formData);
  const strengthText = allLow
    ? 'No single strong area right now. Build baseline performance across all core academic factors.'
    : `${toLabel(resolvedStrengthFeature)} is currently the strongest actionable driver for improving satisfaction.`;
  const allMaxed = areAllCoreRatingsMax(formData);
  const improvementText = allMaxed
    ? 'All major factors are already strong. Focus on consistency and sentiment quality for incremental gains.'
    : allLow
      ? `All major factors are currently low. Start with ${toLabel(nonDuplicateImprovement.feature)} and then uplift the remaining core areas.`
      : `Improving ${toLabel(nonDuplicateImprovement.feature)} can significantly increase overall satisfaction.`;

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

      {hasSentimentImpact && (
        <div className="sentiment-alert">
          <h4>Text Sentiment Impact</h4>
          <p className="text fade-in">
            Free-text reviews shift predictions by <span className="delta">
              {sentimentDelta > 0 ? '+' : ''}
              {sentimentDelta.toFixed(2)} pts
            </span>.
            {sentimentScore !== null && (
              <>
                {' '}
                ({sentimentScore > 0 ? 'Positive' : 'Negative'} sentiment)
              </>
            )}
          </p>
        </div>
      )}
    </div>
  );
}
