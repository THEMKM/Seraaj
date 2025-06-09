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
    <table className="min-w-full divide-y divide-gray-200 text-left text-sm">
      <thead className="bg-gray-50">
        <tr>
          {columns.map((col) => (
            <th key={String(col.key)} className="px-4 py-2 font-medium text-gray-700">
              {col.header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody className="divide-y divide-gray-100 bg-white">
        {rows.map((row) => (
          <tr key={row.id} className="hover:bg-gray-50">
            {columns.map((col) => (
              <td key={String(col.key)} className="px-4 py-2">
                {col.render ? col.render(row) : (row as any)[col.key as keyof T]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
