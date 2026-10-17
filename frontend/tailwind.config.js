/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        paper: 'var(--paper)',
        'paper-2': 'var(--paper-2)',
        panel: 'var(--panel)',
        ink: 'var(--ink)',
        'ink-2': 'var(--ink-2)',
        band: 'var(--band)',
        'on-band': 'var(--on-band)',
        'on-band-2': 'var(--on-band-2)',
        clay: 'var(--clay)',
        'clay-text': 'var(--clay-text)',
        olive: 'var(--olive)',
        'olive-text': 'var(--olive-text)',
        mustard: 'var(--mustard)',
        peach: 'var(--peach)',
        plate: 'var(--plate)',
        'plate-edge': 'var(--plate-edge)',
        line: 'var(--line)',
        'line-strong': 'var(--line-strong)',
      },
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'Times New Roman', 'serif'],
        sans: ['Nunito', 'Avenir Next', 'Segoe UI', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'leaf-sm': '1.1rem 0.3rem 1.1rem 0.3rem',
        'leaf': '1.4rem 0.35rem 1.4rem 0.35rem',
        'leaf-lg': '2rem 0.5rem 2rem 0.5rem',
        'leaf-reverse': '0.4rem 1.4rem 0.4rem 1.4rem',
        'leaf-petal': '0 100% 0 100%',
        'leaf-blob': '58% 42% 52% 48% / 46% 56% 44% 54%',
      },
      animation: {
        'pulse-subtle': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float-slow': 'floatSlow 6s ease-in-out infinite',
      },
      keyframes: {
        floatSlow: {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '50%': { transform: 'translateY(-6px) rotate(1deg)' },
        }
      }
    },
  },
  plugins: [],
}
