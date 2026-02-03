import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Download, BarChart3 } from 'lucide-react';
import UploadSection from './UploadSection';
import SummarySection from './SummarySection';
import ChartsSection from './ChartsSection';
import DataTable from './DataTable';
import HistorySection from './HistorySection';

// Main dashboard component - orchestrates all sub-components
// Manages state for current dataset, history, and loading
function Dashboard({ username, onLogout }) {
  const [currentDataset, setCurrentDataset] = useState(null);  // Currently displayed dataset
  const [history, setHistory] = useState([]);  // List of last 5 uploaded datasets
  const [loading, setLoading] = useState(false);  // Loading state while fetching data

  // Load history on component mount
  useEffect(() => {
    fetchHistory();
  }, []);

  // Fetch list of previously uploaded datasets
  const fetchHistory = async () => {
    try {
      const response = await axios.get('/api/history/');
      const historyData = response.data;
      setHistory(historyData);

      if (currentDataset) {
        const exists = historyData.some((ds) => ds.id === currentDataset.id);
        if (!exists) {
          if (historyData.length > 0) {
            try {
              const latest = historyData[0];
              const latestResponse = await axios.get(`/api/summary/${latest.id}/`);
              setCurrentDataset(latestResponse.data);
            } catch (err) {
              setCurrentDataset(null);
            }
          } else {
            setCurrentDataset(null);
          }
        }
      }
    } catch (error) {
      console.error('Failed to fetch history:', error);
    }
  };

  // Called when user uploads new CSV file - updates current dataset and refreshes history
  const handleUploadSuccess = (dataset) => {
    setCurrentDataset(dataset);
    fetchHistory();  // Refresh history list after new upload
  };

  // Load a previously uploaded dataset by ID - called when user selects from history
  const handleSelectDataset = async (datasetId) => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/summary/${datasetId}/`);
      setCurrentDataset(response.data);
    } catch (error) {
      console.error('Failed to fetch dataset:', error);
    } finally {
      setLoading(false);
    }
  };

  // Generate and download PDF report for current dataset
  const handleDownloadPDF = async () => {
    if (!currentDataset) return;
    
    try {
      const response = await axios.get(`/api/report/${currentDataset.id}/`, {
        responseType: 'blob'  // Get binary PDF data
      });
      
      // Create temporary download link and trigger download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${currentDataset.id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      if (error.response?.status === 404) {
        fetchHistory();
      }
      console.error('Failed to download PDF:', error);
    }
  };

  // Extract first character of username for avatar display
  const getInitial = (name) => {
    return name ? name.charAt(0).toUpperCase() : 'U';
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Equipment Visualizer</h1>
        <div className="user-info">
          <span>Welcome, <strong>{username}</strong></span>
          <div className="user-avatar">{getInitial(username)}</div>
        </div>
      </div>

      <UploadSection onUploadSuccess={handleUploadSuccess} />

      {loading && (
        <div style={{ textAlign: 'center', padding: '40px 20px' }}>
          <p style={{ marginTop: '20px', color: '#2563eb', fontWeight: '600' }}>Loading dataset...</p>
        </div>
      )}

      {currentDataset && !loading && (
        <>
          <div className="content-grid">
            <SummarySection dataset={currentDataset} />
            <HistorySection 
              history={history} 
              onSelectDataset={handleSelectDataset}
            />
          </div>

          <ChartsSection dataset={currentDataset} />
          
          <DataTable equipment={currentDataset.equipment} />

          <div className="card" style={{ marginTop: '30px' }}>
            <button className="btn btn-success" onClick={handleDownloadPDF}>
              <Download size={16} />
              Download PDF Report
            </button>
          </div>
        </>
      )}

      {!currentDataset && !loading && (
        <div className="empty-state">
          <BarChart3 size={64} className="empty-state-icon" />
          <h3>No data yet</h3>
          <p>Upload a CSV file to begin equipment analysis</p>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
