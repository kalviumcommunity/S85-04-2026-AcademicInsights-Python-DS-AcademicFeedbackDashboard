import React from 'react';
import { render, screen } from '@testing-library/react';
import InsightsPanel from '../InsightsPanel';

describe('InsightsPanel', () => {
  test('renders without crashing when sentimentImpact is numeric', () => {
    render(
      <InsightsPanel
        topFeatures={{ teaching_score: 0.5, lab_score: 0.3 }}
        impactAnalysis={{ teaching_score: 0.1, lab_score: 0.05 }}
        formData={{ teaching_rating: 4, lab_rating: 4 }}
        sentimentImpact={0.125}
      />
    );

    expect(screen.getByText(/Free-text reviews shift predictions by/i)).toBeInTheDocument();
    expect(screen.getByText(/\+0\.13 pts/i)).toBeInTheDocument();
  });

  test('uses current contribution to choose Strength dynamically', () => {
    render(
      <InsightsPanel
        topFeatures={{ teaching_score: 0.6, lab_score: 0.4 }}
        impactAnalysis={{ teaching_score: 0.12, lab_score: 0.08 }}
        formData={{ teaching_rating: 1, lab_rating: 5 }}
        sentimentImpact={0}
      />
    );

    expect(
      screen.getByText(/Lab Score is currently the strongest actionable driver/i)
    ).toBeInTheDocument();
  });

  test('shows all-strong message when all core ratings are max', () => {
    render(
      <InsightsPanel
        topFeatures={{ extra_score: 0.5, lab_score: 0.3, teaching_score: 0.2 }}
        impactAnalysis={{ extra_score: 0.02, lab_score: 0.01, teaching_score: 0.005 }}
        formData={{
          teaching_rating: 5,
          course_rating: 5,
          exam_rating: 5,
          lab_rating: 5,
          library_rating: 5,
          extra_rating: 5,
        }}
        sentimentImpact={0}
      />
    );

    expect(
      screen.getByText(/All major factors are already strong/i)
    ).toBeInTheDocument();
  });

  test('prefers highest current ratings for Strength (not lower-rated lab)', () => {
    render(
      <InsightsPanel
        topFeatures={{ lab_score: 0.5, teaching_score: 0.25, course_score: 0.25 }}
        impactAnalysis={{ lab_score: 0.06, teaching_score: 0.01, course_score: 0.01 }}
        formData={{
          teaching_rating: 5,
          course_rating: 5,
          exam_rating: 3,
          lab_rating: 3,
          library_rating: 3,
          extra_rating: 3,
        }}
        sentimentImpact={0}
      />
    );

    expect(screen.queryByText(/Lab Score is currently the strongest actionable driver/i)).not.toBeInTheDocument();
    expect(screen.getByText(/(Teaching|Course) Score is currently the strongest actionable driver/i)).toBeInTheDocument();
  });

  test('shows low-baseline guidance when all core ratings are minimum', () => {
    render(
      <InsightsPanel
        topFeatures={{ lab_score: 0.5, teaching_score: 0.3, course_score: 0.2 }}
        impactAnalysis={{ lab_score: 0.08, teaching_score: 0.05, course_score: 0.03 }}
        formData={{
          teaching_rating: 1,
          course_rating: 1,
          exam_rating: 1,
          lab_rating: 1,
          library_rating: 1,
          extra_rating: 1,
        }}
        sentimentImpact={0}
      />
    );

    expect(screen.getByText(/No single strong area right now/i)).toBeInTheDocument();
    expect(screen.getByText(/All major factors are currently low/i)).toBeInTheDocument();
  });
});
