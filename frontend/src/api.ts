let token: string | null = null;
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export function setToken(t: string) {
  token = t;
  if (typeof window !== 'undefined') {
    localStorage.setItem('token', t);
  }
}

export function getToken(): string | null {
  if (!token && typeof window !== 'undefined') {
    token = localStorage.getItem('token');
  }
  return token;
}

export async function login(email: string, password: string): Promise<string> {
  const res = await fetch(`${BACKEND_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    throw new Error('Invalid credentials');
  }
  const data = await res.json();
  setToken(data.access_token);
  return data.access_token as string;
}

export async function authFetch(input: RequestInfo | URL, init: RequestInit = {}) {
  const headers = new Headers(init.headers);
  const t = getToken();
  if (t) headers.set('Authorization', `Bearer ${t}`);
  let url: RequestInfo | URL = input;
  if (typeof input === 'string' && input.startsWith('/')) {
    url = `${BACKEND_URL}${input}`;
  }
  return fetch(url, { ...init, headers });
}

