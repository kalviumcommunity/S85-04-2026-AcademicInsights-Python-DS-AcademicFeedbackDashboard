import { FORM_LABELS } from '../config';

export default function Sidebar({ formData, onSliderChange }) {
  return (
    <aside className="dashboard-sidebar">
      <div className="sidebar-header">
        <h2>Input Parameters</h2>
        <span className="subtitle">Real-time What-If Analysis</span>
      </div>
      
      <div className="sliders-container">
        {Object.entries(FORM_LABELS).map(([key, label]) => (
          <div key={key} className="slider-group">
            <div className="slider-header">
              <label htmlFor={key}>{label}</label>
              <span className="slider-value">
                {key.includes('sentiment') ? formData[key].toFixed(2) : formData[key]}
              </span>
            </div>
            <input
              type="range"
              id={key}
              name={key}
              min={key.includes('sentiment') ? "-1" : "1"}
              max={key.includes('sentiment') ? "1" : "5"}
              step={key.includes('sentiment') ? "0.05" : "1"}
              value={formData[key]}
              onChange={(e) => onSliderChange(key, e.target.value)}
              className="styled-range"
            />
          </div>
        ))}
      </div>
    </aside>
  );
}
