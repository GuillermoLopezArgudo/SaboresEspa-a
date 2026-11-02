/**
 * Comprime una imagen en el cliente antes de subirla (base64).
 * Devuelve { name, base64 } listo para el API.
 */
export function compressImageFile(file, options = {}) {
  const {
    maxWidth = 1600,
    maxHeight = 1600,
    quality = 0.82,
    mimeType = 'image/jpeg',
  } = options

  return new Promise((resolve, reject) => {
    if (!file || !file.type?.startsWith('image/')) {
      reject(new Error('Archivo de imagen no válido'))
      return
    }

    // GIF/animados: no reencodear
    if (file.type === 'image/gif') {
      const reader = new FileReader()
      reader.onloadend = () =>
        resolve({ name: file.name, base64: reader.result })
      reader.onerror = () => reject(new Error('No se pudo leer la imagen'))
      reader.readAsDataURL(file)
      return
    }

    const url = URL.createObjectURL(file)
    const img = new Image()
    img.onload = () => {
      URL.revokeObjectURL(url)
      let { width, height } = img
      const ratio = Math.min(maxWidth / width, maxHeight / height, 1)
      width = Math.round(width * ratio)
      height = Math.round(height * ratio)

      const canvas = document.createElement('canvas')
      canvas.width = width
      canvas.height = height
      const ctx = canvas.getContext('2d')
      if (!ctx) {
        reject(new Error('Canvas no disponible'))
        return
      }
      ctx.drawImage(img, 0, 0, width, height)

      const outType = file.type === 'image/png' && quality >= 0.95 ? 'image/png' : mimeType
      const base64 = canvas.toDataURL(outType, quality)
      const base = file.name.replace(/\.[^.]+$/, '')
      const ext = outType === 'image/png' ? 'png' : 'jpg'
      resolve({
        name: `${base}.${ext}`,
        base64,
      })
    }
    img.onerror = () => {
      URL.revokeObjectURL(url)
      reject(new Error('No se pudo cargar la imagen'))
    }
    img.src = url
  })
}

export function responsiveSrc(url) {
  if (!url) return { src: '', srcset: '' }
  // Cloudinary: generar tamaños si es URL de Cloudinary
  if (/res\.cloudinary\.com\//.test(url) && /\/upload\//.test(url)) {
    const make = (w) => url.replace('/upload/', `/upload/c_fill,f_auto,q_auto,w_${w}/`)
    return {
      src: make(800),
      srcset: `${make(400)} 400w, ${make(800)} 800w, ${make(1200)} 1200w`,
      sizes: '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 400px',
    }
  }
  return { src: url, srcset: '', sizes: '' }
}
