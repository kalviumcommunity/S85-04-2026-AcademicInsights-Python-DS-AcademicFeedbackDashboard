import React from 'react';
import { render, screen } from '@testing-library/react';
import ImpactPanel from '../ImpactPanel';

describe('ImpactPanel', () => {
  test('shows no significant impact for near-zero deltas', () => {
    render(
      <ImpactPanel
        data={{ course_score: 0.0, lab_score: 0.0001 }}
        basePrediction={0.65}
      />
    );

    expect(screen.getAllByText(/No significant impact/i).length).toBeGreaterThan(0);
  });

  test('shows impact explanation subtitle', () => {
    render(
      <ImpactPanel
        data={{ extra_score: 0.08 }}
        basePrediction={0.65}
      />
    );

    expect(
      screen.getByText(/Impact shows how much score improves if a feature is maximized/i)
    ).toBeInTheDocument();
  });
});
