import clsx from 'clsx'
import type { ButtonHTMLAttributes } from 'react'

export type ButtonVariant = 'primary' | 'ghost' | 'danger'

export type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant
  size?: 'sm' | 'md'
}

export function Button({
  className,
  variant = 'primary',
  size = 'md',
  type,
  ...props
}: ButtonProps) {
  return (
    <button
      className={clsx(
        'ds-btn',
        `ds-btn--${variant}`,
        `ds-btn--${size}`,
        className,
      )}
      type={type ?? 'button'}
      {...props}
    />
  )
}
