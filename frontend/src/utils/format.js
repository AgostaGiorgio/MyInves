// Formattazione condivisa. I numeri restano in formato italiano (it-IT),
// indipendentemente dalla lingua delle etichette UI.

const LOCALE = 'it-IT'

export function formatMoney(value, decimals = 2) {
  const n = toNumber(value)
  if (n === null) return '—'
  return '€ ' + n.toLocaleString(LOCALE, { minimumFractionDigits: decimals, maximumFractionDigits: decimals })
}

export function formatMoneySigned(value, decimals = 2) {
  const n = toNumber(value)
  if (n === null) return '—'
  const sign = n > 0 ? '+' : n < 0 ? '−' : ''
  return `${sign}€ ${Math.abs(n).toLocaleString(LOCALE, { minimumFractionDigits: decimals, maximumFractionDigits: decimals })}`
}

export function formatNumber(value, decimals = 2) {
  const n = toNumber(value)
  if (n === null) return '—'
  return n.toLocaleString(LOCALE, { minimumFractionDigits: decimals, maximumFractionDigits: decimals })
}

export function formatPct(value, decimals = 2) {
  const n = toNumber(value)
  if (n === null) return '—'
  const sign = n > 0 ? '+' : ''
  return sign + n.toFixed(decimals).replace('.', ',') + '%'
}

export function formatDate(value) {
  const d = toDate(value)
  if (!d) return '—'
  return d.toLocaleDateString(LOCALE, { day: '2-digit', month: '2-digit', year: 'numeric' })
}

export function formatMonth(month) {
  if (!month) return '—'
  const [year, m] = String(month).split('-')
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  const idx = Number(m) - 1
  return `${months[idx] ?? m} ${year}`
}

// yyyy-mm-dd per gli <input type="date">
export function toDateInput(value) {
  const d = toDate(value)
  if (!d) return ''
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

export function toNumber(value) {
  if (value === null || value === undefined || value === '') return null
  const n = Number(value)
  return Number.isNaN(n) ? null : n
}

function toDate(value) {
  if (!value) return null
  const d = new Date(value)
  return Number.isNaN(d.getTime()) ? null : d
}
