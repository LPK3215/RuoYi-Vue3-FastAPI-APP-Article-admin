import clsx from 'clsx'
import { Button } from '@/ui/Button'
import { portalThemeOptions } from './theme-config'
import { useTheme } from './useTheme'

export function ThemeSwitcher() {
  const { theme, setTheme } = useTheme()

  return (
    <div className="ds-themePicker" role="toolbar" aria-label="主题切换">
      <div className="ds-themePickerLead" aria-hidden="true">
        <span className={clsx('ds-themePickerHalo', `ds-themePickerHalo--${theme}`)} />
      </div>
      <div className="ds-themePickerRail">
        {portalThemeOptions.map((option) => (
          <Button
            key={option.id}
            variant="ghost"
            size="sm"
            className={clsx('ds-themeChoice', theme === option.id && 'ds-themeChoice--active')}
            onClick={(event) => void setTheme(option.id, { clientX: event.clientX, clientY: event.clientY })}
            aria-pressed={theme === option.id}
            aria-label={`切换为${option.label}主题`}
            title={`切换为${option.label}主题`}
          >
            <span className={clsx('ds-themeChoiceIcon', `ds-themeChoiceIcon--${option.id}`)} aria-hidden="true" />
            <span className="ds-themeChoiceLabel">{option.shortLabel}</span>
          </Button>
        ))}
      </div>
    </div>
  )
}
