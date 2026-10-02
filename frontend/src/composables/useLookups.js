import { ref, computed } from 'vue'
import { api } from '../services/api'

// Lookup di sola lettura: catalogo tipi (chiuso) e valute.
const assetTypes = ref([])
const currencies = ref([])
const loading = ref(false)
const error = ref(null)
let loaded = false

export function useLookups() {
  const typeLabels = computed(() =>
    Object.fromEntries(assetTypes.value.map((t) => [t.code, t.label]))
  )

  const currencyLabels = computed(() =>
    Object.fromEntries(currencies.value.map((c) => [c.code, c.label]))
  )

  const load = async (force = false) => {
    if (loaded && !force) return
    loading.value = true
    error.value = null
    try {
      const [types, currencyRows] = await Promise.all([api.getAssetTypes(), api.getCurrencies()])
      assetTypes.value = types
      currencies.value = currencyRows
      loaded = true
    } catch (e) {
      error.value = e
      console.error('Failed to load lookups:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    assetTypes,
    currencies,
    typeLabels,
    currencyLabels,
    loading,
    error,
    load,
    reload: () => load(true),
  }
}
