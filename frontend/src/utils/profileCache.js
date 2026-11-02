const KEY = 'sabores_profile'

export function getCachedProfile() {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return null
    const data = JSON.parse(raw)
    if (!data || typeof data !== 'object') return null
    return {
      name: data.name || '',
      email: data.email || '',
      image: data.image || '',
    }
  } catch {
    return null
  }
}

export function setCachedProfile(profile) {
  if (!profile || typeof profile !== 'object') return
  localStorage.setItem(
    KEY,
    JSON.stringify({
      name: profile.name || '',
      email: profile.email || '',
      image: profile.image || '',
    })
  )
}

export function patchCachedProfile(partial) {
  const current = getCachedProfile() || { name: '', email: '', image: '' }
  setCachedProfile({ ...current, ...partial })
}

export function clearCachedProfile() {
  localStorage.removeItem(KEY)
}
