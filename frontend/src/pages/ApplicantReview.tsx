import { useQuery } from '@tanstack/react-query';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import { useState } from 'react';

interface ApplicantRow {
  id: string;
  name: string;
  email: string;
  match: number;
  status: string;
}

export default function ApplicantReview() {
  const [selected, setSelected] = useState<ApplicantRow | null>(null);
  const { data: applicants = [] } = useQuery<ApplicantRow[]>(['apps'], async () => {
    const res = await fetch('/api/applicants');
    if (!res.ok) return [];
    return res.json();
  });

  return (
    <div className="p-4">
      <h2 className="mb-4 text-2xl font-semibold">Applicants</h2>
      <DataTable
        columns={[
          { key: 'name', header: 'Name' },
          { key: 'email', header: 'Email' },
          { key: 'match', header: 'Match %', render: (r) => `${Math.round(r.match * 100)}%` },
          {
            key: 'status',
            header: 'Actions',
            render: (r) => (
              <div className="space-x-2">
                <button className="rounded bg-brand px-2 py-1 text-white" onClick={() => setSelected(r)}>Share Recognition</button>
              </div>
            ),
          },
        ]}
        rows={applicants}
      />
      <Modal open={!!selected} onClose={() => setSelected(null)}>
        <h3 className="mb-2 text-lg font-semibold">Share Recognition</h3>
        {selected && <p>{selected.name}</p>}
        <button className="mt-4 rounded-2xl bg-brand px-4 py-2 text-white" onClick={() => setSelected(null)}>
          Close
        </button>
      </Modal>
    </div>
  );
}
