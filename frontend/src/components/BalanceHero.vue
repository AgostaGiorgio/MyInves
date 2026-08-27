<script setup>
    import { useSensitiveVisibility, maskAmount } from '../composables/useSensitiveVisibility'
    const { isSensitiveHidden } = useSensitiveVisibility()

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
      <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Current Balance</span>
    </div>

    <div class="text-4xl font-extrabold text-brand-textMain tracking-tighter">
      <span v-if="isSensitiveHidden">{{ maskAmount() }}</span>
      <span v-else>€ {{ total.toLocaleString('it-IT', { minimumFractionDigits: 2 }) }}</span>
    </div>
  </section>
</template>
