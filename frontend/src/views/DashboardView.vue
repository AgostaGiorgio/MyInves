<script setup>
import { ref, computed, onMounted } from 'vue'

import { api } from '../services/api'
import { usePortfolio } from '../composables/usePortfolio'
import { useLookups } from '../composables/useLookups'
import { useStatistics } from '../composables/useStatistics'
import SegmentedControl from '../components/ui/SegmentedControl.vue'
import PortfolioHero from '../components/PortfolioHero.vue'
import MarketTicker from '../components/MarketTicker.vue'

const { items, total, load } = usePortfolio()
const { typeLabels, load: loadLookups } = useLookups()
const { stats, load: loadStats } = useStatistics()

const period = ref('3m')
const periodOptions = [
  { value: '3m', label: '3M' },
  { value: '6m', label: '6M' },
  { value: '12m', label: '12M' },
  { value: '24m', label: '24M' },
  { value: 'all', label: 'All' },
]
const MONTHS = { '3m': 3, '6m': 6, '12m': 12, '24m': 24 }
const SERIES_LENGTH = 6

const history = ref([])
const marketItems = ref([])

const loadExtras = async () => {
  try {
    const [hist, market] = await Promise.all([
      api.getPortfolioHistory('all'),
      api.getMarketHistory(SERIES_LENGTH),
    ])

    history.value = Array.isArray(hist) ? hist.filter(Boolean) : []

    marketItems.value = market.map((item) => ({
      id: `${item.kind}-${item.id}`,
      name: item.name,
      value: item.value !== null && item.value !== undefined ? Number(item.value) : null,
      date: item.date,
      iconUrl: item.icon_base64,
      series: (item.points || []).map((p) => Number(p.value)),
    }))
  } catch (e) {
    console.error('Failed to load dashboard data:', e)
  }
}

onMounted(async () => {
  loadLookups()
  await Promise.all([load(), loadExtras(), loadStats()])
})

const filteredPoints = computed(() => {
  if (period.value === 'all') return history.value
  const months = MONTHS[period.value]
  const now = new Date()
  const start = new Date(now.getFullYear(), now.getMonth() - months, 1)
  return history.value.filter((p) => new Date(p.record_date) >= start)
})

const change = computed(() => {
  const pts = filteredPoints.value
  if (pts.length < 2) return { changeEur: null, changePct: null }
  const first = Number(pts[0].total_value_eur)
  const last = Number(pts[pts.length - 1].total_value_eur)
  return { changeEur: last - first, changePct: first ? ((last - first) / first) * 100 : null }
})
</script>

<template>
  <main class="w-full px-4">
    <div class="py-3 flex flex-col gap-5 w-full">
      <div class="w-full lg:pr-28">
        <div class="w-full max-w-sm mx-auto">
          <SegmentedControl v-model="period" :options="periodOptions" />
        </div>
      </div>

      <PortfolioHero
        :total="total"
        :change-eur="change.changeEur"
        :change-pct="change.changePct"
        :month-pct="stats?.change_vs_prev_month_pct"
        :points="filteredPoints"
        :items="items"
        :labels="typeLabels"
      />

      <MarketTicker :items="marketItems" />
    </div>
  </main>
</template>
