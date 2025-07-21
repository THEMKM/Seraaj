import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import FormField from '../components/FormField';

export default function OpportunityForm() {
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (title.length < 5 || description.length < 20) return;
    navigate('/org/dashboard');
  }

  return (
    <main className="p-4">
      <form onSubmit={handleSubmit} className="max-w-xl space-y-4">
        <FormField label="Title" error={title.length < 5 ? 'Min 5 chars' : undefined}>
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full rounded border px-3 py-2"
          />
        </FormField>
        <FormField label="Description" error={description.length < 20 ? 'Min 20 chars' : undefined}>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full rounded border px-3 py-2"
            rows={4}
          />
        </FormField>
        <button type="submit" className="rounded-2xl bg-brand px-4 py-2 text-white">
          Publish
        </button>
      </form>
    </main>
  );
}
