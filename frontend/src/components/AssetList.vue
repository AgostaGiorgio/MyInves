<script setup>
    defineProps({
    assets: {
        type: Array,
        required: true
    }
    })
</script>

<template>
  <section class="w-full max-w-md px-5 mb-6">
    <h2 class="text-brand-textMuted text-[11px] font-semibold uppercase tracking-wider mb-2">
      I Miei Asset
    </h2>
    <div class="flex flex-col gap-3">
      <div 
        v-for="asset in assets" 
        :key="asset.id" 
        class="bg-brand-surface rounded-app-sm p-4 border border-white/5 flex items-center justify-between cursor-pointer hover:bg-brand-surface/80 transition-colors"
      >
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 rounded-full bg-brand-background flex items-center justify-center border border-white/5 overflow-hidden shrink-0 shadow-inner">
             <img v-if="asset.iconUrl" :src="asset.iconUrl" alt="icona" class="w-full h-full object-cover p-1.5" />
             <span v-else class="text-brand-primary font-bold text-sm">
               {{ asset.name.charAt(0) }}
             </span>
          </div>
          <div class="flex flex-col">
            <span class="text-brand-textMain font-semibold text-sm">{{ asset.name }}</span>
            <span class="text-brand-textMuted text-[10px] uppercase tracking-wider">{{ asset.type.replace('_', ' ') }}</span>
          </div>
        </div>
        <div class="text-right">
          <span class="text-brand-textMain font-bold text-sm">
            € {{ asset.value.toLocaleString('it-IT', { minimumFractionDigits: 2 }) }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>