<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Pencil, Trash2 } from 'lucide-vue-next'

import { api } from '../services/api'
import { useLookups } from '../composables/useLookups'
import { useToast } from '../composables/useToast'
import { formatDate } from '../utils/format'

import Skeleton from '../components/ui/Skeleton.vue'
import CurrencyForm from '../components/CurrencyForm.vue'
import ExchangeRateForm from '../components/ExchangeRateForm.vue'

const { currencies, load: loadLookups } = useLookups()
const toast = useToast()

const rates = ref([])
const loadingRates = ref(false)

const showCurrencyForm = ref(false)
const editingCurrency = ref(null)
const showRateForm = ref(false)
const editingRate = ref(null)

const loadRates = async () => {
  loadingRates.value = true
  try {
    rates.value = await api.getAllExchangeRates()
  } catch (e) {
    console.error('Failed to load exchange rates:', e)
  } finally {
    loadingRates.value = false
  }
}

onMounted(() => {
  loadLookups()
  loadRates()
})

const fmtRate = (v) => Number(v).toLocaleString('it-IT', { maximumFractionDigits: 6 })

const openNewCurrency = () => {
  editingCurrency.value = null
  showCurrencyForm.value = true
}

const openEditCurrency = (currency) => {
  editingCurrency.value = currency
  showCurrencyForm.value = true
}

const openNewRate = () => {
  editingRate.value = null
  showRateForm.value = true
}

const openEditRate = (rate) => {
  editingRate.value = rate
  showRateForm.value = true
}

const deleteRate = async (rate) => {
  if (!confirm(`Delete the ${rate.currency} rate of ${formatDate(rate.record_date)}?`)) return
  try {
    await api.deleteExchangeRate(rate.id)
    toast.success('Exchange rate deleted')
    await loadRates()
  } catch (e) {
    toast.error('Could not delete the exchange rate')
    console.error('Error deleting exchange rate:', e)
  }
}
</script>

<template>
  <main class="w-full px-4">
    <div class="py-4 flex flex-col gap-5 w-full">
      <!-- Currencies -->
      <section class="app-card rounded-app p-5 flex flex-col gap-3">
        <div class="flex items-center justify-between">
          <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">Currencies</h2>
          <button
            type="button"
            @click="openNewCurrency"
            class="w-9 h-9 rounded-full bg-brand-primary text-white flex items-center justify-center shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary active:scale-95 transition-all"
          >
            <Plus :size="18" :stroke-width="2.5" />
          </button>
        </div>

        <div class="flex flex-col divide-y divide-white/5">
          <button
            v-for="currency in currencies"
            :key="currency.code"
            type="button"
            @click="openEditCurrency(currency)"
            class="flex items-center gap-3 py-3 first:pt-0 last:pb-0 text-left hover:bg-white/[0.03] transition-colors"
          >
            <span class="text-brand-textMain font-bold text-sm w-12 shrink-0">{{ currency.code }}</span>
            <span class="text-brand-textMuted text-sm truncate flex-1">{{ currency.label }}</span>
            <Pencil :size="14" class="text-brand-textMuted shrink-0" />
          </button>
        </div>
      </section>

      <!-- Exchange rates -->
      <section class="app-card rounded-app p-5 flex flex-col gap-3">
        <div class="flex items-center justify-between">
          <h2 class="text-[11px] uppercase tracking-widest font-semibold text-brand-textMuted">Exchange rates</h2>
          <button
            type="button"
            @click="openNewRate"
            class="w-9 h-9 rounded-full bg-brand-primary text-white flex items-center justify-center shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary active:scale-95 transition-all"
          >
            <Plus :size="18" :stroke-width="2.5" />
          </button>
        </div>

        <Skeleton v-if="loadingRates && rates.length === 0" :lines="3" height="h-10" />
        <p v-else-if="rates.length === 0" class="text-brand-textMuted text-xs py-2">No exchange rate recorded.</p>

        <div v-else class="flex flex-col divide-y divide-white/5">
          <div
            v-for="rate in rates"
            :key="rate.id"
            class="flex items-center gap-3 py-3 first:pt-0 last:pb-0"
          >
            <span class="text-brand-textMain font-bold text-sm w-12 shrink-0">{{ rate.currency }}</span>
            <span class="text-brand-textMuted text-xs flex-1">{{ formatDate(rate.record_date) }}</span>
            <span class="text-brand-textMain text-sm font-semibold tabular-nums">{{ fmtRate(rate.rate_to_eur) }}</span>
            <div class="flex items-center gap-3 shrink-0">
              <button type="button" @click="openEditRate(rate)" class="text-brand-textMuted hover:text-brand-primary transition-colors">
                <Pencil :size="14" />
              </button>
              <button type="button" @click="deleteRate(rate)" class="text-brand-textMuted hover:text-red-400 transition-colors">
                <Trash2 :size="14" />
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>

  <CurrencyForm v-if="showCurrencyForm" :currency="editingCurrency" @close="showCurrencyForm = false" />
  <ExchangeRateForm v-if="showRateForm" :rate="editingRate" @close="showRateForm = false" @saved="loadRates" />
</template>
