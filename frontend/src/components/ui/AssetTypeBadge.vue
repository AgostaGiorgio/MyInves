<script setup>
import { computed } from 'vue'
import { typeColor, typeLabel } from '../../constants/assetTypes'
import Badge from './Badge.vue'

const props = defineProps({
  code: { type: String, default: '' },
  label: { type: String, default: '' },
  dot: { type: Boolean, default: false },
})

const text = computed(() => props.label || typeLabel(props.code))
const color = computed(() => typeColor(props.code))
</script>

<template>
  <Badge :color="color" :dot="dot">{{ text }}</Badge>
</template>
