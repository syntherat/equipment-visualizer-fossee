import React, { useState } from 'react';
import { Table, Search, ArrowUp, ArrowDown } from 'lucide-react';

function DataTable({ equipment }) {
  const [sortColumn, setSortColumn] = useState('equipment_name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [searchTerm, setSearchTerm] = useState('');

  if (!equipment || equipment.length === 0) {
    return null;
  }

  const sortedEquipment = [...equipment].sort((a, b) => {
    const aValue = a[sortColumn];
    const bValue = b[sortColumn];

    if (typeof aValue === 'number') {
      return sortOrder === 'asc' ? aValue - bValue : bValue - aValue;
    }

    return sortOrder === 'asc'
      ? String(aValue).localeCompare(String(bValue))
      : String(bValue).localeCompare(String(aValue));
  });

  const filteredEquipment = sortedEquipment.filter(item =>
    item.equipment_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.equipment_type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSort = (column) => {
    if (sortColumn === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortOrder('asc');
    }
  };

  const TableHeader = ({ label, column }) => (
    <th onClick={() => handleSort(column)} style={{ cursor: 'pointer', userSelect: 'none' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        {label}
        {sortColumn === column && (sortOrder === 'asc' ? <ArrowUp size={14} /> : <ArrowDown size={14} />)}
      </div>
    </th>
  );

  return (
    <div className="card" style={{ marginBottom: '20px' }}>
      <h3>
        <Table size={20} />
        Equipment Data
      </h3>

      <div className="search-bar">
        <Search size={18} style={{ color: '#64748b' }} />
        <input
          type="text"
          placeholder="Search by name or type..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      <p style={{ marginBottom: '15px', color: '#64748b', fontSize: '14px' }}>
        Showing <strong>{filteredEquipment.length}</strong> of <strong>{equipment.length}</strong> items
      </p>

      <div style={{ overflowX: 'auto' }}>
        <table className="data-table">
          <thead>
            <tr>
              <TableHeader label="Equipment Name" column="equipment_name" />
              <TableHeader label="Type" column="equipment_type" />
              <TableHeader label="Flowrate" column="flowrate" />
              <TableHeader label="Pressure" column="pressure" />
              <TableHeader label="Temperature" column="temperature" />
            </tr>
          </thead>
          <tbody>
            {filteredEquipment.map((item, idx) => (
              <tr key={item.id} style={{ animation: `fadeIn 0.3s ease-out ${idx * 0.05}s` }}>
                <td><strong>{item.equipment_name}</strong></td>
                <td>
                  <span style={{
                    background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2))',
                    padding: '4px 12px',
                    borderRadius: '20px',
                    fontSize: '13px',
                    fontWeight: '500',
                    color: '#667eea'
                  }}>
                    {item.equipment_type}
                  </span>
                </td>
                <td>{item.flowrate.toFixed(2)}</td>
                <td>{item.pressure.toFixed(2)}</td>
                <td>{item.temperature.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default DataTable;
