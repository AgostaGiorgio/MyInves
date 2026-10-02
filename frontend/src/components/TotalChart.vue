<script setup>
import { computed, ref, watch } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Filler } from 'chart.js'

import { useSensitiveVisibility } from '../composables/useSensitiveVisibility'
import { formatMoney } from '../utils/format'

const props = defineProps({
  points: { type: Array, default: () => [] }, // [{ record_date, total_value_eur }]
  height: { type: String, default: 'h-48' },
  fill: { type: Boolean, default: false },
})

const { isSensitiveHidden } = useSensitiveVisibility()
const chartEl = ref(null)

// Linea verticale + pallina sul punto attivo (crosshair "scorrevole").
const crosshairPlugin = {
  id: 'crosshair',
  afterDatasetsDraw(chart) {
    const active = chart.getActiveElements ? chart.getActiveElements() : []
    if (!active || active.length === 0) return
    const { ctx, chartArea } = chart
    const { x, y } = active[0].element
    ctx.save()
    ctx.beginPath()
    ctx.moveTo(x, chartArea.top)
    ctx.lineTo(x, chartArea.bottom)
    ctx.lineWidth = 1
    ctx.strokeStyle = 'rgba(139, 92, 246, 0.45)'
    ctx.stroke()
    ctx.beginPath()
    ctx.arc(x, y, 4, 0, Math.PI * 2)
    ctx.fillStyle = '#8b5cf6'
    ctx.fill()
    ctx.lineWidth = 2
    ctx.strokeStyle = '#f8fafc'
    ctx.stroke()
    ctx.restore()
  },
}

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Filler, crosshairPlugin)

watch(isSensitiveHidden, () => {
  if (chartEl.value && chartEl.value.chart) chartEl.value.chart.update()
})

const hasData = computed(() => props.points.length > 0)

const chartData = computed(() => {
  const labels = props.points.map((p) => {
    const d = new Date(p.record_date)
    return d.toLocaleDateString('it-IT', { day: 'numeric', month: 'short', year: '2-digit' })
  })
  const values = props.points.map((p) => Number(p.total_value_eur))

  return {
    labels,
    datasets: [{
      data: values,
      borderColor: '#8b5cf6',
      borderWidth: 3,
      tension: 0.4,
      spanGaps: true,
      fill: true,
      backgroundColor: (ctx) => {
        const { chart } = ctx
        const { ctx: c, chartArea } = chart
        if (!chartArea) return 'rgba(139, 92, 246, 0.12)'
        const gradient = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom)
        gradient.addColorStop(0, 'rgba(139, 92, 246, 0.28)')
        gradient.addColorStop(1, 'rgba(139, 92, 246, 0)')
        return gradient
      },
      pointRadius: values.length === 1 ? 4 : 0,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: '#8b5cf6',
      pointHoverBorderColor: '#f8fafc',
      pointHoverBorderWidth: 2,
    }],
  }
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
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
      caretSize: 0,
      callbacks: {
        label: (item) => (isSensitiveHidden.value ? '€ ••••' : formatMoney(item.parsed.y)),
      },
    },
  },
  scales: {
    x: {
      display: true,
      border: { display: false },
      grid: { display: false },
      ticks: { display: false, autoSkip: false },
    },
    y: {
      position: 'right',
      border: { display: false },
      grid: { color: 'rgba(255, 255, 255, 0.03)' },
      ticks: {
        color: '#94a3b8',
        font: { size: 10 },
        maxTicksLimit: 5,
        callback: function (value) {
          if (isSensitiveHidden.value) return '••••'
          return '€' + (value / 1000).toFixed(0) + 'k'
        },
      },
    },
  },
}))
</script>

<template>
  <div class="w-full relative" :class="fill ? 'flex-1 min-h-[12rem]' : height">
    <Line ref="chartEl" v-if="hasData" :data="chartData" :options="chartOptions" />
    <div v-else class="absolute inset-0 flex items-center justify-center text-brand-textMuted text-xs font-medium">
      No historical data
    </div>
  </div>
</template>
