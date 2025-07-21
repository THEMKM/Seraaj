import { Link, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut } from 'lucide-react';
import { motion } from 'framer-motion';

export default function AppLayout() {
  const { user, logout } = useAuth();
  return (
    <div className="h-full grid grid-cols-[240px_1fr]">
      <aside className="bg-brand text-white flex flex-col p-4">
        <span className="font-bold text-xl mb-6">Seraaj</span>
        <nav className="space-y-2">
          <Link to="/dashboard" className="hover:underline">
            Dashboard
          </Link>
          <Link to="/matches" className="hover:underline">
            Matches
          </Link>
        </nav>
        <button
          onClick={logout}
          className="mt-auto flex items-center gap-2 hover:opacity-80"
        >
          <LogOut size={18} /> Logout
        </button>
      </aside>

      <motion.main
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.25 }}
        className="p-6 overflow-y-auto"
      >
        <Outlet />
      </motion.main>
    </div>
  );
}
