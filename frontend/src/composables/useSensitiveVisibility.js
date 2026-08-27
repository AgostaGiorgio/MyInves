import { ref } from 'vue'

const STORAGE_KEY = 'myinves_sensitive_hidden'

const isSensitiveHidden = ref(false)

try {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored !== null) isSensitiveHidden.value = stored === 'true'
} catch (e) {}

function toggleSensitiveHidden() {
  isSensitiveHidden.value = !isSensitiveHidden.value
  try {
    localStorage.setItem(STORAGE_KEY, String(isSensitiveHidden.value))
  } catch (e) {}
}

export function useSensitiveVisibility() {
  return { isSensitiveHidden, toggleSensitiveHidden }
}

export const maskAmount = () => '€ ••••'
