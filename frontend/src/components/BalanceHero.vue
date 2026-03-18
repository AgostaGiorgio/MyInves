<script setup>
    defineProps({
    total: {
        type: Number,
        required: true
    }
    })
</script>

<template>
  <main class="w-full max-w-md px-5 mb-4 flex flex-col items-start mt-4">
    <h2 class="text-brand-textMuted text-[11px] font-semibold uppercase tracking-wider mb-2">
      Bilancio Attuale
    </h2>
    <div class="text-4xl font-extrabold text-brand-textMain tracking-tighter">
      € {{ total.toLocaleString('it-IT', { minimumFractionDigits: 2 }) }}
    </div>
  </main>
</template>