<script setup>
defineProps({
  label: { type: String, default: '' },
  accent: { type: String, default: '' },
})
</script>

<template>
  <div class="flex flex-col gap-1 bg-brand-surface/30 rounded-app-sm p-4 border border-white/5">
    <span class="text-[11px] text-brand-textMuted uppercase tracking-widest font-semibold">{{ label }}</span>
    <div class="flex items-center gap-2 min-w-0">
      <slot />
    </div>
    <div v-if="$slots.hint" class="text-[11px] text-brand-textMuted">
      <slot name="hint" />
    </div>
  </div>
</template>
