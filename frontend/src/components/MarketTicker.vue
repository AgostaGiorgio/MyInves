<script setup>
    defineProps({
    items: {
        type: Array,
        required: true
    }
    })
</script>

<template>
  <section class="w-full max-w-md mb-6 relative">
    <h3 class="text-brand-textMuted text-[11px] font-semibold uppercase tracking-wider mb-2 px-5">
      Mercati & Cambi (€)
    </h3>
    <div class="overflow-hidden relative flex w-full">
      <div class="absolute left-0 top-0 bottom-0 w-6 bg-gradient-to-r from-brand-background to-transparent z-10 pointer-events-none"></div>
      <div class="absolute right-0 top-0 bottom-0 w-6 bg-gradient-to-l from-brand-background to-transparent z-10 pointer-events-none"></div>

      <div class="flex gap-2 animate-marquee w-max hover:pause pl-5">
        <template v-for="loopIndex in 2" :key="loopIndex">
          <div 
            v-for="item in items" 
            :key="loopIndex + '-' + item.id"
            class="flex-none w-32 bg-brand-surface/50 rounded-app-sm p-2.5 border border-white/5 flex flex-col justify-between cursor-pointer"
          >
            <div class="flex items-center justify-between mb-2">
              <img v-if="item.iconUrl" :src="item.iconUrl" alt="icona" class="w-5 h-5 rounded-full object-cover bg-white/10 p-0.5" />
              <div v-else class="w-5 h-5 rounded-full bg-brand-primary/20 text-brand-primary flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"></path><path d="M12 18V6"></path>
                </svg>
              </div>
              <span class="text-brand-textMain font-medium text-xs">{{ item.name }}</span>
            </div>
            <div class="flex items-end justify-between gap-1">
              <span class="text-brand-textMain font-bold text-sm truncate">
                {{ item.value.toLocaleString('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 3 }) }}
              </span>
              <span class="text-brand-textMuted text-[9px] uppercase font-medium tracking-wide whitespace-nowrap">
                {{ item.date }}
              </span>
            </div>
          </div>
        </template>
      </div>
    </div>
  </section>
</template>

<style scoped>
    @keyframes marquee {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
    }
    .animate-marquee { animation: marquee 15s linear infinite; }
    .hover\:pause:hover { animation-play-state: paused; }
</style>