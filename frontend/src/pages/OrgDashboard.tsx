import { useQuery } from "@tanstack/react-query";
import DataTable from "../components/DataTable";
import { authFetch } from "../api";
import { useNavigate } from "react-router-dom";

interface OppRow {
  id: string;
  title: string;
  status: string;
  applicants: number;
}

export default function OrgDashboard() {
  const navigate = useNavigate();
  const { data: opps = [] } = useQuery<OppRow[]>({
    queryKey: ["orgOpps"],
    queryFn: async () => {
      const res = await authFetch("/api/org/opportunities");
      if (res.status === 401) {
        localStorage.removeItem('token');
        navigate('/login');
        return [] as OppRow[];
      }
      if (!res.ok) return [] as OppRow[];
      return res.json();
    },
    initialData: [],
  });

  return (
    <div className="p-4">
      <h2 className="mb-4 text-2xl font-semibold">Organization Dashboard</h2>
      <button className="mb-4 rounded-2xl bg-brand px-4 py-2 text-white">
        Create Opportunity
      </button>
      <DataTable
        columns={[
          { key: "title", header: "Title" },
          { key: "status", header: "Status" },
          { key: "applicants", header: "#Applicants" },
        ]}
        rows={opps}
      />
    </div>
  );
}
