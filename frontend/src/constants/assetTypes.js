// Metadati di presentazione per i tipi di asset.
// I codici sono allineati al catalogo del backend (`asset_types`).
// I colori sono accenti UI (badge/grafici) coerenti col tema orbit.

export const ASSET_TYPE_META = {
  ETF: { color: '#8b5cf6' },
  CRYPTO: { color: '#f59e0b' },
  METAL: { color: '#eab308' },
  CASH: { color: '#10b981' },
  BANK_ACCOUNT: { color: '#3b82f6' },
  BANK_ACCOUNT_STATIC: { color: '#6366f1' },
  OTHER: { color: '#94a3b8' },
}

export const DEFAULT_TYPE_COLOR = '#94a3b8'

// Classificazione per la allocation statica/dinamica.
// - dynamic: il valore cambia nel tempo (ETF, crypto, metalli, conti con interessi)
// - static:  il valore non cambia (cash, conti senza interessi)
// - other:   beni generici (orologi, auto, immobili, ...)
export const ALLOCATION_CLASS = {
  ETF: 'dynamic',
  CRYPTO: 'dynamic',
  METAL: 'dynamic',
  BANK_ACCOUNT: 'dynamic',
  CASH: 'static',
  BANK_ACCOUNT_STATIC: 'static',
  OTHER: 'other',
}

export const CLASS_META = {
  dynamic: { label: 'Dynamic', color: '#8b5cf6' },
  static: { label: 'Static', color: '#3b82f6' },
  other: { label: 'Other', color: '#94a3b8' },
}

export function allocationClass(type) {
  return ALLOCATION_CLASS[type] || 'other'
}

// Tipi tracciati a valore diretto: la lettura e' il valore posseduto,
// i prezzi di mercato non si applicano.
export const VALUE_TRACKED = ['CASH', 'BANK_ACCOUNT', 'BANK_ACCOUNT_STATIC', 'OTHER']

// Tipi a posizione: quantita' x prezzo, ammettono ordini.
export const ORDER_TRACKED = ['ETF', 'CRYPTO', 'METAL']

export function typeColor(code) {
  return ASSET_TYPE_META[code]?.color || DEFAULT_TYPE_COLOR
}

export function isValueTracked(code) {
  return VALUE_TRACKED.includes(code)
}

export function isOrderTracked(code) {
  return ORDER_TRACKED.includes(code)
}

// Fallback leggibile se il label del backend non e' disponibile.
export function typeLabel(code) {
  if (!code) return '—'
  return code.replaceAll('_', ' ')
}

// Ordine canonico dei tipi (catalogo): usato per ordinare gruppi e liste.
export const TYPE_ORDER = [
  'ETF',
  'CRYPTO',
  'METAL',
  'CASH',
  'BANK_ACCOUNT',
  'BANK_ACCOUNT_STATIC',
  'OTHER',
]

export function typeOrder(code) {
  const index = TYPE_ORDER.indexOf(code)
  return index === -1 ? TYPE_ORDER.length : index
}

// Schema dei campi `details` per tipo: guida il form dinamico.
// Deve restare allineato ai modelli Pydantic del backend.
export const DETAIL_FIELDS = {
  ETF: [
    { key: 'isin', label: 'ISIN' },
    { key: 'ticker', label: 'Ticker' },
    { key: 'exchange', label: 'Exchange' },
    { key: 'ter', label: 'TER (%)', type: 'number' },
    { key: 'distribution_policy', label: 'Distribution', options: ['accumulating', 'distributing'] },
  ],
  CRYPTO: [
    { key: 'symbol', label: 'Symbol' },
    { key: 'chain', label: 'Chain' },
    { key: 'contract_address', label: 'Contract address' },
    { key: 'broker', label: 'Broker / Exchange' },
  ],
  METAL: [
    { key: 'metal', label: 'Metal', options: ['gold', 'silver'] },
    { key: 'form', label: 'Form', options: ['bar', 'coin', 'jewelry', 'other'] },
    { key: 'purity', label: 'Purity', type: 'number' },
    { key: 'weight_grams', label: 'Weight (g)', type: 'number' },
  ],
  CASH: [
    { key: 'location', label: 'Location' },
    { key: 'notes', label: 'Notes' },
  ],
  BANK_ACCOUNT: [
    { key: 'bank_name', label: 'Bank' },
    { key: 'iban', label: 'IBAN' },
    { key: 'interest_rate', label: 'Interest rate (%)', type: 'number' },
    { key: 'interest_frequency', label: 'Interest frequency', options: ['monthly', 'quarterly', 'yearly'] },
  ],
  BANK_ACCOUNT_STATIC: [
    { key: 'bank_name', label: 'Bank' },
    { key: 'iban', label: 'IBAN' },
  ],
  OTHER: [
    { key: 'category', label: 'Category' },
    { key: 'notes', label: 'Notes' },
    { key: 'purchase_date', label: 'Purchase date', type: 'date' },
    { key: 'purchase_value', label: 'Purchase value', type: 'number' },
  ],
}
