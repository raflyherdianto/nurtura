<script setup lang="ts">
import { ref } from 'vue';
import ChildAvatarSvg from './ChildAvatarSvg.vue';
import { useChildProfile, type ChildGender } from '../../composables/useChildProfile';
import { usePlateLab } from '../../composables/usePlateLab';

const { activeChild, updateProfile } = useChildProfile();
const { setAge } = usePlateLab();

const isEditing = ref(false);

const formName = ref(activeChild.value.name);
const formGender = ref<ChildGender>(activeChild.value.gender || 'boy');
const formAge = ref(activeChild.value.ageMonths);
const formWeight = ref(activeChild.value.weightKg);
const formHeight = ref(activeChild.value.heightCm);

const openEditForm = () => {
  formName.value = activeChild.value.name;
  formGender.value = activeChild.value.gender || 'boy';
  formAge.value = activeChild.value.ageMonths;
  formWeight.value = activeChild.value.weightKg;
  formHeight.value = activeChild.value.heightCm;
  isEditing.value = true;
};

const cancelEdit = () => {
  isEditing.value = false;
};

const saveProfileForm = () => {
  const age = Number(formAge.value) || 12;
  const weight = Number(formWeight.value) || 9;
  const height = Number(formHeight.value) || 75;
  const name = formName.value.trim() || 'Anak';

  updateProfile({
    name,
    gender: formGender.value,
    ageMonths: age,
    weightKg: weight,
    heightCm: height,
    presetKey: 'custom',
  });

  // Synchronize age across Plate Lab and Playbook
  if (age <= 8) {
    setAge(7);
  } else if (age <= 12) {
    setAge(10);
  } else {
    setAge(14);
  }

  isEditing.value = false;
};
</script>

<template>
  <aside
    class="panel"
    style="margin-bottom: 2.2rem; padding: 1.1rem 1.4rem; background: var(--paper-2); border-radius: 1.4rem .4rem 1.4rem .4rem; border: 1.5px solid var(--line);"
    aria-label="Konteks Profil Anak Aktif"
  >
    <!-- Top Summary Row -->
    <div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
      <div style="display: flex; align-items: center; gap: .9rem; flex-wrap: wrap;">
        <!-- Dynamic Child Vector SVG Illustration -->
        <ChildAvatarSvg
          :age-months="activeChild.ageMonths"
          :gender="activeChild.gender"
          :size="48"
        />

        <div>
          <div style="display: flex; align-items: center; gap: .55rem; flex-wrap: wrap;">
            <span style="font-weight: 800; font-size: .88rem; letter-spacing: .08em; text-transform: uppercase; color: var(--clay-text);">
              <span lang="id">Profil Anak Aktif:</span>
              <span lang="en">Active Child Profile:</span>
            </span>
            <strong style="font-family: var(--display); font-size: 1.25rem; color: var(--ink);">
              {{ activeChild.name }}
            </strong>
            <span
              style="display: inline-flex; align-items: center; padding: .15rem .5rem; border-radius: .4rem; font-size: .75rem; font-weight: 700; background: var(--panel); border: 1px solid var(--line-strong); color: var(--ink-2);"
            >
              <span v-if="activeChild.gender === 'girl'">
                <span lang="id">Perempuan</span>
                <span lang="en">Girl</span>
              </span>
              <span v-else>
                <span lang="id">Laki-laki</span>
                <span lang="en">Boy</span>
              </span>
            </span>
          </div>

          <div style="font-size: .92rem; color: var(--ink-2); font-weight: 700; margin-top: .15rem;">
            {{ activeChild.ageMonths }} <span lang="id">bulan</span><span lang="en">months</span> • {{ activeChild.weightKg }} kg • {{ activeChild.heightCm }} cm
          </div>
        </div>
      </div>

      <!-- Action: Edit Profile -->
      <div style="display: flex; align-items: center; gap: .6rem; flex-wrap: wrap;">
        <button
          type="button"
          class="btn btn--ghost"
          style="padding: .45rem .85rem; font-size: .85rem; border: 1.5px solid var(--line-strong);"
          @click="isEditing ? cancelEdit() : openEditForm()"
        >
          <span v-if="!isEditing">
            <span lang="id">✏️ Isi / Ubah Profil</span>
            <span lang="en">✏️ Edit Profile Form</span>
          </span>
          <span v-else>
            <span lang="id">Tutup Form</span>
            <span lang="en">Close Form</span>
          </span>
        </button>
      </div>
    </div>

    <!-- Collapsible / Editable Profile Form -->
    <form
      v-if="isEditing"
      @submit.prevent="saveProfileForm"
      style="margin-top: 1.2rem; padding-top: 1.1rem; border-top: 1.5px dotted var(--line-strong);"
    >
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 1rem; align-items: end;">
        <!-- Input Nama -->
        <div>
          <label style="display: block; font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .08em; color: var(--ink-2); margin-bottom: .35rem;">
            <span lang="id">Nama Anak</span>
            <span lang="en">Child Name</span>
          </label>
          <input
            v-model="formName"
            type="text"
            required
            placeholder="Contoh: Bima"
            style="width: 100%; padding: .55rem .85rem; border: 1.5px solid var(--line-strong); border-radius: .8rem .2rem .8rem .2rem; background: var(--panel); color: var(--ink); font-family: var(--sans); font-weight: 700; font-size: .95rem;"
          />
        </div>

        <!-- Input Jenis Kelamin -->
        <div>
          <label style="display: block; font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .08em; color: var(--ink-2); margin-bottom: .35rem;">
            <span lang="id">Jenis Kelamin</span>
            <span lang="en">Gender</span>
          </label>
          <div style="display: flex; gap: .35rem;">
            <button
              type="button"
              :class="['btn', formGender === 'boy' ? '' : 'btn--ghost']"
              :style="formGender === 'boy' ? 'padding: .5rem .5rem; font-size: .84rem; flex: 1; text-align: center;' : 'padding: .5rem .5rem; font-size: .84rem; flex: 1; text-align: center; border: 1.5px solid var(--line-strong);'"
              @click="formGender = 'boy'"
            >
              <span lang="id">Laki-laki</span>
              <span lang="en">Boy</span>
            </button>
            <button
              type="button"
              :class="['btn', formGender === 'girl' ? '' : 'btn--ghost']"
              :style="formGender === 'girl' ? 'padding: .5rem .5rem; font-size: .84rem; flex: 1; text-align: center;' : 'padding: .5rem .5rem; font-size: .84rem; flex: 1; text-align: center; border: 1.5px solid var(--line-strong);'"
              @click="formGender = 'girl'"
            >
              <span lang="id">Perempuan</span>
              <span lang="en">Girl</span>
            </button>
          </div>
        </div>

        <!-- Input Umur -->
        <div>
          <label style="display: block; font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .08em; color: var(--ink-2); margin-bottom: .35rem;">
            <span lang="id">Umur (0–60 Bulan)</span>
            <span lang="en">Age (0–60 Months)</span>
          </label>
          <input
            v-model.number="formAge"
            type="number"
            min="0"
            max="60"
            required
            placeholder="14"
            style="width: 100%; padding: .55rem .85rem; border: 1.5px solid var(--line-strong); border-radius: .8rem .2rem .8rem .2rem; background: var(--panel); color: var(--ink); font-family: var(--sans); font-weight: 700; font-size: .95rem;"
          />
        </div>

        <!-- Input Berat Badan -->
        <div>
          <label style="display: block; font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .08em; color: var(--ink-2); margin-bottom: .35rem;">
            <span lang="id">Berat Badan (kg)</span>
            <span lang="en">Weight (kg)</span>
          </label>
          <input
            v-model.number="formWeight"
            type="number"
            step="0.1"
            min="1"
            max="40"
            required
            placeholder="9.8"
            style="width: 100%; padding: .55rem .85rem; border: 1.5px solid var(--line-strong); border-radius: .8rem .2rem .8rem .2rem; background: var(--panel); color: var(--ink); font-family: var(--sans); font-weight: 700; font-size: .95rem;"
          />
        </div>

        <!-- Input Tinggi Badan -->
        <div>
          <label style="display: block; font-size: .78rem; font-weight: 800; text-transform: uppercase; letter-spacing: .08em; color: var(--ink-2); margin-bottom: .35rem;">
            <span lang="id">Tinggi Badan (cm)</span>
            <span lang="en">Height (cm)</span>
          </label>
          <input
            v-model.number="formHeight"
            type="number"
            step="0.1"
            min="30"
            max="150"
            required
            placeholder="78"
            style="width: 100%; padding: .55rem .85rem; border: 1.5px solid var(--line-strong); border-radius: .8rem .2rem .8rem .2rem; background: var(--panel); color: var(--ink); font-family: var(--sans); font-weight: 700; font-size: .95rem;"
          />
        </div>

        <!-- Tombol Aksi -->
        <div style="display: flex; gap: .5rem;">
          <button
            type="submit"
            class="btn"
            style="padding: .6rem 1.1rem; font-size: .88rem; flex: 1; text-align: center;"
          >
            <span lang="id">Simpan</span>
            <span lang="en">Save</span>
          </button>
          <button
            type="button"
            class="btn btn--ghost"
            style="padding: .6rem .85rem; font-size: .88rem;"
            @click="cancelEdit"
          >
            <span lang="id">Batal</span>
            <span lang="en">Cancel</span>
          </button>
        </div>
      </div>
    </form>
  </aside>
</template>
