import React from 'react';
import { Chart as ChartJS, ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, PointElement, LineElement } from 'chart.js';
import { Pie, Bar, Line } from 'react-chartjs-2';
import { PieChart, BarChart3, TrendingUp } from 'lucide-react';

ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, PointElement, LineElement);

function ChartsSection({ dataset }) {
  // Modern color palette
  const colors = ['#2563eb', '#1e40af', '#3b82f6', '#059669', '#d97706', '#dc2626'];

  // Pie chart for type distribution
  const pieData = {
    labels: Object.keys(dataset.type_distribution),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(dataset.type_distribution),
        backgroundColor: colors.map(c => c + 'cc'),
        borderColor: colors,
        borderWidth: 2,
      },
    ],
  };

  // Bar chart for average parameters
  const barData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [
          dataset.avg_flowrate,
          dataset.avg_pressure,
          dataset.avg_temperature,
        ],
        backgroundColor: [
          'rgba(37, 99, 235, 0.7)',
          'rgba(30, 64, 175, 0.7)',
          'rgba(59, 130, 246, 0.7)',
        ],
        borderColor: [
          '#2563eb',
          '#1e40af',
          '#3b82f6',
        ],
        borderWidth: 2,
        borderRadius: 8,
        hoverBackgroundColor: [
          'rgba(37, 99, 235, 0.9)',
          'rgba(30, 64, 175, 0.9)',
          'rgba(59, 130, 246, 0.9)',
        ],
      },
    ],
  };

  // Line chart showing distribution
  const lineData = {
    labels: Object.keys(dataset.type_distribution),
    datasets: [
      {
        label: 'Equipment Count by Type',
        data: Object.values(dataset.type_distribution),
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37, 99, 235, 0.1)',
        borderWidth: 3,
        fill: true,
        pointBackgroundColor: '#2563eb',
        pointBorderColor: '#1e40af',
        pointBorderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8,
        tension: 0.4,
      },
    ],
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: '#e2e8f0',
        },
        ticks: {
          color: '#64748b',
        },
      },
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: '#64748b',
        },
      },
    },
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          font: {
            size: 12,
            weight: 'bold',
          },
          color: '#0f172a',
        },
      },
      title: {
        display: false,
      },
    },
  };

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        labels: {
          color: '#64748b',
          font: {
            size: 12,
            weight: 'bold',
          },
        },
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: '#e2e8f0',
        },
        ticks: {
          color: '#64748b',
        },
      },
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: '#64748b',
        },
      },
    },
  };

  return (
    <div className="charts-grid">
      <div className="card">
        <h3>
          <PieChart size={20} />
          Equipment Type Distribution
        </h3>
        <div className="chart-container">
          <Pie data={pieData} options={pieOptions} />
        </div>
      </div>
      
      <div className="card">
        <h3>
          <BarChart3 size={20} />
          Average Parameter Values
        </h3>
        <div className="chart-container">
          <Bar data={barData} options={barOptions} />
        </div>
      </div>

      <div className="card">
        <h3>
          <TrendingUp size={20} />
          Equipment Count Trend
        </h3>
        <div className="chart-container">
          <Line data={lineData} options={lineOptions} />
        </div>
      </div>

      <div className="card">
        <h3>Quick Stats</h3>
        <div style={{ padding: '20px' }}>
          <div style={{ 
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '15px'
          }}>
            <div style={{
              padding: '15px',
              background: 'rgba(37, 99, 235, 0.05)',
              borderRadius: '8px',
              borderLeft: '4px solid #2563eb'
            }}>
              <p style={{ color: '#64748b', fontSize: '12px', margin: '0 0 5px 0' }}>Total Equipment</p>
              <p style={{ color: '#2563eb', fontSize: '24px', fontWeight: 'bold', margin: '0' }}>{dataset.total_count}</p>
            </div>
            <div style={{
              padding: '15px',
              background: 'rgba(5, 150, 105, 0.05)',
              borderRadius: '8px',
              borderLeft: '4px solid #059669'
            }}>
              <p style={{ color: '#64748b', fontSize: '12px', margin: '0 0 5px 0' }}>Equipment Types</p>
              <p style={{ color: '#059669', fontSize: '24px', fontWeight: 'bold', margin: '0' }}>{Object.keys(dataset.type_distribution).length}</p>
            </div>
            <div style={{
              padding: '15px',
              background: 'rgba(217, 119, 6, 0.05)',
              borderRadius: '8px',
              borderLeft: '4px solid #d97706'
            }}>
              <p style={{ color: '#64748b', fontSize: '12px', margin: '0 0 5px 0' }}>Avg Flowrate</p>
              <p style={{ color: '#d97706', fontSize: '24px', fontWeight: 'bold', margin: '0' }}>{dataset.avg_flowrate.toFixed(1)}</p>
            </div>
            <div style={{
              padding: '15px',
              background: 'rgba(59, 130, 246, 0.05)',
              borderRadius: '8px',
              borderLeft: '4px solid #3b82f6'
            }}>
              <p style={{ color: '#64748b', fontSize: '12px', margin: '0 0 5px 0' }}>Avg Pressure</p>
              <p style={{ color: '#3b82f6', fontSize: '24px', fontWeight: 'bold', margin: '0' }}>{dataset.avg_pressure.toFixed(1)}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChartsSection;
