export type PortalTheme = 'metal' | 'admin-light' | 'admin-dark'
export type ThemeSwitchOrigin = {
  clientX?: number
  clientY?: number
}

type ThemeTone = 'light' | 'dark'

const THEME_STORAGE_KEY = 'deskops:portal-theme'

export const THEME_ORDER: PortalTheme[] = ['metal', 'admin-light', 'admin-dark']

export const portalThemeOptions = [
  { id: 'metal', label: '金属科技', shortLabel: '金属', tone: 'dark' },
  { id: 'admin-light', label: '后台浅色', shortLabel: '浅色', tone: 'light' },
  { id: 'admin-dark', label: '后台深色', shortLabel: '深色', tone: 'dark' },
] as const satisfies ReadonlyArray<{
  id: PortalTheme
  label: string
  shortLabel: string
  tone: ThemeTone
}>

function isPortalTheme(value: string | null): value is PortalTheme {
  return value === 'metal' || value === 'admin-light' || value === 'admin-dark'
}

function resolveStoredTheme(): PortalTheme | null {
  if (typeof window === 'undefined') {
    return null
  }

  try {
    const cached = window.localStorage.getItem(THEME_STORAGE_KEY)
    if (isPortalTheme(cached)) {
      return cached
    }
    if (cached === 'dark') {
      return 'metal'
    }
    if (cached === 'light') {
      return 'admin-light'
    }
  } catch {
    // Ignore localStorage access errors and fall back to defaults.
  }

  return null
}

export function getThemeTone(theme: PortalTheme): ThemeTone {
  return portalThemeOptions.find((option) => option.id === theme)?.tone ?? 'dark'
}

function getSystemTheme(): PortalTheme {
  if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') {
    return 'metal'
  }
  return window.matchMedia('(prefers-color-scheme: light)').matches ? 'admin-light' : 'metal'
}

export function resolveInitialTheme(): PortalTheme {
  if (typeof window === 'undefined') {
    return 'metal'
  }

  const cachedTheme = resolveStoredTheme()
  if (cachedTheme) {
    return cachedTheme
  }

  return getSystemTheme()
}

export function applyTheme(theme: PortalTheme) {
  if (typeof document === 'undefined') return
  document.documentElement.dataset.theme = theme
  document.documentElement.style.colorScheme = getThemeTone(theme)
}

export function persistTheme(theme: PortalTheme) {
  if (typeof window === 'undefined') {
    return
  }

  try {
    window.localStorage.setItem(THEME_STORAGE_KEY, theme)
  } catch {
    // Ignore storage failures in private mode or restricted contexts.
  }
}
