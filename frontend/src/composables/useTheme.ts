import { ref, watchEffect } from 'vue';

export type Theme = 'light' | 'dark';
const STORAGE_KEY = 'nurtura-theme';

const getInitialTheme = (): Theme => {
  if (typeof window === 'undefined') return 'light';
  const saved = localStorage.getItem(STORAGE_KEY) as Theme | null;
  if (saved === 'dark' || saved === 'light') return saved;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

const currentTheme = ref<Theme>(getInitialTheme());

export function useTheme() {
  const setTheme = (theme: Theme) => {
    currentTheme.value = theme;
    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(STORAGE_KEY, theme);
        document.documentElement.setAttribute('data-theme', theme);
        if (theme === 'dark') {
          document.documentElement.classList.add('dark');
        } else {
          document.documentElement.classList.remove('dark');
        }
      } catch {
        // ignore
      }
    }
  };

  const toggleTheme = () => {
    setTheme(currentTheme.value === 'dark' ? 'light' : 'dark');
  };

  watchEffect(() => {
    if (typeof window !== 'undefined') {
      document.documentElement.setAttribute('data-theme', currentTheme.value);
      if (currentTheme.value === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    }
  });

  return {
    currentTheme,
    setTheme,
    toggleTheme,
  };
}
