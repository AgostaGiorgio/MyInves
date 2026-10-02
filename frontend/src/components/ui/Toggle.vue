<script setup>
const props = defineProps({
  modelValue: { type: Boolean, default: false },
  label: { type: String, default: '' },
  hint: { type: String, default: '' },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <label class="flex items-center justify-between gap-3 py-1 cursor-pointer">
    <span class="flex flex-col">
      <span v-if="label" class="text-sm text-brand-textMain">{{ label }}</span>
      <span v-if="hint" class="text-[11px] text-brand-textMuted">{{ hint }}</span>
    </span>
    <button
      type="button"
      role="switch"
      :aria-checked="modelValue"
      @click="emit('update:modelValue', !modelValue)"
      class="relative w-11 h-6 rounded-full transition-colors duration-200 focus:outline-none shrink-0"
      :class="modelValue ? 'bg-brand-primary' : 'bg-white/10'"
    >
      <span
        class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform duration-200"
        :class="modelValue ? 'translate-x-5' : ''"
      />
    </button>
  </label>
</template>
