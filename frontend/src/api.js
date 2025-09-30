const API = 'http://localhost:5000/api';

export async function login(username, password) {
  const res = await fetch(`${API}/auth/login`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({username, password})
  });
  if (!res.ok) throw new Error('Login failed');
  return await res.json();
}

export async function register(username, password) {
  const res = await fetch(`${API}/auth/register`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({username, password})
  });
  if (!res.ok) throw new Error('Register failed');
  return await res.json();
}

export async function submitComplaint(user_id, description) {
  const res = await fetch(`${API}/complaints/`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({user_id, description})
  });
  if (!res.ok) throw new Error('Complaint failed');
  return await res.json();
}

export async function getAllComplaints() {
  const res = await fetch(`${API}/admin/complaints`);
  return await res.json();
}

export async function updateStatus(complaint_id, status) {
  await fetch(`${API}/admin/update_status`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({complaint_id, status})
  });
}

export async function getAnalytics() {
  const res = await fetch(`${API}/admin/analytics`);
  return await res.json();
}
