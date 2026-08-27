<script setup>
import { useRoute } from 'vue-router'
import { Home, BarChart3, Settings } from 'lucide-vue-next'

const route = useRoute()

const items = [
  { to: '/', label: 'Dashboard', icon: Home },
  { to: '/statistics', label: 'Statistics', icon: BarChart3 },
  { to: '/settings', label: 'Settings', icon: Settings },
]
</script>

<template>
  <nav class="fixed bottom-6 left-6 right-6 bg-brand-surface/70 backdrop-blur-xl border border-white/10 shadow-app rounded-[24px] z-50">
    <div class="flex justify-around items-center p-4">
      <RouterLink
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        class="flex flex-col items-center gap-1 transition-colors duration-200"
        :class="route.path === item.to ? 'text-brand-primary' : 'text-brand-textMuted'"
      >
        <component
          :is="item.icon"
          :size="20"
          :stroke-width="route.path === item.to ? 2.5 : 2"
        />
      </RouterLink>
    </div>
  </nav>
</template>
