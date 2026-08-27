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
const newAsset = ref({ name: '', asset_type: '', currency: '', icon_base64: '' })

const currenciesOpen = ref(false)
const assetTypesOpen = ref(false)
const assetsOpen = ref(false)

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
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
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
    showMessage('Errore nel caricamento dei dati.', true)
  } finally {
    loading.value = false
  }
}

const loadAssets = async () => {
  try {
    assets.value = (await api.getAssets()).map(item => ({
      ...item,
      _original: { name: item.name, asset_type: item.asset_type, currency: item.currency, icon_base64: item.icon_base64 || '' },
      pricesOpen: false,
      prices: [],
      newPrice: { record_date: '', price: '' },
    }))
  } catch (e) {
    showMessage('Errore nel caricamento degli asset.', true)
  }
}

const addCurrency = async () => {
  const code = newCurrency.value.code.trim().toUpperCase()
  const label = newCurrency.value.label.trim()
  if (!code || !label) { showMessage('Inserisci codice e nome della valuta.', true); return }
  try {
    await api.createCurrency({ code, label })
    newCurrency.value = { code: '', label: '' }
    showMessage(`Valuta ${code} aggiunta.`)
    await loadData()
  } catch (e) {
    showMessage('Impossibile aggiungere la valuta (forse esiste già).', true)
  }
}

const addAssetType = async () => {
  const code = newAssetType.value.code.trim().toUpperCase()
  const label = newAssetType.value.label.trim()
  if (!code || !label) { showMessage('Inserisci codice e nome del tipo asset.', true); return }
  try {
    await api.createAssetType({ code, label })
    newAssetType.value = { code: '', label: '' }
    showMessage(`Tipo asset ${code} aggiunto.`)
    await loadData()
  } catch (e) {
    showMessage('Impossibile aggiungere il tipo asset (forse esiste già).', true)
  }
}

const addAsset = async () => {
  const name = newAsset.value.name.trim()
  const { asset_type, currency } = newAsset.value
  if (!name || !asset_type || !currency) { showMessage('Compila nome, tipo e valuta.', true); return }
  try {
    await api.createAsset({
      name,
      asset_type,
      currency,
      icon_base64: newAsset.value.icon_base64 || null,
    })
    newAsset.value = { name: '', asset_type: '', currency: '', icon_base64: '' }
    showMessage(`Asset ${name} aggiunto.`)
    await loadAssets()
  } catch (e) {
    showMessage('Impossibile aggiungere l\'asset.', true)
  }
}

const updateAsset = async (item) => {
  const orig = item._original
  if (item.name === orig.name && item.asset_type === orig.asset_type && item.currency === orig.currency && (item.icon_base64 || '') === orig.icon_base64) return
  try {
    await api.updateAsset(item.id, {
      name: item.name,
      asset_type: item.asset_type,
      currency: item.currency,
      icon_base64: item.icon_base64 || null,
    })
    item._original = { name: item.name, asset_type: item.asset_type, currency: item.currency, icon_base64: item.icon_base64 || '' }
    showMessage(`Asset ${item.name} aggiornato.`)
  } catch (e) {
    item.name = orig.name
    item.asset_type = orig.asset_type
    item.currency = orig.currency
    item.icon_base64 = orig.icon_base64
    showMessage('Impossibile aggiornare l\'asset.', true)
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
  if (!record_date || price === '') { showMessage('Inserisci data e prezzo.', true); return }
  try {
    await api.addAssetPrice(item.id, { record_date, price: parseFloat(price) })
    item.newPrice = { record_date: '', price: '' }
    showMessage('Prezzo aggiunto.')
    await reloadPrices(item)
  } catch (e) {
    showMessage('Impossibile aggiungere il prezzo.', true)
  }
}

const savePrice = async (item, price) => {
  const orig = price._original
  const recordDate = price._localDate ? new Date(price._localDate).toISOString() : orig.record_date
  if (recordDate === orig.record_date && price.price === orig.price) return
  try {
    await api.updateAssetPrice(price.id, {
      record_date: recordDate,
      price: parseFloat(price.price),
    })
    await reloadPrices(item)
    showMessage('Prezzo aggiornato.')
  } catch (e) {
    price._localDate = toLocalInput(orig.record_date)
    price.price = orig.price
    showMessage('Impossibile aggiornare il prezzo.', true)
  }
}

const deletePrice = async (item, price) => {
  if (!confirm(`Eliminare il prezzo del ${new Date(price.record_date).toLocaleDateString('it-IT')}?`)) return
  try {
    await api.deleteAssetPrice(price.id)
    showMessage('Prezzo eliminato.')
    await reloadPrices(item)
  } catch (e) {
    showMessage('Impossibile eliminare il prezzo.', true)
  }
}

const renameCurrency = async (item) => {
  if (item.label === item._originalLabel) return
  try {
    await api.renameCurrency(item.code, item.label)
    item._originalLabel = item.label
    showMessage(`Valuta ${item.code} rinominata.`)
  } catch (e) {
    item.label = item._originalLabel
    showMessage('Impossibile rinominare la valuta.', true)
  }
}

const renameAssetType = async (item) => {
  if (item.label === item._originalLabel) return
  try {
    await api.renameAssetType(item.code, item.label)
    item._originalLabel = item.label
    showMessage(`Tipo asset ${item.code} rinominato.`)
  } catch (e) {
    item.label = item._originalLabel
    showMessage('Impossibile rinominare il tipo asset.', true)
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
          <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Asset</span>
          <ChevronDown :size="18" class="text-brand-textMuted transition-transform duration-200"
            :class="assetsOpen ? 'rotate-180' : ''" />
        </button>

        <div v-show="assetsOpen" class="px-4 pb-4 pt-4 border-t border-white/5 flex flex-col gap-3">
          <div class="flex flex-col gap-2">
            <input v-model="newAsset.name" placeholder="Nome (es. Bitcoin)"
              class="w-full bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40" />
            <div class="flex flex-col sm:flex-row gap-2">
              <select v-model="newAsset.asset_type"
                class="app-select flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none">
                <option value="" disabled>Tipo</option>
                <option v-for="t in assetTypes" :key="t.code" :value="t.code">{{ t.label }}</option>
              </select>
              <select v-model="newAsset.currency"
                class="app-select flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none">
                <option value="" disabled>Valuta</option>
                <option v-for="c in currencies" :key="c.code" :value="c.code">{{ c.code }}</option>
              </select>
            </div>
            <textarea v-model="newAsset.icon_base64" rows="3" placeholder="Icona Base64 (opzionale)"
              class="w-full bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40 resize-y" />
            <button @click="addAsset"
              class="flex items-center justify-center gap-1 px-4 py-2 rounded-md bg-brand-primary text-white text-sm font-semibold hover:bg-brand-secondary transition-colors">
              <Plus :size="16" /> Aggiungi Asset
            </button>
          </div>

          <div class="flex flex-col gap-2">
            <div v-for="item in assets" :key="item.id"
              class="flex flex-col gap-2 bg-brand-background rounded-md px-3 py-2 border border-white/5">
              <div class="flex items-center gap-3">
                <button @click="openIconEditor(item)" title="Modifica icona"
                  class="relative w-8 h-8 rounded-full overflow-hidden shrink-0 bg-brand-surface ring-1 ring-white/10 hover:ring-brand-primary focus:outline-none focus:ring-2 focus:ring-brand-primary transition-all">
                  <img v-if="item.icon_base64" :src="item.icon_base64" alt="icona" class="w-full h-full object-cover" />
                  <span v-else class="w-full h-full flex items-center justify-center text-brand-primary text-xs font-bold">{{ item.name.charAt(0) }}</span>
                </button>
                <input v-model="item.name" @blur="updateAsset(item)" placeholder="Nome"
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

              <div class="border-t border-white/5 pt-2">
                <button @click="togglePrices(item)"
                  class="w-full flex items-center justify-between py-1 text-brand-textMuted hover:text-brand-primary transition-colors">
                  <span class="text-xs font-semibold uppercase tracking-widest">Prezzi</span>
                  <ChevronDown :size="16" class="transition-transform duration-200"
                    :class="item.pricesOpen ? 'rotate-180' : ''" />
                </button>

                <div v-show="item.pricesOpen" class="flex flex-col gap-2 pt-2">
                  <div class="flex flex-col sm:flex-row gap-2">
                    <input v-model="item.newPrice.record_date" type="datetime-local"
                      class="flex-1 bg-brand-surface border border-white/10 rounded-md py-1 px-2 text-brand-textMain text-sm outline-none" />
                    <input v-model="item.newPrice.price" type="number" step="any" placeholder="Prezzo"
                      class="flex-1 bg-brand-surface border border-white/10 rounded-md py-1 px-2 text-brand-textMain text-sm outline-none placeholder-brand-textMuted/40" />
                    <button @click="addPrice(item)"
                      class="flex items-center justify-center gap-1 px-3 py-1 rounded-md bg-brand-primary text-white text-xs font-semibold hover:bg-brand-secondary transition-colors">
                      <Plus :size="14" /> Aggiungi
                    </button>
                  </div>

                  <div class="flex flex-col gap-1.5">
                    <div v-for="p in item.prices" :key="p.id"
                      class="flex items-center gap-2 bg-brand-surface/60 rounded-md px-2 py-1.5 border border-white/5">
                      <input v-model="p._localDate" type="datetime-local" @change="savePrice(item, p)"
                        class="flex-1 bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-0.5 px-1 text-brand-textMain text-xs outline-none transition-all" />
                      <input v-model="p.price" type="number" step="any" @blur="savePrice(item, p)"
                        class="w-20 bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-0.5 px-1 text-brand-textMain text-xs text-right outline-none transition-all" />
                      <button @click="deletePrice(item, p)" title="Elimina"
                        class="text-brand-textMuted hover:text-red-400 transition-colors shrink-0">✕</button>
                    </div>
                    <span v-if="item.prices.length === 0" class="text-brand-textMuted text-xs">Nessun prezzo registrato.</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section class="w-full bg-brand-surface rounded-app-sm border border-white/5 overflow-hidden">
        <button @click="currenciesOpen = !currenciesOpen"
          class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/80 transition-colors">
          <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Valute</span>
          <ChevronDown :size="18" class="text-brand-textMuted transition-transform duration-200"
            :class="currenciesOpen ? 'rotate-180' : ''" />
        </button>

        <div v-show="currenciesOpen" class="px-4 pb-4 pt-4 border-t border-white/5 flex flex-col gap-3">
          <div class="flex flex-col sm:flex-row gap-2">
            <input v-model="newCurrency.code" placeholder="Codice (es. GBP)"
              class="flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40 uppercase" />
            <input v-model="newCurrency.label" placeholder="Nome (es. Sterlina britannica)"
              class="flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40" />
            <button @click="addCurrency"
              class="flex items-center justify-center gap-1 px-4 py-2 rounded-md bg-brand-primary text-white text-sm font-semibold hover:bg-brand-secondary transition-colors">
              <Plus :size="16" /> Aggiungi
            </button>
          </div>

          <div class="flex flex-col gap-2">
            <div v-for="item in currencies" :key="item.code"
              class="flex items-center gap-2 bg-brand-background rounded-md px-3 py-2 border border-white/5">
              <span class="text-brand-textMuted text-xs font-bold w-12 uppercase shrink-0">{{ item.code }}</span>
              <input v-model="item.label" @blur="renameCurrency(item)" placeholder="Nome visualizzato"
                class="flex-1 bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-1 px-2 text-brand-textMain text-sm outline-none transition-all" />
            </div>
          </div>
        </div>
      </section>

      <section class="w-full bg-brand-surface rounded-app-sm border border-white/5 overflow-hidden">
        <button @click="assetTypesOpen = !assetTypesOpen"
          class="w-full flex items-center justify-between p-4 hover:bg-brand-surface/80 transition-colors">
          <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Tipi di Asset</span>
          <ChevronDown :size="18" class="text-brand-textMuted transition-transform duration-200"
            :class="assetTypesOpen ? 'rotate-180' : ''" />
        </button>

        <div v-show="assetTypesOpen" class="px-4 pb-4 pt-4 border-t border-white/5 flex flex-col gap-3">
          <div class="flex flex-col sm:flex-row gap-2">
            <input v-model="newAssetType.code" placeholder="Codice (es. BOND)"
              class="flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40 uppercase" />
            <input v-model="newAssetType.label" placeholder="Nome (es. Obbligazione)"
              class="flex-1 bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40" />
            <button @click="addAssetType"
              class="flex items-center justify-center gap-1 px-4 py-2 rounded-md bg-brand-primary text-white text-sm font-semibold hover:bg-brand-secondary transition-colors">
              <Plus :size="16" /> Aggiungi
            </button>
          </div>

          <div class="flex flex-col gap-2">
            <div v-for="item in assetTypes" :key="item.code"
              class="flex flex-wrap items-center gap-2 bg-brand-background rounded-md px-3 py-2 border border-white/5">
              <span class="text-brand-textMuted text-xs font-bold uppercase shrink-0">{{ item.code }}</span>
              <input v-model="item.label" @blur="renameAssetType(item)" placeholder="Nome visualizzato"
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
        <h3 class="text-brand-textMain font-bold text-sm">Icona Asset</h3>
        <button @click="iconEditor = null" class="text-brand-textMuted hover:text-brand-textMain">✕</button>
      </div>
      <div class="flex items-center gap-3">
        <img v-if="iconEditorValue" :src="iconEditorValue" alt="anteprima"
          class="w-12 h-12 rounded-full object-cover bg-brand-background p-0.5" />
        <span v-else class="w-12 h-12 rounded-full bg-brand-background flex items-center justify-center text-brand-primary text-sm font-bold">{{ (iconEditor.name || '?').charAt(0) }}</span>
        <span class="text-brand-textMuted text-sm">{{ iconEditor.name }}</span>
      </div>
      <textarea v-model="iconEditorValue" rows="4" placeholder="Incolla qui il Base64 dell'icona"
        class="w-full bg-brand-background border border-white/10 rounded-md py-2 px-3 text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none placeholder-brand-textMuted/40 resize-y" />
      <div class="flex gap-2 justify-end">
        <button @click="iconEditor = null"
          class="px-4 py-2 rounded-md bg-brand-surface text-brand-textMuted text-sm font-semibold border border-white/10 hover:text-brand-textMain transition-colors">
          Annulla
        </button>
        <button @click="saveIcon"
          class="px-4 py-2 rounded-md bg-brand-primary text-white text-sm font-semibold hover:bg-brand-secondary transition-colors">
          Salva
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
