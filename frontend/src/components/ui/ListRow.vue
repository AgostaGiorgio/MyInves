<script setup>
defineProps({
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  clickable: { type: Boolean, default: false },
})
</script>

<template>
  <div
    class="flex items-center gap-3 bg-brand-surface rounded-app-sm p-3 border border-white/5 min-w-0"
    :class="clickable ? 'hover:bg-brand-surface/80 active:scale-[0.99] transition-all cursor-pointer' : ''"
  >
    <div v-if="$slots.leading" class="shrink-0">
      <slot name="leading" />
    </div>
    <div class="flex-1 min-w-0 flex flex-col">
      <span v-if="title" class="text-brand-textMain font-semibold text-sm truncate">{{ title }}</span>
      <span v-if="subtitle" class="text-brand-textMuted text-[11px] truncate">{{ subtitle }}</span>
      <slot />
    </div>
    <div v-if="$slots.trailing" class="shrink-0 text-right">
      <slot name="trailing" />
    </div>
  </div>
</template>
