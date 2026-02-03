import React from 'react';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import './App.css';

// Configure axios to use backend API URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
axios.defaults.baseURL = API_BASE_URL;

function App() {
  return (
    <div className="App">
      <Dashboard username="admin" onLogout={() => {}} />
    </div>
  );
}

export default App;
