export function hashCardSeed(value) {
  const text = String(value || '')
  let hash = 0
  for (let i = 0; i < text.length; i += 1) {
    hash = (hash << 5) - hash + text.charCodeAt(i)
    hash |= 0
  }
  return Math.abs(hash)
}

export function pickCardTone(seed, tones) {
  if (!Array.isArray(tones) || !tones.length) {
    return {
      accent: '#2f6fed',
      surface: '#dce8ff',
      contrast: '#0d2b6b'
    }
  }
  return tones[hashCardSeed(seed) % tones.length]
}

export function cardToneVars(seed, tones, prefix = 'card') {
  const tone = pickCardTone(seed, tones)
  return {
    [`--${prefix}-accent`]: tone.accent,
    [`--${prefix}-surface`]: tone.surface,
    [`--${prefix}-contrast`]: tone.contrast || tone.accent
  }
}

export function firstCardGlyph(value, fallback = '?') {
  const text = String(value || '').trim()
  if (!text) return fallback
  return Array.from(text)[0]
}
