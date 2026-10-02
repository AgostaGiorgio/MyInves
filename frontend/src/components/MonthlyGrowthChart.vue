<script setup>
import { computed, ref, watch } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip } from 'chart.js'

import { useSensitiveVisibility } from '../composables/useSensitiveVisibility'
import { formatPct, formatMoney } from '../utils/format'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip)

const props = defineProps({
  points: { type: Array, default: () => [] }, // [{ record_date, total_value_eur }]
  height: { type: String, default: 'h-44' },
  fill: { type: Boolean, default: false },
})

const { isSensitiveHidden } = useSensitiveVisibility()
const chartEl = ref(null)

watch(isSensitiveHidden, () => {
  if (chartEl.value && chartEl.value.chart) chartEl.value.chart.update()
})

const monthLabel = (iso) => {
  const d = new Date(iso)
  return d.toLocaleDateString('it-IT', { month: 'short', year: '2-digit' })
}

// Variazione mese-su-mese tra snapshot consecutivi.
const changes = computed(() => {
  const pts = props.points
  const out = []
  for (let i = 1; i < pts.length; i++) {
    const prev = Number(pts[i - 1].total_value_eur)
    const curr = Number(pts[i].total_value_eur)
    if (!prev) continue
    out.push({ date: pts[i].record_date, pct: ((curr - prev) / prev) * 100, eur: curr - prev })
  }
  return out
})

const hasData = computed(() => changes.value.length > 0)

const chartData = computed(() => ({
  labels: changes.value.map((c) => monthLabel(c.date)),
  datasets: [{
    data: changes.value.map((c) => Number(c.pct.toFixed(2))),
    backgroundColor: changes.value.map((c) =>
      c.pct > 0
        ? 'rgba(16, 185, 129, 0.85)'
        : c.pct < 0
          ? 'rgba(239, 68, 68, 0.85)'
          : 'rgba(148, 163, 184, 0.55)'
    ),
    borderRadius: 4,
    maxBarThickness: 34,
  }],
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      enabled: true,
      displayColors: false,
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      borderWidth: 1,
      padding: 10,
      titleColor: '#94a3b8',
      titleFont: { size: 10 },
      bodyColor: '#f8fafc',
      bodyFont: { size: 13, weight: '700' },
      callbacks: {
        label: (item) => {
          const c = changes.value[item.dataIndex]
          const eur = isSensitiveHidden.value ? '€ ••••' : formatMoney(c.eur)
          return `${formatPct(c.pct)}  (${eur})`
        },
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      border: { display: false },
      ticks: { color: '#94a3b8', font: { size: 10 }, maxRotation: 0, autoSkip: true },
    },
    y: {
      grid: { color: 'rgba(255, 255, 255, 0.03)' },
      border: { display: false },
      ticks: {
        color: '#94a3b8',
        font: { size: 10 },
        maxTicksLimit: 4,
        callback: (v) => v + '%',
      },
    },
  },
}))
</script>

<template>
  <div class="w-full relative" :class="fill ? 'flex-1 min-h-[11rem]' : height">
    <Bar ref="chartEl" v-if="hasData" :data="chartData" :options="chartOptions" />
    <div v-else class="absolute inset-0 flex items-center justify-center text-brand-textMuted text-xs font-medium">
      No monthly data
    </div>
  </div>
</template>
