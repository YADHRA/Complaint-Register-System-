import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import ComplaintForm from './components/ComplaintForm';
import AdminDashboard from './components/AdminDashboard';

export default function App() {
  const [user, setUser] = useState(null);
  const [showRegister, setShowRegister] = useState(false);

  if (!user) {
    return showRegister
      ? <Register onRegister={() => setShowRegister(false)} onSwitchToLogin={() => setShowRegister(false)} />
      : <Login onLogin={setUser} onSwitchToRegister={() => setShowRegister(true)} />;
  }

  if (user.role === 'admin') {
    return <AdminDashboard />;
  }

  return (
    <div>
      <h1>Student Complaint System</h1>
      <ComplaintForm userId={user.user_id} onSubmitted={() => {}} />
      <button className="btn-primary" onClick={() => setUser(null)}>Logout</button>
    </div>
  );
}
