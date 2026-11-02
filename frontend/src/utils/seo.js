const DEFAULT_TITLE = 'Sabores España'
const DEFAULT_DESC = 'Descubre y comparte recetas de la cocina española'

function ensureMeta(attr, key, content) {
  if (!content) return
  let el = document.head.querySelector(`meta[${attr}="${key}"]`)
  if (!el) {
    el = document.createElement('meta')
    el.setAttribute(attr, key)
    document.head.appendChild(el)
  }
  el.setAttribute('content', content)
}

export function setPageSeo({
  title,
  description = DEFAULT_DESC,
  image,
  url,
  type = 'website',
} = {}) {
  const fullTitle = title ? `${title} · ${DEFAULT_TITLE}` : DEFAULT_TITLE
  document.title = fullTitle

  ensureMeta('name', 'description', description)
  ensureMeta('property', 'og:title', fullTitle)
  ensureMeta('property', 'og:description', description)
  ensureMeta('property', 'og:type', type)
  ensureMeta('name', 'twitter:card', image ? 'summary_large_image' : 'summary')
  ensureMeta('name', 'twitter:title', fullTitle)
  ensureMeta('name', 'twitter:description', description)

  if (image) {
    ensureMeta('property', 'og:image', image)
    ensureMeta('name', 'twitter:image', image)
  }
  if (url) {
    ensureMeta('property', 'og:url', url)
  }
}

export function resetPageSeo() {
  setPageSeo({ title: '', description: DEFAULT_DESC })
}
