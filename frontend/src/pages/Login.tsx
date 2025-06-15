import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import FormField from '../components/FormField';
import { login as apiLogin } from '../api';

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!email || !password) {
      setError('Email and password required');
      return;
    }
    try {
      await apiLogin(email, password);
      navigate('/dashboard');
    } catch {
      setError('Invalid credentials');
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50 p-4">
      <form onSubmit={handleSubmit} className="w-full max-w-sm rounded-2xl bg-white p-6 shadow-md">
        <h2 className="mb-4 text-xl font-semibold">Log In</h2>
        <button type="button" className="mb-4 w-full rounded-2xl bg-red-500 px-4 py-2 text-white" aria-label="Continue with Google">
          Continue with Google
        </button>
        <FormField label="Email" error={!email && error ? 'Required' : undefined}>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded border px-3 py-2"
            required
          />
        </FormField>
        <FormField label="Password" error={!password && error ? 'Required' : undefined}>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded border px-3 py-2"
            required
          />
        </FormField>
        <button type="submit" className="mt-2 w-full rounded-2xl bg-brand px-4 py-2 text-white">
          Log In
        </button>
        {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      </form>
    </main>
  );
}
