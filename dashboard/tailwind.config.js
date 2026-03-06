/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts}'],
  theme: {
    extend: {
      colors: {
        foundry: {
          bg: '#0C0C0F',
          panel: '#141417',
          'panel-alt': '#1A1A1E',
          border: '#2A2A2E',
          'border-light': '#353539',
          molten: '#E8600A',
          green: '#2D8A4E',
          red: '#C43030',
          brass: '#B8923E',
          white: '#F5F0E8',
          slag: '#6B6B73',
          'slag-dim': '#3A3A3E',
          blue: '#2E6B9E',
        },
      },
      fontFamily: {
        display: ["'Bebas Neue'", 'sans-serif'],
        body: ["'IBM Plex Sans'", 'sans-serif'],
        mono: ["'IBM Plex Mono'", 'monospace'],
      },
      keyframes: {
        blink: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0' },
        },
        slideUp: {
          from: { opacity: '0', transform: 'translateY(6px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        glow: {
          '0%, 100%': { boxShadow: '0 0 4px rgba(232,96,10,0.3)' },
          '50%': { boxShadow: '0 0 12px rgba(232,96,10,0.6)' },
        },
      },
      animation: {
        blink: 'blink 1s step-end infinite',
        'slide-up': 'slideUp 0.3s ease-out',
        glow: 'glow 2s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
