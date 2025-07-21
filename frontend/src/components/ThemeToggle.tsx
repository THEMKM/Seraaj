import { useEffect, useState } from 'react';

export default function ThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem('dark') === 'true';
    setDark(stored);
    document.documentElement.classList.toggle('dark', stored);
  }, []);

  const toggle = () => {
    const newVal = !dark;
    setDark(newVal);
    document.documentElement.classList.toggle('dark', newVal);
    localStorage.setItem('dark', String(newVal));
  };

  return (
    <button
      aria-label="Toggle dark mode"
      onClick={toggle}
      className="rounded-full p-2 border border-gray-300 dark:border-gray-600"
    >
      {dark ? '🌙' : '☀️'}
    </button>
  );
}
