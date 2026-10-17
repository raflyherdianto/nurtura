import { ref, computed } from 'vue';
import confetti from 'canvas-confetti';
import type { MilestoneScenario } from '../types';
import { apiClient } from '../services/api';
import { useChildProfile } from './useChildProfile';

const STORAGE_KEY = 'nurtura-checks';

const getInitialChecks = (): Record<string, boolean> => {
  if (typeof window === 'undefined') return {};
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
};

const getInitialScenario = (): MilestoneScenario => ({
  id: '',
  name: { id: '', en: '' },
  targetAge: 0,
  note: { id: '', en: '' },
  ref: { id: '', en: '' },
  statusType: 'ok',
  statusTitle: { id: '', en: '' },
  statusDesc: { id: '', en: '' },
  safety: { id: '', en: '' },
  focusArea: { id: '', en: '' },
  playbook: [],
});

const checks = ref<Record<string, boolean>>(getInitialChecks());
const currentScenario = ref<MilestoneScenario>(getInitialScenario());
const isAnalyzing = ref<boolean>(false);
const isLiveEvaluated = ref<boolean>(false);
const hasEvaluated = ref<boolean>(false);
const analysisError = ref<string | null>(null);

export function usePlaybook() {
  const save = () => {
    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(checks.value));
      } catch {
        // ignore
      }
    }
  };

  const days = computed(() => currentScenario.value.playbook);
  const totalSteps = 9;

  const completedCount = computed(() => {
    let count = 0;
    const prefix = currentScenario.value.id;
    for (let d = 0; d < 3; d++) {
      for (let s = 0; s < 3; s++) {
        if (checks.value[`${prefix}_d${d}s${s}`]) count++;
      }
    }
    return count;
  });

  const isComplete = computed(() => completedCount.value === totalSteps);

  const toggleStep = (keySuffix: string) => {
    const key = `${currentScenario.value.id}_${keySuffix}`;
    const wasComplete = isComplete.value;
    if (checks.value[key]) {
      delete checks.value[key];
    } else {
      checks.value[key] = true;
    }
    save();

    if (!wasComplete && isComplete.value && typeof window !== 'undefined') {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#7b8348', '#e0a03f', '#c06240', '#f5a777'],
      });
    }
  };

  const isStepChecked = (keySuffix: string): boolean => {
    return !!checks.value[`${currentScenario.value.id}_${keySuffix}`];
  };

  // AI evaluation of parent's natural observation via FastAPI backend
  const simulateAiEvaluation = async (customNote?: string) => {
    isAnalyzing.value = true;
    analysisError.value = null;
    const noteText = customNote || currentScenario.value.note.id;

    try {
      const { activeChild } = useChildProfile();
      const res = await apiClient.evaluateMilestone(
        {
          name: activeChild.value.name,
          age_months: activeChild.value.ageMonths,
          weight_kg: activeChild.value.weightKg,
          height_cm: activeChild.value.heightCm,
        },
        noteText
      );

      currentScenario.value = {
        id: res.id,
        name: { id: `Analisis AI: ${res.focus_area.id}`, en: `AI Assessment: ${res.focus_area.en}` },
        targetAge: activeChild.value.ageMonths,
        note: { id: noteText, en: noteText },
        ref: res.ref,
        statusType: res.status_type,
        statusTitle: res.status_title,
        statusDesc: res.status_desc,
        safety: res.safety,
        focusArea: res.focus_area,
        playbook: res.playbook,
        ragSources: res.rag_sources || [],
      };
      isLiveEvaluated.value = true;
      hasEvaluated.value = true;
    } catch (error) {
      analysisError.value = error instanceof Error
        ? error.message
        : 'Analisis Gemini tidak tersedia.';
      isLiveEvaluated.value = false;
      hasEvaluated.value = false;
    } finally {
      isAnalyzing.value = false;
      save();
    }
  };

  const resetAll = () => {
    const prefix = currentScenario.value.id;
    for (let d = 0; d < 3; d++) {
      for (let s = 0; s < 3; s++) {
        delete checks.value[`${prefix}_d${d}s${s}`];
      }
    }
    save();
  };

  return {
    currentScenario,
    days,
    checks,
    totalSteps,
    completedCount,
    isComplete,
    isAnalyzing,
    isLiveEvaluated,
    hasEvaluated,
    analysisError,
    toggleStep,
    isStepChecked,
    simulateAiEvaluation,
    resetAll,
  };
}
