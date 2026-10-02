import { ref, computed } from 'vue'
import { api } from '../services/api'
import { typeOrder } from '../constants/assetTypes'

// Stato del portafoglio condiviso (singleton di modulo).
const assets = ref([])
const portfolio = ref([])
const loading = ref(false)
const error = ref(null)
let loaded = false

function mergeItem(item, asset) {
  return {
    ...item,
    icon_base64: asset?.icon_base64 || null,
    details: asset?.details || {},
    price: asset?.price ?? null,
    price_date: asset?.price_date ?? null,
  }
}

export function usePortfolio() {
  const items = computed(() => {
    const byId = new Map(assets.value.map((a) => [a.id, a]))
    return portfolio.value.map((p) => mergeItem(p, byId.get(p.id)))
  })

  const total = computed(() =>
    items.value.reduce((sum, item) => sum + (Number(item.total_value_eur) || 0), 0)
  )

  const byType = computed(() => {
    const groups = new Map()
    for (const item of items.value) {
      if (!groups.has(item.asset_type)) {
        groups.set(item.asset_type, { type: item.asset_type, label: item.asset_label, items: [], total: 0 })
      }
      const group = groups.get(item.asset_type)
      group.items.push(item)
      group.total += Number(item.total_value_eur) || 0
    }
    return [...groups.values()]
      .map((group) => ({
        ...group,
        items: [...group.items].sort(
          (a, b) => (Number(b.total_value_eur) || 0) - (Number(a.total_value_eur) || 0)
        ),
      }))
      .sort((a, b) => typeOrder(a.type) - typeOrder(b.type))
  })

  const load = async (force = false) => {
    if (loaded && !force) return
    loading.value = true
    error.value = null
    try {
      const [rawAssets, rawPortfolio] = await Promise.all([api.getAssets(), api.getPortfolio()])
      assets.value = rawAssets
      portfolio.value = rawPortfolio
      loaded = true
    } catch (e) {
      error.value = e
      console.error('Failed to load portfolio:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    assets,
    portfolio,
    items,
    total,
    byType,
    loading,
    error,
    load,
    reload: () => load(true),
  }
}
