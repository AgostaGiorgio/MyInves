<script setup>
import { ref, computed } from 'vue'
import { Upload, Trash2 } from 'lucide-vue-next'
import { api } from '../services/api'
import { useToast } from '../composables/useToast'
import { usePortfolio } from '../composables/usePortfolio'
import { useLookups } from '../composables/useLookups'
import { typeLabel } from '../constants/assetTypes'
import BottomSheet from './ui/BottomSheet.vue'
import Field from './ui/Field.vue'
import SelectField from './ui/SelectField.vue'
import AssetAvatar from './ui/AssetAvatar.vue'
import AssetDetailsForm from './AssetDetailsForm.vue'

const props = defineProps({
  asset: { type: Object, default: null }, // presente = modifica
})

const emit = defineEmits(['close', 'saved'])

const toast = useToast()
const { reload } = usePortfolio()
const { assetTypes, currencies, load: loadLookups } = useLookups()
loadLookups()

const isEdit = computed(() => !!props.asset?.id)

const form = ref({
  name: props.asset?.name || '',
  asset_type: props.asset?.asset_type || '',
  currency: props.asset?.currency || 'EUR',
  icon_base64: props.asset?.icon_base64 || '',
  details: { ...(props.asset?.details || {}) },
})

const errors = ref({})
const saving = ref(false)

// Legge il file come Data URL (data:image/...;base64,...): e' il valore che salviamo.
const onIconFile = (event) => {
  const file = event.target.files && event.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    form.value.icon_base64 = String(reader.result || '')
  }
  reader.readAsDataURL(file)
  event.target.value = ''
}

const typeOptions = computed(() => assetTypes.value.map((t) => ({ value: t.code, label: t.label })))
const currencyOptions = computed(() => currencies.value.map((c) => ({ value: c.code, label: c.code })))
const typeLabelText = computed(() => typeLabel(form.value.asset_type))

const cleanDetails = (details) => {
  const out = {}
  for (const [key, value] of Object.entries(details || {})) {
    if (value === null || value === undefined || value === '') continue
    out[key] = value
  }
  return out
}

const submit = async () => {
  errors.value = {}
  if (!form.value.name.trim()) errors.value.name = 'Required'
  if (!form.value.asset_type) errors.value.asset_type = 'Required'
  if (!form.value.currency) errors.value.currency = 'Required'
  if (Object.keys(errors.value).length) return

  const payload = {
    name: form.value.name.trim(),
    asset_type: form.value.asset_type,
    currency: form.value.currency,
    icon_base64: form.value.icon_base64 || null,
    details: cleanDetails(form.value.details),
  }

  saving.value = true
  try {
    if (isEdit.value) {
      await api.updateAsset(props.asset.id, payload)
    } else {
      await api.createAsset(payload)
    }
    toast.success(isEdit.value ? 'Asset updated' : 'Asset created')
    await reload()
    emit('saved')
    emit('close')
  } catch (e) {
    const detail = e?.response?.data?.detail
    if (Array.isArray(detail) && detail.length) {
      const first = detail[0]
      const field = Array.isArray(first.loc) ? first.loc[first.loc.length - 1] : 'details'
      errors.value[field] = first.msg || 'Invalid value'
      toast.error(`Invalid ${field}`)
    } else {
      toast.error('Could not save asset')
    }
    console.error('Error saving asset:', e)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <BottomSheet :open="true" :title="isEdit ? 'Edit asset' : 'New asset'" @close="emit('close')">
    <div class="flex flex-col gap-4">
      <Field v-model="form.name" label="Name" placeholder="e.g. VWCE" :error="errors.name" />

      <div class="flex items-center gap-4">
        <AssetAvatar :name="form.name || '?'" :icon="form.icon_base64 || null" :size="56" />
        <div class="flex flex-col gap-2">
          <label class="inline-flex items-center gap-1.5 px-3 py-2 rounded-app-sm bg-brand-surface border border-white/10 text-brand-textMain text-xs font-semibold hover:bg-brand-surface/80 transition-colors cursor-pointer w-max">
            <Upload :size="14" />
            Upload icon
            <input type="file" accept="image/*" class="hidden" @change="onIconFile" />
          </label>
          <button
            v-if="form.icon_base64"
            type="button"
            @click="form.icon_base64 = ''"
            class="inline-flex items-center gap-1 text-[11px] text-brand-textMuted hover:text-red-400 transition-colors w-max"
          >
            <Trash2 :size="12" /> Remove icon
          </button>
        </div>
      </div>

      <SelectField
        v-if="!isEdit"
        v-model="form.asset_type"
        label="Type"
        placeholder="Select type"
        :options="typeOptions"
        :error="errors.asset_type"
      />
      <div v-else class="flex flex-col gap-1.5">
        <span class="text-[11px] uppercase tracking-wider font-semibold text-brand-textMuted">Type</span>
        <span class="text-sm text-brand-textMain">{{ typeLabelText }}</span>
      </div>

      <SelectField v-model="form.currency" label="Currency" :options="currencyOptions" :error="errors.currency" />

      <div v-if="form.asset_type" class="flex flex-col gap-3 pt-1 border-t border-white/5">
        <span class="text-[11px] uppercase tracking-wider font-semibold text-brand-textMuted mt-3">Details</span>
        <AssetDetailsForm v-model="form.details" :asset-type="form.asset_type" />
      </div>
      <span v-if="errors.details" class="text-[11px] text-red-400">{{ errors.details }}</span>
    </div>

    <template #footer>
      <button
        type="button"
        :disabled="saving"
        @click="submit"
        class="w-full bg-brand-primary text-white py-3.5 rounded-app-sm font-bold shadow-lg shadow-brand-primary/20 hover:bg-brand-secondary transition-colors disabled:opacity-60"
      >
        {{ saving ? 'Saving…' : isEdit ? 'Save changes' : 'Create asset' }}
      </button>
    </template>
  </BottomSheet>
</template>
