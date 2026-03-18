import { useEffect, useMemo, useState, type ReactNode } from 'react'
import { flushSync } from 'react-dom'
import { ThemeContext, type ThemeContextValue } from './theme-context'
import {
  THEME_ORDER,
  applyTheme,
  getThemeTone,
  persistTheme,
  resolveInitialTheme,
  type PortalTheme,
  type ThemeSwitchOrigin,
} from './theme-config'

type ViewTransitionLike = {
  ready: Promise<void>
  finished: Promise<void>
}

type DocumentWithViewTransition = Document & {
  startViewTransition?: (callback: () => void | Promise<void>) => ViewTransitionLike
}

async function runThemeTransition(
  nextTheme: PortalTheme,
  origin: ThemeSwitchOrigin | undefined,
  commit: () => void,
) {
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    commit()
    return
  }

  const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const startViewTransition = (document as DocumentWithViewTransition).startViewTransition
  if (!startViewTransition || isReducedMotion) {
    commit()
    return
  }

  const x = origin?.clientX ?? window.innerWidth / 2
  const y = origin?.clientY ?? window.innerHeight / 2
  const revealOldSnapshot = getThemeTone(nextTheme) === 'dark'
  const clipPath = [
    `circle(0px at ${x}px ${y}px)`,
    `circle(${Math.hypot(Math.max(x, window.innerWidth - x), Math.max(y, window.innerHeight - y))}px at ${x}px ${y}px)`,
  ]
  let committed = false
  const commitTheme = () => {
    if (committed) return
    committed = true
    commit()
  }

  try {
    const transition = startViewTransition(() => {
      flushSync(() => {
        commitTheme()
      })
    })

    await transition.ready
    document.documentElement.animate(
      {
        clipPath: revealOldSnapshot ? [...clipPath].reverse() : clipPath,
      },
      {
        duration: 650,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
        fill: 'forwards',
        pseudoElement: revealOldSnapshot ? '::view-transition-old(root)' : '::view-transition-new(root)',
      },
    )
    await transition.finished
  } catch {
    commitTheme()
  }
}

export function ThemeProvider(props: { children: ReactNode }) {
  const [theme, setThemeState] = useState<PortalTheme>(() => resolveInitialTheme())

  useEffect(() => {
    applyTheme(theme)
    persistTheme(theme)
  }, [theme])

  const value = useMemo<ThemeContextValue>(
    () => ({
      theme,
      setTheme: async (nextTheme, origin) => {
        if (nextTheme === theme) {
          return
        }
        await runThemeTransition(nextTheme, origin, () => setThemeState(nextTheme))
      },
      cycleTheme: async (origin) => {
        const currentIndex = THEME_ORDER.indexOf(theme)
        const nextTheme = THEME_ORDER[(currentIndex + 1) % THEME_ORDER.length]
        await runThemeTransition(nextTheme, origin, () => setThemeState(nextTheme))
      },
    }),
    [theme],
  )

  return <ThemeContext.Provider value={value}>{props.children}</ThemeContext.Provider>
}
