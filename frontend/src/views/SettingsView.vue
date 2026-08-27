<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Settings, ChevronDown } from 'lucide-vue-next'
import { api } from '../services/api'

const currencies = ref([])
const assetTypes = ref([])
const assets = ref([])
const loading = ref(false)
const message = ref('')
const isError = ref(false)

const newCurrency = ref({ code: '', label: '' })
const newAssetType = ref({ code: '', label: '' })
const newAsset = ref({ name: '', asset_type: '', currency: '', icon_base64: '', include_in_stats: false })

const currenciesOpen = ref(false)
const assetTypesOpen = ref(false)
const assetsOpen = ref(false)
const exchangeRatesOpen = ref(false)
const exchangeRates = ref([])
const newExchangeRate = ref({ currency: '', record_date: '', rate_to_eur: '' })

const showMessage = (text, error = false) => {
  message.value = text
  isError.value = error
  setTimeout(() => { message.value = '' }, 3000)
}

const toLocalInput = (iso) => {
  if (!iso) return ''
  const d = new Date(iso)
  if (isNaN(d.getTime())) return ''
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

const loadData = async () => {
  loading.value = true
  try {
    const [cur, types] = await Promise.all([
      api.getCurrencies(),
      api.getAssetTypes()
    ])
    currencies.value = cur.map(item => ({ ...item, _originalLabel: item.label }))
    assetTypes.value = types.map(item => ({ ...item, _originalLabel: item.label }))
  } catch (e) {
    showMessage('Error loading data.', true)
  } finally {
    loading.value = false
  }
}

const loadAssets = async () => {
  try {
    assets.value = (await api.getAssets()).map(item => ({
      ...item,
      _original: { name: item.name, asset_type: item.asset_type, currency: item.currency, icon_base64: item.icon_base64 || '', include_in_stats: item.include_in_stats },
      pricesOpen: false,
      prices: [],
      newPrice: { record_date: '', price: '' },
    }))
  } catch (e) {
    showMessage('Error loading assets.', true)
  }
}

const addCurrency = async () => {
  const code = newCurrency.value.code.trim().toUpperCase()
  const label = newCurrency.value.label.trim()
  if (!code || !label) { showMessage('Enter currency code and name.', true); return }
  try {
    await api.createCurrency({ code, label })
    newCurrency.value = { code: '', label: '' }
    showMessage(`Currency ${code} added.`)
    await loadData()
  } catch (e) {
    showMessage('Unable to add the currency (it may already exist).', true)
  }
}

const addAssetType = async () => {
  const code = newAssetType.value.code.trim().toUpperCase()
  const label = newAssetType.value.label.trim()
  if (!code || !label) { showMessage('Enter asset type code and name.', true); return }
  try {
    await api.createAssetType({ code, label })
    newAssetType.value = { code: '', label: '' }
    showMessage(`Asset type ${code} added.`)
    await loadData()
  } catch (e) {
    showMessage('Unable to add the asset type (it may already exist).', true)
  }
}

const addAsset = async () => {
  const name = newAsset.value.name.trim()
  const { asset_type, currency } = newAsset.value
  if (!name || !asset_type || !currency) { showMessage('Fill in name, type and currency.', true); return }
  try {
    await api.createAsset({
      name,
      asset_type,
      currency,
      icon_base64: newAsset.value.icon_base64 || null,
      include_in_stats: newAsset.value.include_in_stats,
    })
    newAsset.value = { name: '', asset_type: '', currency: '', icon_base64: '', include_in_stats: false }
    showMessage(`Asset ${name} added.`)
    await loadAssets()
  } catch (e) {
    showMessage('Unable to add the asset.', true)
  }
}

const updateAsset = async (item) => {
  const orig = item._original
  if (item.name === orig.name && item.asset_type === orig.asset_type && item.currency === orig.currency && (item.icon_base64 || '') === orig.icon_base64 && item.include_in_stats === orig.include_in_stats) return
  try {
    await api.updateAsset(item.id, {
      name: item.name,
      asset_type: item.asset_type,
      currency: item.currency,
      icon_base64: item.icon_base64 || null,
      include_in_stats: item.include_in_stats,
    })
    item._original = { name: item.name, asset_type: item.asset_type, currency: item.currency, icon_base64: item.icon_base64 || '', include_in_stats: item.include_in_stats }
    showMessage(`Asset ${item.name} updated.`)
  } catch (e) {
    item.name = orig.name
    item.asset_type = orig.asset_type
    item.currency = orig.currency
    item.icon_base64 = orig.icon_base64
    item.include_in_stats = orig.include_in_stats
    showMessage('Unable to update the asset.', true)
  }
}

const iconEditor = ref(null)
const iconEditorValue = ref('')

const openIconEditor = (item) => {
  iconEditor.value = item
  iconEditorValue.value = item.icon_base64 || ''
}

const saveIcon = async () => {
  const item = iconEditor.value
  if (!item) return
  item.icon_base64 = iconEditorValue.value
  iconEditor.value = null
  await updateAsset(item)
}

const decoratePrices = (rows) => rows.map(p => ({
  ...p,
  price: String(p.price),
  _localDate: toLocalInput(p.record_date),
  _original: { record_date: p.record_date, price: String(p.price) },
}))

const reloadPrices = async (item) => {
  item.prices = decoratePrices(await api.getAssetPrices(item.id))
}

const togglePrices = async (item) => {
  item.pricesOpen = !item.pricesOpen
  if (item.pricesOpen && item.prices.length === 0) {
    await reloadPrices(item)
  }
}

const addPrice = async (item) => {
  const { record_date, price } = item.newPrice
  if (!record_date || price === '') { showMessage('Enter date and price.', true); return }
  try {
    await api.addAssetPrice(item.id, { record_date, price: parseFloat(price) })
    item.newPrice = { record_date: '', price: '' }
    showMessage('Price added.')
    await reloadPrices(item)
  } catch (e) {
    showMessage('Unable to add the price.', true)
  }
}

const savePrice = async (item, price) => {
  const orig = price._original
  const recordDate = price._localDate || toLocalInput(orig.record_date)
  if (recordDate === toLocalInput(orig.record_date) && price.price === orig.price) return
  try {
    await api.updateAssetPrice(price.id, {
      record_date: recordDate,
      price: parseFloat(price.price),
    })
    await reloadPrices(item)
    showMessage('Price updated.')
  } catch (e) {
    price._localDate = toLocalInput(orig.record_date)
    price.price = orig.price
    showMessage('Unable to update the price.', true)
  }
}

const deletePrice = async (item, price) => {
  if (!confirm(`Delete the price of ${new Date(price.record_date).toLocaleDateString('it-IT')}?`)) return
  try {
    await api.deleteAssetPrice(price.id)
    showMessage('Price deleted.')
    await reloadPrices(item)
  } catch (e) {
    showMessage('Unable to delete the price.', true)
  }
}

const decorateRates = (rows) => rows.map(r => ({
  ...r,
  rate_to_eur: String(r.rate_to_eur),
  _localDate: toLocalInput(r.record_date),
  _original: { currency: r.currency, record_date: r.record_date, rate_to_eur: String(r.rate_to_eur) },
}))

const reloadExchangeRates = async () => {
  exchangeRates.value = decorateRates(await api.getAllExchangeRates())
}

const toggleExchangeRates = async () => {
  exchangeRatesOpen.value = !exchangeRatesOpen.value
  if (exchangeRatesOpen.value && exchangeRates.value.length === 0) {
    await reloadExchangeRates()
  }
}

const addExchangeRate = async () => {
  const { currency, record_date, rate_to_eur } = newExchangeRate.value
  if (!currency || !record_date || rate_to_eur === '') { showMessage('Select currency, date and rate.', true); return }
  try {
    await api.addExchangeRate({ currency, record_date, rate_to_eur: parseFloat(rate_to_eur) })
    newExchangeRate.value = { currency: '', record_date: '', rate_to_eur: '' }
    showMessage('Exchange rate added.')
    await reloadExchangeRates()
  } catch (e) {
    showMessage('Unable to add the exchange rate.', true)
  }
}

const saveExchangeRate = async (rate) => {
  const orig = rate._original
  const recordDate = rate._localDate || toLocalInput(orig.record_date)
  if (rate.currency === orig.currency && recordDate === toLocalInput(orig.record_date) && rate.rate_to_eur === orig.rate_to_eur) return
  try {
    await api.updateExchangeRate(rate.id, { currency: rate.currency, record_date: recordDate, rate_to_eur: parseFloat(rate.rate_to_eur) })
    await reloadExchangeRates()
    showMessage('Exchange rate updated.')
  } catch (e) {
    rate.currency = orig.currency
    rate._localDate = toLocalInput(orig.record_date)
    rate.rate_to_eur = orig.rate_to_eur
    showMessage('Unable to update the exchange rate.', true)
  }
}

const deleteExchangeRate = async (rate) => {
  if (!confirm(`Delete the exchange ${rate.currency} of ${new Date(rate.record_date).toLocaleDateString('it-IT')}?`)) return
  try {
    await api.deleteExchangeRate(rate.id)
    showMessage('Exchange rate deleted.')
    await reloadExchangeRates()
  } catch (e) {
    showMessage('Unable to delete the exchange rate.', true)
  }
}

const renameCurrency = async (item) => {
  if (item.label === item._originalLabel) return
  try {
    await api.renameCurrency(item.code, item.label)
    item._originalLabel = item.label
    showMessage(`Currency ${item.code} renamed.`)
  } catch (e) {
    item.label = item._originalLabel
    showMessage('Unable to rename the currency.', true)
  }
}

const renameAssetType = async (item) => {
  if (item.label === item._originalLabel) return
  try {
    await api.renameAssetType(item.code, item.label)
    item._originalLabel = item.label
    showMessage(`Asset type ${item.code} renamed.`)
  } catch (e) {
    item.label = item._originalLabel
    showMessage('Unable to rename the asset type.', true)
  }
}

const toggleAssets = async () => {
  assetsOpen.value = !assetsOpen.value
  if (assetsOpen.value && assets.value.length === 0) {
    await loadAssets()
  }
}

onMounted(loadData)
</script>

<template>
  <main class="w-full px-4">
    <div class="py-3 flex flex-col gap-7 w-full">
      <section class="w-full bg-brand-surface rounded-app-sm border border-white/5 overflow-hidden">
        <button @click="toggleAssets"
          class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/80 transition-colors">
          <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Assets</span>
          <ChevronDown :size="18" class="text-brand-textMuted transition-transform duration-200"
            :class="assetsOpen ? 'rotate-180' : ''" />
        </button>

        <div v-show="assetsOpen" class="px-4 pb-4 pt-4 border-t border-white/5 flex flex-col gap-3">
          <div class="flex flex-col gap-2">
            <input v-model="newAsset.name" placeholder="Name (e.g. Bitcoin)"
              class="w-full bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40" />
            <div class="flex flex-col sm:flex-row gap-2">
              <select v-model="newAsset.asset_type"
                class="app-select flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none">
                <option value="" disabled>Type</option>
                <option v-for="t in assetTypes" :key="t.code" :value="t.code">{{ t.label }}</option>
              </select>
              <select v-model="newAsset.currency"
                class="app-select flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none">
                <option value="" disabled>Currency</option>
                <option v-for="c in currencies" :key="c.code" :value="c.code">{{ c.code }}</option>
              </select>
            </div>
            <textarea v-model="newAsset.icon_base64" rows="3" placeholder="Icon Base64 (optional)"
              class="w-full bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40 resize-y" />
            <label class="flex items-center justify-between gap-3 py-1 cursor-pointer">
              <span class="text-sm text-brand-textMain">Include in statistics</span>
              <button type="button" @click="newAsset.include_in_stats = !newAsset.include_in_stats"
                class="relative w-10 h-6 rounded-full transition-colors duration-200 focus:outline-none"
                :class="newAsset.include_in_stats ? 'bg-brand-primary' : 'bg-white/10'">
                <span class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform duration-200"
                  :class="newAsset.include_in_stats ? 'translate-x-4' : ''"></span>
              </button>
            </label>
            <button @click="addAsset"
              class="flex items-center justify-center gap-1 px-4 py-2 rounded-md bg-brand-primary text-white text-sm font-semibold hover:bg-brand-secondary transition-colors">
              <Plus :size="16" /> Add Asset
            </button>
          </div>

          <div class="flex flex-col gap-2">
            <div v-for="item in assets" :key="item.id"
              class="flex flex-col gap-2 bg-brand-background rounded-md px-3 py-2 border border-white/5">
              <div class="flex items-center gap-3">
                <button @click="openIconEditor(item)" title="Edit icon"
                  class="relative w-8 h-8 rounded-full overflow-hidden shrink-0 bg-brand-surface ring-1 ring-white/10 hover:ring-brand-primary focus:outline-none focus:ring-2 focus:ring-brand-primary transition-all">
                  <img v-if="item.icon_base64" :src="item.icon_base64" alt="icon" class="w-full h-full object-cover" />
                  <span v-else class="w-full h-full flex items-center justify-center text-brand-primary text-xs font-bold">{{ item.name.charAt(0) }}</span>
                </button>
                <input v-model="item.name" @blur="updateAsset(item)" placeholder="Name"
                  class="flex-1 bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-1 px-2 text-brand-textMain text-sm outline-none transition-all" />
              </div>
              <div class="flex flex-col sm:flex-row gap-2">
                <select v-model="item.asset_type" @change="updateAsset(item)"
                  class="app-select flex-1 bg-brand-surface border border-white/10 rounded-md py-1 px-2 text-brand-textMain text-sm outline-none">
                  <option v-for="t in assetTypes" :key="t.code" :value="t.code">{{ t.label }}</option>
                </select>
                <select v-model="item.currency" @change="updateAsset(item)"
                  class="app-select flex-1 bg-brand-surface border border-white/10 rounded-md py-1 px-2 text-brand-textMain text-sm outline-none">
                  <option v-for="c in currencies" :key="c.code" :value="c.code">{{ c.code }}</option>
                </select>
              </div>

              <label class="flex items-center justify-between gap-3 py-1 cursor-pointer">
                <span class="text-sm text-brand-textMain">Include in statistics</span>
                <button type="button" @click="item.include_in_stats = !item.include_in_stats; updateAsset(item)"
                  class="relative w-10 h-6 rounded-full transition-colors duration-200 focus:outline-none"
                  :class="item.include_in_stats ? 'bg-brand-primary' : 'bg-white/10'">
                  <span class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform duration-200"
                    :class="item.include_in_stats ? 'translate-x-4' : ''"></span>
                </button>
              </label>

              <div class="border-t border-white/5 pt-2">
                <button @click="togglePrices(item)"
                  class="w-full flex items-center justify-between py-1 text-brand-textMuted hover:text-brand-primary transition-colors">
                  <span class="text-xs font-semibold uppercase tracking-widest">Asset values</span>
                  <ChevronDown :size="16" class="transition-transform duration-200"
                    :class="item.pricesOpen ? 'rotate-180' : ''" />
                </button>

                <div v-show="item.pricesOpen" class="flex flex-col gap-2 pt-2">
                  <div class="flex flex-col sm:flex-row gap-2">
                    <input v-model="item.newPrice.record_date" type="date"
                      class="flex-1 bg-brand-surface border border-white/10 rounded-md py-1 px-2 text-brand-textMain text-sm outline-none" />
                    <input v-model="item.newPrice.price" type="number" step="any" placeholder="Price"
                      class="flex-1 bg-brand-surface border border-white/10 rounded-md py-1 px-2 text-brand-textMain text-sm outline-none placeholder-brand-textMuted/40" />
                    <button @click="addPrice(item)"
                      class="flex items-center justify-center gap-1 px-3 py-1 rounded-md bg-brand-primary text-white text-xs font-semibold hover:bg-brand-secondary transition-colors">
                      <Plus :size="14" /> Add
                    </button>
                  </div>

                  <div class="flex flex-col gap-1.5">
                    <div v-for="p in item.prices" :key="p.id"
                      class="flex items-center gap-2 bg-brand-surface/60 rounded-md px-2 py-1.5 border border-white/5">
                      <input v-model="p._localDate" type="date" @change="savePrice(item, p)"
                        class="flex-1 bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-0.5 px-1 text-brand-textMain text-xs outline-none transition-all" />
                      <input v-model="p.price" type="number" step="any" @blur="savePrice(item, p)"
                        class="w-20 bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-0.5 px-1 text-brand-textMain text-xs text-right outline-none transition-all" />
                      <button @click="deletePrice(item, p)" title="Delete"
                        class="text-brand-textMuted hover:text-red-400 transition-colors shrink-0">✕</button>
                    </div>
                    <span v-if="item.prices.length === 0" class="text-brand-textMuted text-xs">No price recorded.</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section class="w-full bg-brand-surface rounded-app-sm border border-white/5 overflow-hidden">
        <button @click="toggleExchangeRates"
          class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/80 transition-colors">
          <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Exchange Rates</span>
          <ChevronDown :size="18" class="text-brand-textMuted transition-transform duration-200"
            :class="exchangeRatesOpen ? 'rotate-180' : ''" />
        </button>

        <div v-show="exchangeRatesOpen" class="px-4 pb-4 pt-4 border-t border-white/5 flex flex-col gap-3">
          <div class="flex flex-col sm:flex-row gap-2">
            <select v-model="newExchangeRate.currency" placeholder="Currency"
              class="app-select flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none">
              <option value="" disabled>Currency</option>
              <option v-for="c in currencies.filter(x => x.code !== 'EUR')" :key="c.code" :value="c.code">{{ c.code }}</option>
            </select>
            <input v-model="newExchangeRate.record_date" type="date"
              class="flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none" />
            <input v-model="newExchangeRate.rate_to_eur" type="number" step="any" placeholder="Rate/1 EUR"
              class="flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40" />
            <button @click="addExchangeRate"
              class="flex items-center justify-center gap-1 px-4 py-2 rounded-md bg-brand-primary text-white text-sm font-semibold hover:bg-brand-secondary transition-colors shrink-0">
              <Plus :size="16" /> Add
            </button>
          </div>

          <div class="flex flex-col gap-1.5">
            <div v-for="r in exchangeRates" :key="r.id"
              class="flex items-center gap-2 bg-brand-background/40 rounded-md px-2 py-1.5 border border-white/5">
              <select v-model="r.currency" @change="saveExchangeRate(r)"
                class="app-select w-20 bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-0.5 px-1 text-brand-textMain text-xs outline-none transition-all">
                <option v-for="c in currencies.filter(x => x.code !== 'EUR')" :key="c.code" :value="c.code">{{ c.code }}</option>
              </select>
              <input v-model="r._localDate" type="date" @change="saveExchangeRate(r)"
                class="flex-1 bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-0.5 px-1 text-brand-textMain text-xs outline-none transition-all" />
              <input v-model="r.rate_to_eur" type="number" step="any" @blur="saveExchangeRate(r)"
                class="w-24 bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-0.5 px-1 text-brand-textMain text-xs text-right outline-none transition-all" />
              <button @click="deleteExchangeRate(r)" title="Delete"
                class="text-brand-textMuted hover:text-red-400 transition-colors shrink-0">✕</button>
            </div>
            <span v-if="exchangeRates.length === 0" class="text-brand-textMuted text-xs">No exchange rate recorded.</span>
          </div>
        </div>
      </section>
      
      <section class="w-full bg-brand-surface rounded-app-sm border border-white/5 overflow-hidden">
        <button @click="currenciesOpen = !currenciesOpen"
          class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/80 transition-colors">
          <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Currencies</span>
          <ChevronDown :size="18" class="text-brand-textMuted transition-transform duration-200"
            :class="currenciesOpen ? 'rotate-180' : ''" />
        </button>

        <div v-show="currenciesOpen" class="px-4 pb-4 pt-4 border-t border-white/5 flex flex-col gap-3">
          <div class="flex flex-col sm:flex-row gap-2">
            <input v-model="newCurrency.code" placeholder="Code (e.g. GBP)"
              class="flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40 uppercase" />
            <input v-model="newCurrency.label" placeholder="Name (e.g. British pound)"
              class="flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40" />
            <button @click="addCurrency"
              class="flex items-center justify-center gap-1 px-4 py-2 rounded-md bg-brand-primary text-white text-sm font-semibold hover:bg-brand-secondary transition-colors">
              <Plus :size="16" /> Add
            </button>
          </div>

          <div class="flex flex-col gap-2">
            <div v-for="item in currencies" :key="item.code"
              class="flex items-center gap-2 bg-brand-background rounded-md px-3 py-2 border border-white/5">
              <span class="text-brand-textMuted text-xs font-bold w-12 uppercase shrink-0">{{ item.code }}</span>
              <input v-model="item.label" @blur="renameCurrency(item)" placeholder="Display name"
                class="flex-1 bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-1 px-2 text-brand-textMain text-sm outline-none transition-all" />
            </div>
          </div>
        </div>
      </section>

      <section class="w-full bg-brand-surface rounded-app-sm border border-white/5 overflow-hidden">
        <button @click="assetTypesOpen = !assetTypesOpen"
          class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/80 transition-colors">
          <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Asset Types</span>
          <ChevronDown :size="18" class="text-brand-textMuted transition-transform duration-200"
            :class="assetTypesOpen ? 'rotate-180' : ''" />
        </button>

        <div v-show="assetTypesOpen" class="px-4 pb-4 pt-4 border-t border-white/5 flex flex-col gap-3">
          <div class="flex flex-col sm:flex-row gap-2">
            <input v-model="newAssetType.code" placeholder="Code (e.g. BOND)"
              class="flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40 uppercase" />
            <input v-model="newAssetType.label" placeholder="Name (e.g. Bond)"
              class="flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40" />
            <button @click="addAssetType"
              class="flex items-center justify-center gap-1 px-4 py-2 rounded-md bg-brand-primary text-white text-sm font-semibold hover:bg-brand-secondary transition-colors">
              <Plus :size="16" /> Add
            </button>
          </div>

          <div class="flex flex-col gap-2">
            <div v-for="item in assetTypes" :key="item.code"
              class="flex flex-wrap items-center gap-2 bg-brand-background rounded-md px-3 py-2 border border-white/5">
              <span class="text-brand-textMuted text-xs font-bold uppercase shrink-0">{{ item.code }}</span>
              <input v-model="item.label" @blur="renameAssetType(item)" placeholder="Display name"
                class="w-full bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-1 px-2 text-brand-textMain text-sm outline-none transition-all" />
            </div>
          </div>
        </div>
      </section>

    </div>
  </main>

  <div v-if="iconEditor" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center">
    <div class="absolute inset-0 bg-black/70 backdrop-blur-sm" @click="iconEditor = null"></div>
    <div class="relative w-full sm:max-w-md bg-brand-surface rounded-t-[24px] sm:rounded-app-sm border border-white/10 p-6 flex flex-col gap-4 shadow-app">
      <div class="flex items-center justify-between">
        <h3 class="text-brand-textMain font-bold text-sm">Asset Icon</h3>
        <button @click="iconEditor = null" class="text-brand-textMuted hover:text-brand-textMain">✕</button>
      </div>
      <div class="flex items-center gap-3">
        <img v-if="iconEditorValue" :src="iconEditorValue" alt="preview"
          class="w-12 h-12 rounded-full object-cover bg-brand-background p-0.5" />
        <span v-else class="w-12 h-12 rounded-full bg-brand-background flex items-center justify-center text-brand-primary text-sm font-bold">{{ (iconEditor.name || '?').charAt(0) }}</span>
        <span class="text-brand-textMuted text-sm">{{ iconEditor.name }}</span>
      </div>
      <textarea v-model="iconEditorValue" rows="4" placeholder="Paste the icon Base64 here"
        class="w-full bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40 resize-y" />
      <div class="flex gap-2 justify-end">
        <button @click="iconEditor = null"
          class="px-4 py-2 rounded-md bg-brand-surface text-brand-textMuted text-sm font-semibold border border-white/10 hover:text-brand-textMain transition-colors">
          Cancel
        </button>
        <button @click="saveIcon"
          class="px-4 py-2 rounded-md bg-brand-primary text-white text-sm font-semibold hover:bg-brand-secondary transition-colors">
          Save
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-select {
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.9rem center;
  background-size: 1em;
  padding-right: 2.2rem;
}
</style>
