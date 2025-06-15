import { useQuery } from "@tanstack/react-query";
import ProfileCompletionMeter from "../components/ProfileCompletionMeter";
import OpportunityCard from "../components/OpportunityCard";
import DataTable from "../components/DataTable";
import { authFetch } from "../api";

interface ApplicationRow {
  id: string;
  title: string;
  org: string;
  date: string;
  status: string;
}

export default function VolunteerDashboard() {
  interface OppRow {
    id: string;
    title: string;
    orgName: string;
  }

  const { data: opps = [] } = useQuery<OppRow[]>({
    queryKey: ["opps"],
    queryFn: async () => {
      const res = await authFetch("/api/opportunity/search?match_me=true");
      if (!res.ok) return [] as OppRow[];
      return res.json();
    },
    initialData: [],
  });

  const { data: apps = [] } = useQuery<ApplicationRow[]>({
    queryKey: ["apps"],
    queryFn: async () => {
      const res = await authFetch("/api/applications/me");
      if (!res.ok) return [] as ApplicationRow[];
      return res.json();
    },
    initialData: [],
  });

  return (
    <div className="p-4">
      <ProfileCompletionMeter percent={80} />
      <h3 className="mb-2 text-lg font-semibold">Recommended Opportunities</h3>
      <div className="grid gap-4 md:grid-cols-3">
        {opps.map((o) => (
          <OpportunityCard
            key={o.id}
            title={o.title}
            orgName={o.orgName}
            onApply={() => {}}
          />
        ))}
      </div>
      <h3 className="mt-8 mb-2 text-lg font-semibold">Recent Applications</h3>
      <DataTable
        columns={[
          { key: "title", header: "Opportunity" },
          { key: "org", header: "Organization" },
          { key: "date", header: "Applied" },
          { key: "status", header: "Status" },
        ]}
        rows={apps}
      />
    </div>
  );
}
