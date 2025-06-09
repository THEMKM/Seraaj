import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import OpportunityCard from '../components/OpportunityCard';

export default function Opportunities() {
  const [keywords, setKeywords] = useState('');
  const { data: results = [] } = useQuery(['search', keywords], async () => {
    const params = new URLSearchParams({ q: keywords });
    const res = await fetch(`/api/opportunity/search?${params.toString()}`);
    if (!res.ok) return [];
    return res.json();
  });

  return (
    <main className="p-4">
      <div className="mb-4 flex gap-2">
        <input
          type="text"
          placeholder="Search"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          className="flex-1 rounded border px-3 py-2"
        />
      </div>
      {results.length === 0 ? (
        <p>No matches—try broadening your skills filter.</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-3">
          {results.map((o: any) => (
            <OpportunityCard key={o.id} title={o.title} orgName={o.orgName} />
          ))}
        </div>
      )}
    </main>
  );
}
