<script setup lang="ts">
import { ref } from 'vue';
import { usePlaybook } from '../../composables/usePlaybook';
import { useChildProfile } from '../../composables/useChildProfile';
import ChildContextBar from '../common/ChildContextBar.vue';
import ChildAvatarSvg from '../common/ChildAvatarSvg.vue';

const { activeChild } = useChildProfile();
const {
  currentScenario,
  days,
  completedCount,
  isAnalyzing,
  isLiveEvaluated,
  hasEvaluated,
  analysisError,
  toggleStep,
  isStepChecked,
  simulateAiEvaluation,
} = usePlaybook();

const parentObservationNote = ref('');

const handleStartAnalysis = async () => {
  const note =
    parentObservationNote.value.trim() ||
    `Pengamatan tumbuh kembang untuk ${activeChild.value.name} usia ${activeChild.value.ageMonths} bulan.`;
  await simulateAiEvaluation(note);
};
</script>

<template>
  <section id="modul-1" class="band">
    <div class="wrap">
      <ChildContextBar />

      <!-- Curated Clinical RAG Knowledge Base Disclaimer Banner -->
      <div
        style="margin-bottom: 2rem; padding: .85rem 1.15rem; background: var(--paper-2); border: 1.5px solid var(--line-strong); border-left: 4.5px solid var(--forest); border-radius: .7rem; display: flex; align-items: flex-start; gap: .75rem;"
        role="note"
        aria-label="Clinical Grounding Disclaimer"
      >
        <span style="font-size: 1.25rem; line-height: 1.2;" aria-hidden="true">🛡️</span>
        <div style="font-size: .84rem; color: var(--ink-2); line-height: 1.55;">
          <strong style="color: var(--ink); display: block; margin-bottom: .2rem;">
            <span lang="id">Pemberitahuan Klinis &amp; Sumber RAG Terkurasi:</span>
            <span lang="en">Clinical Grounding &amp; Curated RAG Sources:</span>
          </strong>
          <span lang="id">
            Seluruh evaluasi perkembangan dan rekomendasi nutrisi Nurtura di-<i>grounding</i> langsung menggunakan teknologi RAG berbasis dokumen klinis terkurasi: <b>WHO (2023) Complementary Feeding Guidelines</b>, <b>CDC Developmental Milestones (2m–60m)</b>, <b>WHO/UNICEF Care for Child Development (CCD)</b>, serta <b>Standar SDIDTK Kemenkes RI &amp; IDAI</b>. Fitur ini dirancang untuk edukasi orang tua dan pencegahan stunting dini, bukan sebagai pengganti pemeriksaan atau diagnosis langsung oleh dokter spesialis anak.
          </span>
          <span lang="en">
            All developmental evaluations and nutritional audits in Nurtura are grounded via RAG in curated clinical literature: <b>WHO (2023) Complementary Feeding Guidelines</b>, <b>CDC Developmental Milestones (2m–60m)</b>, <b>WHO/UNICEF Care for Child Development (CCD)</b>, and <b>Indonesian Pediatric Society (IDAI) Standards</b>. This platform is designed for co-parenting education and early stunting prevention, not as a replacement for professional clinical care.
          </span>
        </div>
      </div>

      <div class="mod__head">
        <div>
          <p class="label">
            <span lang="id">Modul 1</span>
            <span lang="en">Module 1</span>
          </p>
          <h2>Milestone &amp; Daily Playbook Agent</h2>
          <p class="mod__sub">
            <span lang="id">Dari pengamatan orang tua ke rencana bermain tiga hari</span>
            <span lang="en">From parent observations to a three-day play plan</span>
          </p>
        </div>
        <dl class="feats">
          <div>
            <dt>
              <span lang="id">Evaluasi sesuai konteks</span>
              <span lang="en">Context-aware evaluation</span>
            </dt>
            <dd>
              <span lang="id">Mencocokkan pengamatan dan daftar milestone orang tua dengan panduan perkembangan WHO dan CDC, lengkap dengan batasan keamanan.</span>
              <span lang="en">Matches parental observations and milestones against WHO and CDC developmental guidance, with clear safety thresholds.</span>
            </dd>
          </div>
          <div>
            <dt>
              <span lang="id">Playbook stimulasi 3 hari</span>
              <span lang="en">3-day stimulation playbook</span>
            </dt>
            <dd>
              <span lang="id">Bukan teks medis umum. Nurtura menyusun kurikulum rumah mini selama tiga hari, hanya dari barang yang sudah ada di rumah: kardus, cangkir plastik, sendok, dan majalah bekas.</span>
              <span lang="en">Not generic medical prose. Nurtura drafts a three-day home curriculum using everyday household objects: boxes, plastic cups, spoons, and food wrappers.</span>
            </dd>
          </div>
        </dl>
      </div>

      <div class="demo">
        <!-- Left Panel: Clinical Evaluation & Observation -->
        <section class="panel" aria-labelledby="eval-title">
          <div class="demo__top">
            <h3 class="demo__title" id="eval-title">
              <span lang="id">Evaluasi hari ini</span>
              <span lang="en">Today’s evaluation</span>
            </h3>
            <span class="tag">
              <span lang="id">RAG Klinis WHO/CDC</span>
              <span lang="en">WHO/CDC Clinical RAG</span>
            </span>
          </div>

          <!-- Active Child Demographic Context -->
          <p class="agebadge" style="display: inline-flex; align-items: center; gap: .45rem; flex-wrap: wrap;">
            <ChildAvatarSvg :age-months="activeChild.ageMonths" :gender="activeChild.gender" :size="24" />
            <b>{{ activeChild.name }}</b>
            <span>•</span>
            <b>{{ activeChild.ageMonths }}</b> <span lang="id">bulan</span><span lang="en">months</span>
            <span>•</span>
            <span>{{ activeChild.weightKg }} kg</span>
            <span>•</span>
            <span>{{ activeChild.heightCm }} cm</span>
          </p>

          <!-- Parent Note Box -->
          <div class="note mt">
            <small style="margin-bottom: .4rem; display: block; font-weight: 800;">
              <span lang="id">Catatan observasi orang tua</span>
              <span lang="en">Parent observation note</span>
            </small>
            <textarea
              v-model="parentObservationNote"
              rows="3"
              style="width: 100%; padding: .65rem .8rem; border: 1.5px solid var(--line-strong); border-radius: .6rem; background: var(--panel); color: var(--ink); font-family: var(--sans); font-size: .95rem; resize: vertical;"
              :placeholder="'Ceritakan pengamatan tumbuh kembang ' + activeChild.name + ' (misal: belum bisa berdiri sendiri tanpa pegangan, respons bicara, interaksi sosial, dsb)...'"
            ></textarea>
          </div>

          <!-- AI Evaluation Trigger Button (Without Emoji) -->
          <div style="margin-bottom: 1.1rem;">
            <button
              type="button"
              class="btn"
              style="width: 100%; text-align: center; padding: .75rem 1.2rem; font-size: .92rem;"
              :disabled="isAnalyzing"
              @click="handleStartAnalysis"
            >
              <span v-if="isAnalyzing">
                <span lang="id">Sedang Menganalisis dengan Gemini (RAG WHO/CDC)...</span>
                <span lang="en">Analyzing with Gemini (WHO/CDC RAG)...</span>
              </span>
              <span v-else>
                <span lang="id">Evaluasi Status &amp; Buat Playbook 3 Hari</span>
                <span lang="en">Audit Status &amp; Generate 3-Day Playbook</span>
              </span>
            </button>
          </div>

          <!-- Evaluation Results (Shown after evaluation) -->
          <template v-if="hasEvaluated">
            <!-- RAG Knowledge Base Clinical Grounding Box -->
            <div
              v-if="currentScenario.ragSources && currentScenario.ragSources.length"
              style="margin-bottom: .85rem; padding: .65rem .85rem; background: rgba(74, 94, 53, 0.08); border: 1.5px solid var(--forest); border-radius: .6rem;"
            >
              <div style="font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .06em; color: var(--olive-text); margin-bottom: .3rem; display: flex; align-items: center; gap: .35rem;">
                <span lang="id">Rujukan Pedoman Klinis (RAG Grounding):</span>
                <span lang="en">Clinical Grounding Guidelines (RAG):</span>
              </div>
              <ul style="margin: 0; padding-left: 1.1rem; font-size: .8rem; color: var(--ink-2);">
                <li v-for="(src, idx) in currentScenario.ragSources" :key="idx">
                  {{ src }}
                </li>
              </ul>
            </div>

            <p class="ref">
              <span lang="id">{{ currentScenario.ref.id }}</span>
              <span lang="en">{{ currentScenario.ref.en }}</span>
            </p>

            <!-- Status Indicator -->
            <div v-if="isLiveEvaluated" style="margin-bottom: .6rem;">
              <span class="tag" style="background: var(--band); color: var(--mustard); border: 1.5px solid var(--band); display: inline-flex; align-items: center;">
                <span lang="id">Hasil Analisis Dinamis AI</span>
                <span lang="en">Live Dynamic AI Evaluation</span>
              </span>
            </div>
            <div
              :class="[
                'status',
                currentScenario.statusType === 'ok' ? 'status--ok' : '',
                currentScenario.statusType === 'alert' ? 'status--coarse' : '',
              ]"
            >
              <span class="status__icon" aria-hidden="true"></span>
              <div>
                <strong>
                  <span lang="id">{{ currentScenario.statusTitle.id }}</span>
                  <span lang="en">{{ currentScenario.statusTitle.en }}</span>
                </strong>
                <p>
                  <span lang="id">{{ currentScenario.statusDesc.id }}</span>
                  <span lang="en">{{ currentScenario.statusDesc.en }}</span>
                </p>
              </div>
            </div>

            <p class="safety">
              <span lang="id">{{ currentScenario.safety.id }}</span>
              <span lang="en">{{ currentScenario.safety.en }}</span>
            </p>
          </template>

          <!-- Placeholder before evaluation -->
          <div
            v-else
            style="margin-top: .6rem; padding: 1.1rem; background: var(--paper-2); border: 1.5px dashed var(--line-strong); border-radius: .8rem; text-align: center;"
          >
            <p style="font-size: .88rem; color: var(--ink-2); margin: 0;">
              <span lang="id">Masukkan catatan observasi <b>{{ activeChild.name }}</b> di atas lalu klik <b>Evaluasi Status &amp; Buat Playbook 3 Hari</b> untuk mencocokkan dengan standar WHO &amp; CDC.</span>
              <span lang="en">Enter <b>{{ activeChild.name }}</b>'s observation note above and click <b>Audit Status &amp; Generate 3-Day Playbook</b> to evaluate against WHO &amp; CDC standards.</span>
            </p>
          </div>
          <div
            v-if="analysisError"
            role="alert"
            style="margin-top: .75rem; padding: .75rem .9rem; background: rgba(192, 98, 64, .1); border: 1.5px solid #c06240; border-radius: .6rem; color: #7d3522; font-size: .85rem;"
          >
            <span lang="id">Analisis Gemini gagal dan tidak ada hasil sample yang ditampilkan. Silakan coba lagi setelah koneksi Vertex AI tersedia.</span>
            <span lang="en">Gemini analysis failed and no sample result was displayed. Please try again when Vertex AI is available.</span>
          </div>
        </section>

        <!-- Right Panel: Interactive 3-Day Playbook -->
        <section class="panel" aria-labelledby="play-title">
          <div class="demo__top">
            <h3 class="demo__title" id="play-title">
              <span v-if="hasEvaluated">
                <span lang="id">Playbook 3 hari: {{ currentScenario.focusArea.id }}</span>
                <span lang="en">3-day playbook: {{ currentScenario.focusArea.en }}</span>
              </span>
              <span v-else>
                <span lang="id">Playbook 3 hari</span>
                <span lang="en">3-day playbook</span>
              </span>
            </h3>
            <span class="tag">Zero-Cost Tools</span>
          </div>

          <!-- Empty State before evaluation: Don't show playbook contents yet -->
          <div
            v-if="!hasEvaluated"
            style="padding: 3rem 1.5rem; text-align: center; background: var(--paper-2); border: 1.5px dashed var(--line-strong); border-radius: 1rem; margin-top: 1rem;"
          >
            <div style="font-size: 2.2rem; margin-bottom: .6rem;">📋</div>
            <h4 style="font-family: var(--display); font-size: 1.2rem; color: var(--ink); margin-bottom: .4rem;">
              <span lang="id">Playbook Belum Dibuat</span>
              <span lang="en">Playbook Not Generated Yet</span>
            </h4>
            <p style="font-size: .88rem; color: var(--ink-2); max-width: 360px; margin: 0 auto;">
              <span lang="id">Tulis catatan observasi untuk <b>{{ activeChild.name }}</b> di sebelah kiri, lalu klik <b>Evaluasi Status &amp; Buat Playbook 3 Hari</b> untuk menyusun kurikulum stimulasi rumah berbasis rujukan CDC &amp; WHO.</span>
              <span lang="en">Write observation notes for <b>{{ activeChild.name }}</b> on the left, then click <b>Audit Status &amp; Generate 3-Day Playbook</b> to generate your 3-day home curriculum.</span>
            </p>
          </div>

          <!-- Playbook rendered AFTER user evaluation -->
          <div v-else>
            <div class="progress" aria-live="polite">
              <div class="leafrow" id="leaves" aria-hidden="true">
                <i
                  v-for="j in 9"
                  :key="j"
                  class="lf"
                  :class="{ on: j <= completedCount }"
                ></i>
              </div>
              <span class="progress__txt" id="ptxt">
                <span lang="id">{{ completedCount }} dari 9 langkah selesai</span>
                <span lang="en">{{ completedCount }} of 9 steps done</span>
              </span>
            </div>

            <div id="playbook" class="mt">
              <div v-for="(d, i) in days" :key="i" class="day">
                <div class="day__meta">
                  <span class="day__n">
                    <span lang="id">Hari {{ i + 1 }}</span>
                    <span lang="en">Day {{ i + 1 }}</span>
                  </span>
                  <span class="day__item">
                    <span lang="id">{{ d.item.id }}</span>
                    <span lang="en">{{ d.item.en }}</span>
                  </span>
                </div>
                <h3>
                  <span lang="id">{{ d.title.id }}</span>
                  <span lang="en">{{ d.title.en }}</span>
                </h3>
                <ul class="steps">
                  <li
                    v-for="(s, j) in d.steps"
                    :key="j"
                    class="step"
                  >
                    <input
                      type="checkbox"
                      :id="`d${i}s${j}`"
                      :checked="isStepChecked(`d${i}s${j}`)"
                      @change="toggleStep(`d${i}s${j}`)"
                    />
                    <label :for="`d${i}s${j}`">
                      <span lang="id">{{ s.id }}</span>
                      <span lang="en">{{ s.en }}</span>
                    </label>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </section>
</template>
