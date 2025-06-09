import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import FormField from '../components/FormField';

export default function Signup() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!email || !password) {
      setError('Email and password required');
      return;
    }
    // stub success
    navigate('/dashboard');
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50 p-4">
      <form onSubmit={handleSubmit} className="w-full max-w-sm rounded-2xl bg-white p-6 shadow-md">
        <h2 className="mb-4 text-xl font-semibold">Sign Up</h2>
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
            minLength={8}
          />
        </FormField>
        <button type="submit" className="mt-2 w-full rounded-2xl bg-brand px-4 py-2 text-white">
          Create Account
        </button>
      </form>
    </main>
  );
}
