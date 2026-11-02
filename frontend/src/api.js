import axios from 'axios'

const raw =
  (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_URL) ||
  'http://localhost:5000'

// Trim espacios (Vercel a veces deja un trailing space → %20 y ERR_NAME_NOT_RESOLVED)
const API_URL = String(raw).trim().replace(/\/$/, '')

// Solo Mercadona/health: no enviar Authorization (evita preflight innecesario).
// viewAll/viewRecipe/etc. SÍ deben llevar JWT si existe (favoritos, privadas).
const SKIP_AUTH_PATH_RE =
  /\/(categories|productos|searchIngredient|health)(\/|$|\?)/i

axios.interceptors.request.use((config) => {
  const url = String(config.url || '')
  const skipAuth = config.skipAuth === true || SKIP_AUTH_PATH_RE.test(url)
  const token = localStorage.getItem('userToken')
  if (token && !skipAuth) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      const reqUrl = String(error.config?.url || '')
      const headers = error.config?.headers || {}
      const sentAuth = Boolean(
        headers.Authorization || headers.authorization
      )
      // Solo cerrar sesión si HABÍAMOS enviado Bearer (Mercadona/skipAuth no cuenta)
      // y no es validación de credenciales / rotación de token en curso
      const ignoreLogout =
        !sentAuth ||
        /\/(changePassword|changeEmail|categories|productos|searchIngredient|health)(\/|$|\?)/i.test(
          reqUrl
        )
      if (ignoreLogout) {
        return Promise.reject(error)
      }
      const path = window.location.pathname
      if (path !== '/login' && path !== '/register' && path !== '/') {
        clearSession()
        if (!path.startsWith('/login')) {
          window.location.assign('/login')
        }
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
  localStorage.removeItem('sabores_profile')
}

/** Comprueba expiración del JWT en cliente (la firma la valida el API). */
export function isTokenValid(token = localStorage.getItem('userToken')) {
  if (!token || typeof token !== 'string') return false
  const parts = token.split('.')
  if (parts.length < 2) return false
  try {
    const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')))
    if (payload.exp && Date.now() >= payload.exp * 1000) return false
    return true
  } catch {
    return false
  }
}

export async function logoutRequest() {
  const token = localStorage.getItem('userToken')
  try {
    if (token && isTokenValid(token)) {
      await axios.post(apiUrl('/logout'), {})
    }
  } catch {
    // ignorar errores de red al cerrar sesión
  } finally {
    clearSession()
  }
}

export default API_URL
