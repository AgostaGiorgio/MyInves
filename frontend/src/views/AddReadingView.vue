<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'

import { api } from '../services/api'
import { usePortfolio } from '../composables/usePortfolio'
import { useToast } from '../composables/useToast'
import { isOrderTracked } from '../constants/assetTypes'
import { formatNumber } from '../utils/format'

import Field from '../components/ui/Field.vue'
import SegmentedControl from '../components/ui/SegmentedControl.vue'
import AssetAvatar from '../components/ui/AssetAvatar.vue'
import AssetTypeBadge from '../components/ui/AssetTypeBadge.vue'
import Skeleton from '../components/ui/Skeleton.vue'

const router = useRouter()
const { byType, loading, load, reload } = usePortfolio()
const toast = useToast()

const values = reactive({}) // id -> nuova quantita'/valore
const modes = reactive({}) // id -> 'value' | 'order'
const sides = reactive({}) // id -> 'BUY' | 'SELL'
const orderQty = reactive({})
const orderAmount = reactive({})

onMounted(() => load())

const orderTracked = (asset) => isOrderTracked(asset.asset_type)
const modeOf = (asset) => modes[asset.id] || 'value'
const sideOf = (asset) => sides[asset.id] || 'BUY'

const valueOptions = [
  { value: 'value', label: 'Value' },
  { value: 'order', label: 'Order' },
]
const sideOptions = [
  { value: 'BUY', label: 'Buy' },
  { value: 'SELL', label: 'Sell' },
]

const hasInput = computed(() =>
  byType.value.some((group) =>
    group.items.some((asset) =>
      modeOf(asset) === 'value' ? !!values[asset.id] : !!orderQty[asset.id]
    )
  )
)

const saving = ref(false)

const save = async () => {
  const readings = []
  const orders = []

  for (const group of byType.value) {
    for (const asset of group.items) {
      if (modeOf(asset) === 'value') {
        const raw = values[asset.id]
        if (raw === '' || raw === undefined || raw === null) continue
        const reading = { asset_id: asset.id, quantity: Number(raw) }
        // Per gli asset a ordini preserva il costo medio attuale (il batch non lo modifica).
        if (orderTracked(asset) && asset.cost_price !== null && asset.cost_price !== undefined) {
          reading.cost_price = Number(asset.cost_price)
        }
        readings.push(reading)
      } else {
        const raw = orderQty[asset.id]
        if (raw === '' || raw === undefined || raw === null) continue
        orders.push({
          assetId: asset.id,
          payload: {
            side: sideOf(asset),
            quantity: Number(raw),
            amount_invested: Number(orderAmount[asset.id] || 0),
          },
        })
      }
    }
  }

  if (readings.length === 0 && orders.length === 0) {
    toast.error('Nothing to save')
    return
  }

  saving.value = true
  try {
    if (readings.length) await api.addReadings(readings)
    for (const order of orders) {
      await api.addAssetOrder(order.assetId, order.payload)
    }
    toast.success('Saved')
    await reload()
    router.back()
  } catch (e) {
    toast.error('Could not save the readings')
    console.error('Error saving readings:', e)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <main class="w-full px-4">
    <div class="py-4 flex flex-col gap-5 w-full">
      <div class="flex items-center justify-between gap-3">
        <div class="flex items-center gap-1">
          <button type="button" @click="router.back()" class="w-9 h-9 rounded-full flex items-center justify-center text-brand-textMuted hover:text-brand-textMain transition-colors">
            <ArrowLeft :size="18" />
          </button>
          <h1 class="text-lg font-bold tracking-tight">Add reading</h1>
        </div>
        <button
          type="button"
          :disabled="saving || !hasInput"
          @click="save"
          class="px-4 py-2 rounded-app-sm bg-brand-primary text-white text-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors disabled:opacity-40"
        >
          {{ saving ? 'Saving…' : 'Save' }}
        </button>
      </div>

      <Skeleton v-if="loading && byType.length === 0" :lines="5" height="h-24" />

      <template v-else>
        <div v-for="group in byType" :key="group.type" class="flex flex-col gap-2">
          <div class="px-1">
            <AssetTypeBadge :code="group.type" :label="group.label" dot />
          </div>

          <div v-for="asset in group.items" :key="asset.id" class="app-card p-4 flex flex-col gap-3">
            <div class="flex items-center gap-3">
              <AssetAvatar :name="asset.name" :icon="asset.icon_base64" :size="36" />
              <div class="flex flex-col min-w-0 flex-1">
                <span class="text-brand-textMain font-semibold text-sm truncate">{{ asset.name }}</span>
                <span class="text-brand-textMuted text-[11px]">
                  {{ orderTracked(asset) ? 'Current' : 'Current value' }}
                  {{ formatNumber(asset.quantity, 4) }}
                </span>
              </div>
              <div v-if="orderTracked(asset)" class="w-32 shrink-0">
                <SegmentedControl
                  :model-value="modeOf(asset)"
                  :options="valueOptions"
                  @update:model-value="(v) => (modes[asset.id] = v)"
                />
              </div>
            </div>

            <Field
              v-if="modeOf(asset) === 'value'"
              :model-value="values[asset.id] || ''"
              :label="orderTracked(asset) ? 'New total quantity' : 'New value'"
              type="number"
              inputmode="decimal"
              :placeholder="formatNumber(asset.quantity, 4)"
              :suffix="asset.currency"
              @update:model-value="(v) => (values[asset.id] = v)"
            />

            <div v-else class="flex flex-col gap-3">
              <SegmentedControl
                :model-value="sideOf(asset)"
                :options="sideOptions"
                @update:model-value="(v) => (sides[asset.id] = v)"
              />
              <div class="flex gap-3">
                <Field
                  :model-value="orderQty[asset.id] || ''"
                  label="Quantity"
                  type="number"
                  inputmode="decimal"
                  placeholder="0"
                  @update:model-value="(v) => (orderQty[asset.id] = v)"
                />
                <Field
                  :model-value="orderAmount[asset.id] || ''"
                  label="Amount"
                  type="number"
                  inputmode="decimal"
                  placeholder="0"
                  :suffix="asset.currency"
                  @update:model-value="(v) => (orderAmount[asset.id] = v)"
                />
              </div>
            </div>
          </div>
        </div>

        <button
          type="button"
          :disabled="saving || !hasInput"
          @click="save"
          class="w-full bg-brand-primary text-white py-3.5 rounded-app-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors disabled:opacity-40"
        >
          {{ saving ? 'Saving…' : 'Save' }}
        </button>
      </template>
    </div>
  </main>
</template>
