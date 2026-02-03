import React from 'react';
import { BarChart3, Calendar, User, Package } from 'lucide-react';

function SummarySection({ dataset }) {
  return (
    <div className="card">
      <h3>
        <BarChart3 size={20} />
        Summary Statistics
      </h3>
      
      <div style={{
        marginBottom: '25px',
        padding: '16px',
        background: '#f8fafc',
        borderRadius: '10px',
        border: '1px solid #e2e8f0'
      }}>
        <p style={{ margin: '8px 0', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Package size={16} style={{ color: '#2563eb' }} />
          <strong>{dataset.name}</strong>
        </p>
        <p style={{ margin: '8px 0', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Calendar size={16} style={{ color: '#2563eb' }} />
          {new Date(dataset.uploaded_at).toLocaleString()}
        </p>
        <p style={{ margin: '8px 0', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <User size={16} style={{ color: '#2563eb' }} />
          {dataset.uploaded_by_username}
        </p>
      </div>
      
      <div className="summary-grid">
        <div className="summary-item">
          <div className="summary-label">Total Equipment</div>
          <div className="summary-value">{dataset.total_count}</div>
        </div>
        
        <div className="summary-item">
          <div className="summary-label">Avg Flowrate</div>
          <div className="summary-value">{dataset.avg_flowrate.toFixed(2)}</div>
        </div>
        
        <div className="summary-item">
          <div className="summary-label">Avg Pressure</div>
          <div className="summary-value">{dataset.avg_pressure.toFixed(2)}</div>
        </div>
        
        <div className="summary-item">
          <div className="summary-label">Avg Temperature</div>
          <div className="summary-value">{dataset.avg_temperature.toFixed(2)}</div>
        </div>
      </div>

      <div style={{ marginTop: '25px' }}>
        <h4 style={{ marginBottom: '15px', fontSize: '14px', fontWeight: '600', color: '#0f172a', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Equipment Type Distribution</h4>
        {Object.entries(dataset.type_distribution).map(([type, count]) => (
          <div key={type} style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '12px',
            background: '#f8fafc',
            marginBottom: '8px',
            borderRadius: '8px',
            border: '1px solid #e2e8f0',
            transition: 'all 0.3s ease',
            cursor: 'pointer'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1))';
            e.currentTarget.style.borderColor = '#667eea';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = '#f9fafb';
            e.currentTarget.style.borderColor = '#e5e7eb';
          }}>
            <span style={{ fontWeight: '500', color: '#374151' }}>{type}</span>
            <span style={{
              background: 'linear-gradient(135deg, #667eea, #764ba2)',
              color: 'white',
              padding: '4px 12px',
              borderRadius: '20px',
              fontSize: '12px',
              fontWeight: '600'
            }}>{count}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SummarySection;
