<script setup>
import { ref } from 'vue'
import { api } from '../services/api'
import { useToast } from '../composables/useToast'
import { toDateInput, dateWithCurrentTime } from '../utils/format'
import BottomSheet from './ui/BottomSheet.vue'
import Field from './ui/Field.vue'

const props = defineProps({
  assetId: { type: String, required: true },
  currency: { type: String, default: 'EUR' },
  price: { type: Object, default: null }, // presente = modifica
})

const emit = defineEmits(['close', 'saved'])

const toast = useToast()
const isEdit = Boolean(props.price?.id)

const form = ref({
  record_date: props.price ? toDateInput(props.price.record_date) : toDateInput(new Date()),
  price: props.price ? String(props.price.price) : '',
})

const errors = ref({})
const saving = ref(false)

const submit = async () => {
  errors.value = {}
  const value = Number(form.value.price)
  if (!form.value.record_date) errors.value.record_date = 'Required'
  if (form.value.price === '' || Number.isNaN(value)) errors.value.price = 'Enter a price'
  if (Object.keys(errors.value).length) return

  // In modifica con data invariata mantieni il timestamp originale; altrimenti usa la data scelta + ora corrente.
  const keepOriginal = isEdit && props.price && toDateInput(props.price.record_date) === form.value.record_date
  const recordDate = keepOriginal ? props.price.record_date : dateWithCurrentTime(form.value.record_date)
  const payload = { record_date: recordDate, price: value }

  saving.value = true
  try {
    if (isEdit) {
      await api.updateAssetPrice(props.price.id, payload)
    } else {
      await api.addAssetPrice(props.assetId, payload)
    }
    toast.success(isEdit ? 'Price updated' : 'Price added')
    emit('saved')
    emit('close')
  } catch (e) {
    toast.error('Could not save price')
    console.error('Error saving price:', e)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <BottomSheet :open="true" :title="isEdit ? 'Edit price' : 'Add price'" @close="emit('close')">
    <div class="flex flex-col gap-4">
      <Field v-model="form.record_date" label="Date" type="date" :error="errors.record_date" />
      <Field
        v-model="form.price"
        label="Price"
        type="number"
        inputmode="decimal"
        placeholder="0"
        :error="errors.price"
        :suffix="currency"
      />
    </div>

    <template #footer>
      <button
        type="button"
        :disabled="saving"
        @click="submit"
        class="w-full bg-brand-primary text-white py-3.5 rounded-app-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors disabled:opacity-60"
      >
        {{ saving ? 'Saving…' : 'Save price' }}
      </button>
    </template>
  </BottomSheet>
</template>
