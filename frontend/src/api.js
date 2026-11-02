const API_URL = (process.env.VUE_APP_API_URL || 'http://localhost:5000').replace(/\/$/, '')

export function apiUrl(path = '') {
  if (!path) return API_URL
  if (/^https?:\/\//i.test(path)) return path
  return `${API_URL}/${String(path).replace(/^\//, '')}`
}

export function mediaUrl(path) {
  if (!path) return ''
  if (/^https?:\/\//i.test(path)) return path
  return apiUrl(path)
}

export default API_URL
