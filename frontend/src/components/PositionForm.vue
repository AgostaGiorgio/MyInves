<script setup>
import { ref } from 'vue'
import { api } from '../services/api'
import { useToast } from '../composables/useToast'
import BottomSheet from './ui/BottomSheet.vue'
import Field from './ui/Field.vue'

const props = defineProps({
  asset: { type: Object, required: true }, // item di portfolio (id, name, currency, quantity, cost_price)
  valueTracked: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'saved'])

const toast = useToast()

const startQty = props.asset.quantity ?? ''
const startAvg = props.asset.cost_price ?? ''
const startBasis =
  startAvg !== '' && startAvg !== null ? String(Number(Math.round(Number(startQty) * Number(startAvg) * 100) / 100)) : ''

const form = ref({
  quantity: startQty,
  cost_price: startAvg,
  cost_basis: startBasis,
})

const errors = ref({})
const saving = ref(false)

const round = (n, digits) => Number(Math.round((n + Number.EPSILON) * 10 ** digits) / 10 ** digits)

// Cost basis = quantity x average cost
const syncBasisFromAvg = () => {
  const qty = Number(form.value.quantity)
  const avg = form.value.cost_price
  if (avg === '' || avg === null) {
    form.value.cost_basis = ''
    return
  }
  if (!Number.isNaN(qty) && qty > 0) {
    form.value.cost_basis = String(round(qty * Number(avg), 2))
  }
}

// Average cost = cost basis / quantity
const syncAvgFromBasis = () => {
  const qty = Number(form.value.quantity)
  const basis = form.value.cost_basis
  if (basis === '' || basis === null) {
    form.value.cost_price = ''
    return
  }
  if (!Number.isNaN(qty) && qty > 0) {
    form.value.cost_price = String(round(Number(basis) / qty, 8))
  }
}

const onQuantity = (v) => {
  form.value.quantity = v
  syncBasisFromAvg()
}

const onAvg = (v) => {
  form.value.cost_price = v
  syncBasisFromAvg()
}

const onBasis = (v) => {
  form.value.cost_basis = v
  syncAvgFromBasis()
}

const submit = async () => {
  errors.value = {}
  const quantity = Number(form.value.quantity)
  if (form.value.quantity === '' || Number.isNaN(quantity)) errors.value.quantity = 'Enter a value'
  if (Object.keys(errors.value).length) return

  const reading = { asset_id: props.asset.id, quantity }
  if (!props.valueTracked && form.value.cost_price !== '' && form.value.cost_price !== null) {
    reading.cost_price = Number(form.value.cost_price)
  }

  saving.value = true
  try {
    await api.addReadings([reading])
    toast.success('Position updated')
    emit('saved')
    emit('close')
  } catch (e) {
    toast.error('Could not update position')
    console.error('Error adding reading:', e)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <BottomSheet :open="true" title="Update position" @close="emit('close')">
    <div class="flex flex-col gap-4">
      <Field
        :model-value="form.quantity"
        :label="valueTracked ? 'Current value' : 'Quantity held'"
        type="number"
        inputmode="decimal"
        placeholder="0"
        :error="errors.quantity"
        :suffix="asset.currency"
        :hint="valueTracked ? 'The total value you hold right now' : undefined"
        @update:model-value="onQuantity"
      />

      <template v-if="!valueTracked">
        <Field
          :model-value="form.cost_price"
          label="Average cost per unit"
          type="number"
          inputmode="decimal"
          placeholder="Optional"
          :suffix="asset.currency"
          hint="Cost basis per unit"
          @update:model-value="onAvg"
        />

        <Field
          :model-value="form.cost_basis"
          label="Cost basis"
          type="number"
          inputmode="decimal"
          placeholder="Optional"
          :suffix="asset.currency"
          hint="Total invested (quantity × average cost)"
          @update:model-value="onBasis"
        />
      </template>
    </div>

    <template #footer>
      <button
        type="button"
        :disabled="saving"
        @click="submit"
        class="w-full bg-brand-primary text-white py-3.5 rounded-app-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors disabled:opacity-60"
      >
        {{ saving ? 'Saving…' : 'Save position' }}
      </button>
    </template>
  </BottomSheet>
</template>
