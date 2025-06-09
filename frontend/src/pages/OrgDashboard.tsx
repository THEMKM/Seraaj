import { useQuery } from '@tanstack/react-query';
import DataTable from '../components/DataTable';

interface OppRow {
  id: string;
  title: string;
  status: string;
  applicants: number;
}

export default function OrgDashboard() {
  const { data: opps = [] } = useQuery<OppRow[]>(['orgOpps'], async () => {
    const res = await fetch('/api/org/opportunities');
    if (!res.ok) return [];
    return res.json();
  });

  return (
    <div className="p-4">
      <h2 className="mb-4 text-2xl font-semibold">Organization Dashboard</h2>
      <button className="mb-4 rounded-2xl bg-brand px-4 py-2 text-white">Create Opportunity</button>
      <DataTable
        columns={[
          { key: 'title', header: 'Title' },
          { key: 'status', header: 'Status' },
          { key: 'applicants', header: '#Applicants' },
        ]}
        rows={opps}
      />
    </div>
  );
}
