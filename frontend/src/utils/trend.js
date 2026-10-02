import { TrendingUp, TrendingDown } from 'lucide-vue-next'

// Classe colore per un valore di trend/P&L: positivo verde, negativo rosso,
// zero (o non disponibile) neutro.
export function trendClass(value) {
  const n = Number(value)
  if (!Number.isFinite(n) || n === 0) return 'text-brand-textMuted'
  return n > 0 ? 'text-emerald-400' : 'text-red-400'
}

// Icona per un valore di trend/P&L: null quando e' neutro (zero/assente).
export function trendIcon(value) {
  const n = Number(value)
  if (!Number.isFinite(n) || n === 0) return null
  return n > 0 ? TrendingUp : TrendingDown
}
