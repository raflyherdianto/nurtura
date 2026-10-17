<script setup lang="ts">
import { ref, computed } from 'vue';
import { usePlateLab } from '../../composables/usePlateLab';
import {
  FOOD_ITEMS,
  TEXTURES,
  TARGET_TEXTURES,
  generateBlobPath,
} from '../../data/foodItems';
import type { MealTime } from '../../data/mealScans';
import ChildAvatarSvg from '../common/ChildAvatarSvg.vue';

const {
  activeChild,
  activeMealTime,
  selectedItems,
  selectedAge,
  selectedTexture,
  uploadedPhotoUrl,
  isAnalyzingPlate,
  isLiveAudit,
  hasAudited,
  analysisError,
  ragSources,
  dynamicBoosterRecipe,
  dynamicUpgradeSummary,
  dynamicSuggestions,
  detectedFoods,
  detectedTextureText,
  clearPlate,
  setTexture,
  setMealTime,
  auditPlateWithPhoto,
  macros,
  textureVerdict,
  deficientMacros,
} = usePlateLab();

const KIND_COLORS: Record<string, string> = {
  animal: '#e76f51',
  fat: '#e09f3e',
  carb: '#c4af78',
  veg: '#4a7c59',
  plant: '#8b5e3c',
};

const KIND_LABELS: Record<string, { id: string; en: string }> = {
  animal: { id: 'Protein Hewani', en: 'Animal Protein' },
  fat: { id: 'Lemak Sehat', en: 'Healthy Fat' },
  carb: { id: 'Karbohidrat', en: 'Carb' },
  veg: { id: 'Sayur & Serat', en: 'Vegetable' },
  plant: { id: 'Protein Nabati', en: 'Plant Protein' },
};

const activeDetectedFoodItems = computed(() => {
  if (!detectedFoods.value || detectedFoods.value.length === 0) {
    return [];
  }
  return detectedFoods.value.map((df) => {
    const idName = typeof df.name === 'string' ? df.name : df.name?.id || '';
    const enName = typeof df.name === 'string' ? df.name : df.name?.en || idName;
    const kind = df.kind || 'carb';
    const swatchColor = KIND_COLORS[kind] || 'var(--olive)';
    const categoryLabel = KIND_LABELS[kind] || { id: 'Bahan MPASI', en: 'Ingredient' };

    return {
      id: idName,
      en: enName,
      kind,
      swatchColor,
      categoryLabel,
    };
  });
});

const currentTargetTexture = computed(() => {
  const age = selectedAge.value;
  return age <= 8 ? TARGET_TEXTURES[7] : age <= 11 ? TARGET_TEXTURES[10] : TARGET_TEXTURES[14];
});

const fileInputRef = ref<HTMLInputElement | null>(null);

const triggerFileInput = () => {
  fileInputRef.value?.click();
};

const handlePhotoSelected = async (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    await auditPlateWithPhoto(target.files[0]);
    target.value = '';
  }
};

const blob = (cx: number, cy: number, rx: number, ry: number, seed: number) => {
  return generateBlobPath(cx, cy, rx, ry, seed);
};

const STATE: Record<'low' | 'ok' | 'good', { id: string; en: string; w: number }> = {
  low: { id: 'Kurang', en: 'Low', w: 12 },
  ok: { id: 'Cukup', en: 'Fair', w: 66 },
  good: { id: 'Baik', en: 'Good', w: 100 },
};

const mealTimes: { key: MealTime; label: { id: string; en: string } }[] = [
  { key: 'pagi', label: { id: 'Sarapan / Pagi', en: 'Breakfast / Morning' } },
  { key: 'siang', label: { id: 'Makan Siang', en: 'Lunch' } },
  { key: 'malam', label: { id: 'Makan Malam', en: 'Dinner' } },
  { key: 'camilan', label: { id: 'Camilan Sehat', en: 'Snack' } },
];
</script>

<template>
  <section id="modul-2" class="band band--paper2">
    <div class="wrap">
      <div
        v-if="analysisError"
        role="alert"
        style="margin-bottom: 1rem; padding: .8rem 1rem; border: 1.5px solid #b42318; border-left: 4px solid #b42318; border-radius: .6rem; background: #fff4f2; color: #7a271a; line-height: 1.45;"
      >
        <span lang="id">Analisis Gemini gagal: {{ analysisError }}</span>
        <span lang="en">Gemini analysis failed: {{ analysisError }}</span>
      </div>
      <div class="mod__head">
        <div>
          <p class="label">
            <span lang="id">Modul 2</span>
            <span lang="en">Module 2</span>
          </p>
          <h2>Smart Plate Vision</h2>
          <p class="mod__sub">
            <span lang="id">Pengoptimal gizi multimodal untuk piring bayi dan balita</span>
            <span lang="en">Multimodal nutrition optimizer for baby and toddler plates</span>
          </p>
        </div>
        <dl class="feats feats--four">
          <div>
            <dt>
              <span lang="id">Audit piring instan</span>
              <span lang="en">Instant plate audit</span>
            </dt>
            <dd>
              <span lang="id">Orang tua mengunggah foto makanan bayi atau balita.</span>
              <span lang="en">Parents upload a photo of the baby or toddler meal.</span>
            </dd>
          </div>
          <div>
            <dt>
              <span lang="id">Cek tekstur oral-motor</span>
              <span lang="en">Oral-motor texture check</span>
            </dt>
            <dd>
              <span lang="id">Menilai apakah tekstur, dari saring sampai makanan keluarga, cocok dengan usia anak dalam bulan.</span>
              <span lang="en">Evaluates whether the texture—puree to family food—fits the child’s age in months.</span>
            </dd>
          </div>
          <div>
            <dt>
              <span lang="id">Meter makro anti-stunting</span>
              <span lang="en">Anti-stunting macro meter</span>
            </dt>
            <dd>
              <span lang="id">Memeriksa protein hewani, lemak sehat, dan karbohidrat.</span>
              <span lang="en">Audits animal protein, healthy fats, and carbohydrates.</span>
            </dd>
          </div>
          <div>
            <dt>
              <span lang="id">Agen perbaikan makan berikutnya</span>
              <span lang="en">Next-meal improvisation agent</span>
            </dt>
            <dd>
              <span lang="id">Peningkatan hemat dan resep penguat 5 menit untuk menutup kekurangan gizi.</span>
              <span lang="en">Budget-friendly swaps and 5-minute booster recipes to cover nutritional gaps.</span>
            </dd>
          </div>
        </dl>
      </div>

      <section class="panel" aria-labelledby="lab-title">
        <!-- Editorial Clinical Disclaimer -->
        <div
          style="margin-bottom: 1.25rem; padding: .85rem 1.15rem; background: var(--paper-2); border: 1.5px solid var(--line-strong); border-left: 4.5px solid var(--olive); border-radius: .85rem .25rem .85rem .25rem; display: flex; align-items: flex-start; gap: .75rem;"
          role="note"
          aria-label="Pedoman Gizi MPASI Terkurasi"
        >
          <span style="font-size: 1.25rem; line-height: 1.2;" aria-hidden="true">🌱</span>
          <div style="font-size: .84rem; color: var(--ink-2); line-height: 1.6;">
            <strong style="color: var(--ink); display: block; margin-bottom: .2rem; font-weight: 800;">
              <span lang="id">Pedoman Gizi MPASI Terkurasi:</span>
              <span lang="en">Curated MPASI Clinical Guidelines:</span>
            </strong>
            <span lang="id">
              Analisis kecukupan makronutrisi dan tekstur oral-motor piring makan ini mengacu pada pedoman klinis resmi <b>WHO (2023) Infant and Young Child Feeding</b> dan <b>Pedoman MPASI IDAI (Ikatan Dokter Anak Indonesia)</b>, memprioritaskan konsumsi protein hewani harian serta lemak tambahan untuk pencegahan stunting secara dini.
            </span>
            <span lang="en">
              Macronutrient adequacy and oral-motor texture evaluations are grounded in official clinical recommendations from <b>WHO (2023) Infant and Young Child Feeding</b> and the <b>Indonesian Pediatric Society (IDAI)</b>, prioritizing daily bioavailable animal protein and healthy fats for linear growth.
            </span>
          </div>
        </div>

        <div class="demo__top">
          <h3 class="demo__title" id="lab-title">
            <span lang="id">Audit Piring Nutrisi &amp; Vision AI</span>
            <span lang="en">Plate Nutrition &amp; Vision AI Audit</span>
          </h3>
        </div>

        <!-- Active Child Demographic Context (Style identical to Evaluasi Hari Ini in Module 1) -->
        <p class="agebadge" style="display: inline-flex; align-items: center; gap: .45rem; flex-wrap: wrap; margin-bottom: 1.25rem;">
          <ChildAvatarSvg :age-months="activeChild.ageMonths" :gender="activeChild.gender" :size="24" />
          <b>{{ activeChild.name }}</b>
          <span>•</span>
          <b>{{ activeChild.ageMonths }}</b> <span lang="id">bulan</span><span lang="en">months</span>
          <span>•</span>
          <span>{{ activeChild.weightKg }} kg</span>
          <span>•</span>
          <span>{{ activeChild.heightCm }} cm</span>
        </p>

        <!-- Photo Upload Bar -->
        <div style="margin-bottom: 1.5rem; padding: .85rem 1rem; background: var(--paper-2); border-radius: 1.1rem .3rem 1.1rem .3rem; border: 1.5px solid var(--line);">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: .5rem;">
            <div>
              <p style="font-size: .84rem; color: var(--ink-2); margin: 0;">
                <span lang="id">Ambil foto makanan anak secara langsung atau unggah dari galeri perangkat.</span>
                <span lang="en">Capture meal photo directly or upload from your device gallery.</span>
              </p>
            </div>

            <!-- Hidden File Input & Upload Trigger -->
            <input
              ref="fileInputRef"
              type="file"
              accept="image/jpeg,image/png,image/webp"
              style="display: none;"
              @change="handlePhotoSelected"
            />
            <button
              type="button"
              class="btn"
              style="padding: .45rem .85rem; font-size: .84rem; display: inline-flex; align-items: center; gap: .4rem;"
              :disabled="isAnalyzingPlate"
              @click="triggerFileInput"
            >
              <span lang="id">Unggah Foto Makanan Saat Ini</span>
              <span lang="en">Upload Current Meal Photo</span>
            </button>
          </div>
          <p v-if="isAnalyzingPlate" style="margin-top: .6rem; font-size: .85rem; font-weight: 800; color: var(--clay-text);">
            <span lang="id">Memproses citra piring dengan Gemini Multimodal Vision via FastAPI...</span>
            <span lang="en">Processing plate image with Gemini Multimodal Vision via FastAPI...</span>
          </p>
        </div>

        <div class="lab">
          <!-- Left Column: SVG Plate & Ingredient Chips -->
          <div>
            <svg class="plate" id="plate" viewBox="0 0 320 320" role="img" aria-label="Piring makan bayi">
              <defs>
                <clipPath id="innerPlateClip">
                  <circle cx="160" cy="160" r="120" />
                </clipPath>
              </defs>

              <!-- Lingkaran Luar Keramik Piring -->
              <circle cx="160" cy="160" r="150" fill="var(--plate)" stroke="var(--plate-edge)" stroke-width="3" />

              <!-- Foto Nyata User yang Ditempelkan di Dalam Piring -->
              <image
                v-if="uploadedPhotoUrl"
                :href="uploadedPhotoUrl"
                x="40"
                y="40"
                width="240"
                height="240"
                preserveAspectRatio="xMidYMid slice"
                clip-path="url(#innerPlateClip)"
              />

              <!-- Garis Putus-putus Batas Dalam Piring -->
              <circle
                cx="160"
                cy="160"
                r="122"
                fill="none"
                stroke="var(--plate-edge)"
                stroke-width="2"
                stroke-dasharray="2 7"
                stroke-linecap="round"
              />

              <!-- Tampilan Ilustrasi Bahan Jika Belum Ada Foto Nyata -->
              <template v-if="!uploadedPhotoUrl">
                <g
                  v-for="it in FOOD_ITEMS"
                  :key="it.k"
                  class="food"
                  :id="'food-' + it.k"
                  :class="{ on: !!selectedItems[it.k] }"
                >
                  <path
                    v-for="(s, sIdx) in it.shapes"
                    :key="sIdx"
                    :d="blob(s[0], s[1], s[2], s[3], s[4])"
                    :fill="it.fill"
                    :stroke="it.stroke"
                    stroke-width="2.5"
                    stroke-linejoin="round"
                  />
                </g>
              </template>
            </svg>

            <!-- Waktu Makan Selector -->
            <fieldset class="field" style="margin-bottom: 1rem;">
              <legend>
                <span lang="id">Jadwal Makan</span>
                <span lang="en">Meal Timing</span>
              </legend>
              <div class="chips" style="gap: .4rem;">
                <label v-for="m in mealTimes" :key="m.key" class="chip">
                  <input
                    type="radio"
                    name="mealtime"
                    :value="m.key"
                    :checked="activeMealTime === m.key"
                    @change="setMealTime(m.key)"
                  />
                  <span class="chip__face" style="padding: .35rem .65rem; font-size: .82rem;">
                    <span lang="id">{{ m.label.id }}</span>
                    <span lang="en">{{ m.label.en }}</span>
                  </span>
                </label>
              </div>
            </fieldset>

            <!-- Deteksi Bahan Otomatis oleh Gemini -->
            <fieldset class="field" style="margin-bottom:0">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: .45rem;">
                <legend style="margin-bottom: 0;">
                  <span lang="id">Bahan Terdeteksi AI</span>
                  <span lang="en">AI-Detected Ingredients</span>
                </legend>
                <button
                  v-if="hasAudited"
                  type="button"
                  style="font-size: .75rem; font-weight: 700; color: var(--clay-text); background: none; border: none; cursor: pointer; text-decoration: underline; padding: 0;"
                  @click="clearPlate"
                >
                  <span lang="id">Ganti Foto / Reset</span>
                  <span lang="en">Change Photo / Reset</span>
                </button>
              </div>

              <!-- State 1: Ada bahan terdeteksi -->
              <div v-if="activeDetectedFoodItems.length > 0" class="ings" id="ings">
                <div
                  v-for="(item, idx) in activeDetectedFoodItems"
                  :key="idx"
                  class="chip ing"
                  :style="{ '--sw': item.swatchColor }"
                >
                  <span class="chip__face" style="background: var(--paper-2); border-color: var(--line-strong); font-weight: 700;">
                    <span lang="id">{{ item.id }}</span>
                    <span lang="en">{{ item.en }}</span>
                  </span>
                </div>
              </div>

              <!-- State 2: Belum ada bahan terdeteksi -->
              <div
                v-else
                style="padding: .85rem 1rem; border: 1.5px dashed var(--line-strong); border-radius: .85rem; background: var(--paper-2); text-align: center; color: var(--ink-2); font-size: .84rem; line-height: 1.5;"
              >
                <span lang="id">Belum ada bahan terdeteksi. Silakan unggah foto makanan untuk deteksi otomatis oleh Gemini AI.</span>
                <span lang="en">No ingredients detected yet. Please upload a meal photo for automatic Gemini AI detection.</span>
              </div>
            </fieldset>

            <!-- Upload / Audit Trigger Button -->
            <button
              type="button"
              class="btn"
              style="width: 100%; margin-top: .85rem; padding: .75rem 1.2rem; font-size: .92rem;"
              :disabled="isAnalyzingPlate"
              @click="triggerFileInput"
            >
              <span v-if="isAnalyzingPlate">
                <span lang="id">Sedang Memproses Foto dengan Gemini AI...</span>
                <span lang="en">Processing Photo with Gemini AI...</span>
              </span>
              <span v-else-if="!hasAudited">
                <span lang="id">Unggah Foto Makanan Saat Ini</span>
                <span lang="en">Upload Current Meal Photo</span>
              </span>
              <span v-else>
                <span lang="id">Unggah Foto Makanan Lain</span>
                <span lang="en">Upload Another Meal Photo</span>
              </span>
            </button>
          </div>

          <!-- Right Column: Evaluation Results & Manual Validation -->
          <div>
            <!-- State A: Belum Audit -> Placeholder Bersih -->
            <div
              v-if="!hasAudited"
              style="border: 2px dashed var(--line-strong); background: var(--paper-2); border-radius: 1.4rem .35rem 1.4rem .35rem; padding: 2.2rem 1.5rem; text-align: center; color: var(--ink-2);"
            >
              <div style="margin: 0 auto .85rem; width: 3.2rem; height: 3.2rem; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: var(--panel); border: 1.5px solid var(--line); font-size: 1.5rem;">
                🍽️
              </div>
              <h4 style="font-family: var(--display); font-size: 1.25rem; font-weight: 800; color: var(--ink); margin: 0 0 .5rem 0;">
                <span lang="id">Belum Ada Audit Piring Makan</span>
                <span lang="en">No Plate Audit Performed Yet</span>
              </h4>
              <p style="margin: 0 auto; max-width: 24rem; font-size: .84rem; line-height: 1.6; color: var(--ink-2);">
                <span lang="id">
                  Unggah foto makanan anak Anda melalui tombol <strong>Unggah Foto Makanan Saat Ini</strong> untuk memulai evaluasi klinis nutrisi &amp; deteksi tekstur oral-motor.
                </span>
                <span lang="en">
                  Upload a photo of your child's meal using the <strong>Upload Current Meal Photo</strong> button to generate an evidence-based clinical evaluation.
                </span>
              </p>
            </div>

            <!-- State B: Sudah Audit -> Tampilkan Hasil Evaluasi, Validasi Tekstur, Meter Makro & Booster -->
            <div v-else class="results" id="results" aria-live="polite">
              <!-- RAG Grounding Clinical Citations -->
              <div
                v-if="ragSources && ragSources.length"
                style="margin-bottom: 1rem; padding: .75rem 1rem; background: var(--paper-2); border: 1.5px solid var(--line); border-radius: .9rem .25rem .9rem .25rem;"
              >
                <div style="font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .06em; color: var(--olive-text); margin-bottom: .35rem; display: flex; align-items: center; gap: .35rem;">
                  <span lang="id">Rujukan Pedoman Klinis (RAG Grounding):</span>
                  <span lang="en">Clinical Grounding Guidelines (RAG):</span>
                </div>
                <ul style="margin: 0; padding-left: 1.2rem; font-size: .8rem; color: var(--ink-2); line-height: 1.5;">
                  <li v-for="(source, sIdx) in ragSources" :key="sIdx">
                    {{ source }}
                  </li>
                </ul>
              </div>

              <!-- Live AI Audit Badge -->
              <div
                v-if="isLiveAudit"
                style="margin-bottom: 1rem; padding: .85rem 1rem; background: var(--paper-2); border: 1.5px solid var(--line-strong); border-left: 4px solid var(--olive); border-radius: .85rem .25rem .85rem .25rem;"
              >
                <div style="font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .06em; color: var(--olive-text); margin-bottom: .45rem;">
                  <span lang="id">Hasil Audit Dinamis (Gemini Multimodal Vision)</span>
                  <span lang="en">Live Dynamic Audit (Gemini Multimodal Vision)</span>
                </div>
                <p v-if="detectedTextureText" style="font-size: .92rem; font-weight: 600; color: var(--ink); margin: 0 0 .35rem 0;">
                  <span lang="id">Tekstur Fisik Terdeteksi AI: <b style="font-weight: 750;">{{ detectedTextureText }}</b></span>
                  <span lang="en">AI Detected Physical Texture: <b style="font-weight: 750;">{{ detectedTextureText }}</b></span>
                </p>
                <p v-if="detectedFoods && detectedFoods.length" style="font-size: .9rem; color: var(--ink-2); margin: 0;">
                  <span lang="id">Bahan Terdeteksi AI: 
                    <b style="color: var(--ink); font-weight: 700;">
                      <span v-for="(f, idx) in detectedFoods" :key="idx">
                        {{ typeof f === 'string' ? f : (f.name?.id || f.name) }}<span v-if="idx < detectedFoods.length - 1">, </span>
                      </span>
                    </b>
                  </span>
                  <span lang="en">AI Detected Items: 
                    <b style="color: var(--ink); font-weight: 700;">
                      <span v-for="(f, idx) in detectedFoods" :key="idx">
                        {{ typeof f === 'string' ? f : (f.name?.en || f.name?.id || f.name) }}<span v-if="idx < detectedFoods.length - 1">, </span>
                      </span>
                    </b>
                  </span>
                </p>
              </div>

              <!-- Tekstur Makanan (Pilihan Observasi / Validasi Manual) -->
              <fieldset
                class="field"
                style="margin-bottom: 1.15rem; padding: .85rem 1rem; background: var(--paper-2); border: 1.5px solid var(--line-strong); border-left: 4px solid var(--clay); border-radius: .85rem .25rem .85rem .25rem;"
              >
                <legend style="font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .06em; color: var(--clay-text); margin-bottom: .25rem;">
                  <span lang="id">Tekstur Makanan (Pilihan Observasi / Validasi Manual)</span>
                  <span lang="en">Food Texture (Observed Selection / Manual Validation)</span>
                </legend>
                <p style="font-size: .83rem; color: var(--ink-2); margin: 0 0 .55rem 0; line-height: 1.5;">
                  <span lang="id">Pilih tekstur aktual makanan jika analisis AI perlu disesuaikan. Hasil evaluasi oromotor akan diperbarui secara realtime:</span>
                  <span lang="en">Select actual food texture if AI analysis needs adjustment. Clinical oral-motor evaluation will update in real-time:</span>
                </p>
                <div class="chips" id="texs">
                  <label v-for="(x, i) in TEXTURES" :key="i" class="chip">
                    <input
                      type="radio"
                      name="tex"
                      :value="i"
                      :checked="selectedTexture === i"
                      @change="setTexture(i)"
                    />
                    <span class="chip__face">
                      <span lang="id">{{ x.id }}</span>
                      <span lang="en">{{ x.en }}</span>
                    </span>
                  </label>
                </div>
              </fieldset>

              <div>
                <p class="result__h">
                  <span lang="id">Cek Tekstur Oral-Motor (WHO 2023 / IDAI)</span>
                  <span lang="en">Oral-Motor Texture Check (WHO 2023 / IDAI)</span>
                </p>
                <div :class="['status', 'status--' + textureVerdict.status]">
                  <span class="status__icon" aria-hidden="true"></span>
                  <div>
                    <template v-if="textureVerdict.status === 'fine'">
                      <strong>
                        <span lang="id">Terlalu halus untuk {{ selectedAge }} bulan</span>
                        <span lang="en">Too smooth for {{ selectedAge }} months</span>
                      </strong>
                      <p>
                        <span lang="id">Naikkan bertahap ke {{ currentTargetTexture.id }} supaya anak berlatih mengunyah dan mencegah keterlambatan bicara.</span>
                        <span lang="en">Move up gradually to {{ currentTargetTexture.en }} so your child practices chewing and avoids oral-motor delay.</span>
                      </p>
                    </template>
                    <template v-else-if="textureVerdict.status === 'coarse'">
                      <strong>
                        <span lang="id">Terlalu kasar untuk {{ selectedAge }} bulan</span>
                        <span lang="en">Too coarse for {{ selectedAge }} months</span>
                      </strong>
                      <p>
                        <span lang="id">Haluskan menjadi {{ currentTargetTexture.id }} untuk mengurangi risiko tersedak (choking risk).</span>
                        <span lang="en">Mash it down to {{ currentTargetTexture.en }} to eliminate choking hazard risk.</span>
                      </p>
                    </template>
                    <template v-else>
                      <strong>
                        <span lang="id">{{ textureVerdict.title ? textureVerdict.title.id : `Tekstur sesuai untuk ${selectedAge} bulan` }}</span>
                        <span lang="en">{{ textureVerdict.title ? textureVerdict.title.en : `Texture fits ${selectedAge} months` }}</span>
                      </strong>
                      <p>
                        <span lang="id">{{ textureVerdict.description ? textureVerdict.description.id : 'Cocok dengan tahap kesiapan oral-motor anak pada usia ini.' }}</span>
                        <span lang="en">{{ textureVerdict.description ? textureVerdict.description.en : 'Matches your child’s oral-motor readiness at this age.' }}</span>
                      </p>
                    </template>
                  </div>
                </div>
              </div>

              <div>
                <p class="result__h">
                  <span lang="id">Meter Makro Anti-Stunting (3 Pilar Pertumbuhan)</span>
                  <span lang="en">Anti-Stunting Macro Meter (3 Growth Pillars)</span>
                </p>
                <div class="meter">
                  <div v-for="m in macros" :key="m.key" class="meter__row">
                    <div class="meter__top">
                      <span>
                        <span lang="id">{{ m.name.id }}</span>
                        <span lang="en">{{ m.name.en }}</span>
                      </span>
                      <span class="meter__state">
                        <span lang="id">{{ STATE[m.rating].id }}</span>
                        <span lang="en">{{ STATE[m.rating].en }}</span>
                      </span>
                    </div>
                    <div class="meter__track">
                      <div :class="['meter__fill', m.rating]" :style="{ width: m.percentage + '%' }"></div>
                    </div>
                    <span v-if="m.hint" class="meter__hint">
                      <span lang="id">{{ m.hint.id }}</span>
                      <span lang="en">{{ m.hint.en }}</span>
                    </span>
                  </div>
                </div>
              </div>

              <div class="booster">
                <p class="result__h">
                  <span lang="id">Agen Tambal Gizi &amp; Resep Booster 5 Menit</span>
                  <span lang="en">Nutrient Booster Agent &amp; 5-Min Recipe</span>
                </p>

                <!-- Dynamic AI Booster Recipe if available -->
                <div v-if="dynamicBoosterRecipe" style="padding: 1.1rem 1.25rem; background: var(--paper); border-radius: .9rem .3rem .9rem .3rem; border: 1.5px solid var(--line-strong); margin-bottom: .9rem;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: .6rem; flex-wrap: wrap; gap: .5rem;">
                    <strong style="color: var(--clay-text); font-size: 1.15rem; font-family: var(--display); font-weight: 850; letter-spacing: -.01em;">
                      <span lang="id">{{ dynamicBoosterRecipe.name.id }}</span><span lang="en">{{ dynamicBoosterRecipe.name.en }}</span>
                    </strong>
                    <span class="tag" style="padding: .25rem .65rem; font-size: .82rem; font-weight: 700; background: var(--sand); border: 1px solid var(--line); color: var(--ink);">
                      <span lang="id">{{ dynamicBoosterRecipe.prep_time.id }}</span><span lang="en">{{ dynamicBoosterRecipe.prep_time.en }}</span>
                    </span>
                  </div>
                  <div style="font-size: .95rem; line-height: 1.6; color: var(--ink); margin-bottom: .6rem;">
                    <b style="color: var(--ink); font-weight: 800;">Bahan: </b>
                    <span v-for="(ing, idx) in dynamicBoosterRecipe.ingredients" :key="idx" style="color: var(--ink-2);">
                      <span lang="id">{{ ing.id }}</span><span lang="en">{{ ing.en }}</span><span v-if="idx < dynamicBoosterRecipe.ingredients.length - 1">, </span>
                    </span>
                  </div>
                  <div style="font-size: .95rem; line-height: 1.6; color: var(--ink);">
                    <b style="color: var(--ink); font-weight: 800;">Langkah Cepat:</b>
                    <ol style="padding-left: 1.3rem; margin: .35rem 0 0 0; line-height: 1.6; color: var(--ink-2);">
                      <li v-for="(inst, idx) in dynamicBoosterRecipe.instructions" :key="idx" style="margin-bottom: .3rem;">
                        <span lang="id">{{ inst.id }}</span><span lang="en">{{ inst.en }}</span>
                      </li>
                    </ol>
                  </div>
                  <div v-if="dynamicUpgradeSummary" style="margin-top: .85rem; padding: .75rem 1rem; background: var(--panel); border: 1px solid var(--line-strong); border-left: 3.5px solid var(--clay); border-radius: .5rem; font-size: .95rem; line-height: 1.55; color: var(--clay-text); font-weight: 700;">
                    <span lang="id">{{ dynamicUpgradeSummary.id }}</span><span lang="en">{{ dynamicUpgradeSummary.en }}</span>
                  </div>
                  <div v-if="dynamicSuggestions && dynamicSuggestions.length" style="margin-top: .85rem; padding-top: .75rem; border-top: 1px dashed var(--line); font-size: .95rem; line-height: 1.6; color: var(--ink);">
                    <b style="color: var(--ink); font-weight: 800; display: block; margin-bottom: .35rem;"><span lang="id">Rekomendasi Ahli Gizi:</span><span lang="en">Clinical Recommendations:</span></b>
                    <ul style="margin: 0; padding-left: 1.3rem; line-height: 1.6; color: var(--ink-2); display: grid; gap: .3rem;">
                      <li v-for="(sug, idx) in dynamicSuggestions" :key="idx">
                        <span lang="id">{{ sug.id }}</span><span lang="en">{{ sug.en }}</span>
                      </li>
                    </ul>
                  </div>
                </div>

                <!-- Fallback or additional tips -->
                <ul v-else-if="deficientMacros.length">
                  <li v-for="m in deficientMacros" :key="m.key">
                    <span>
                      <span lang="id">{{ m.recipe ? m.recipe.id : '' }}</span>
                      <span lang="en">{{ m.recipe ? m.recipe.en : '' }}</span>
                    </span>
                  </li>
                </ul>
                <ul v-else>
                  <li>
                    <span>
                      <span lang="id"><b>Piring sudah mencakup ketiga pilar esensial.</b> Untuk makan berikutnya, rotasi jenis protein hewani (misal: hati ayam, telur, atau ikan kembung) agar mikronutrisi zat besi &amp; zinc optimal.</span>
                      <span lang="en"><b>This plate covers all three essential pillars.</b> For the next meal, rotate the animal protein source (e.g., chicken liver, eggs, or mackerel) for optimal iron &amp; zinc bioavailability.</span>
                    </span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </section>
</template>
