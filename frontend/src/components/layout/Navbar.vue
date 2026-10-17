<script setup lang="ts">
import { useLanguage } from '../../composables/useLanguage';

const { currentLang, setLanguage } = useLanguage();
</script>

<template>
  <header class="wrap top">
    <a class="top__brand" href="#atas" aria-label="Nurtura">
      <span class="top__mark" role="img" aria-label="Logo Nurtura"></span>
      <span class="top__name">Nurtura</span>
    </a>
    <nav aria-label="Navigasi">
      <a href="#masalah"><span lang="id">Masalah</span><span lang="en">Problem</span></a>
      <a href="#modul-1"><span lang="id">Modul 1</span><span lang="en">Module 1</span></a>
      <a href="#modul-2"><span lang="id">Modul 2</span><span lang="en">Module 2</span></a>
    </nav>
    <div class="lang" role="group" aria-label="Bahasa / Language">
      <button
        type="button"
        id="lang-id"
        :aria-pressed="currentLang === 'id'"
        @click="setLanguage('id')"
      >
        ID
      </button>
      <button
        type="button"
        id="lang-en"
        :aria-pressed="currentLang === 'en'"
        @click="setLanguage('en')"
      >
        EN
      </button>
    </div>
  </header>
</template>
