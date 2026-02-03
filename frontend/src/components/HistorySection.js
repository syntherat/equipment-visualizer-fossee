import React, { useState } from 'react';
import { Clock, Package } from 'lucide-react';

function HistorySection({ history, onSelectDataset }) {
  const [hoveredId, setHoveredId] = useState(null);

  return (
    <div className="card">
      <h3>
        <Clock size={20} />
        Recent Uploads
      </h3>
      
      {history.length === 0 ? (
        <div className="empty-state" style={{ padding: '40px 20px' }}>
          <Package className="empty-state-icon" size={48} />
          <h3>No datasets yet</h3>
          <p>Upload a CSV file to get started</p>
        </div>
      ) : (
        <ul className="history-list">
          {history.slice(0, 5).map((item, idx) => (
            <li
              key={item.id}
              className="history-item"
              onClick={() => onSelectDataset(item.id)}
              onMouseEnter={() => setHoveredId(item.id)}
              onMouseLeave={() => setHoveredId(null)}
              style={{
                animation: `fadeIn 0.3s ease-out ${idx * 0.05}s`
              }}
            >
              <div style={{ flex: 1 }}>
                <h4>{item.name}</h4>
                <p>{new Date(item.uploaded_at).toLocaleString()}</p>
                <p>{item.total_count} items</p>
              </div>
              <div style={{
                background: '#2563eb',
                color: 'white',
                padding: '8px 16px',
                borderRadius: '8px',
                fontSize: '12px',
                fontWeight: '600',
                whiteSpace: 'nowrap',
                marginLeft: '10px'
              }}>
                View
              </div>
            </li>
          ))}
          {history.length > 5 && (
            <p style={{ textAlign: 'center', color: '#9ca3af', fontSize: '13px', marginTop: '15px' }}>
              +{history.length - 5} more
            </p>
          )}
        </ul>
      )}
    </div>
  );
}

export default HistorySection;
