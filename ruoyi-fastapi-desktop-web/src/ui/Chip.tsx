import clsx from 'clsx'
import type { ButtonHTMLAttributes } from 'react'

export type ChipProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  selected?: boolean
  tone?: 'neutral' | 'accent' | 'muted' | 'danger'
  size?: 'sm' | 'md'
}

export function Chip({
  className,
  selected,
  tone = 'neutral',
  size = 'md',
  type,
  ...props
}: ChipProps) {
  return (
    <button
      type={type ?? 'button'}
      className={clsx(
        'ds-chip',
        `ds-chip--${tone}`,
        `ds-chip--${size}`,
        selected && 'ds-chip--selected',
        className,
      )}
      {...props}
    />
  )
}

