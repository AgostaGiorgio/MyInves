<script setup>
import { ref, computed } from 'vue'
import { api } from '../services/api'
import { useToast } from '../composables/useToast'
import { useLookups } from '../composables/useLookups'
import { toDateInput, dateWithCurrentTime } from '../utils/format'
import BottomSheet from './ui/BottomSheet.vue'
import Field from './ui/Field.vue'
import SelectField from './ui/SelectField.vue'

const props = defineProps({
  rate: { type: Object, default: null }, // presente = modifica
})

const emit = defineEmits(['close', 'saved'])

const toast = useToast()
const { currencies, load: loadLookups } = useLookups()
loadLookups()

const isEdit = computed(() => !!props.rate?.id)

const currencyOptions = computed(() =>
  currencies.value
    .filter((c) => c.code !== 'EUR')
    .map((c) => ({ value: c.code, label: `${c.code} — ${c.label}` }))
)

const form = ref({
  currency: props.rate?.currency || '',
  record_date: props.rate ? toDateInput(props.rate.record_date) : toDateInput(new Date()),
  rate_to_eur: props.rate ? String(props.rate.rate_to_eur) : '',
})

const errors = ref({})
const saving = ref(false)

const submit = async () => {
  errors.value = {}
  const value = Number(form.value.rate_to_eur)
  if (!form.value.currency) errors.value.currency = 'Required'
  if (!form.value.record_date) errors.value.record_date = 'Required'
  if (form.value.rate_to_eur === '' || Number.isNaN(value)) errors.value.rate_to_eur = 'Enter a rate'
  if (Object.keys(errors.value).length) return

  const keepOriginal = isEdit.value && props.rate && toDateInput(props.rate.record_date) === form.value.record_date
  const recordDate = keepOriginal ? props.rate.record_date : dateWithCurrentTime(form.value.record_date)
  const payload = {
    currency: form.value.currency,
    record_date: recordDate,
    rate_to_eur: value,
  }

  saving.value = true
  try {
    if (isEdit.value) {
      await api.updateExchangeRate(props.rate.id, payload)
    } else {
      await api.addExchangeRate(payload)
    }
    toast.success(isEdit.value ? 'Exchange rate updated' : 'Exchange rate added')
    emit('saved')
    emit('close')
  } catch (e) {
    toast.error('Could not save the exchange rate')
    console.error('Error saving exchange rate:', e)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <BottomSheet :open="true" :title="isEdit ? 'Edit exchange rate' : 'New exchange rate'" @close="emit('close')">
    <div class="flex flex-col gap-4">
      <SelectField
        v-model="form.currency"
        label="Currency"
        placeholder="Select currency"
        :options="currencyOptions"
        :error="errors.currency"
      />
      <Field v-model="form.record_date" label="Date" type="date" :error="errors.record_date" />
      <Field
        v-model="form.rate_to_eur"
        label="Rate to EUR"
        type="number"
        inputmode="decimal"
        placeholder="Value of 1 unit in EUR"
        :error="errors.rate_to_eur"
      />
    </div>

    <template #footer>
      <button
        type="button"
        :disabled="saving"
        @click="submit"
        class="w-full bg-brand-primary text-white py-3.5 rounded-app-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors disabled:opacity-60"
      >
        {{ saving ? 'Saving…' : isEdit ? 'Save changes' : 'Add rate' }}
      </button>
    </template>
  </BottomSheet>
</template>
