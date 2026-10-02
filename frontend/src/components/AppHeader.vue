<script setup>
import { Eye, EyeOff, Plus } from 'lucide-vue-next'
import { useSensitiveVisibility } from '../composables/useSensitiveVisibility'

const { isSensitiveHidden, toggleSensitiveHidden } = useSensitiveVisibility()
</script>

<template>
  <header class="w-full flex justify-between items-center mb-2 px-5 mt-8">
    <div class="text-2xl font-extrabold tracking-tighter cursor-default">
        <span class="text-brand-textMain">My</span><span class="text-brand-primary">Inves.</span>
    </div>
    <div class="flex items-center gap-2">
      <RouterLink
        to="/readings/new"
        class="h-10 pl-3 pr-4 rounded-full bg-brand-primary text-white flex items-center gap-1.5 shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary active:scale-95 transition-all"
      >
        <Plus :size="18" :stroke-width="2.5" />
        <span class="text-xs font-bold whitespace-nowrap">Add reading</span>
      </RouterLink>

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
