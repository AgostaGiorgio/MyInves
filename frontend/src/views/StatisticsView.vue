<script setup>
import { computed, onMounted, ref } from 'vue'
import { Wallet } from 'lucide-vue-next'

import { api } from '../services/api'
import { useStatistics } from '../composables/useStatistics'
import { usePortfolio } from '../composables/usePortfolio'
import { typeColor, allocationClass, typeOrder } from '../constants/assetTypes'
import { formatPct, toNumber } from '../utils/format'
import { trendClass, trendIcon } from '../utils/trend'

import Money from '../components/ui/Money.vue'
import PnLValue from '../components/ui/PnLValue.vue'
import AssetAvatar from '../components/ui/AssetAvatar.vue'
import Skeleton from '../components/ui/Skeleton.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import AllocationClasses from '../components/AllocationClasses.vue'
import MonthlyGrowthChart from '../components/MonthlyGrowthChart.vue'

const { stats, loading, load } = useStatistics()
const { items, load: loadPortfolio } = usePortfolio()

const history = ref([])
const assetHistory = ref([])

onMounted(async () => {
  await Promise.all([load(), loadPortfolio()])
  try {
    const [pf, ah] = await Promise.all([api.getPortfolioHistory('all'), api.getAssetsHistory()])
    history.value = (pf || []).filter(Boolean)
    assetHistory.value = ah || []
  } catch (e) {
    console.error('Failed to load history:', e)
  }
})

const allocation = computed(() => stats.value?.allocation || [])

// Ultimi 8 punti -> 7 variazioni mensili (il grafico Growth mostra max 7 mesi).
const growthPoints = computed(() => history.value.slice(-8))

const avgByName = computed(() =>
  Object.fromEntries((stats.value?.per_asset_avg_monthly || []).map((a) => [a.asset_name, a.avg_monthly_pct]))
)

// Variazione ultimo mese vs precedente, per asset (da /assets/history).
const momByName = computed(() => {
  const out = {}
  for (const entry of assetHistory.value) {
    const vals = (entry.values || [])
      .filter((v) => toNumber(v.total_value_eur) !== null)
      .sort((a, b) => new Date(a.record_date) - new Date(b.record_date))
    if (vals.length < 2) continue
    const prev = Number(vals[vals.length - 2].total_value_eur)
    const curr = Number(vals[vals.length - 1].total_value_eur)
    if (!prev) continue
    out[entry.asset_name] = { pct: ((curr - prev) / prev) * 100, eur: curr - prev, prev, curr }
  }
  return out
})

// MoM aggregato per tipo (somma delle variazioni € / somma dei valori precedenti).
const momByType = computed(() => {
  const acc = {}
  for (const a of items.value) {
    const m = momByName.value[a.name]
    if (!m) continue
    if (!acc[a.asset_type]) acc[a.asset_type] = { eur: 0, prev: 0 }
    acc[a.asset_type].eur += m.eur
    acc[a.asset_type].prev += m.prev
  }
  return Object.fromEntries(
    Object.entries(acc).map(([type, v]) => [type, v.prev ? (v.eur / v.prev) * 100 : null])
  )
})

const allocationRows = computed(() =>
  allocation.value.map((row) => ({ ...row, momPct: momByType.value[row.asset_type] ?? null }))
)

const isDynamic = (type) => allocationClass(type) === 'dynamic'

// Asset ordinati per tipo (ordine canonico) e, dentro il tipo, per valore.
const assetRows = computed(() =>
  [...items.value]
    .map((a) => ({
      ...a,
      avgMonthly: avgByName.value[a.name] ?? null,
      momPct: momByName.value[a.name]?.pct ?? null,
      dynamic: isDynamic(a.asset_type),
    }))
    .sort((a, b) => {
      const byTypeOrder = typeOrder(a.asset_type) - typeOrder(b.asset_type)
      if (byTypeOrder !== 0) return byTypeOrder
      return (Number(b.total_value_eur) || 0) - (Number(a.total_value_eur) || 0)
    })
)

const pctColor = trendClass
</script>

<template>
  <main class="w-full px-4">
    <div class="py-4 flex flex-col gap-5 w-full">
      <Skeleton v-if="loading && !stats" :lines="4" height="h-24" />

      <EmptyState
        v-else-if="!stats"
        :icon="Wallet"
        title="Unable to load statistics"
        description="Please try again later."
      />

      <template v-else>
        <!-- Totale + variazione mese + score medio -->
        <section class="app-card rounded-app p-5 flex flex-col gap-4">
          <div class="text-4xl font-extrabold tracking-tighter">
            <Money :value="stats.current_total_eur" />
          </div>

          <div class="flex items-center gap-3 flex-wrap">
            <span class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">vs last month</span>
            <span class="flex items-center gap-1 text-sm font-bold" :class="pctColor(stats.change_vs_prev_month_pct)">
              <component :is="trendIcon(stats.change_vs_prev_month_pct)" v-if="trendIcon(stats.change_vs_prev_month_pct)" :size="14" />
              {{ formatPct(stats.change_vs_prev_month_pct) }}
            </span>
            <span class="text-sm font-semibold" :class="pctColor(stats.change_vs_prev_month_eur)">
              <Money :value="stats.change_vs_prev_month_eur" signed />
            </span>
          </div>

          <div class="flex items-center gap-3">
            <span class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">avg monthly score</span>
            <span class="text-sm font-bold" :class="pctColor(stats.avg_monthly_growth_pct)">
              {{ formatPct(stats.avg_monthly_growth_pct) }}<span class="text-brand-textMuted font-medium"> / month</span>
            </span>
          </div>
        </section>

        <!-- Growth + Allocation: affiancate su desktop -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <!-- Come sta crescendo: variazione mensile (ultimi 7 mesi) -->
          <section class="app-card rounded-app p-5 flex flex-col gap-3">
            <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">Growth</h2>
            <MonthlyGrowthChart :points="growthPoints" fill />
          </section>

          <!-- Dove sono allocati i fondi (dinamico / statico / other) -->
          <section v-if="items.length" class="app-card rounded-app p-5 flex flex-col">
            <AllocationClasses :items="items" />
          </section>
        </div>

        <!-- Performance per tipo -->
        <section v-if="allocation.length" class="app-card rounded-app p-5 flex flex-col gap-3">
          <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">By type</h2>
          <div class="flex flex-col divide-y divide-white/5">
            <div
              v-for="row in allocationRows"
              :key="row.asset_type"
              class="flex items-center gap-3 py-3 first:pt-0 last:pb-0"
            >
              <div class="flex flex-col min-w-0 flex-1 gap-0.5">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="w-2.5 h-2.5 rounded-full shrink-0" :style="{ backgroundColor: typeColor(row.asset_type) }" />
                  <span class="text-brand-textMain text-sm font-medium truncate">{{ row.label }}</span>
                  <span class="text-[11px] text-brand-textMuted tabular-nums shrink-0">{{ row.weight_pct }}%</span>
                </div>
                <div class="flex items-center gap-1.5 text-[10px] font-semibold pl-[18px]">
                  <span :class="pctColor(row.momPct)">MoM {{ formatPct(row.momPct) }}</span>
                  <template v-if="isDynamic(row.asset_type)">
                    <span class="text-brand-textMuted">·</span>
                    <span :class="pctColor(row.avg_monthly_pct)">avg {{ formatPct(row.avg_monthly_pct) }}/mo</span>
                  </template>
                </div>
              </div>
              <div class="flex flex-col items-end shrink-0 gap-0.5">
                <Money :value="row.total_value_eur" class="text-brand-textMain font-bold text-sm" />
                <PnLValue :pl-eur="row.unrealized_pl_eur" :pct="row.unrealized_pl_pct" :show-amount="false" />
              </div>
            </div>
          </div>
        </section>

        <!-- Asset: top performer in alto, chi rallenta in basso -->
        <section v-if="assetRows.length" class="app-card rounded-app p-5 flex flex-col gap-3">
          <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">Assets</h2>
          <div class="flex flex-col divide-y divide-white/5">
            <RouterLink
              v-for="asset in assetRows"
              :key="asset.id"
              :to="`/assets/${asset.id}`"
              class="flex items-center gap-3 py-3 first:pt-0 last:pb-0 hover:bg-white/[0.03] transition-colors"
            >
              <AssetAvatar :name="asset.name" :icon="asset.icon_base64" :size="32" />
              <div class="flex flex-col min-w-0 flex-1 gap-0.5">
                <span class="text-brand-textMain font-semibold text-sm truncate">{{ asset.name }}</span>
                <div class="flex items-center gap-1.5 text-[10px] font-semibold">
                  <span :class="pctColor(asset.momPct)">MoM {{ formatPct(asset.momPct) }}</span>
                  <template v-if="asset.dynamic">
                    <span class="text-brand-textMuted">·</span>
                    <span :class="pctColor(asset.avgMonthly)">avg {{ formatPct(asset.avgMonthly) }}/mo</span>
                  </template>
                </div>
              </div>
              <div class="flex flex-col items-end shrink-0 gap-0.5">
                <Money :value="asset.total_value_eur" class="text-brand-textMain font-bold text-sm" />
                <PnLValue :pl-eur="asset.unrealized_pl_eur" :pct="asset.unrealized_pl_pct" :show-amount="false" />
              </div>
            </RouterLink>
          </div>
        </section>
      </template>
    </div>
  </main>
</template>
