import { ref } from 'vue'
import { api } from '../services/api'

const stats = ref(null)
const loading = ref(false)
const error = ref(null)
let loaded = false

export function useStatistics() {
  const load = async (force = false) => {
    if (loaded && !force) return
    loading.value = true
    error.value = null
    try {
      stats.value = await api.getStatistics()
      loaded = true
    } catch (e) {
      error.value = e
      console.error('Failed to load statistics:', e)
    } finally {
      loading.value = false
    }
  }

  return { stats, loading, error, load, reload: () => load(true) }
}
