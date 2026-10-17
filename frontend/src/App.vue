<script setup lang="ts">
import Navbar from './components/layout/Navbar.vue';
import HeroSection from './components/home/HeroSection.vue';
import ProblemSection from './components/home/ProblemSection.vue';
import MilestoneModule from './components/home/MilestoneModule.vue';
import SmartPlateModule from './components/home/SmartPlateModule.vue';
import Footer from './components/layout/Footer.vue';
</script>

<template>
  <Navbar />
  <main id="atas">
    <HeroSection />
    <ProblemSection />
    <MilestoneModule />
    <SmartPlateModule />
  </main>
  <Footer />
</template>
