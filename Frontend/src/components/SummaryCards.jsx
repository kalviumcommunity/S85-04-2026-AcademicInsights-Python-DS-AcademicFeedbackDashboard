export default function SummaryCards({ data }) {
  const {
    predicted_score = 0,
    average_score = 0,
    difference_from_average = 0,
    most_important_feature = '',
  } = data;

  const isAboveAverage = difference_from_average >= 0;
  const scaleMax = Math.max(predicted_score, average_score) <= 1.05 ? 1 : 5;
  const topFeatureLabel = (most_important_feature || 'lab_score').replace(/_/g, ' ');

  return (
    <div className="summary-cards">
      <div className="dashboard-panel hero-card">
        <div className="card-header">
          <h3>Predicted Satisfaction</h3>
          <span className="tooltip">🎯 Gradient Boosting Confidence</span>
        </div>
        <div className="metric">
          <span className="value primary">{predicted_score.toFixed(2)}</span>
          <span className="unit">/ {scaleMax.toFixed(1)}</span>
        </div>
        <div className="trend">
          <span className={isAboveAverage ? 'positive' : 'negative'}>
            {isAboveAverage ? '▲' : '▼'} {Math.abs(difference_from_average).toFixed(2)} vs Average
          </span>
          <p className="subtext">({average_score.toFixed(2)} base mean)</p>
        </div>

        <p className="prediction-explainer">
          This prediction is generated using a Gradient Boosting model that learns complex relationships between academic factors. Unlike simple averaging, the model assigns different importance to each feature.
        </p>
      </div>

      <div className="dashboard-panel comparison-card">
        <div className="card-header">
          <h3>Average vs Model</h3>
          <span className={`delta-badge ${isAboveAverage ? 'up' : 'down'}`}>
            {isAboveAverage ? 'Model Above Average' : 'Model Below Average'}
          </span>
        </div>

        <div className="comparison-grid">
          <div className="comparison-item">
            <span className="label">Average Score</span>
            <span className="value">{average_score.toFixed(2)}</span>
          </div>
          <div className="comparison-item">
            <span className="label">Model Prediction</span>
            <span className="value">{predicted_score.toFixed(2)}</span>
          </div>
          <div className="comparison-item">
            <span className="label">Difference</span>
            <span className={`value ${isAboveAverage ? 'positive' : 'negative'}`}>
              {difference_from_average >= 0 ? '+' : ''}
              {difference_from_average.toFixed(2)}
            </span>
          </div>
        </div>

        <p className="comparison-note">
          Model prediction differs from simple average due to learned feature importance.
        </p>

        <p className={`average-reason ${isAboveAverage ? 'above' : 'below'}`}>
          {isAboveAverage
            ? `The score is above average due to strong performance in high-impact features like ${topFeatureLabel}.`
            : `The score is below average primarily due to lower values in high-impact features such as ${topFeatureLabel}.`}
        </p>
      </div>
    </div>
  );
}
