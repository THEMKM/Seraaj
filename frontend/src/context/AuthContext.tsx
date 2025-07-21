import { createContext, useContext } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';

type User = { id: string; email: string; role: string };
interface AuthCtx {
  user?: User;
  isLoading: boolean;
  logout(): void;
}

const Ctx = createContext<AuthCtx>({ isLoading: true, logout: () => {} });

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const { data, isLoading, refetch } = useQuery<User>({
    queryKey: ['me'],
    queryFn: () => api.get('auth/me').json<User>(),
    retry: false,
    staleTime: 5 * 60_000,
  });

  function logout() {
    localStorage.removeItem('token');
    refetch();
  }

  return (
    <Ctx.Provider value={{ user: data, isLoading, logout }}>{children}</Ctx.Provider>
  );
};

export const useAuth = () => useContext(Ctx);
