const API_BASE = import.meta.env.VITE_API_URL || '/api';
const SESSION_KEY = 'health-ai-session-id';

export function getSessionId() {
  return sessionStorage.getItem(SESSION_KEY);
}

export function setSessionId(id) {
  sessionStorage.setItem(SESSION_KEY, id);
}

export function clearSessionId() {
  sessionStorage.removeItem(SESSION_KEY);
}

async function handleResponse(response) {
  if (response.ok) {
    const sessionId = response.headers.get('X-Session-Id');
    if (sessionId) setSessionId(sessionId);
    const data = await response.json();
    return { data, error: null };
  }

  try {
    const body = await response.json();
    return { data: null, error: body.detail || `Request failed (${response.status})` };
  } catch {
    return { data: null, error: `Request failed (${response.status})` };
  }
}

function buildHeaders(json = false) {
  const headers = {};
  const sid = getSessionId();
  if (sid) headers['X-Session-Id'] = sid;
  if (json) headers['Content-Type'] = 'application/json';
  return headers;
}

export async function apiGet(path) {
  try {
    const res = await fetch(`${API_BASE}${path}`, { headers: buildHeaders() });
    return handleResponse(res);
  } catch {
    return { data: null, error: 'Backend is not reachable.' };
  }
}

export async function apiPost(path, body) {
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: buildHeaders(true),
      body: JSON.stringify(body),
    });
    return handleResponse(res);
  } catch {
    return { data: null, error: 'Backend is not reachable.' };
  }
}

export async function apiUploadFile(path, file) {
  try {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: buildHeaders(false),
      body: formData,
    });
    return handleResponse(res);
  } catch {
    return { data: null, error: 'Backend is not reachable.' };
  }
}
