import { useState, useEffect } from 'react';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import SummaryCards from './SummaryCards';
import FeatureChart from './FeatureChart';
import ImpactPanel from './ImpactPanel';
import NonLinearPanel from './NonLinearPanel';
import InsightsPanel from './InsightsPanel';
import { INITIAL_FORM } from '../config';
import { predictSatisfaction } from '../api';

function buildFeatureChartData(result) {
  const topFeatures = result?.top_features || {};
  if (Object.keys(topFeatures).length > 0) return topFeatures;

  const impact = result?.impact_analysis || {};
  const impactEntries = Object.entries(impact)
    .filter(([feature]) => !feature.includes('sentiment') && !feature.includes('comment'))
    .map(([feature, delta]) => [feature, Math.abs(Number(delta || 0))])
    .filter(([, value]) => value > 0);

  const total = impactEntries.reduce((sum, [, value]) => sum + value, 0);
  if (impactEntries.length === 0 || total <= 0) return {};

  const normalized = {};
  for (const [feature, value] of impactEntries) {
    normalized[feature] = Number((value / total).toFixed(6));
  }
  return normalized;
}

export default function Dashboard() {
  const [formData, setFormData] = useState(INITIAL_FORM);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Auto-fetch when form changes
  useEffect(() => {
    let active = true;
    const fetchPrediction = async () => {
      setLoading(true);
      setError(null);
      try {
        const toUnit = (value) => (Number(value) - 1) / 4.0;
        const toSentimentUnit = (value) => (Number(value) + 1) / 2.0;

        const normalizedRatings = {
          teaching_rating: toUnit(formData.teaching_rating),
          course_rating: toUnit(formData.course_rating),
          exam_rating: toUnit(formData.exam_rating),
          lab_rating: toUnit(formData.lab_rating),
          library_rating: toUnit(formData.library_rating),
          extra_rating: toUnit(formData.extra_rating),
        };

        // Keep engineered score features in sync with rating sliders
        const normalizedScores = {
          teaching_score: normalizedRatings.teaching_rating,
          course_score: normalizedRatings.course_rating,
          exam_score: normalizedRatings.exam_rating,
          lab_score: normalizedRatings.lab_rating,
          library_score: normalizedRatings.library_rating,
          extra_score: normalizedRatings.extra_rating,
        };

        const teachingSent = toSentimentUnit(formData.teaching_comment_sentiment);
        const courseSent = toSentimentUnit(formData.course_comment_sentiment);
        const avgSent = (teachingSent + courseSent) / 2;

        // Backend expects all sentiment columns; mirror available sliders for missing domains
        const normalizedSentiments = {
          teaching_comment_sentiment: teachingSent,
          course_comment_sentiment: courseSent,
          exam_comment_sentiment: avgSent,
          lab_comment_sentiment: avgSent,
          library_comment_sentiment: avgSent,
          extra_comment_sentiment: avgSent,
        };

        const payload = {
          ...normalizedRatings,
          ...normalizedScores,
          ...normalizedSentiments,
        };

        const data = await predictSatisfaction(payload);
        if (active) setResult(data);
      } catch (err) {
        if (active) setError(err.message || 'Error fetching prediction');
      } finally {
        if (active) setLoading(false);
      }
    };
    
    // add small debounce so it doesn't spam backend while dragging
    const timer = setTimeout(() => {
      fetchPrediction();
    }, 200);

    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [formData]);

  const handleSliderChange = (key, value) => {
    setFormData((prev) => ({ ...prev, [key]: Number(value) }));
  };

  return (
    <div className="app-container">
      <Sidebar formData={formData} onSliderChange={handleSliderChange} />
      
      <div className="main-content">
        <Navbar title="AI-Powered Academic Analytics" />
        
        <main className="dashboard-layout">
          {error && <div className="error-banner">⚠️ {error}</div>}
          
          <div className="scroll-wrapper">
            {loading && !result && <div className="loading-state">Analyzing relationships...</div>}
            
            {result && (
              <div className="dashboard-grid">
                <SummaryCards data={result} />
                
                <div className="panel-row split">
                  <FeatureChart data={buildFeatureChartData(result)} />
                  <ImpactPanel data={result.impact_analysis || {}} basePrediction={result.predicted_score} />
                </div>

                <div className="panel-row split">
                  <NonLinearPanel data={result.non_linear_test} />
                  <InsightsPanel 
                    topFeatures={result.top_features || {}}
                    impactAnalysis={result.impact_analysis || {}}
                    formData={formData}
                    sentimentImpact={result.sentiment_impact}
                    strengthFeature={result.top_feature || result.most_important_feature}
                  />
                </div>

                <p className="dashboard-tagline">
                  AI-powered decision system for measuring and improving student satisfaction
                </p>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
