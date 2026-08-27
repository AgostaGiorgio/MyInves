<script setup>
import { ref, onMounted } from 'vue'
import { Wallet, TrendingUp, TrendingDown, Trophy, ArrowUpRight, ArrowDownRight, Percent } from 'lucide-vue-next'
import { api } from '../services/api'

const stats = ref(null)
const isLoading = ref(true)

const loadStatistics = async () => {
  try {
    stats.value = await api.getStatistics()
  } catch (error) {
    console.error("Error loading statistics:", error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadStatistics()
})

const formatMoney = (value) => {
  if (value === null || value === undefined) return '—'
  return '€ ' + Number(value).toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatPct = (value) => {
  if (value === null || value === undefined) return '—'
  const num = Number(value)
  const sign = num > 0 ? '+' : ''
  return sign + num.toFixed(2).replace('.', ',') + '%'
}

const pctColor = (value) => {
  if (value === null || value === undefined) return 'text-brand-textMuted'
  return Number(value) >= 0 ? 'text-emerald-400' : 'text-red-400'
}

const pctArrow = (value) => {
  if (value === null || value === undefined) return null
  return Number(value) >= 0 ? TrendingUp : TrendingDown
}

const formatMonth = (month) => {
  if (!month) return '—'
  const [year, m] = month.split('-')
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  return `${months[Number(m) - 1]} ${year}`
}

const isPositive = (value) => value !== null && value !== undefined && Number(value) >= 0
</script>

<template>
  <main class="w-full px-4">
    <div v-if="isLoading" class="flex items-center justify-center py-24">
      <span class="text-brand-textMuted text-sm font-medium">Loading statistics...</span>
    </div>

    <div v-else-if="!stats" class="flex flex-col items-center justify-center gap-2 py-24 px-6 text-center">
      <Wallet :size="28" :stroke-width="2" class="text-brand-primary" />
      <p class="text-brand-textMuted text-sm">Unable to load statistics.</p>
    </div>

    <div v-else class="py-6 flex flex-col gap-7 w-full">
      <div class="flex flex-col gap-3">
        <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Current Total</span>
        <div class="flex items-center gap-3">
          <span class="text-4xl font-extrabold text-brand-textMain tracking-tighter">
            {{ formatMoney(stats.current_total_eur) }}
          </span>
          <span v-if="stats.change_vs_prev_month_pct !== null" class="flex items-center gap-1 text-sm font-semibold px-2 py-1 rounded-md"
            :class="isPositive(stats.change_vs_prev_month_pct) ? 'bg-emerald-400/10 text-emerald-400' : 'bg-red-400/10 text-red-400'">
            <component :is="pctArrow(stats.change_vs_prev_month_pct)" :size="14" />
            {{ formatPct(stats.change_vs_prev_month_pct) }}
          </span>
        </div>
        <span class="text-xs text-brand-textMuted">vs previous month</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="flex flex-col gap-1 bg-brand-surface/30 rounded-app-sm p-4 border border-white/5">
          <div class="flex items-center gap-2 text-brand-textMuted">
            <Percent :size="14" />
            <span class="text-xs uppercase tracking-widest font-semibold">Avg Monthly Growth</span>
          </div>
          <span class="text-2xl font-bold" :class="pctColor(stats.avg_monthly_growth_pct)">
            {{ formatPct(stats.avg_monthly_growth_pct) }}
          </span>
        </div>

        <div class="flex flex-col gap-1 bg-brand-surface/30 rounded-app-sm p-4 border border-white/5">
          <div class="flex items-center gap-2 text-brand-textMuted">
            <Trophy :size="14" />
            <span class="text-xs uppercase tracking-widest font-semibold">Best Growth to Date</span>
          </div>
          <div class="flex items-center gap-2">
            <span v-if="stats.best_growth_to_date && stats.best_growth_to_date.asset_icon"
              class="w-6 h-6 rounded-full overflow-hidden shrink-0 ring-1 ring-white/10 bg-brand-surface">
              <img :src="stats.best_growth_to_date.asset_icon" alt="icon" class="w-full h-full object-cover" />
            </span>
            <span class="text-brand-textMain font-semibold text-base truncate">
              {{ stats.best_growth_to_date ? stats.best_growth_to_date.asset_name : '—' }}
            </span>
          </div>
          <span class="text-sm font-bold text-emerald-400">
            {{ stats.best_growth_to_date ? formatPct(stats.best_growth_to_date.growth_pct) : '—' }}
          </span>
        </div>

        <div class="flex flex-col gap-1 bg-brand-surface/30 rounded-app-sm p-4 border border-white/5">
          <div class="flex items-center gap-2 text-brand-textMuted">
            <ArrowUpRight :size="14" />
            <span class="text-xs uppercase tracking-widest font-semibold">Best Single Month</span>
          </div>
          <div class="flex items-center gap-2">
            <span v-if="stats.best_single_month && stats.best_single_month.asset_icon"
              class="w-6 h-6 rounded-full overflow-hidden shrink-0 ring-1 ring-white/10 bg-brand-surface">
              <img :src="stats.best_single_month.asset_icon" alt="icon" class="w-full h-full object-cover" />
            </span>
            <span class="text-brand-textMain font-semibold text-base truncate">
              {{ stats.best_single_month ? stats.best_single_month.asset_name : '—' }}
            </span>
          </div>
          <span class="text-xs text-brand-textMuted">
            {{ stats.best_single_month ? formatMonth(stats.best_single_month.month) : '' }}
          </span>
          <span class="text-sm font-bold text-emerald-400">
            {{ stats.best_single_month ? formatPct(stats.best_single_month.change_pct) : '—' }}
          </span>
        </div>

        <div class="flex flex-col gap-1 bg-brand-surface/30 rounded-app-sm p-4 border border-white/5">
          <div class="flex items-center gap-2 text-brand-textMuted">
            <ArrowDownRight :size="14" />
            <span class="text-xs uppercase tracking-widest font-semibold">Lowest Single Month</span>
          </div>
            <div class="flex items-center gap-2">
              <span v-if="stats.worst_single_month && stats.worst_single_month.asset_icon"
                class="w-6 h-6 rounded-full overflow-hidden shrink-0 ring-1 ring-white/10 bg-brand-surface">
                <img :src="stats.worst_single_month.asset_icon" alt="icon" class="w-full h-full object-cover" />
              </span>
              <span class="text-brand-textMain font-semibold text-base truncate">
                {{ stats.worst_single_month ? stats.worst_single_month.asset_name : '—' }}
              </span>
            </div>
          <span class="text-xs text-brand-textMuted">
            {{ stats.worst_single_month ? formatMonth(stats.worst_single_month.month) : '' }}
          </span>
          <span class="text-sm font-bold text-red-400">
            {{ stats.worst_single_month ? formatPct(stats.worst_single_month.change_pct) : '—' }}
          </span>
        </div>
      </div>

      <div class="flex flex-col gap-3 bg-brand-surface/30 rounded-app-sm p-4 border border-white/5">
        <div class="flex items-center gap-2 text-brand-textMuted">
          <Percent :size="14" />
          <span class="text-xs uppercase tracking-widest font-semibold">Avg Monthly Growth per Asset</span>
        </div>
        <div v-if="!stats.per_asset_avg_monthly || stats.per_asset_avg_monthly.length === 0"
          class="text-brand-textMuted text-sm">No data available.</div>
        <div v-else class="flex flex-col divide-y divide-white/5">
          <div v-for="row in stats.per_asset_avg_monthly" :key="row.asset_name"
            class="flex items-center justify-between gap-3 py-2">
            <div class="flex items-center gap-3 min-w-0">
              <span v-if="row.asset_icon"
                class="w-6 h-6 rounded-full overflow-hidden shrink-0 ring-1 ring-white/10 bg-brand-surface">
                <img :src="row.asset_icon" alt="icon" class="w-full h-full object-cover" />
              </span>
              <span class="text-brand-textMain text-sm font-medium truncate">{{ row.asset_name }}</span>
            </div>
            <span class="text-sm font-semibold" :class="pctColor(row.avg_monthly_pct)">
              {{ formatPct(row.avg_monthly_pct) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
