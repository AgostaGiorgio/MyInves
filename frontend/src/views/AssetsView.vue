<script setup>
import { ref, computed, onMounted } from 'vue'
import { Wallet, Plus } from 'lucide-vue-next'
import { usePortfolio } from '../composables/usePortfolio'
import { useLookups } from '../composables/useLookups'
import { typeLabel } from '../constants/assetTypes'
import Money from '../components/ui/Money.vue'
import PnLValue from '../components/ui/PnLValue.vue'
import AssetTypeBadge from '../components/ui/AssetTypeBadge.vue'
import AssetAvatar from '../components/ui/AssetAvatar.vue'
import SegmentedControl from '../components/ui/SegmentedControl.vue'
import Skeleton from '../components/ui/Skeleton.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import AssetForm from '../components/AssetForm.vue'

const { byType, loading, load } = usePortfolio()
const { typeLabels, load: loadLookups } = useLookups()

const activeType = ref('all')
const showCreate = ref(false)

onMounted(() => {
  load()
  loadLookups()
})

const typeOptions = computed(() => [
  { value: 'all', label: 'All' },
  ...byType.value.map((g) => ({ value: g.type, label: typeLabel(g.type) })),
])

const filteredGroups = computed(() =>
  byType.value.filter((g) => activeType.value === 'all' || g.type === activeType.value)
)

const labelFor = (group) => typeLabels.value[group.type] || group.label || typeLabel(group.type)
</script>

<template>
  <main class="w-full px-4">
    <div class="py-4 flex flex-col gap-4 w-full">
      <div class="flex justify-end">
        <button
          type="button"
          @click="showCreate = true"
          class="w-9 h-9 rounded-full bg-brand-primary text-white flex items-center justify-center shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary active:scale-95 transition-all"
        >
          <Plus :size="18" :stroke-width="2.5" />
        </button>
      </div>

      <SegmentedControl v-if="typeOptions.length > 2" v-model="activeType" :options="typeOptions" />

      <Skeleton v-if="loading && items.length === 0" :lines="5" height="h-16" />

      <template v-else>
        <section v-for="group in filteredGroups" :key="group.type" class="flex flex-col gap-2">
          <div class="flex items-center justify-between px-1">
            <AssetTypeBadge :code="group.type" :label="labelFor(group)" dot />
            <Money :value="group.total" class="text-brand-textMuted text-xs font-semibold" />
          </div>

          <RouterLink
            v-for="asset in group.items"
            :key="asset.id"
            :to="`/assets/${asset.id}`"
            class="flex items-center gap-3 bg-brand-surface rounded-app-sm p-3 border border-white/5 hover:bg-brand-surface/80 active:scale-[0.99] transition-all"
          >
            <AssetAvatar :name="asset.name" :icon="asset.icon_base64" :size="40" />
            <div class="flex flex-col min-w-0 flex-1">
              <span class="text-brand-textMain font-semibold text-sm truncate">{{ asset.name }}</span>
              <span class="text-brand-textMuted text-[11px]">{{ asset.currency }}</span>
            </div>
            <div class="flex flex-col items-end shrink-0">
              <Money :value="asset.total_value_eur" class="text-brand-textMain font-bold text-sm" />
              <PnLValue :pl-eur="asset.unrealized_pl_eur" :pct="asset.unrealized_pl_pct" :show-amount="false" />
            </div>
          </RouterLink>
        </section>

        <EmptyState
          v-if="filteredGroups.length === 0"
          :icon="Wallet"
          title="No assets found"
          description="Create a new asset to get started."
        >
          <button
            type="button"
            @click="showCreate = true"
            class="flex items-center gap-1.5 px-4 py-2 rounded-app-sm bg-brand-primary text-white text-sm font-semibold hover:bg-brand-secondary transition-colors"
          >
            <Plus :size="16" /> New asset
          </button>
        </EmptyState>
      </template>
    </div>
  </main>

  <AssetForm v-if="showCreate" @close="showCreate = false" />
</template>
