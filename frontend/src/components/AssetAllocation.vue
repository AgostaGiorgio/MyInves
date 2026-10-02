<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js'
import { typeColor, typeLabel } from '../constants/assetTypes'

ChartJS.register(ArcElement, Tooltip)

const props = defineProps({
  // Portfolio items: [{ asset_type, total_value_eur }]
  items: { type: Array, default: () => [] },
  // code -> label (dal catalogo backend)
  labels: { type: Object, default: () => ({}) },
})

const slices = computed(() => {
  const totals = new Map()
  let total = 0

  for (const item of props.items) {
    const value = Number(item.total_value_eur) || 0
    totals.set(item.asset_type, (totals.get(item.asset_type) || 0) + value)
    total += value
  }

  return [...totals.entries()]
    .map(([type, value]) => ({
      type,
      label: props.labels[type] || typeLabel(type),
      value,
      color: typeColor(type),
      percentage: total > 0 ? (value / total) * 100 : 0,
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
  <div v-if="slices.length" class="flex flex-col items-center gap-4">
    <div class="relative w-40 h-40 shrink-0">
      <Doughnut :data="chartData" :options="chartOptions" />
    </div>

    <div class="w-full flex flex-col gap-2.5">
      <div v-for="slice in slices" :key="slice.type" class="flex items-center justify-between gap-3">
        <div class="flex items-center gap-2 min-w-0">
          <span class="w-2.5 h-2.5 rounded-full shrink-0" :style="{ backgroundColor: slice.color }" />
          <span class="text-brand-textMain text-xs font-medium truncate">{{ slice.label }}</span>
        </div>
        <span class="text-brand-textMain text-xs font-bold tracking-wide shrink-0">
          {{ slice.percentage.toFixed(1) }}%
        </span>
      </div>
    </div>
  </div>

  <div v-else class="flex items-center justify-center py-16 text-brand-textMuted text-xs">
    No composition data
  </div>
</template>
