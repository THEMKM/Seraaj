import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';
import { api } from '../lib/api';

export default function Messages() {
  const qc = useQueryClient();
  const { data: conversations = [] } = useQuery({
    queryKey: ['conversations'],
    queryFn: () => api.get('conversation').json<any[]>(),
  });
  const [active, setActive] = useState<string | null>(
    conversations[0]?.id ?? null,
  );
  const { data: msgs = [] } = useQuery({
    queryKey: ['msgs', active],
    enabled: !!active,
    queryFn: () => api.get(`conversation/${active}/messages`).json<any[]>(),
  });
  const [content, setContent] = useState('');
  const send = useMutation({
    mutationFn: () =>
      api
        .post(`conversation/${active}/message`, { json: { content } })
        .json(),
    onSuccess: () => {
      setContent('');
      qc.invalidateQueries({ queryKey: ['msgs', active] });
    },
  });
  return (
    <div className="grid grid-cols-[200px_1fr] h-full">
      <aside className="border-r pr-4">
        <h3 className="font-semibold mb-2">Conversations</h3>
        <ul className="space-y-1">
          {conversations.map((c) => (
            <li key={c.id}>
              <button
                className={`${
                  active === c.id ? 'font-bold' : ''
                } underline`}
                onClick={() => setActive(c.id)}
              >
                {c.id.slice(0, 8)}
              </button>
            </li>
          ))}
        </ul>
      </aside>
      <div className="p-2 flex flex-col h-full">
        <div className="flex-1 overflow-y-auto space-y-2">
          {msgs.map((m) => (
            <div key={m.id} className="border rounded p-1">
              {m.content}
            </div>
          ))}
        </div>
        {active && (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              send.mutate();
            }}
            className="mt-2 flex gap-2"
          >
            <input
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="border px-2 py-1 flex-1"
            />
            <button
              type="submit"
              className="bg-brand text-white px-3 rounded"
              disabled={send.isLoading}
            >
              Send
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
