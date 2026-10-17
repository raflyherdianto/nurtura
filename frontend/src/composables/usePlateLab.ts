import { ref, computed } from 'vue';
import {
  FOOD_ITEMS,
  AGES,
  TEXTURES,
  TARGET_TEXTURES,
  RECIPES,
} from '../data/foodItems';
import type { MealTime } from '../data/mealScans';
import type { MacroRating, MacroInfo, TextureVerdict, LocalizedString } from '../types';
import { apiClient, type PlateAuditApiResponse } from '../services/api';
import { useChildProfile } from './useChildProfile';

const selectedItems = ref<Record<string, boolean>>({});
const selectedTexture = ref<number>(2);
const activeMealTime = ref<MealTime>('siang');
const isAnalyzingPlate = ref<boolean>(false);
const lastAuditResult = ref<PlateAuditApiResponse | null>(null);
const hasAudited = ref<boolean>(false);
const uploadedPhotoUrl = ref<string | null>(null);
const userOverrodeTexture = ref<boolean>(false);

export function computeTextureVerdict(age: number, tex: number): TextureVerdict {
  const range: [number, number] = age <= 8 ? [0, 1] : age <= 11 ? [1, 3] : [3, 4];
  const target = age <= 8 ? TARGET_TEXTURES[7] : age <= 11 ? TARGET_TEXTURES[10] : TARGET_TEXTURES[14];

  if (tex < range[0]) {
    return {
      status: 'fine',
      title: {
        id: `Terlalu halus untuk ${age} bulan`,
        en: `Too smooth for ${age} months`,
      },
      description: {
        id: `Naikkan bertahap ke ${target.id} supaya anak berlatih mengunyah dan mencegah keterlambatan bicara.`,
        en: `Move up gradually to ${target.en} so your child practices chewing and avoids oral-motor delay.`,
      },
    };
  } else if (tex > range[1]) {
    return {
      status: 'coarse',
      title: {
        id: `Terlalu kasar untuk ${age} bulan`,
        en: `Too coarse for ${age} months`,
      },
      description: {
        id: `Haluskan menjadi ${target.id} untuk mengurangi risiko tersedak (choking risk).`,
        en: `Mash it down to ${target.en} to eliminate choking hazard risk.`,
      },
    };
  } else {
    return {
      status: 'ok',
      title: {
        id: `Tekstur sesuai untuk ${age} bulan`,
        en: `Texture fits ${age} months`,
      },
      description: {
        id: 'Cocok dengan tahap kesiapan oral-motor anak pada usia ini.',
        en: 'Matches your child’s oral-motor readiness at this age.',
      },
    };
  }
}

export function mapTextureTextToIndex(texStr: string, age: number): number {
  const s = texStr.toLowerCase();
  if (s.includes('saring') || s.includes('puree')) return 0;
  if (s.includes('lumat') || s.includes('mash')) return 1;
  if (s.includes('cincang') || s.includes('mince') || s.includes('tim')) return 2;
  if (s.includes('finger')) return 3;
  if (s.includes('keluarga') || s.includes('family') || s.includes('padat')) return 4;
  return age <= 8 ? 0 : age <= 11 ? 2 : 4;
}

export function usePlateLab() {
  const { activeChild } = useChildProfile();
  const selectedAge = computed(() => activeChild.value.ageMonths);

  const toggleItem = (key: string) => {
    selectedItems.value[key] = !selectedItems.value[key];
    lastAuditResult.value = null;
  };

  const clearPlate = () => {
    if (uploadedPhotoUrl.value) {
      URL.revokeObjectURL(uploadedPhotoUrl.value);
      uploadedPhotoUrl.value = null;
    }
    selectedItems.value = {};
    lastAuditResult.value = null;
    hasAudited.value = false;
    userOverrodeTexture.value = false;
  };

  const setItemState = (key: string, state: boolean) => {
    selectedItems.value[key] = state;
  };

  const setAge = (age: number) => {
    activeChild.value.ageMonths = age;
  };

  const setTexture = (texIndex: number) => {
    selectedTexture.value = texIndex;
    userOverrodeTexture.value = true;
  };

  const setMealTime = (time: MealTime) => {
    activeMealTime.value = time;
  };

  // Category counts
  const categoryCounts = computed(() => {
    const counts = { animal: 0, fat: 0, carb: 0, plant: 0, veg: 0 };
    FOOD_ITEMS.forEach((it) => {
      if (selectedItems.value[it.k]) {
        if (counts[it.kind] !== undefined) {
          counts[it.kind]++;
        }
      }
    });
    return counts;
  });

  const getLevel = (count: number, goodThreshold: number): MacroRating => {
    if (count === 0) return 'low';
    if (count >= goodThreshold) return 'good';
    return 'ok';
  };

  const STATE_INFO: Record<MacroRating, { label: LocalizedString; width: number }> = {
    low: { label: { id: 'Kurang', en: 'Low' }, width: 15 },
    ok: { label: { id: 'Cukup', en: 'Fair' }, width: 66 },
    good: { label: { id: 'Baik', en: 'Good' }, width: 100 },
  };

  // Macro distribution metrics (Reads from Gemini AI if audited, or fallback formula)
  const macros = computed<MacroInfo[]>(() => {
    if (lastAuditResult.value && lastAuditResult.value.macros && lastAuditResult.value.macros.length > 0) {
      return lastAuditResult.value.macros;
    }

    const counts = categoryCounts.value;
    const animalLevel = getLevel(counts.animal, 2);
    const fatLevel = getLevel(counts.fat, 2);
    const carbLevel = getLevel(counts.carb, 1);

    const hasTempehHint = counts.animal === 0 && counts.plant > 0;

    return [
      {
        key: 'animal',
        name: RECIPES.animal.name,
        rating: animalLevel,
        percentage: STATE_INFO[animalLevel].width,
        label: STATE_INFO[animalLevel].label,
        hint: hasTempehHint
          ? {
              id: 'Tempe baik, tetapi belum menggantikan protein hewani.',
              en: 'Tempeh is good, but it does not replace animal protein.',
            }
          : undefined,
        recipe: RECIPES.animal.rec,
      },
      {
        key: 'fat',
        name: RECIPES.fat.name,
        rating: fatLevel,
        percentage: STATE_INFO[fatLevel].width,
        label: STATE_INFO[fatLevel].label,
        recipe: RECIPES.fat.rec,
      },
      {
        key: 'carb',
        name: RECIPES.carb.name,
        rating: carbLevel,
        percentage: STATE_INFO[carbLevel].width,
        label: STATE_INFO[carbLevel].label,
        recipe: RECIPES.carb.rec,
      },
    ];
  });

  // Texture validation against oral-motor age guidelines (WHO & IDAI)
  const textureVerdict = computed<TextureVerdict>(() => {
    if (userOverrodeTexture.value || !lastAuditResult.value?.texture_verdict) {
      return computeTextureVerdict(selectedAge.value, selectedTexture.value);
    }
    return lastAuditResult.value.texture_verdict;
  });

  // Gaps for next meal booster
  const deficientMacros = computed(() => {
    return macros.value.filter((m) => m.rating === 'low');
  });

  // Live Audit with FastAPI backend
  const auditPlateWithApi = async (notes?: string) => {
    isAnalyzingPlate.value = true;
    const currentItemList = Object.keys(selectedItems.value).filter((k) => selectedItems.value[k]);
    try {
      const res = await apiClient.auditPlate(
        {
          name: activeChild.value.name,
          age_months: activeChild.value.ageMonths,
          weight_kg: activeChild.value.weightKg,
          height_cm: activeChild.value.heightCm,
        },
        activeMealTime.value,
        currentItemList,
        notes
      );
      lastAuditResult.value = res;
    } catch {
      // Graceful offline fallback
      await new Promise((resolve) => setTimeout(resolve, 600));
    } finally {
      isAnalyzingPlate.value = false;
      hasAudited.value = true;
    }
  };

  const auditPlateWithPhoto = async (file: File) => {
    isAnalyzingPlate.value = true;
    userOverrodeTexture.value = false;
    if (uploadedPhotoUrl.value) {
      URL.revokeObjectURL(uploadedPhotoUrl.value);
    }
    uploadedPhotoUrl.value = URL.createObjectURL(file);

    try {
      const formData = new FormData();
      formData.append('image', file);
      formData.append('child_name', activeChild.value.name);
      formData.append('age_months', String(activeChild.value.ageMonths));
      formData.append('weight_kg', String(activeChild.value.weightKg));
      formData.append('height_cm', String(activeChild.value.heightCm));
      formData.append('meal_time', activeMealTime.value);

      const res = await apiClient.auditPlateUpload(formData);
      lastAuditResult.value = res;

      // Automatically map detected texture to selectedTexture
      if (res.detected_texture) {
        selectedTexture.value = mapTextureTextToIndex(res.detected_texture, activeChild.value.ageMonths);
      }

      // Map detected items dynamically
      if (res.detected_foods && res.detected_foods.length > 0) {
        const newMap: Record<string, boolean> = {};
        res.detected_foods.forEach((df) => {
          const nameStr = typeof df.name === 'string' ? df.name : df.name.id;
          newMap[nameStr] = true;
          const key = nameStr.toLowerCase();
          const matched = FOOD_ITEMS.find(
            (it) => it.k === key || it.name.id.toLowerCase() === key || it.name.en.toLowerCase() === key
          );
          if (matched) {
            newMap[matched.k] = true;
          }
        });
        selectedItems.value = newMap;
      }
    } catch {
      await new Promise((resolve) => setTimeout(resolve, 800));
    } finally {
      isAnalyzingPlate.value = false;
      hasAudited.value = true;
    }
  };

  const isLiveAudit = computed(() => lastAuditResult.value !== null);
  const dynamicBoosterRecipe = computed(() => lastAuditResult.value?.upgrade_plan.booster_recipe);
  const dynamicUpgradeSummary = computed(() => lastAuditResult.value?.upgrade_plan.summary);
  const dynamicSuggestions = computed(() => lastAuditResult.value?.upgrade_plan.suggestions);
  const detectedFoods = computed(() => lastAuditResult.value?.detected_foods);
  const detectedTextureText = computed(() => {
    if (userOverrodeTexture.value) {
      return TEXTURES[selectedTexture.value].id;
    }
    return lastAuditResult.value?.detected_texture;
  });
  const ragSources = computed<string[]>(() => {
    if (lastAuditResult.value?.rag_sources && lastAuditResult.value.rag_sources.length > 0) {
      return lastAuditResult.value.rag_sources;
    }
    return [
      'WHO (2023) Infant and Young Child Feeding Guidelines',
      'Pedoman MPASI IDAI (Ikatan Dokter Anak Indonesia)',
      'UNICEF / WHO Care for Child Development (CCD)',
    ];
  });

  return {
    foodItems: FOOD_ITEMS,
    ages: AGES,
    textures: TEXTURES,
    activeChild,
    activeMealTime,
    selectedItems,
    selectedAge,
    selectedTexture,
    uploadedPhotoUrl,
    userOverrodeTexture,
    isAnalyzingPlate,
    isLiveAudit,
    hasAudited,
    ragSources,
    dynamicBoosterRecipe,
    dynamicUpgradeSummary,
    dynamicSuggestions,
    detectedFoods,
    detectedTextureText,
    toggleItem,
    clearPlate,
    setItemState,
    setAge,
    setTexture,
    setMealTime,
    macros,
    textureVerdict,
    deficientMacros,
    auditPlateWithApi,
    auditPlateWithPhoto,
  };
}
