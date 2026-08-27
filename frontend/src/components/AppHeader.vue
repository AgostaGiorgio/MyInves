<script setup>
import { Eye, EyeOff } from 'lucide-vue-next'
import { useSensitiveVisibility } from '../composables/useSensitiveVisibility'

const { isSensitiveHidden, toggleSensitiveHidden } = useSensitiveVisibility()
</script>

<template>
  <header class="w-full flex justify-between items-center mb-2 px-5 mt-8">
    <div class="text-2xl font-extrabold tracking-tighter cursor-default">
        <span class="text-brand-textMain">My</span><span class="text-brand-primary">Inves.</span>
    </div>
    <div class="flex items-center gap-2">
      <button
        @click="toggleSensitiveHidden"
        :title="isSensitiveHidden ? 'Show sensitive data' : 'Hide sensitive data'"
        class="w-10 h-10 rounded-full bg-brand-surface border border-white/10 flex items-center justify-center shadow-sm hover:bg-brand-surface/80 transition-colors"
        :class="isSensitiveHidden ? 'text-brand-primary' : 'text-brand-textMuted'"
      >
        <EyeOff v-if="isSensitiveHidden" :size="18" />
        <Eye v-else :size="18" />
      </button>
    </div>
  </header>
</template>
