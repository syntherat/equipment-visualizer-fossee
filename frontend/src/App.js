import React from 'react';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import './App.css';

// Configure axios defaults
axios.defaults.withCredentials = true;

function App() {
  return (
    <div className="App">
      <Dashboard username="admin" onLogout={() => {}} />
    </div>
  );
}

export default App;
