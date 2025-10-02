import React, { useState } from 'react';
import { register } from '../api';
import Loading from './Loading';

export default function Register({ onRegister, onSwitchToLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await register(username, password);
      onRegister();
    } catch (err) {
      setError('Registration failed');
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        <button className="btn-primary" type="submit" disabled={loading}>Register</button>
      </form>
      {loading && <Loading />}
      {error && <div style={{color:'#ff4d4f'}}>{error}</div>}
      <div style={{marginTop: '1rem'}}>
        Already have an account?{' '}
        <button onClick={onSwitchToLogin} style={{background:'none',color:'#c084fc',border:'none',cursor:'pointer'}}>Login</button>
      </div>
    </div>
  );
}
