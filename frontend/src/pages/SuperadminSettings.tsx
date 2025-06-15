import { useEffect, useState } from 'react';
import { authFetch } from '../api';

interface Flags {
  alg_v2: boolean;
  referrals: boolean;
  i18n: boolean;
  oauth_un: boolean;
}

interface Health {
  db: boolean;
  redis: boolean;
  worker: boolean;
}

export default function SuperadminSettings() {
  const [flags, setFlags] = useState<Flags | null>(null);
  const [health, setHealth] = useState<Health | null>(null);

  const fetchFlags = async () => {
    const res = await authFetch('/api/settings/flags');
    if (res.ok) setFlags(await res.json());
  };

  const fetchHealth = async () => {
    const res = await authFetch('/api/settings/health');
    if (res.ok) setHealth(await res.json());
  };

  useEffect(() => {
    fetchFlags();
    fetchHealth();
  }, []);

  const toggle = async (flag: keyof Flags) => {
    const res = await authFetch(`/api/settings/flags/${flag}`, { method: 'POST' });
    if (res.ok) fetchFlags();
  };

  if (!flags || !health) return <p>Loading...</p>;

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <div className="space-y-2">
        {Object.entries(flags).map(([key, value]) => (
          <label key={key} className="flex items-center space-x-2">
            <span className="w-32">{key}</span>
            <input
              type="checkbox"
              checked={value}
              onChange={() => toggle(key as keyof Flags)}
              aria-label={key}
            />
          </label>
        ))}
      </div>
      <div className="space-x-2">
        <span className={health.db ? 'text-green-600' : 'text-red-600'}>DB {health.db ? '✓' : '✗'}</span>
        <span className={health.redis ? 'text-green-600' : 'text-red-600'}>Redis {health.redis ? '✓' : '✗'}</span>
        <span className={health.worker ? 'text-green-600' : 'text-red-600'}>Worker {health.worker ? '✓' : '✗'}</span>
        <button className="ml-4 rounded-2xl bg-brand text-white px-3 py-1" onClick={fetchHealth}>
          Refresh
        </button>
      </div>
    </div>
  );
}
