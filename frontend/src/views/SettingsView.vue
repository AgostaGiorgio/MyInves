<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Check, Settings } from 'lucide-vue-next'
import { api } from '../services/api'

const currencies = ref([])
const assetTypes = ref([])
const loading = ref(false)
const message = ref('')
const isError = ref(false)

const newCurrency = ref({ code: '', label: '' })
const newAssetType = ref({ code: '', label: '' })

const showMessage = (text, error = false) => {
  message.value = text
  isError.value = error
  setTimeout(() => { message.value = '' }, 3000)
}

const loadData = async () => {
  loading.value = true
  try {
    const [cur, types] = await Promise.all([
      api.getCurrencies(),
      api.getAssetTypes(),
    ])
    currencies.value = cur
    assetTypes.value = types
  } catch (e) {
    showMessage('Errore nel caricamento dei dati.', true)
  } finally {
    loading.value = false
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

const renameCurrency = async (item) => {
  try {
    await api.renameCurrency(item.code, item.label)
    showMessage(`Valuta ${item.code} rinominata.`)
  } catch (e) {
    showMessage('Impossibile rinominare la valuta.', true)
  }
}

const renameAssetType = async (item) => {
  try {
    await api.renameAssetType(item.code, item.label)
    showMessage(`Tipo asset ${item.code} rinominato.`)
  } catch (e) {
    showMessage('Impossibile rinominare il tipo asset.', true)
  }
}

onMounted(loadData)
</script>

<template>
  <main class="w-full px-4">
    <div class="py-3 flex flex-col gap-7 w-full">

      <section class="w-full flex flex-col items-start gap-3">
        <div class="flex items-center">
          <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Valute</span>
        </div>

        <div class="w-full bg-brand-surface rounded-app-sm p-4 border border-white/5 flex flex-col gap-3">
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
              <input v-model="item.label" placeholder="Nome visualizzato"
                class="flex-1 bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-1 px-2 text-brand-textMain text-sm outline-none transition-all" />
              <button @click="renameCurrency(item)"
                class="flex items-center gap-1 px-3 py-1 rounded-md bg-brand-surface text-brand-primary text-xs font-semibold border border-white/10 hover:bg-brand-surface/70 transition-colors">
                <Check :size="14" />
              </button>
            </div>
          </div>
        </div>
      </section>

      <section class="w-full flex flex-col items-start gap-3">
        <div class="flex items-center">
          <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Tipi di Asset</span>
        </div>

        <div class="w-full bg-brand-surface rounded-app-sm p-4 border border-white/5 flex flex-col gap-3">
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
              <input v-model="item.label" placeholder="Nome visualizzato"
                class="flex-1 min-w-[120px] bg-transparent border border-transparent focus:border-white/10 focus:bg-brand-surface rounded-md py-1 px-2 text-brand-textMain text-sm outline-none transition-all" />
              <button @click="renameAssetType(item)"
                class="flex items-center gap-1 px-3 py-1 rounded-md bg-brand-surface text-brand-primary text-xs font-semibold border border-white/10 hover:bg-brand-surface/70 transition-colors">
                <Check :size="14" />
              </button>
            </div>
          </div>
        </div>
      </section>

    </div>
  </main>
</template>
