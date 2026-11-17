import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import './i18n';
import './data/local/syncOutbox';
import { API_BASE_URL } from './data/remote/apiClient';
import { db } from './data/local/db';

// Auto-migrate legacy Maharashtra/Pune keys to Mangalore
if (typeof window !== 'undefined' && window.localStorage) {
  const dist = localStorage.getItem('kabadiwala_district');
  if (dist && /pune|hadapsar|kothrud|wakad|chinchwad|maharashtra/i.test(dist)) {
    localStorage.setItem('kabadiwala_district', 'Mangalore');
  }
  const addr = localStorage.getItem('kabadiwala_collector_address');
  if (addr && /pune|hadapsar|kothrud|wakad|chinchwad|maharashtra/i.test(addr)) {
    localStorage.setItem('kabadiwala_collector_address', 'Hampankatta, Mangalore');
    localStorage.setItem('kabadiwala_collector_lat', '12.9141');
    localStorage.setItem('kabadiwala_collector_lng', '74.8560');
  }
  const recAddr = localStorage.getItem('kabadiwala_recycler_address');
  if (recAddr && /pune|hadapsar|wakad|chinchwad|maharashtra/i.test(recAddr)) {
    localStorage.setItem('kabadiwala_recycler_address', 'Baikampady Industrial Hub, Mangalore');
    localStorage.setItem('kabadiwala_recycler_lat', '12.9463');
    localStorage.setItem('kabadiwala_recycler_lng', '74.8080');
  }
  const userRaw = localStorage.getItem('kabadiwala_user');
  if (userRaw) {
    try {
      const u = JSON.parse(userRaw);
      let changed = false;
      if (u.district && /pune|hadapsar|kothrud|wakad|maharashtra/i.test(u.district)) {
        u.district = 'Mangalore';
        changed = true;
      }
      if (u.operating_locality && /pune|hadapsar|kothrud|wakad|maharashtra/i.test(u.operating_locality)) {
        u.operating_locality = 'Bunder, Mangalore';
        changed = true;
      }
      if (changed) {
        localStorage.setItem('kabadiwala_user', JSON.stringify(u));
      }
    } catch {}
  }

  // Clean legacy Maharashtra recyclers from local IndexedDB
  db.recyclers.toArray().then(items => {
    const idsToDelete = items
      .filter(r => /pune|hadapsar|mumbai|thane|nagpur|chinchwad|dharavi/i.test(r.name || '') || /pune|hadapsar|maharashtra/i.test((r as any).location || ''))
      .map(r => r.recycler_id);
    if (idsToDelete.length > 0) {
      db.recyclers.bulkDelete(idsToDelete);
    }
  }).catch(() => {});
}

const nativeFetch = window.fetch.bind(window);
window.fetch = (input, init = {}) => {
  const request = input instanceof Request ? input : null;
  const url = typeof input === 'string' ? input : request?.url || input.toString();
  const token = window.localStorage.getItem('kabadiwala_access_token');
  if (!token || !url.startsWith(API_BASE_URL)) return nativeFetch(input, init);
  const headers = new Headers(init.headers || request?.headers);
  headers.set('Authorization', `Bearer ${token}`);
  return nativeFetch(input, { ...init, headers });
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
