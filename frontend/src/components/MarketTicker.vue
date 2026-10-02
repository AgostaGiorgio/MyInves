<script setup>
import { Coins } from 'lucide-vue-next'
import Sparkline from './ui/Sparkline.vue'

defineProps({
  // [{ id, name, value, date, iconUrl, series: number[] }]
  items: { type: Array, default: () => [] },
})

const fmtValue = (v) => Number(v).toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 4 })
const fmtDate = (d) => new Date(d).toLocaleDateString('it-IT', { day: 'numeric', month: 'short' })
</script>

<template>
  <div v-if="items.length" class="app-card divide-y divide-white/5">
    <div v-for="item in items" :key="item.id" class="flex items-center gap-3 px-4 py-3">
      <span class="w-8 h-8 rounded-full bg-brand-background border border-white/5 overflow-hidden flex items-center justify-center shrink-0">
        <img v-if="item.iconUrl" :src="item.iconUrl" :alt="item.name" class="w-full h-full object-cover" />
        <Coins v-else :size="15" class="text-brand-primary" />
      </span>

      <span class="flex-1 min-w-0 text-brand-textMain text-sm font-medium truncate">{{ item.name }}</span>

      <Sparkline v-if="item.series && item.series.length > 1" :values="item.series" :width="56" :height="26" />

      <span class="text-right shrink-0 w-[72px]">
        <span class="block text-brand-textMain text-sm font-bold">{{ fmtValue(item.value) }}</span>
        <span class="block text-brand-textMuted text-[10px]">{{ fmtDate(item.date) }}</span>
      </span>
    </div>
  </div>

  <div v-else class="app-card px-4 py-6 text-center text-brand-textMuted text-xs">
    No market data
  </div>
</template>
