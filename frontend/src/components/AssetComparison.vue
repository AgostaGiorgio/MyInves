<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Tooltip } from 'chart.js'

import { api } from '../services/api'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip)

const props = defineProps({
  assets: {
    type: Array,
    required: true
  }
})

const comparisonColors = ['#3b82f6', '#10b981', '#f59e0b', '#ec4899', '#06b6d4']

const rawHistoryData = ref([])
const isLoading = ref(true)

const selectedAssetIds = ref([])

watch(() => props.assets, (newAssets) => {
  if (selectedAssetIds.value.length === 0 && newAssets.length > 0) {
    selectedAssetIds.value = newAssets.slice(0, 2).map(a => a.id)
  }
}, { immediate: true })

const fetchHistory = async () => {
  try {
    rawHistoryData.value = await api.getAssetsHistory()
  } catch (error) {
    console.error("Errore nel caricamento storico asset:", error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchHistory()
})

const toggleAssetSelection = (id) => {
  if (selectedAssetIds.value.includes(id)) {
    selectedAssetIds.value = selectedAssetIds.value.filter(selectedId => selectedId !== id)
  } else if (selectedAssetIds.value.length < 5) {
    selectedAssetIds.value.push(id)
  }
}

const comparisonChartData = computed(() => {
  let maxLength = 0

  const datasets = selectedAssetIds.value.map((id, index) => {
    const asset = props.assets.find(a => a.id === id)
    if (!asset) return null

    const historyObj = rawHistoryData.value.find(h => h.asset_name === asset.name)
    const values = historyObj ? historyObj.values : []

    const dataPoints = values.map(v => parseFloat(v.total_value_eur))
    
    if (dataPoints.length > maxLength) maxLength = dataPoints.length

    return {
      label: asset.name,
      data: dataPoints,
      borderColor: comparisonColors[index % comparisonColors.length],
      backgroundColor: comparisonColors[index % comparisonColors.length],
      borderWidth: 2.5,
      tension: 0.4,
      pointRadius: dataPoints.length === 1 ? 4 : 0,
      pointHoverRadius: dataPoints.length === 1 ? 6 : 0
    }
  }).filter(d => d !== null)

  const labels = Array.from({ length: maxLength }, (_, i) => String(i + 1))

  return {
    labels: labels,
    datasets: datasets.length > 0 ? datasets : [{ data: [] }]
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
    <div class="flex items-center">
      <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Confronta Andamento</span>
    </div>

    <div class="w-full flex overflow-x-auto gap-2 hide-scrollbar">
      <button 
        v-for="asset in assets" 
        :key="'compare-' + asset.id" 
        @click="toggleAssetSelection(asset.id)"
        class="flex-none px-3 py-1.5 rounded-full text-[11px] font-bold tracking-wide transition-all border border-white/5 flex items-center gap-1.5"
        :class="selectedAssetIds.includes(asset.id) ? 'bg-brand-surface text-brand-textMain shadow-sm' : 'bg-transparent text-brand-textMuted hover:bg-brand-surface/50'"
      >
        <span 
          v-if="selectedAssetIds.includes(asset.id)" 
          class="w-2 h-2 rounded-full" 
          :style="{ backgroundColor: comparisonColors[selectedAssetIds.indexOf(asset.id)] }"
        ></span>
        {{ asset.name }}
      </button>
    </div>

    <div class="w-full h-48 bg-brand-surface/30 rounded-app-sm p-2 border border-white/5 relative">
      <Line v-if="selectedAssetIds.length > 0 && !isLoading" :data="comparisonChartData" :options="chartOptions" />
      
      <div v-else-if="isLoading" class="absolute inset-0 flex items-center justify-center text-brand-textMuted text-xs font-medium">
        Caricamento storico...
      </div>
      
      <div v-else class="absolute inset-0 flex items-center justify-center text-brand-textMuted text-xs font-medium">
        Seleziona un asset per visualizzare il grafico
      </div>
    </div>
  </section>
</template>