<script setup>
import { ref } from 'vue'

import AppHeader from './components/AppHeader.vue'
import MarketTicker from './components/MarketTicker.vue'
import BalanceHero from './components/BalanceHero.vue'
import AssetList from './components/AssetList.vue'
import TotalChart from './components/TotalChart.vue'
import AssetAllocation from './components/AssetAllocation.vue'
import AssetComparison from './components/AssetComparison.vue'
import AddReadingModal from './components/AddReadingModal.vue'

const portfolioTotal = ref(15250.75)

const marketData = ref([
  { id: 1, type: 'asset', name: 'BTC', value: 58420.50, date: '27 Feb', iconUrl: 'https://cryptologos.cc/logos/bitcoin-btc-logo.svg?v=029' },
  { id: 2, type: 'asset', name: 'IWDA', value: 94.20, date: '26 Feb', iconUrl: 'https://cdn-icons-png.flaticon.com/512/2635/2635285.png' },
  { id: 3, type: 'rate', name: 'USD', value: 0.923, date: '27 Feb', iconUrl: null },
  { id: 4, type: 'rate', name: 'AED', value: 0.251, date: '27 Feb', iconUrl: null }
])

const portfolioAssets = ref([
  { id: 1, name: 'IWDA', type: 'ETF', value: 5240.50, iconUrl: 'https://cdn-icons-png.flaticon.com/512/2635/2635285.png' },
  { id: 2, name: 'BINANCE', type: 'CRYPTO', value: 3150.25, iconUrl: 'https://cryptologos.cc/logos/binance-coin-bnb-logo.svg?v=029' },
  { id: 3, name: 'UNICREDIT', type: 'BANK_ACCOUNT', value: 4500.00, iconUrl: null },
  { id: 4, name: 'ORO', type: 'GOLD', value: 2360.00, iconUrl: null },
  { id: 5, name: 'WIO', type: 'BANK_ACCOUNT', value: 1250.00, iconUrl: null }
])

const isModalOpen = ref(false)

</script>

<template>
  <div class="min-h-screen bg-brand-background flex flex-col items-center pb-24 font-sans">
    <AppHeader />

    <MarketTicker :items="marketData" />
    
    <BalanceHero :total="portfolioTotal" />

    <TotalChart />

    <AssetComparison :assets="portfolioAssets" />

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