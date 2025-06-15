import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import OpportunityCard from "../components/OpportunityCard";
import { authFetch } from "../api";

export default function OpportunityDetail() {
  const { id } = useParams();

  interface OppDetail {
    title: string;
    orgName: string;
    description: string;
    matchScore?: number;
  }

  const { data } = useQuery<OppDetail | null>({
    queryKey: ["opp", id],
    queryFn: async () => {
      const res = await authFetch(`/api/opportunity/${id}`);
      if (!res.ok) return null;
      return res.json();
    },
  });

  if (!data) return <p className="p-4">Loading...</p>;

  return (
    <div className="p-4 md:flex md:gap-8">
      <div className="md:flex-1">
        <h2 className="mb-2 text-2xl font-semibold">{data.title}</h2>
        <p className="mb-4 text-gray-600">{data.description}</p>
        <button className="rounded-2xl bg-brand px-4 py-2 text-white">
          Apply Now
        </button>
      </div>
      <aside className="mt-8 md:mt-0 md:w-1/3">
        <OpportunityCard
          title={data.title}
          orgName={data.orgName}
          matchScore={data.matchScore}
        />
      </aside>
    </div>
  );
}
