<script setup>
import { computed, ref } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js'
import { Info } from 'lucide-vue-next'
import { allocationClass, CLASS_META } from '../constants/assetTypes'
import Money from './ui/Money.vue'

ChartJS.register(ArcElement, Tooltip)

const props = defineProps({
  // Portfolio items: [{ asset_type, total_value_eur }]
  items: { type: Array, default: () => [] },
  title: { type: String, default: 'Allocation' },
})

const showInfo = ref(false)

const slices = computed(() => {
  const totals = { dynamic: 0, static: 0, other: 0 }
  let total = 0

  for (const item of props.items) {
    const value = Number(item.total_value_eur) || 0
    const cls = allocationClass(item.asset_type)
    totals[cls] += value
    total += value
  }

  return ['dynamic', 'static', 'other']
    .map((cls) => ({
      cls,
      label: CLASS_META[cls].label,
      color: CLASS_META[cls].color,
      value: totals[cls],
      percentage: total > 0 ? (totals[cls] / total) * 100 : 0,
    }))
    .filter((s) => s.value > 0)
    .sort((a, b) => b.value - a.value)
})

const chartData = computed(() => ({
  labels: slices.value.map((s) => s.label),
  datasets: [{
    data: slices.value.map((s) => s.value),
    backgroundColor: slices.value.map((s) => s.color),
    borderWidth: 0,
    hoverOffset: 4,
  }],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '62%',
  plugins: { legend: { display: false }, tooltip: { enabled: false } },
}
</script>

<template>
  <div class="flex flex-col gap-3 flex-1 min-h-0">
    <div class="flex items-center justify-between">
      <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">{{ title }}</h2>
      <button
        type="button"
        @click="showInfo = !showInfo"
        class="w-7 h-7 rounded-full bg-brand-surface border border-white/10 flex items-center justify-center transition-colors"
        :class="showInfo ? 'text-brand-primary' : 'text-brand-textMuted hover:text-brand-primary'"
      >
        <Info :size="14" />
      </button>
    </div>

    <div v-if="slices.length" class="flex-1 flex flex-col items-center justify-center gap-4 min-h-0">
      <div class="relative w-40 h-40 shrink-0">
        <Doughnut :data="chartData" :options="chartOptions" />
      </div>

      <div class="w-full flex flex-col gap-2.5">
        <div v-for="slice in slices" :key="slice.cls" class="flex items-center justify-between gap-3">
          <div class="flex items-center gap-2 min-w-0">
            <span class="w-2.5 h-2.5 rounded-full shrink-0" :style="{ backgroundColor: slice.color }" />
            <span class="text-brand-textMain text-xs font-medium truncate">{{ slice.label }}</span>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <span class="text-brand-textMain text-xs font-bold tracking-wide">
              {{ slice.percentage.toFixed(1) }}%
            </span>
            <Money :value="slice.value" class="text-brand-textMuted text-xs" />
          </div>
        </div>
      </div>

      <Transition name="info">
        <div
          v-if="showInfo"
          class="w-full text-[11px] text-brand-textMuted bg-brand-background/40 rounded-app-sm p-3 flex flex-col gap-1.5 border border-white/5"
        >
          <p><span class="font-semibold text-brand-textMain">Dynamic</span> — value changes over time: ETFs, Crypto, Metals, bank accounts with interest.</p>
          <p><span class="font-semibold text-brand-textMain">Static</span> — value stays the same: cash, bank accounts without interest.</p>
          <p><span class="font-semibold text-brand-textMain">Other</span> — everything else (watches, cars, real estate, ...).</p>
        </div>
      </Transition>
    </div>

    <div v-else class="flex-1 flex items-center justify-center text-brand-textMuted text-xs">
      No allocation data
    </div>
  </div>
</template>

<style scoped>
.info-enter-active,
.info-leave-active {
  transition: all 0.2s ease;
}
.info-enter-from,
.info-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
