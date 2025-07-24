import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const backend =
  process.env.VITE_BACKEND_URL ||
  `http://localhost:${process.env.BACKEND_PORT || 8000}`;


export default defineConfig({
  plugins: [react()],
  server: {
    port: Number(process.env.FRONTEND_PORT) || 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: backend,
        changeOrigin: true,
        rewrite: p => p.replace(/^\/api/, ''),
      },
    },
  },
});
