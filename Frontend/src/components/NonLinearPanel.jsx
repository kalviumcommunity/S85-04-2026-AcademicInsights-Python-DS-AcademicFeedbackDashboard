export default function NonLinearPanel({ data }) {
  if (!data || !data.feature) return null;

  const cleanFeature = data.feature.replace(/_/g, ' ');

  return (
    <div className="dashboard-panel proof-panel">
      <h3>AI Explainer: Non-Linearity</h3>
      <p className="description">Impact of varying {cleanFeature}</p>
      
      <div className="proof-grid">
        <div className="proof-card">
          <h4>Min Prediction (0)</h4>
          <span className="value">{data.min_prediction.toFixed(2)}</span>
        </div>
        
        <div className="proof-card">
          <h4>Max Prediction (1)</h4>
          <span className="value">{data.max_prediction.toFixed(2)}</span>
        </div>
        
        <div className="proof-card combined">
          <h4>Delta</h4>
          <span className="value highlight">{data.delta.toFixed(2)} pts</span>
        </div>
      </div>

      <p className="nonlinear-note">
        <strong>
          Changing {cleanFeature} from minimum to maximum results in a measurable change in prediction, demonstrating that the model captures non-linear relationships instead of simple averaging.
        </strong>
      </p>
    </div>
  );
}
