<script setup>
import { ref, computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Tooltip } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip)

const props = defineProps({
  assets: {
    type: Array,
    required: true
  }
})

// Logica del confronto
const comparisonColors = ['#3b82f6', '#10b981', '#f59e0b', '#ec4899', '#06b6d4']
const assetHistoricalData = {
  1: [4800, 4950, 4900, 5100, 5050, 5180, 5240.50],
  2: [2200, 2400, 2100, 2800, 2950, 3000, 3150.25],
  3: [4500, 4500, 4500, 4500, 4500, 4500, 4500.00],
  4: [2100, 2150, 2200, 2180, 2250, 2300, 2360.00],
  5: [1250, 1250, 1250, 1250, 1250, 1250, 1250.00]
}

const selectedAssetIds = ref([1, 2])

const toggleAssetSelection = (id) => {
  if (selectedAssetIds.value.includes(id)) {
    selectedAssetIds.value = selectedAssetIds.value.filter(selectedId => selectedId !== id)
  } else if (selectedAssetIds.value.length < 5) {
    selectedAssetIds.value.push(id)
  }
}

const comparisonChartData = computed(() => {
  const datasets = selectedAssetIds.value.map((id, index) => {
    const asset = props.assets.find(a => a.id === id)
    return {
      label: asset?.name || 'Sconosciuto',
      data: assetHistoricalData[id] || [],
      borderColor: comparisonColors[index % comparisonColors.length],
      borderWidth: 2.5, tension: 0.4, pointRadius: 0, pointHoverRadius: 0
    }
  })

  return {
    labels: ['1', '2', '3', '4', '5', '6', '7'],
    datasets: datasets.length > 0 ? datasets : [{ data: [] }]
  }
})

// Opzioni del grafico (identiche al TotalChart)
const chartOptions = {
  responsive: true, maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { enabled: false } },
  scales: {
    x: { display: false },
    y: {
      position: 'right', border: { display: false }, grid: { color: 'rgba(255, 255, 255, 0.03)' },
      ticks: { color: '#94a3b8', font: { size: 10 }, maxTicksLimit: 5, callback: function(value) { return '€' + (value / 1000).toFixed(0) + 'k' } }
    }
  }
}
</script>

<template>
  <section class="w-full max-w-md px-5 mb-10 flex flex-col items-start">
    <h2 class="text-brand-textMuted text-[11px] font-semibold uppercase tracking-wider mb-2">
      Confronta Andamento
    </h2>

    <div class="w-full flex overflow-x-auto gap-2 pb-2 hide-scrollbar mb-4">
      <button 
        v-for="asset in assets" :key="'compare-' + asset.id" @click="toggleAssetSelection(asset.id)"
        class="flex-none px-3 py-1.5 rounded-full text-[11px] font-bold tracking-wide transition-all border border-white/5 flex items-center gap-1.5"
        :class="selectedAssetIds.includes(asset.id) ? 'bg-brand-surface text-brand-textMain shadow-sm' : 'bg-transparent text-brand-textMuted hover:bg-brand-surface/50'"
      >
        <span v-if="selectedAssetIds.includes(asset.id)" class="w-2 h-2 rounded-full" :style="{ backgroundColor: comparisonColors[selectedAssetIds.indexOf(asset.id)] }"></span>
        {{ asset.name }}
      </button>
    </div>

    <div class="w-full h-48 bg-brand-surface/30 rounded-app-sm p-2 border border-white/5 relative">
      <Line v-if="selectedAssetIds.length > 0" :data="comparisonChartData" :options="chartOptions" />
      <div v-else class="absolute inset-0 flex items-center justify-center text-brand-textMuted text-xs font-medium">
        Seleziona un asset per visualizzare il grafico
      </div>
    </div>
  </section>
</template>