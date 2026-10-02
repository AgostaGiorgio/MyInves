<script setup>
import { ref, computed, onMounted } from 'vue'
import { Sparkles, Wallet, PlusCircle, TrendingUp, Coins, ChevronLeft } from 'lucide-vue-next'

const STORAGE_KEY = 'myinves_onboarding_v1'

const visible = ref(false)
const index = ref(0)

const slides = [
  {
    icon: Sparkles,
    title: 'Welcome to myInves',
    text: 'Track your whole net worth in one place — crypto, ETFs, metals, cash and bank accounts. Private and self-hosted.',
  },
  {
    icon: Wallet,
    title: 'Add your assets',
    text: 'Create an asset from the Assets page: choose a type and a currency, and optionally upload an icon.',
  },
  {
    icon: PlusCircle,
    title: 'Record what you own',
    text: 'Tap “Add reading” in the header to update several assets at once, or record a buy/sell order for ETFs, crypto and metals.',
  },
  {
    icon: TrendingUp,
    title: 'See how you grow',
    text: 'The Dashboard and Statistics show how your portfolio evolves over time and where your money is allocated.',
  },
  {
    icon: Coins,
    title: 'Multiple currencies',
    text: 'Hold assets in different currencies: everything is converted to EUR using the exchange rates you manage in Currencies.',
  },
]

onMounted(() => {
  try {
    if (!localStorage.getItem(STORAGE_KEY)) visible.value = true
  } catch (e) {
    visible.value = true
  }
})

const slide = computed(() => slides[index.value])
const isLast = computed(() => index.value === slides.length - 1)

const finish = () => {
  visible.value = false
  try {
    localStorage.setItem(STORAGE_KEY, '1')
  } catch (e) {}
}

const next = () => {
  if (isLast.value) finish()
  else index.value += 1
}

const prev = () => {
  if (index.value > 0) index.value -= 1
}
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="visible" class="fixed inset-0 z-[150] flex items-center justify-center p-5">
        <div class="absolute inset-0 bg-black/75 backdrop-blur-sm" @click="finish" />

        <div class="relative w-full max-w-sm bg-brand-background rounded-app shadow-app border border-white/10 p-6 flex flex-col gap-5">
          <div class="flex items-center gap-3">
            <span class="w-11 h-11 rounded-full bg-brand-primary/15 text-brand-primary flex items-center justify-center shrink-0">
              <component :is="slide.icon" :size="22" />
            </span>
            <h2 class="text-lg font-bold text-brand-textMain">{{ slide.title }}</h2>
          </div>

          <p class="text-sm text-brand-textMuted leading-relaxed min-h-[4.5rem]">{{ slide.text }}</p>

          <div class="flex items-center justify-center gap-1.5">
            <span
              v-for="(s, i) in slides"
              :key="i"
              class="h-1.5 rounded-full transition-all duration-300"
              :class="i === index ? 'w-5 bg-brand-primary' : 'w-1.5 bg-white/20'"
            />
          </div>

          <div class="flex items-center justify-between gap-3">
            <button
              type="button"
              @click="finish"
              class="text-xs font-semibold text-brand-textMuted hover:text-brand-textMain transition-colors"
            >
              Skip
            </button>

            <div class="flex items-center gap-2">
              <button
                v-if="index > 0"
                type="button"
                @click="prev"
                class="w-9 h-9 rounded-full bg-brand-surface border border-white/10 flex items-center justify-center text-brand-textMuted hover:text-brand-textMain transition-colors"
              >
                <ChevronLeft :size="16" />
              </button>
              <button
                type="button"
                @click="next"
                class="px-5 py-2.5 rounded-app-sm bg-brand-primary text-white text-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors"
              >
                {{ isLast ? 'Get started' : 'Next' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
