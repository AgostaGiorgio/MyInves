<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Tooltip } from 'chart.js'

import { api } from '../services/api'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip)

const timeFilters = ['3 Mesi', '6 Mesi', '12 Mesi', 'Tutto']
const activeFilter = ref('Tutto')
const apiPeriodMap = {
  '3 Mesi': '3m',
  '6 Mesi': '6m',
  '12 Mesi': '12m',
  'Tutto': 'all'
}

const rawHistoryData = ref([])
const isLoading = ref(true)

const fetchChartData = async () => {
  try {
    const periodParam = apiPeriodMap[activeFilter.value]
    
    const data = await api.getPortfolioHistory(periodParam)
    rawHistoryData.value = data
  } catch (error) {
    console.error("Errore nel caricamento del grafico storico:", error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchChartData()
})

watch(activeFilter, () => {
  fetchChartData()
})


const chartData = computed(() => {
  if (rawHistoryData.value.length === 0) {
    return { labels: [], datasets: [] }
  }

  const labels = rawHistoryData.value.map(item => {
    const d = new Date(item.record_date)
    return d.toLocaleDateString('it-IT', { day: 'numeric', month: 'short' })
  })

  const dataPoints = rawHistoryData.value.map(item => parseFloat(item.total_value_eur))

  return {
    labels: labels,
    datasets: [{
      data: dataPoints,
      borderColor: '#8b5cf6',
      borderWidth: 3,
      tension: 0.4,
      pointRadius: dataPoints.length === 1 ? 4 : 0,
      pointHoverRadius: dataPoints.length === 1 ? 6 : 0
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { enabled: false } },
  scales: {
    x: { display: false },
    y: {
      position: 'right',
      border: { display: false },
      grid: { color: 'rgba(255, 255, 255, 0.03)' },
      ticks: {
        color: '#94a3b8',
        font: { size: 10 },
        maxTicksLimit: 5,
        callback: function(value) { return '€' + (value / 1000).toFixed(0) + 'k' }
      }
    }
  }
}
</script>

<template>
  <section class="w-full flex flex-col items-start gap-2">
    
    <div class="w-full h-48 bg-brand-surface/30 rounded-app-sm p-2 border border-white/5 relative">
      <Line v-if="rawHistoryData.length > 0 && !isLoading" :data="chartData" :options="chartOptions" />
      
      <div v-else-if="isLoading" class="absolute inset-0 flex items-center justify-center text-brand-textMuted text-xs font-medium">
        Caricamento storico...
      </div>

      <div v-else class="absolute inset-0 flex items-center justify-center text-brand-textMuted text-xs font-medium">
        Dati storici non presenti sulla piattaforma
      </div>
    </div>

    <div class="bg-brand-surface/60 p-1 rounded-app-sm flex justify-between border border-white/5 mx-auto max-w-xs w-full">
      <button 
        v-for="filter in timeFilters" 
        :key="filter"
        @click="activeFilter = filter"
        class="flex-1 text-[10px] font-semibold py-1.5 rounded-[6px] transition-all duration-300 tracking-wide"
        :class="activeFilter === filter 
          ? 'bg-brand-primary text-brand-textMain shadow-sm' 
          : 'text-brand-textMuted hover:text-brand-textMain'"
      >
        {{ filter }}
      </button>
    </div>

  </section>
</template>