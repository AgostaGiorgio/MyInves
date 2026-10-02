<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ArrowLeft, Pencil, Plus, Trash2, Package, Wallet, Tag } from 'lucide-vue-next'

import { api } from '../services/api'
import { usePortfolio } from '../composables/usePortfolio'
import { useLookups } from '../composables/useLookups'
import { useToast } from '../composables/useToast'
import { typeLabel, isOrderTracked, isValueTracked } from '../constants/assetTypes'
import { formatNumber, formatDate } from '../utils/format'

import Money from '../components/ui/Money.vue'
import PnLValue from '../components/ui/PnLValue.vue'
import AssetTypeBadge from '../components/ui/AssetTypeBadge.vue'
import AssetAvatar from '../components/ui/AssetAvatar.vue'
import Skeleton from '../components/ui/Skeleton.vue'
import EmptyState from '../components/ui/EmptyState.vue'

import AssetForm from '../components/AssetForm.vue'
import OrderForm from '../components/OrderForm.vue'
import PositionForm from '../components/PositionForm.vue'
import PriceSheet from '../components/PriceSheet.vue'
import TotalChart from '../components/TotalChart.vue'

const props = defineProps({
  id: { type: String, required: true },
})

const { items, loading, load, reload } = usePortfolio()
const { typeLabels, load: loadLookups } = useLookups()
const toast = useToast()

const asset = computed(() => items.value.find((a) => a.id === props.id) || null)
const label = computed(() => (asset.value ? typeLabels.value[asset.value.asset_type] || asset.value.asset_label : ''))
const canOrder = computed(() => (asset.value ? isOrderTracked(asset.value.asset_type) : false))
const valueTracked = computed(() => (asset.value ? isValueTracked(asset.value.asset_type) : false))

const detailRows = computed(() =>
  Object.entries(asset.value?.details || {}).map(([key, value]) => ({
    key,
    label: key.replaceAll('_', ' '),
    value: String(value),
  }))
)

// --- Sheet visibility ---
const showEdit = ref(false)
const showOrder = ref(false)
const showPosition = ref(false)
const showPrice = ref(false)
const editingPrice = ref(null)

// --- Orders ---
const orders = ref([])
const ordersLoading = ref(false)

const loadOrders = async () => {
  if (!canOrder.value) {
    orders.value = []
    return
  }
  ordersLoading.value = true
  try {
    orders.value = await api.getAssetOrders(props.id)
  } catch (e) {
    console.error('Failed to load orders:', e)
  } finally {
    ordersLoading.value = false
  }
}

// --- Prices ---
const prices = ref([])
const pricesLoading = ref(false)

const loadPrices = async () => {
  if (valueTracked.value) {
    prices.value = []
    return
  }
  pricesLoading.value = true
  try {
    prices.value = await api.getAssetPrices(props.id)
  } catch (e) {
    console.error('Failed to load prices:', e)
  } finally {
    pricesLoading.value = false
  }
}

const openAddPrice = () => {
  editingPrice.value = null
  showPrice.value = true
}

const openEditPrice = (price) => {
  editingPrice.value = price
  showPrice.value = true
}

const deletePrice = async (price) => {
  if (!confirm(`Delete the price of ${formatDate(price.record_date)}?`)) return
  try {
    await api.deleteAssetPrice(price.id)
    toast.success('Price deleted')
    await loadPrices()
  } catch (e) {
    toast.error('Could not delete the price')
    console.error('Error deleting price:', e)
  }
}

const onOrderSaved = async () => {
  await Promise.all([reload(), loadOrders(), loadHistory()])
}

const deleteOrder = async (order) => {
  if (!confirm('Delete this order? The position will be recalculated.')) return
  try {
    await api.deleteAssetOrder(props.id, order.id)
    toast.success('Order deleted')
    await Promise.all([reload(), loadOrders(), loadHistory()])
  } catch (e) {
    toast.error('Could not delete the order')
    console.error('Error deleting order:', e)
  }
}

const onPositionSaved = async () => {
  await Promise.all([reload(), loadHistory()])
}

const onPriceSaved = async () => {
  await loadPrices()
}

// --- Value over time ---
const assetHistory = ref([])

const loadHistory = async () => {
  try {
    assetHistory.value = await api.getAssetsHistory()
  } catch (e) {
    console.error('Failed to load asset history:', e)
  }
}

const points = computed(() => {
  const entry = assetHistory.value.find((h) => h.asset_name === asset.value?.name)
  if (!entry) return []
  return [...(entry.values || [])]
    .filter((v) => v.total_value_eur !== null && v.total_value_eur !== undefined)
    .sort((a, b) => new Date(a.record_date) - new Date(b.record_date))
})

onMounted(async () => {
  loadLookups()
  await load()
  loadOrders()
  loadPrices()
  loadHistory()
})

watch(() => props.id, async () => {
  orders.value = []
  prices.value = []
  assetHistory.value = []
  await load()
  loadOrders()
  loadPrices()
  loadHistory()
})
</script>

<template>
  <main class="w-full px-4">
    <div class="py-4 flex flex-col gap-5 w-full">
      <RouterLink to="/assets" class="inline-flex items-center gap-1.5 text-brand-textMuted text-sm w-max">
        <ArrowLeft :size="16" /> Assets
      </RouterLink>

      <Skeleton v-if="loading && !asset" :lines="4" height="h-20" />

      <EmptyState
        v-else-if="!asset"
        :icon="Wallet"
        title="Asset not found"
        description="It may have been removed. Go back to the assets list."
      />

      <template v-else>
        <header class="flex items-center gap-3">
          <AssetAvatar :name="asset.name" :icon="asset.icon_base64" :size="48" />
          <div class="flex flex-col min-w-0 flex-1">
            <h1 class="text-lg font-bold truncate">{{ asset.name }}</h1>
            <div class="flex items-center gap-2 mt-0.5">
              <AssetTypeBadge :code="asset.asset_type" :label="label" />
              <span class="text-brand-textMuted text-xs">{{ asset.currency }}</span>
            </div>
          </div>
          <button
            type="button"
            @click="showEdit = true"
            class="w-9 h-9 rounded-full bg-brand-surface border border-white/10 flex items-center justify-center text-brand-textMuted hover:text-brand-primary transition-colors shrink-0"
          >
            <Pencil :size="16" />
          </button>
        </header>

        <section class="app-card rounded-app p-5 flex flex-col gap-2">
          <span class="text-[11px] text-brand-textMuted uppercase tracking-widest font-semibold">Current value</span>
          <div class="text-3xl font-extrabold tracking-tighter">
            <Money :value="asset.total_value_eur" />
          </div>
          <PnLValue :pl-eur="asset.unrealized_pl_eur" :pct="asset.unrealized_pl_pct" size="md" />
        </section>

        <section class="grid grid-cols-2 gap-3">
          <div class="bg-brand-surface/30 rounded-app-sm p-3 border border-white/5 flex flex-col gap-1">
            <span class="text-[10px] text-brand-textMuted uppercase tracking-widest font-semibold">{{ valueTracked ? 'Value' : 'Quantity' }}</span>
            <span class="text-brand-textMain font-semibold text-sm">{{ formatNumber(asset.quantity, 4) }}</span>
          </div>
          <div class="bg-brand-surface/30 rounded-app-sm p-3 border border-white/5 flex flex-col gap-1">
            <span class="text-[10px] text-brand-textMuted uppercase tracking-widest font-semibold">Avg cost</span>
            <span class="text-brand-textMain font-semibold text-sm">{{ formatNumber(asset.cost_price, 4) }}</span>
          </div>
          <div class="bg-brand-surface/30 rounded-app-sm p-3 border border-white/5 flex flex-col gap-1">
            <span class="text-[10px] text-brand-textMuted uppercase tracking-widest font-semibold">Cost basis</span>
            <span class="text-brand-textMain font-semibold text-sm"><Money :value="asset.cost_value_eur" /></span>
          </div>
          <div class="bg-brand-surface/30 rounded-app-sm p-3 border border-white/5 flex flex-col gap-1">
            <span class="text-[10px] text-brand-textMuted uppercase tracking-widest font-semibold">Last update</span>
            <span class="text-brand-textMain font-semibold text-sm">{{ formatDate(asset.reading_date) }}</span>
          </div>
        </section>

        <section v-if="points.length > 1" class="app-card rounded-app p-5 flex flex-col gap-3">
          <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">Value over time</h2>
          <TotalChart :points="points" />
        </section>

        <section class="flex gap-3">
          <button
            type="button"
            @click="showPosition = true"
            class="flex-1 flex items-center justify-center gap-2 bg-brand-surface border border-white/5 rounded-app-sm py-3 text-sm font-semibold text-brand-textMain hover:bg-brand-surface/80 transition-colors"
          >
            <Pencil :size="15" /> {{ valueTracked ? 'Update value' : 'Update position' }}
          </button>
          <button
            v-if="canOrder"
            type="button"
            @click="showOrder = true"
            class="flex-1 flex items-center justify-center gap-2 bg-brand-surface border border-white/5 rounded-app-sm py-3 text-sm font-semibold text-brand-textMain hover:bg-brand-surface/80 transition-colors"
          >
            <Plus :size="15" /> Add order
          </button>
        </section>

        <section v-if="canOrder" class="flex flex-col gap-2">
          <h2 class="text-[11px] text-brand-textMuted uppercase tracking-widest font-semibold px-1">Orders</h2>
          <Skeleton v-if="ordersLoading && orders.length === 0" :lines="2" height="h-14" />
          <div v-else-if="orders.length === 0" class="flex items-center gap-2 text-brand-textMuted text-xs px-1 py-2">
            <Package :size="14" /> No orders recorded yet.
          </div>
          <div v-else class="flex flex-col gap-2">
            <div
              v-for="order in orders"
              :key="order.id"
              class="flex items-center justify-between gap-3 bg-brand-surface rounded-app-sm p-3 border border-white/5"
            >
              <div class="flex items-center gap-3 min-w-0">
                <span
                  class="text-[10px] font-bold px-1.5 py-0.5 rounded"
                  :class="order.side === 'BUY' ? 'bg-emerald-400/10 text-emerald-400' : 'bg-red-400/10 text-red-400'"
                >
                  {{ order.side }}
                </span>
                <div class="flex flex-col min-w-0">
                  <span class="text-brand-textMain text-sm font-semibold">{{ formatNumber(order.quantity, 4) }}</span>
                  <span class="text-brand-textMuted text-[11px]">{{ formatDate(order.order_date) }}</span>
                </div>
              </div>
              <div class="flex items-center gap-3 shrink-0">
                <span class="text-brand-textMain text-sm font-bold"><Money :value="order.amount_invested" /></span>
                <button type="button" @click="deleteOrder(order)" class="text-brand-textMuted hover:text-red-400 transition-colors">
                  <Trash2 :size="14" />
                </button>
              </div>
            </div>
          </div>
        </section>

        <section v-if="detailRows.length" class="flex flex-col gap-2">
          <h2 class="text-[11px] text-brand-textMuted uppercase tracking-widest font-semibold px-1">Details</h2>
          <div class="bg-brand-surface rounded-app-sm border border-white/5 divide-y divide-white/5">
            <div v-for="row in detailRows" :key="row.key" class="flex items-center justify-between gap-3 px-4 py-2.5">
              <span class="text-brand-textMuted text-xs capitalize">{{ row.label }}</span>
              <span class="text-brand-textMain text-sm font-medium text-right">{{ row.value }}</span>
            </div>
          </div>
        </section>

        <section v-if="!valueTracked" class="flex flex-col gap-2">
          <div class="flex items-center justify-between px-1">
            <h2 class="text-[11px] text-brand-textMuted uppercase tracking-widest font-semibold">Prices</h2>
            <button type="button" @click="openAddPrice" class="text-brand-primary text-xs font-semibold flex items-center gap-1">
              <Plus :size="13" /> Add
            </button>
          </div>
          <Skeleton v-if="pricesLoading && prices.length === 0" :lines="2" height="h-12" />
          <div v-else-if="prices.length === 0" class="flex items-center gap-2 text-brand-textMuted text-xs px-1 py-2">
            <Tag :size="14" /> No prices recorded yet.
          </div>
          <div v-else class="flex flex-col gap-2">
            <div
              v-for="price in prices"
              :key="price.id"
              class="flex items-center justify-between gap-3 bg-brand-surface rounded-app-sm px-3 py-2.5 border border-white/5"
            >
              <span class="text-brand-textMuted text-xs">{{ formatDate(price.record_date) }}</span>
              <div class="flex items-center gap-3">
                <span class="text-brand-textMain text-sm font-semibold">{{ formatNumber(price.price, 4) }}</span>
                <button type="button" @click="openEditPrice(price)" class="text-brand-textMuted hover:text-brand-primary transition-colors">
                  <Pencil :size="14" />
                </button>
                <button type="button" @click="deletePrice(price)" class="text-brand-textMuted hover:text-red-400 transition-colors">
                  <Trash2 :size="14" />
                </button>
              </div>
            </div>
          </div>
        </section>
      </template>
    </div>
  </main>

  <AssetForm v-if="showEdit && asset" :asset="asset" @close="showEdit = false" />
  <OrderForm v-if="showOrder && asset" :asset="asset" @close="showOrder = false" @saved="onOrderSaved" />
  <PositionForm v-if="showPosition && asset" :asset="asset" :value-tracked="valueTracked" @close="showPosition = false" @saved="onPositionSaved" />
  <PriceSheet
    v-if="showPrice && asset"
    :asset-id="asset.id"
    :currency="asset.currency"
    :price="editingPrice"
    @close="showPrice = false"
    @saved="onPriceSaved"
  />
</template>
