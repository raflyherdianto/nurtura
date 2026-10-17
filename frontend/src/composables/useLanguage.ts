import { ref, watchEffect } from 'vue';
import type { Language, LocalizedString } from '../types';

const STORAGE_KEY = 'nurtura-lang';
const savedLang = (typeof window !== 'undefined' ? localStorage.getItem(STORAGE_KEY) : null) as Language | null;
const currentLang = ref<Language>(savedLang === 'en' ? 'en' : 'id');

export function useLanguage() {
  const setLanguage = (lang: Language) => {
    currentLang.value = lang;
    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(STORAGE_KEY, lang);
        document.documentElement.setAttribute('data-lang', lang);
        document.documentElement.lang = lang;
      } catch {
        // ignore storage errors
      }
    }
  };

  watchEffect(() => {
    if (typeof window !== 'undefined') {
      document.documentElement.setAttribute('data-lang', currentLang.value);
      document.documentElement.lang = currentLang.value;
    }
  });

  const t = (localized: LocalizedString | undefined | null): string => {
    if (!localized) return '';
    return localized[currentLang.value] || localized.id || '';
  };

  return {
    currentLang,
    setLanguage,
    t,
  };
}
