<script setup>
const props = defineProps({
  name: { type: String, default: '' },
  icon: { type: String, default: null },
  size: { type: Number, default: 40 },
})

const initial = () => (props.name || '?').charAt(0).toUpperCase()
</script>

<template>
  <span
    class="rounded-full bg-brand-background border border-white/5 overflow-hidden flex items-center justify-center shrink-0"
    :style="{ width: size + 'px', height: size + 'px' }"
  >
    <img v-if="icon" :src="icon" :alt="name" class="w-full h-full object-cover" />
    <span v-else class="text-brand-primary font-bold" :style="{ fontSize: size * 0.36 + 'px' }">{{ initial() }}</span>
  </span>
</template>
