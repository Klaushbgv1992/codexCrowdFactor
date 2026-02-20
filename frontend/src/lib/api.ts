import { API_URL } from './constants';

export async function fetchCurrent() {
  const res = await fetch(`${API_URL}/api/crowd/current`, { cache: 'no-store' });
  return res.json();
}

export async function fetchHistory(hours = 12) {
  const res = await fetch(`${API_URL}/api/crowd/history?hours=${hours}`, { cache: 'no-store' });
  return res.json();
}
