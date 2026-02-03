import React, { useState } from 'react';
import axios from 'axios';
import { Upload, CheckCircle, AlertCircle } from 'lucide-react';

function UploadSection({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError('');
      setSuccess('');
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
    setSuccess('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess('File uploaded and analyzed successfully');
      setFile(null);
      document.getElementById('file-input').value = '';
      
      setTimeout(() => {
        onUploadSuccess(response.data.data);
      }, 500);
    } catch (error) {
      setError(error.response?.data?.error || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-section">
      <h2>
        <Upload size={20} style={{ display: 'inline-block', marginRight: '8px', verticalAlign: 'middle' }} />
        Upload CSV File
      </h2>
      
      {error && (
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '12px',
          background: '#fee2e2',
          border: '1px solid #fca5a5',
          color: '#991b1b',
          padding: '12px 16px',
          borderRadius: '8px',
          marginBottom: '16px'
        }}>
          <AlertCircle size={18} />
          {error}
        </div>
      )}
      {success && (
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '12px',
          background: '#dcfce7',
          border: '1px solid #86efac',
          color: '#166534',
          padding: '12px 16px',
          borderRadius: '8px',
          marginBottom: '16px'
        }}>
          <CheckCircle size={18} />
          {success}
        </div>
      )}
      
      <form onSubmit={handleUpload}>
        <div 
          className={`drag-drop-area ${dragActive ? 'active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            id="file-input"
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={uploading}
            className="file-input"
          />
          <label 
            htmlFor="file-input"
            style={{ cursor: 'pointer', display: 'block' }}
          >
            <Upload className="drag-drop-icon" size={48} />
            {file ? (
              <div>
                <p style={{ fontSize: '16px', fontWeight: '600', color: '#059669', margin: '8px 0' }}>
                  {file.name}
                </p>
                <p style={{ fontSize: '12px', color: '#64748b' }}>
                  {(file.size / 1024).toFixed(2)} KB
                </p>
              </div>
            ) : (
              <div>
                <p style={{ fontSize: '16px', fontWeight: '600', color: '#0f172a', margin: '8px 0' }}>
                  {dragActive ? 'Drop your CSV file here' : 'Drag & drop your CSV file'}
                </p>
                <p style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>
                  or click to select
                </p>
              </div>
            )}
          </label>
        </div>
        
        <button 
          type="submit" 
          className="btn btn-primary" 
          disabled={uploading || !file}
          style={{ marginTop: '20px', width: '100%' }}
        >
          <Upload size={16} />
          {uploading ? 'Uploading...' : 'Upload & Analyze'}
        </button>
      </form>
      
      <div style={{ marginTop: '20px', padding: '16px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
        <p style={{ color: '#0f172a', fontSize: '13px', fontWeight: '600', margin: '0 0 10px 0' }}>
          Required CSV columns:
        </p>
        <ul style={{ color: '#64748b', fontSize: '13px', marginLeft: '20px', marginTop: '8px', margin: '0' }}>
          <li>Equipment Name</li>
          <li>Type</li>
          <li>Flowrate</li>
          <li>Pressure</li>
          <li>Temperature</li>
        </ul>
      </div>
    </div>
  );
}

export default UploadSection;
