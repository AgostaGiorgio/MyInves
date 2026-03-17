<script setup>
import { ref, onMounted } from 'vue'

import { api } from './services/api'
import AppHeader from './components/AppHeader.vue'
import MarketTicker from './components/MarketTicker.vue'
import BalanceHero from './components/BalanceHero.vue'
import AssetList from './components/AssetList.vue'
import TotalChart from './components/TotalChart.vue'
import AssetAllocation from './components/AssetAllocation.vue'
import AssetComparison from './components/AssetComparison.vue'
import AddReadingModal from './components/AddReadingModal.vue'

const marketData = ref([])
const portfolioTotal = ref(0)
const portfolioAssets = ref([])

const loadDashboardData = async () => {
  try {
    const [rawAssets, rawRates, rawPortfolio] = await Promise.all([
      api.getAssets(),
      api.getExchangeRates(),
      api.getPortfolio()
    ])

    const formattedRates = rawRates.map(rate => ({
      id: rate.id,
      type: 'rate',
      name: rate.currency,
      value: parseFloat(rate.rate_to_eur),
      date: new Date(rate.record_date).toLocaleDateString('it-IT', { day: 'numeric', month: 'short' }),
      iconUrl: null
    }))

    const formattedAssets = rawAssets
      .filter(asset => parseFloat(asset.price) !== 1)
      .map(asset => ({
        id: asset.id,
        type: 'asset',
        name: asset.name,
        value: parseFloat(asset.price),
        date: new Date(asset.price_date).toLocaleDateString('it-IT', { day: 'numeric', month: 'short' }),
        iconUrl: null 
      }))

    marketData.value = [...formattedAssets, ...formattedRates]

    formattedAssets.forEach(async (item) => {
      try {
        const iconData = await api.getAssetIcon(item.id)
        if (iconData && iconData.icon_base64) {
          const targetIndex = marketData.value.findIndex(m => m.id === item.id)
          if (targetIndex !== -1) {
            marketData.value[targetIndex].iconUrl = iconData.icon_base64
          }
        }
      } catch (err) {
        console.warn(`Nessuna icona trovata per ${item.name}`)
      }
    })

    let calculatedTotal = 0
    portfolioAssets.value = rawPortfolio.map(item => {
      const itemValue = parseFloat(item.total_value_eur)
      calculatedTotal += itemValue
      
      return {
        id: item.id,
        name: item.name,
        type: item.asset_type,
        value: itemValue,
        iconUrl: null 
      }
    })

    portfolioTotal.value = calculatedTotal

    rawAssets.forEach(async (rawAsset) => {
      try {
        const iconData = await api.getAssetIcon(rawAsset.id)
        if (iconData && iconData.icon_base64) {
          const tickerTarget = marketData.value.find(m => m.name === rawAsset.name)
          if (tickerTarget) tickerTarget.iconUrl = iconData.icon_base64
          const portfolioTarget = portfolioAssets.value.find(p => p.name === rawAsset.name)
          if (portfolioTarget) portfolioTarget.iconUrl = iconData.icon_base64
        }
      } catch (err) {
        console.warn(`Nessuna icona trovata per ${rawAsset.name}`)
      }
    })

  } catch (error) {
    console.error("Errore fatale nel caricamento del carosello:", error)
  }
}

onMounted(() => {
  loadDashboardData()
})

const isModalOpen = ref(false)
const refreshKey = ref(0)

const handleReadingsSubmit = async (payload) => {
  try {
    await api.addReadings(payload)
    isModalOpen.value = false
    await loadDashboardData()
    refreshKey.value += 1
  } catch (error) {
    console.error("Errore durante il salvataggio delle letture:", error)
    alert("Si è verificato un errore durante il salvataggio. Riprova.")
  }
}

</script>

<template>
  <div class="min-h-screen bg-brand-background flex flex-col items-center pb-24 font-sans">
    <AppHeader />

    <MarketTicker :items="marketData" />
    
    <BalanceHero :total="portfolioTotal" />

    <TotalChart :key="refreshKey"/>

    <AssetComparison :assets="portfolioAssets" :key="refreshKey"/>

    <AssetAllocation :assets="portfolioAssets" />

    <AssetList :assets="portfolioAssets" />
    

    <button @click="isModalOpen = true" class="fixed bottom-6 right-6 w-14 h-14 bg-brand-primary text-brand-textMain rounded-full flex items-center justify-center shadow-[0_8px_30px_rgba(139,92,246,0.4)] hover:bg-brand-secondary hover:scale-105 active:scale-95 transition-all duration-200 z-50">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
    </button>

    <AddReadingModal 
      v-if="isModalOpen" 
      :assets="portfolioAssets" 
      @close="isModalOpen = false" 
      @submit="handleReadingsSubmit" 
    />

  </div> 
</template>

<style scoped>
</style>