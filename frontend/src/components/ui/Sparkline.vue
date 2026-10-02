<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement)

const props = defineProps({
  values: { type: Array, default: () => [] },
  width: { type: Number, default: 56 },
  height: { type: Number, default: 26 },
})

const up = computed(() => {
  const v = props.values
  if (v.length < 2) return true
  return v[v.length - 1] >= v[0]
})

const color = computed(() => (up.value ? '#10b981' : '#ef4444'))

const chartData = computed(() => ({
  labels: props.values.map((_, i) => i),
  datasets: [{
    data: props.values,
    borderColor: color.value,
    borderWidth: 2,
    tension: 0.4,
    pointRadius: 0,
    pointHoverRadius: 0,
    fill: false,
  }],
}))

const chartOptions = {
  responsive: false,
  animation: false,
  plugins: { legend: { display: false }, tooltip: { enabled: false } },
  scales: { x: { display: false }, y: { display: false } },
  layout: { padding: 2 },
}
</script>

<template>
  <Line v-if="values.length > 1" :data="chartData" :options="chartOptions" :width="width" :height="height" />
</template>
