import React from 'react';
import { render, screen } from '@testing-library/react';
import SummaryCards from '../SummaryCards';

describe('SummaryCards', () => {
  test('renders prediction, average and difference values', () => {
    render(
      <SummaryCards
        data={{
          predicted_score: 0.83,
          average_score: 0.81,
          difference_from_average: 0.02,
          most_important_feature: 'extra_score',
        }}
      />
    );

    expect(screen.getByText(/Predicted Satisfaction/i)).toBeInTheDocument();
    expect(screen.getByText(/Average vs Model/i)).toBeInTheDocument();
    expect(screen.getByText(/\+0\.02/i)).toBeInTheDocument();
  });
});
