<script setup>
import { ref, computed } from 'vue'
import { api } from '../services/api'
import { useToast } from '../composables/useToast'
import { toDateInput } from '../utils/format'
import BottomSheet from './ui/BottomSheet.vue'
import Field from './ui/Field.vue'
import SegmentedControl from './ui/SegmentedControl.vue'

const props = defineProps({
  asset: { type: Object, required: true }, // item di portfolio (id, name, currency, ...)
})

const emit = defineEmits(['close', 'saved'])

const toast = useToast()

const sideOptions = [
  { value: 'BUY', label: 'Buy' },
  { value: 'SELL', label: 'Sell' },
]

const form = ref({
  side: 'BUY',
  quantity: '',
  amount_invested: '',
  order_date: toDateInput(new Date()),
  fees: '',
  note: '',
})

const errors = ref({})
const saving = ref(false)

const side = computed(() => form.value.side)

const submit = async () => {
  errors.value = {}
  const quantity = Number(form.value.quantity)
  const amount = Number(form.value.amount_invested || 0)
  if (!form.value.quantity || Number.isNaN(quantity) || quantity <= 0) errors.value.quantity = 'Enter a quantity'
  if (side.value === 'BUY' && (Number.isNaN(amount) || amount < 0)) errors.value.amount_invested = 'Enter an amount'
  if (Object.keys(errors.value).length) return

  const payload = {
    side: side.value,
    quantity,
    amount_invested: amount,
    fees: Number(form.value.fees || 0),
    note: form.value.note || null,
  }
  if (form.value.order_date) payload.order_date = `${form.value.order_date}T00:00:00Z`

  saving.value = true
  try {
    await api.addAssetOrder(props.asset.id, payload)
    toast.success(side.value === 'BUY' ? 'Buy recorded' : 'Sell recorded')
    emit('saved')
    emit('close')
  } catch (e) {
    toast.error('Could not save order')
    console.error('Error saving order:', e)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <BottomSheet :open="true" title="Add order" @close="emit('close')">
    <div class="flex flex-col gap-4">
      <SegmentedControl v-model="form.side" :options="sideOptions" />

      <Field
        v-model="form.quantity"
        label="Quantity"
        type="number"
        inputmode="decimal"
        placeholder="0"
        :error="errors.quantity"
        :hint="`In ${asset.currency}`"
      />

      <Field
        v-model="form.amount_invested"
        :label="side === 'BUY' ? 'Amount invested' : 'Amount received'"
        type="number"
        inputmode="decimal"
        :placeholder="side === 'BUY' ? 'Total spent' : 'Total received'"
        :error="errors.amount_invested"
        :suffix="asset.currency"
      />

      <Field v-model="form.order_date" label="Date" type="date" />
      <Field v-model="form.fees" label="Fees" type="number" inputmode="decimal" placeholder="0" :suffix="asset.currency" />
      <Field v-model="form.note" label="Note" placeholder="Optional" />
    </div>

    <template #footer>
      <button
        type="button"
        :disabled="saving"
        @click="submit"
        class="w-full bg-brand-primary text-white py-3.5 rounded-app-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors disabled:opacity-60"
      >
        {{ saving ? 'Saving…' : 'Save order' }}
      </button>
    </template>
  </BottomSheet>
</template>
