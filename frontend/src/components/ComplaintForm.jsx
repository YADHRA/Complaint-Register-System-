import React, { useState } from 'react';
import Loading from './Loading';
import { submitComplaint } from '../api';

export default function ComplaintForm({ userId, onSubmitted }) {
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const res = await submitComplaint(userId, description);
      setResult(res);
      onSubmitted();
    } catch (err) {
      setResult({ error: 'Submission failed' });
    }
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Submit Complaint</h2>
      <form onSubmit={handleSubmit}>
        <textarea placeholder="Describe your issue..." value={description} onChange={e => setDescription(e.target.value)} required />
        <button className="btn-primary" type="submit" disabled={loading}>Submit</button>
      </form>
      {loading && <Loading />}
      {result && (
        <div>
          {result.error ? <span style={{color:'#ff4d4f'}}>{result.error}</span> :
          <div>
            <strong>Complaint ID:</strong> {result.complaint_id}<br/>
            <strong>Category:</strong> {result.category}<br/>
            <strong>Suggested Solution:</strong> {result.solution}
          </div>}
        </div>
      )}
    </div>
  );
}
