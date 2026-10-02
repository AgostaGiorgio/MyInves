<script setup>
import { ref } from 'vue'
import BalanceHero from './BalanceHero.vue'
import TotalChart from './TotalChart.vue'
import AssetAllocation from './AssetAllocation.vue'
import SegmentedControl from './ui/SegmentedControl.vue'
import { useMediaQuery } from '../composables/useMediaQuery'

defineProps({
  total: { type: [Number, String], default: 0 },
  changeEur: { type: [Number, String], default: null },
  changePct: { type: [Number, String], default: null },
  monthPct: { type: [Number, String], default: null },
  points: { type: Array, default: () => [] },
  items: { type: Array, default: () => [] },
  labels: { type: Object, default: () => ({}) },
})

const isDesktop = useMediaQuery('(min-width: 1024px)')

const activeTab = ref('performance')
const tabs = [
  { value: 'performance', label: 'Performance' },
  { value: 'composition', label: 'Composition' },
]
</script>

<template>
  <!-- Desktop: Performance e Composition disaccoppiate in due card affiancate -->
  <div v-if="isDesktop" class="grid grid-cols-[2fr_1fr] gap-5">
    <section class="app-card rounded-app p-5 flex flex-col gap-5">
      <BalanceHero :total="total" :change-eur="changeEur" :change-pct="changePct" :month-pct="monthPct" />
      <TotalChart :points="points" fill />
    </section>

    <section class="app-card rounded-app p-5 flex flex-col gap-5 justify-center">
      <AssetAllocation :items="items" :labels="labels" />
    </section>
  </div>

  <!-- Mobile: una card con i tab -->
  <section v-else class="app-card rounded-app p-5 flex flex-col gap-5">
    <BalanceHero :total="total" :change-eur="changeEur" :change-pct="changePct" :month-pct="monthPct" />

    <SegmentedControl v-model="activeTab" :options="tabs" />

    <TotalChart v-if="activeTab === 'performance'" :points="points" />
    <AssetAllocation v-else :items="items" :labels="labels" />
  </section>
</template>
