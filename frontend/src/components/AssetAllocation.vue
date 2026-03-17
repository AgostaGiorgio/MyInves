<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js'

ChartJS.register(ArcElement, Tooltip)

const props = defineProps({
  assets: {
    type: Array,
    required: true
  }
})

const assetTypeColors = {
  'ETF': '#3b82f6', 'CRYPTO': '#10b981', 'BANK_ACCOUNT': '#8b5cf6', 'GOLD': '#f59e0b', 'CASH': '#ec4899'
}

const assetTypeDistribution = computed(() => {
  const totals = {}
  let totalValue = 0

  props.assets.forEach(asset => {
    if (!totals[asset.type]) totals[asset.type] = 0
    totals[asset.type] += asset.value
    totalValue += asset.value
  })

  return Object.keys(totals).map(type => {
    const value = totals[type]
    return {
      type: type.replace('_', ' '),
      value: value,
      percentage: totalValue > 0 ? ((value / totalValue) * 100).toFixed(1) : 0,
      color: assetTypeColors[type] || '#94a3b8'
    }
  }).sort((a, b) => b.value - a.value)
})

const doughnutChartData = computed(() => ({
  labels: assetTypeDistribution.value.map(d => d.type),
  datasets: [{
    data: assetTypeDistribution.value.map(d => d.value),
    backgroundColor: assetTypeDistribution.value.map(d => d.color),
    borderWidth: 0, hoverOffset: 4
  }]
}))

const doughnutChartOptions = {
  responsive: true, maintainAspectRatio: false, cutout: '75%',
  plugins: { legend: { display: false }, tooltip: { enabled: false } }
}
</script>

<template>
  <section class="w-full max-w-md px-5 mb-10 flex flex-col items-start">
    <h2 class="text-brand-textMuted text-[11px] font-semibold uppercase tracking-wider mb-2">
      Allocazione Asset
    </h2>
    <div class="w-full bg-brand-surface rounded-app-sm p-5 border border-white/5 flex items-center gap-6">
      
      <div class="relative w-28 h-28 shrink-0 flex items-center justify-center">
        <Doughnut :data="doughnutChartData" :options="doughnutChartOptions" />
        <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
          <svg class="w-6 h-6 text-brand-textMuted/30" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12V8H6a2 2 0 01-2-2c0-1.1.9-2 2-2h12v4"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6v12a2 2 0 002 2h14v-4H6a2 2 0 01-2-2V6z"></path></svg>
        </div>
      </div>
      
      <div class="flex flex-col gap-3 flex-1">
        <div v-for="item in assetTypeDistribution" :key="item.type" class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full shadow-sm" :style="{ backgroundColor: item.color }"></span>
            <span class="text-brand-textMain text-xs font-medium">{{ item.type }}</span>
          </div>
          <span class="text-brand-textMain text-xs font-bold tracking-wide">{{ item.percentage }}%</span>
        </div>
      </div>

    </div>
  </section>
</template>