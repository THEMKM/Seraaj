import type { Config } from 'tailwindcss';

export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#087ea4',
          dark: '#046494',
        },
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
} satisfies Config;
