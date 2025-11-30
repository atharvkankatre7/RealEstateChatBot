import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const queryAnalysis = async (query) => {
  try {
    const response = await api.post('/api/query/', { query })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.error || error.message || 'Failed to process query')
  }
}

export const getLocalities = async () => {
  try {
    const response = await api.get('/api/localities/')
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.error || error.message || 'Failed to fetch localities')
  }
}

export const downloadData = async (tableData, format = 'csv') => {
  try {
    const response = await api.post(
      '/api/download/',
      { tableData, format },
      { responseType: 'blob' }
    )
    
    // Create blob and download
    const blob = new Blob([response.data], {
      type: format === 'csv' ? 'text/csv' : 'application/json'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `real_estate_data.${format}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    throw new Error(error.response?.data?.error || error.message || 'Failed to download data')
  }
}

export default api

