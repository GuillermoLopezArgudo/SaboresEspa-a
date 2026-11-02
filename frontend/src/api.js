import axios from 'axios'

const API_URL = (process.env.VUE_APP_API_URL || 'http://localhost:5000').replace(/\/$/, '')

axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('userToken')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      const path = window.location.pathname
      if (path !== '/login' && path !== '/register' && path !== '/') {
        localStorage.removeItem('userToken')
        localStorage.removeItem('iduser')
        localStorage.removeItem('type')
      }
    }
    return Promise.reject(error)
  }
)

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

export function clearSession() {
  localStorage.removeItem('userToken')
  localStorage.removeItem('iduser')
  localStorage.removeItem('type')
  localStorage.removeItem('token')
}

export default API_URL
