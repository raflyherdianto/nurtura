import { ref, watchEffect } from 'vue';

export type ChildGender = 'boy' | 'girl';

export interface ChildProfile {
  name: string;
  gender: ChildGender;
  ageMonths: number;
  weightKg: number;
  heightCm: number;
  presetKey?: '6m' | '14m' | '30m' | 'custom';
}

export const CHILD_PRESETS: Record<'6m' | '14m' | '30m', ChildProfile> = {
  '6m': {
    name: 'Aria',
    gender: 'girl',
    ageMonths: 6,
    weightKg: 7.2,
    heightCm: 66,
    presetKey: '6m',
  },
  '14m': {
    name: 'Bima',
    gender: 'boy',
    ageMonths: 14,
    weightKg: 9.8,
    heightCm: 78,
    presetKey: '14m',
  },
  '30m': {
    name: 'Cinta',
    gender: 'girl',
    ageMonths: 30,
    weightKg: 13.5,
    heightCm: 92,
    presetKey: '30m',
  },
};

const STORAGE_KEY = 'nurtura-child';

const getInitialProfile = (): ChildProfile => {
  if (typeof window === 'undefined') return { ...CHILD_PRESETS['14m'] };
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (!parsed.gender) {
        parsed.gender =
          parsed.name?.toLowerCase().includes('cinta') || parsed.name?.toLowerCase().includes('aria')
            ? 'girl'
            : 'boy';
      }
      return parsed;
    }
  } catch {
    // fallback
  }
  return { ...CHILD_PRESETS['14m'] };
};

const activeChild = ref<ChildProfile>(getInitialProfile());

export function useChildProfile() {
  const save = () => {
    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(activeChild.value));
      } catch {
        // ignore
      }
    }
  };

  const applyPreset = (key: '6m' | '14m' | '30m') => {
    activeChild.value = { ...CHILD_PRESETS[key] };
    save();
  };

  const setAgeMonths = (months: number) => {
    activeChild.value.ageMonths = months;
    activeChild.value.presetKey = 'custom';
    save();
  };

  const updateProfile = (partial: Partial<ChildProfile>) => {
    activeChild.value = { ...activeChild.value, ...partial };
    save();
  };

  watchEffect(() => {
    save();
  });

  return {
    activeChild,
    CHILD_PRESETS,
    applyPreset,
    setAgeMonths,
    updateProfile,
  };
}
