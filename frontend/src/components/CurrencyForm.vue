<script setup>
import { ref, computed } from 'vue'
import { api } from '../services/api'
import { useToast } from '../composables/useToast'
import { useLookups } from '../composables/useLookups'
import BottomSheet from './ui/BottomSheet.vue'
import Field from './ui/Field.vue'

const props = defineProps({
  currency: { type: Object, default: null }, // presente = modifica (label)
})

const emit = defineEmits(['close', 'saved'])

const toast = useToast()
const { reload } = useLookups()
const isEdit = computed(() => !!props.currency?.code)

const form = ref({
  code: props.currency?.code || '',
  label: props.currency?.label || '',
})

const errors = ref({})
const saving = ref(false)

const submit = async () => {
  errors.value = {}
  const code = form.value.code.trim().toUpperCase()
  const label = form.value.label.trim()
  if (!isEdit.value && !code) errors.value.code = 'Required'
  if (!label) errors.value.label = 'Required'
  if (Object.keys(errors.value).length) return

  saving.value = true
  try {
    if (isEdit.value) {
      await api.renameCurrency(props.currency.code, label)
    } else {
      await api.createCurrency({ code, label })
    }
    toast.success(isEdit.value ? 'Currency updated' : 'Currency created')
    await reload()
    emit('saved')
    emit('close')
  } catch (e) {
    toast.error('Could not save the currency (it may already exist)')
    console.error('Error saving currency:', e)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <BottomSheet :open="true" :title="isEdit ? 'Edit currency' : 'New currency'" @close="emit('close')">
    <div class="flex flex-col gap-4">
      <Field
        v-model="form.code"
        label="Code"
        placeholder="e.g. GBP"
        :disabled="isEdit"
        :error="errors.code"
      />
      <Field v-model="form.label" label="Name" placeholder="e.g. British Pound" :error="errors.label" />
    </div>

    <template #footer>
      <button
        type="button"
        :disabled="saving"
        @click="submit"
        class="w-full bg-brand-primary text-white py-3.5 rounded-app-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors disabled:opacity-60"
      >
        {{ saving ? 'Saving…' : isEdit ? 'Save changes' : 'Create currency' }}
      </button>
    </template>
  </BottomSheet>
</template>
