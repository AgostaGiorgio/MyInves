import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000, 
  headers: {
    'Content-Type': 'application/json'
  }
})


export const api = {
  
  async getAssets() {
    const response = await apiClient.get('/api/v1/assets')
    return response.data
  },

  async createAsset(payload) {
    const response = await apiClient.post('/api/v1/assets', payload)
    return response.data
  },

  async updateAsset(id, payload) {
    const response = await apiClient.patch(`/api/v1/assets/${id}`, payload)
    return response.data
  },

  async getAssetIcon(assetId) {
    const response = await apiClient.get(`/api/v1/assets/${assetId}/icon`)
    return response.data
  },

  async getExchangeRates() {
    const response = await apiClient.get('/api/v1/exchange-rates')
    return response.data
  },

  async getPortfolio(){
    const response = await apiClient.get('/api/v1/portfolio')
    return response.data
  },

  async getPortfolioHistory(period = 'all') {
    const response = await apiClient.get('/api/v1/portfolio/history', {
      params: { period: period }
    })
    return response.data
  },

  async getAssetsHistory() {
    const response = await apiClient.get('/api/v1/assets/history')
    return response.data
  },

  async addReadings(readingsArray) {
    const response = await apiClient.post('/api/v1/readings', readingsArray)
    return response.data
  },

  async getCurrencies() {
    const response = await apiClient.get('/api/v1/currencies')
    return response.data
  },

  async getAssetTypes() {
    const response = await apiClient.get('/api/v1/asset-types')
    return response.data
  },

  async createCurrency(payload) {
    const response = await apiClient.post('/api/v1/currencies', payload)
    return response.data
  },

  async createAssetType(payload) {
    const response = await apiClient.post('/api/v1/asset-types', payload)
    return response.data
  },

  async renameCurrency(code, label) {
    const response = await apiClient.patch(`/api/v1/currencies/${code}`, { label })
    return response.data
  },

  async renameAssetType(code, label) {
    const response = await apiClient.patch(`/api/v1/asset-types/${code}`, { label })
    return response.data
  }
}