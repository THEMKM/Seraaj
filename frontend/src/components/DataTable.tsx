import { ReactNode } from 'react';

export interface Column<T> {
  key: keyof T | string;
  header: ReactNode;
  render?: (row: T) => ReactNode;
}

export interface DataTableProps<T> {
  columns: Column<T>[];
  rows: T[];
}

export default function DataTable<T extends { id: string | number }>({ columns, rows }: DataTableProps<T>) {
  return (
    <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700 text-left text-sm">
      <thead className="bg-gray-50 dark:bg-gray-800">
        <tr>
          {columns.map((col) => (
            <th key={String(col.key)} className="px-4 py-2 font-medium text-gray-700 dark:text-gray-300">
              {col.header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody className="divide-y divide-gray-100 dark:divide-gray-800 bg-white dark:bg-gray-900">
        {rows.map((row) => (
          <tr key={row.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
            {columns.map((col) => (
              <td key={String(col.key)} className="px-4 py-2 dark:text-gray-100">
                {col.render ? col.render(row) : String(row[col.key as keyof T])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
