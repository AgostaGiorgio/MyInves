<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true
  }
})

// We create "refs" to be able to read dimensions in the DOM (the HTML)
const containerRef = ref(null)
const contentRef = ref(null)

// This variable tells us if the items overflow the screen (true) or not (false)
const isOverflowing = ref(false)

// Function that calculates whether the animation is needed
const checkOverflow = async () => {
  // 1. We temporarily reset the animation to "false" to measure a single block of items
  isOverflowing.value = false
  
  // 2. We tell Vue: "Wait to have updated the graphics before doing the calculations"
  await nextTick()
  
  // 3. We check the dimensions
  if (containerRef.value && contentRef.value) {
    // scrollWidth is the total width of the items
    // clientWidth is the width of the screen/container
    if (contentRef.value.scrollWidth > containerRef.value.clientWidth) {
      isOverflowing.value = true // There are too many items, let's activate the animation!
    }
  }
}

// As soon as the component appears on screen, we do the check
onMounted(() => {
  checkOverflow()
  // We add a listener: if the user rotates the phone or resizes the window, we recalculate!
  window.addEventListener('resize', checkOverflow)
})

// When we leave the page, we clean up memory by removing the listener
onUnmounted(() => {
  window.removeEventListener('resize', checkOverflow)
})

// If the backend suddenly sends new data, we recalculate everything
watch(() => props.items, () => {
  checkOverflow()
}, { deep: true })
</script>

<template>
  <section class="w-full flex flex-col gap-2">
    
    <div class="flex items-center">
      <span class="text-xs text-brand-textMuted uppercase tracking-widest font-semibold">Markets & Rates (€)</span>
    </div>

    <div ref="containerRef" class="overflow-hidden relative flex w-full">
      <div 
        ref="contentRef"
        class="flex gap-2 w-max" 
        :class="isOverflowing ? 'animate-marquee hover:pause' : ''"
      >
        <template v-for="loopIndex in (isOverflowing ? 2 : 1)" :key="loopIndex">
          
          <div 
            v-for="item in items" 
            :key="loopIndex + '-' + item.id"
            class="flex-none w-32 bg-brand-surface/50 rounded-app-sm p-2.5 border border-white/5 flex flex-col justify-between cursor-pointer"
          >
            <div class="flex items-center justify-between mb-2">
              <img v-if="item.iconUrl" :src="item.iconUrl" alt="icon" class="w-5 h-5 rounded-full object-cover" />
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