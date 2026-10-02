<script setup>
import { computed } from 'vue'
import { DETAIL_FIELDS } from '../constants/assetTypes'
import Field from './ui/Field.vue'
import SelectField from './ui/SelectField.vue'

const props = defineProps({
  assetType: { type: String, default: '' },
  modelValue: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:modelValue'])

const fields = computed(() => DETAIL_FIELDS[props.assetType] || [])

const get = (key) => props.modelValue?.[key] ?? ''
const set = (key, value) => emit('update:modelValue', { ...props.modelValue, [key]: value })
</script>

<template>
  <div v-if="fields.length" class="flex flex-col gap-3">
    <template v-for="f in fields" :key="f.key">
      <SelectField
        v-if="f.options"
        :label="f.label"
        :model-value="get(f.key)"
        :options="f.options.map((o) => ({ value: o, label: o }))"
        placeholder="Select"
        @update:model-value="(v) => set(f.key, v)"
      />
      <Field
        v-else
        :label="f.label"
        :type="f.type || 'text'"
        :inputmode="f.type === 'number' ? 'decimal' : undefined"
        :model-value="get(f.key)"
        @update:model-value="(v) => set(f.key, v)"
      />
    </template>
  </div>
</template>
