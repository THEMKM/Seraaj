import ky from 'ky';
import { toast } from 'sonner';

export const api = ky.create({
  prefixUrl: '/api',
  hooks: {
    beforeRequest: [
      (req) => {
        const token = localStorage.getItem('token');
        if (token) req.headers.set('Authorization', `Bearer ${token}`);
      },
    ],
    beforeError: [
      async (err) => {
        const body = await err.response?.json().catch(() => ({}));
        toast.error((body as { detail?: string }).detail ?? err.message);
        return err;
      },
    ],
  },
});
