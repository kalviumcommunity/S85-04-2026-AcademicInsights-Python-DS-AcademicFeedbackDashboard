import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const percentageLabelPlugin = {
  id: 'percentageLabelPlugin',
  afterDatasetsDraw(chart) {
    const { ctx } = chart;
    const meta = chart.getDatasetMeta(0);
    const values = chart.data.datasets[0]?.data || [];

    ctx.save();
    ctx.fillStyle = '#111827';
    ctx.font = '600 12px Inter, system-ui, sans-serif';

    meta.data.forEach((bar, index) => {
      const value = Number(values[index] || 0);
      const label = `${(value * 100).toFixed(1)}%`;
      ctx.fillText(label, bar.x + 8, bar.y + 4);
    });

    ctx.restore();
  },
};

export default function FeatureChart({ data = {} }) {
  const sortedEntries = Object.entries(data).sort((a, b) => b[1] - a[1]);
  const labels = sortedEntries.map(([feature]) => feature.replace(/_/g, ' '));
  const values = sortedEntries.map(([, importance]) => Number(importance || 0));

  const topLabel = labels[0] || 'N/A';
  const backgroundColors = values.map((_, i) =>
    i === 0 ? 'rgba(245, 158, 11, 0.75)' : 'rgba(79, 70, 229, 0.5)'
  );
  const borderColors = values.map((_, i) =>
    i === 0 ? '#D97706' : '#4F46E5'
  );

  const options = {
    indexAxis: 'y',
    elements: { bar: { borderWidth: 2 } },
    responsive: true,
    plugins: {
      legend: { display: false },
      title: { display: true, text: 'Feature Importance (Gradient Boosting)' },
      tooltip: {
        callbacks: {
          label: (ctx) => `${(Number(ctx.raw || 0) * 100).toFixed(2)}% influence`,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          callback: (value) => `${(Number(value) * 100).toFixed(0)}%`,
        },
      },
    },
  };

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Relative Importance Score',
        data: values,
        borderColor: borderColors,
        backgroundColor: backgroundColors,
      },
    ],
  };

  return (
    <div className="dashboard-panel chart-panel">
      <div className="card-header">
        <h3>
          Key Drivers (Current Scenario)
          <span className="info-tooltip" title="Shows how much each factor influences prediction.">
            ⓘ
          </span>
        </h3>
      </div>
      <p className="most-influential">Most Influential Factor: <strong>{topLabel}</strong></p>
      <div className="chart-container">
        <Bar options={options} data={chartData} plugins={[percentageLabelPlugin]} />
      </div>
    </div>
  );
}
