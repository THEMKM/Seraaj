import type { Config } from 'tailwindcss';

export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#0f766e',
          light: '#2dd4bf',
          dark: '#0d9488',
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
