<script setup>
import AppHeader from './components/AppHeader.vue'
import AppNavbar from './components/AppNavbar.vue'
</script>

<template>
  <div class="min-h-screen bg-brand-background flex flex-col items-center text-brand-textMain font-sans pb-36 selection:bg-brand-primary selection:text-white">
    <AppHeader />

    <RouterView />

    <AppNavbar />
  </div>
</template>

<style scoped>
</style>
