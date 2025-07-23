import { motion } from 'framer-motion';

export interface OpportunityCardProps {
  title: string;
  orgName: string;
  matchScore?: number;
  onApply?: () => void;
}

export default function OpportunityCard({ title, orgName, matchScore, onApply }: OpportunityCardProps) {
  return (
    <motion.div
      className="rounded-2xl bg-white dark:bg-gray-800 dark:text-gray-100 shadow-md p-4 flex flex-col justify-between"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div>
        <h4 className="text-lg font-semibold">{title}</h4>
        <p className="text-sm text-gray-600">{orgName}</p>
      </div>
      {matchScore !== undefined && (
        <span className="mt-2 text-sm text-brand font-medium">Match {Math.round(matchScore * 100)}%</span>
      )}
      {onApply && (
        <button
          className="mt-4 rounded-2xl bg-brand dark:bg-brand-dark px-4 py-2 text-white hover:bg-brand-dark focus:outline-none"
          onClick={onApply}
        >
          Apply
        </button>
      )}
    </motion.div>
  );
}
