import React, { useState } from 'react';
import Loading from './Loading';
import { login } from '../api';

export default function Login({ onLogin, onSwitchToRegister }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await login(username, password);
      onLogin(res);
    } catch (err) {
      setError('Invalid credentials');
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
        <button className="btn-primary" type="submit" disabled={loading}>Login</button>
      </form>
      {loading && <Loading />}
      {error && <div style={{color:'#ff4d4f'}}>{error}</div>}
      <div style={{marginTop: '1rem'}}>
        Don't have an account?{' '}
        <button onClick={onSwitchToRegister} style={{background:'none',color:'#c084fc',border:'none',cursor:'pointer'}}>Sign Up</button>
      </div>
    </div>
  );
}
