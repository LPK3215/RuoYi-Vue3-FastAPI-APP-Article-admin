import { createContext } from 'react'
import type { PortalTheme, ThemeSwitchOrigin } from './theme-config'

export type ThemeContextValue = {
  theme: PortalTheme
  setTheme: (theme: PortalTheme, origin?: ThemeSwitchOrigin) => Promise<void>
  cycleTheme: (origin?: ThemeSwitchOrigin) => Promise<void>
}

export const ThemeContext = createContext<ThemeContextValue | null>(null)
