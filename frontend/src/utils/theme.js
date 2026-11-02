import { ref, watch } from 'vue'

const STORAGE_KEY = 'sabores-theme'

const isDark = ref(false)
let initialized = false

function readStoredTheme() {
  try {
    return localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}

export function applyTheme(dark) {
  isDark.value = dark
  const root = document.documentElement
  root.classList.toggle('dark', dark)
  root.dataset.theme = dark ? 'dark' : 'light'
  root.style.colorScheme = dark ? 'dark' : 'light'
  try {
    localStorage.setItem(STORAGE_KEY, dark ? 'dark' : 'light')
  } catch {
    /* ignore */
  }
}

export function initTheme() {
  if (initialized) return isDark
  initialized = true

  const stored = readStoredTheme()
  if (stored === 'light') applyTheme(false)
  else if (stored === 'dark') applyTheme(true)
  else applyTheme(false) // modo día por defecto; la noche se activa con el botón

  watch(isDark, (value) => applyTheme(value))
  return isDark
}

export function toggleTheme() {
  applyTheme(!isDark.value)
}

export function useTheme() {
  if (!initialized) initTheme()
  return { isDark, toggleTheme, applyTheme }
}
