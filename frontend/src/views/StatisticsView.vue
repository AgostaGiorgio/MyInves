<script setup>
import { BarChart3 } from 'lucide-vue-next'
</script>

<template>
  <section class="w-full flex flex-col items-center justify-center gap-4 py-24 px-6 text-center">
    <div class="w-16 h-16 rounded-2xl bg-brand-surface border border-white/10 flex items-center justify-center">
      <BarChart3 :size="28" :stroke-width="2" class="text-brand-primary" />
    </div>
    <h2 class="text-brand-textMain font-bold text-xl">Statistiche</h2>
    <p class="text-brand-textMuted text-sm max-w-xs">
      Coming soon. Qui potrai visualizzare analisi e andamenti del tuo portafoglio.
    </p>
  </section>
</template>
