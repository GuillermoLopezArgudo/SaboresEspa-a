/** Cache en memoria para no refetch al entrar/salir del recetario. */

const TTL_MS = 60_000

const store = {
  viewAll: null,
  averageStars: null,
}

function fresh(entry) {
  return entry && Date.now() - entry.at < TTL_MS
}

export function getViewAllCache() {
  if (!fresh(store.viewAll)) return null
  const data = store.viewAll.data
  const list = data?.recipes_list || []
  // Invalidar cache antiguo sin autor
  if (list.length && !Object.prototype.hasOwnProperty.call(list[0], 'author')) {
    store.viewAll = null
    return null
  }
  return data
}

export function setViewAllCache(data) {
  store.viewAll = { at: Date.now(), data }
}

export function getAverageStarsCache() {
  return fresh(store.averageStars) ? store.averageStars.data : null
}

export function setAverageStarsCache(data) {
  store.averageStars = { at: Date.now(), data }
}

export function invalidateRecipeCaches() {
  store.viewAll = null
  store.averageStars = null
}
