import React, { useEffect, useState } from 'react';
import Loading from './Loading';
import { getAllComplaints, updateStatus, getAnalytics } from '../api';

export default function AdminDashboard() {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [analytics, setAnalytics] = useState({});

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setComplaints(await getAllComplaints());
      setAnalytics(await getAnalytics());
      setLoading(false);
    }
    fetchData();
  }, []);

  const handleStatusChange = async (id, status) => {
    await updateStatus(id, status);
    setComplaints(await getAllComplaints());
  };

  return (
    <div>
      <h2>Admin Dashboard</h2>
      {loading && <Loading />}
      <div className="card">
        <h3>Analytics</h3>
        <ul>
          {Object.entries(analytics).map(([cat, count]) => (
            <li key={cat}><strong>{cat}:</strong> {count}</li>
          ))}
        </ul>
      </div>
      <div className="card">
        <h3>Complaints</h3>
        <table style={{width:'100%', color:'#c54646ff'}}>
          <thead>
            <tr>
              <th>ID</th><th>User</th><th>Type</th><th>Status</th><th>Action</th>
            </tr>
          </thead>
          <tbody>
            {complaints.map(c => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.user_id}</td>
                <td>{c.type}</td>
                <td>{c.status}</td>
                <td>
                  <select value={c.status} onChange={e => handleStatusChange(c.id, e.target.value)}>
                    <option>Pending</option>
                    <option>In Progress</option>
                    <option>Resolved</option>
                    <option>Closed</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
