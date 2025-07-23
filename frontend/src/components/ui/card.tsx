export function Card({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={`rounded-2xl bg-white dark:bg-gray-800 dark:text-gray-100 ${className ?? ''}`}>{children}</div>;
}

export function CardContent({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={className}>{children}</div>;
}
