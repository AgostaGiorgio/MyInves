<script setup>
import { ref, computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Tooltip } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip)

// Filtri interni al componente
const timeFilters = ['3 Mesi', '6 Mesi', '12 Mesi', 'Tutto']
const activeFilter = ref('Tutto')

// Dati mockati (in futuro li passeremo come Props da App.vue)
const chartData = computed(() => {
  return {
    labels: ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago'],
    datasets: [{
      data: [12000, 12500, 11800, 13200, 14000, 13800, 14500, 15250.75],
      borderColor: '#8b5cf6',
      borderWidth: 3,
      tension: 0.4,
      pointRadius: 0,
      pointHoverRadius: 0
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
  <section class="w-full max-w-md px-5 mb-10">
    <div class="w-full h-40 mb-5">
      <Line :data="chartData" :options="chartOptions" />
    </div>
    <div class="bg-brand-surface/60 p-1 rounded-app-sm flex justify-between border border-white/5 mx-auto max-w-xs">
      <button 
        v-for="filter in timeFilters" :key="filter" @click="activeFilter = filter"
        class="flex-1 text-[10px] font-semibold py-1.5 rounded-[6px] transition-all duration-300 tracking-wide"
        :class="activeFilter === filter ? 'bg-brand-primary text-brand-textMain shadow-sm' : 'text-brand-textMuted hover:text-brand-textMain'"
      >
        {{ filter }}
      </button>
    </div>
  </section>
</template>