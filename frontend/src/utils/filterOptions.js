export const foodTypes = [
  { value: 'starters', label: 'Entrantes' },
  { value: 'maindishes', label: 'Platos principales' },
  { value: 'accompaniments', label: 'Acompañamientos' },
  { value: 'dessert', label: 'Postres' },
  { value: 'soups', label: 'Sopas' },
  { value: 'salads', label: 'Ensaladas' },
  { value: 'sauces', label: 'Salsas' },
  { value: 'breads', label: 'Panes y masas' },
]

export const regions = [
  { value: 'andalucia', label: 'Andalucía' },
  { value: 'aragon', label: 'Aragón' },
  { value: 'asturias', label: 'Asturias' },
  { value: 'cantabria', label: 'Cantabria' },
  { value: 'castillalamancha', label: 'Castilla-La Mancha' },
  { value: 'castillaleon', label: 'Castilla y León' },
  { value: 'catalunya', label: 'Cataluña' },
  { value: 'valencia', label: 'Com. Valenciana' },
  { value: 'extremadura', label: 'Extremadura' },
  { value: 'galicia', label: 'Galicia' },
  { value: 'baleares', label: 'Baleares' },
  { value: 'canarias', label: 'Canarias' },
  { value: 'larioja', label: 'La Rioja' },
  { value: 'madrid', label: 'Madrid' },
  { value: 'murcia', label: 'Murcia' },
  { value: 'navarra', label: 'Navarra' },
  { value: 'paisvasco', label: 'País Vasco' },
]

export const proteins = [
  { value: 'pollo', label: 'Pollo' },
  { value: 'res', label: 'Res / Ternera' },
  { value: 'cerdo', label: 'Cerdo / Ibérico' },
  { value: 'cordero', label: 'Cordero' },
  { value: 'conejo', label: 'Conejo' },
  { value: 'pato', label: 'Pato' },
  { value: 'pescado', label: 'Pescado blanco' },
  { value: 'atun', label: 'Atún' },
  { value: 'bacalao', label: 'Bacalao' },
  { value: 'salmon', label: 'Salmón' },
  { value: 'anguila', label: 'Anguila' },
  { value: 'mariscos', label: 'Mariscos' },
  { value: 'pulpo', label: 'Pulpo' },
  { value: 'calamar', label: 'Calamar / Sepia' },
  { value: 'huevo', label: 'Huevo' },
  { value: 'queso', label: 'Queso' },
  { value: 'legumbres', label: 'Legumbres' },
  { value: 'setas', label: 'Setas' },
  { value: 'vegetariana', label: 'Vegetariana' },
  { value: 'vegana', label: 'Vegana' },
]

export const prepTimes = [
  { value: 'menos15', label: 'Rápida', description: '<15 min' },
  { value: '15a30', label: 'Media', description: '15–30 min' },
  { value: '30a60', label: 'Lenta', description: '30–60 min' },
  { value: 'mas60', label: 'Muy lenta', description: '>1 h' },
]

const OPTIONS_BY_CATEGORY = {
  typeeat: foodTypes,
  ccaa: regions,
  time: prepTimes,
  protein: proteins,
}

export function labelForFilter(category, value) {
  const opts = OPTIONS_BY_CATEGORY[category] || []
  return opts.find((o) => o.value === value)?.label || value
}

export function emptyFilterCriteria() {
  return {
    typeeat: '',
    ccaa: '',
    time: '',
    proteins: [],
  }
}

/** Añade o sustituye un filtro según el tipo de categoría de RecipeFilter. */
export function mergeFilterCriteria(current, category, value) {
  const next = {
    typeeat: current?.typeeat || '',
    ccaa: current?.ccaa || '',
    time: current?.time || '',
    proteins: Array.isArray(current?.proteins) ? [...current.proteins] : [],
  }

  if (category === 'typeeat') next.typeeat = value
  else if (category === 'ccaa') next.ccaa = value
  else if (category === 'time') next.time = value
  else if (category === 'protein') {
    if (!next.proteins.includes(value)) next.proteins.push(value)
  }

  return next
}

export function hasActiveFilters(criteria) {
  return Boolean(
    criteria?.typeeat ||
      criteria?.ccaa ||
      criteria?.time ||
      (Array.isArray(criteria?.proteins) && criteria.proteins.length)
  )
}
