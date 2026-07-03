<script setup>
    defineProps({
    total: {
        type: Number,
        required: true
    }
    })
</script>

<template>
  <section class="w-full flex flex-col gap-2">
    <div class="flex items-center">
      <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Bilancio Attuale</span>
    </div>

    <div class="text-4xl font-extrabold text-brand-textMain tracking-tighter">
      € {{ total.toLocaleString('it-IT', { minimumFractionDigits: 2 }) }}
    </div>
  </section>
</template>