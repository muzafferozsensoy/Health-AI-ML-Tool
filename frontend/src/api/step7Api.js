import { apiGet, apiPost, getSessionId } from './client';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

/**
 * Run subgroup bias analysis on test data.
 */
export async function getBiasAnalysis() {
  return apiGet('/step7/bias-analysis');
}

/**
 * Compare training data demographics against real-world reference population.
 */
export async function getPopulationComparison() {
  return apiGet('/step7/population-comparison');
}

/**
 * Generate and download a PDF certificate.
 * @param {boolean[]} checklistStatus - Array of 8 boolean values
 * @param {string} domain - Current domain ID
 * @param {string} modelName - Backend model ID
 */
export async function generateCertificate(checklistStatus, domain, modelName) {
  const sessionId = getSessionId();
  const headers = { 'Content-Type': 'application/json' };
  if (sessionId) headers['X-Session-Id'] = sessionId;

  try {
    const res = await fetch(`${API_BASE}/step7/generate-certificate`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        checklist_status: checklistStatus,
        domain,
        model_name: modelName,
      }),
    });

    if (!res.ok) {
      let detail = `Request failed (${res.status})`;
      try {
        const body = await res.json();
        detail = body.detail || detail;
      } catch {}
      return { blob: null, error: detail };
    }

    const blob = await res.blob();
    return { blob, error: null };
  } catch {
    return { blob: null, error: 'Backend is not reachable.' };
  }
}
