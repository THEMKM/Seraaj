export interface ProfileCompletionMeterProps {
  percent: number;
}

export default function ProfileCompletionMeter({ percent }: ProfileCompletionMeterProps) {
  const pct = Math.min(100, Math.max(0, percent));
  return (
    <div className="my-4">
      <div className="mb-1 text-sm">Profile {pct}% complete</div>
      <div className="h-2 w-full rounded bg-gray-200">
        <div
          className="h-2 rounded bg-brand"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
