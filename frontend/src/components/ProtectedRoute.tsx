import { Navigate } from 'react-router-dom';
import { getToken } from '../api';
import { ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

export default function ProtectedRoute({ children }: Props) {
  const token = getToken();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
}
