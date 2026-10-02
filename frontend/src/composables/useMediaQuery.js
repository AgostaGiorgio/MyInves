import { ref, onMounted, onUnmounted } from 'vue'

// Reactive media query senza dipendenze esterne.
export function useMediaQuery(query) {
  const mql = typeof window !== 'undefined' && window.matchMedia ? window.matchMedia(query) : null
  const matches = ref(mql ? mql.matches : false)

  const update = () => {
    if (mql) matches.value = mql.matches
  }

  onMounted(() => {
    if (mql) mql.addEventListener('change', update)
  })

  onUnmounted(() => {
    if (mql) mql.removeEventListener('change', update)
  })

  return matches
}
