<script setup>
import { ref, reactive, onMounted } from 'vue'

const props = defineProps({
  assets: {
    type: Array,
    required: true
  }
})

// Dichiariamo gli eventi che questo componente può inviare verso l'alto
const emit = defineEmits(['close', 'submit'])

const readingDate = ref(new Date().toISOString().split('T')[0])
const readingsForm = reactive({})

// Quando il pannello si apre, prepariamo i campi vuoti
onMounted(() => {
  props.assets.forEach(asset => {
    readingsForm[asset.id] = null
  })
})

const handleSubmit = () => {
  const payload = Object.keys(readingsForm)
    .filter(id => readingsForm[id] !== null && readingsForm[id] !== '')
    .map(id => ({
      asset_id: parseInt(id),
      record_date: readingDate.value,
      quantity: parseFloat(readingsForm[id])
    }))

  if (payload.length === 0) {
    alert("Inserisci almeno una quantità prima di salvare!")
    return
  }

  // Inviamo i dati al genitore (App.vue) e chiudiamo
  emit('submit', payload)
}
</script>

<template>
  <div class="fixed inset-0 z-[100] flex flex-col justify-end">
    <div class="absolute inset-0 bg-black/70 backdrop-blur-sm transition-opacity" @click="emit('close')"></div>

    <div class="relative w-full max-h-[85vh] bg-brand-background rounded-t-[24px] shadow-2xl flex flex-col border-t border-white/10 animate-slide-up">
      <div class="w-12 h-1.5 bg-white/20 rounded-full mx-auto mt-3 mb-2"></div>

      <div class="flex justify-between items-center px-6 pb-4 pt-2 border-b border-white/5">
        <h2 class="text-brand-textMain font-bold text-lg">Aggiorna Letture</h2>
        <button @click="emit('close')" class="text-brand-textMuted hover:text-brand-textMain p-1 rounded-full bg-brand-surface/50">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>

      <div class="flex-1 overflow-y-auto px-6 py-5 hide-scrollbar">
        <div class="mb-6">
           <label class="text-brand-textMuted text-[11px] uppercase tracking-wider font-semibold mb-2 block">Data Registrazione</label>
           <input type="date" v-model="readingDate" class="w-full bg-brand-surface border border-white/10 text-brand-textMain rounded-app-sm p-3 focus:border-brand-primary outline-none transition-colors" />
        </div>

        <div class="mb-2">
          <label class="text-brand-textMuted text-[11px] uppercase tracking-wider font-semibold mb-3 block">Nuove Quantità (Lascia vuoto se invariato)</label>
          <div class="flex flex-col gap-3">
            <div v-for="asset in assets" :key="'input-'+asset.id" class="flex items-center justify-between bg-brand-surface/50 p-3 rounded-app-sm border border-white/5">
              <div class="flex items-center gap-3">
                <img v-if="asset.iconUrl" :src="asset.iconUrl" class="w-6 h-6 rounded-full object-cover bg-brand-background p-0.5" />
                <div v-else class="w-6 h-6 rounded-full bg-brand-primary/20 text-brand-primary flex items-center justify-center text-[10px] font-bold">{{ asset.name.charAt(0) }}</div>
                <span class="text-brand-textMain text-sm font-semibold">{{ asset.name }}</span>
              </div>
              <div class="relative w-28">
                <input type="number" step="any" v-model="readingsForm[asset.id]" placeholder="0.00" class="w-full bg-brand-background border border-white/10 rounded-md py-2 px-3 text-right text-brand-textMain text-sm focus:border-brand-primary focus:ring-1 focus:ring-brand-primary outline-none transition-all placeholder-brand-textMuted/30" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="p-5 border-t border-white/5 bg-brand-background">
         <button @click="handleSubmit" class="w-full bg-brand-primary text-brand-textMain py-4 rounded-app-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors">
           Salva nel Database
         </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
    .hide-scrollbar::-webkit-scrollbar { display: none; }
    .hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    @keyframes slideUp {
    0% { transform: translateY(100%); opacity: 0; }
    100% { transform: translateY(0); opacity: 1; }
    }
    .animate-slide-up { animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
</style>