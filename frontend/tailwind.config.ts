import type { Config } from 'tailwindcss';
import defaultTheme from 'tailwindcss/defaultTheme';

export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
      },
      backgroundImage: {
        'ai-gradient': 'linear-gradient(135deg, #00e0ff 0%, #ae00ff 100%)',
      },
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
