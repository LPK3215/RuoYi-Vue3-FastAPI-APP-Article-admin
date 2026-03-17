import clsx from 'clsx'
import type { InputHTMLAttributes } from 'react'

export type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label?: string
}

export function Input({ className, label, ...props }: InputProps) {
  return (
    <label className={clsx('ds-field', className)}>
      {label ? <span className="ds-label">{label}</span> : null}
      <input className="ds-input" {...props} />
    </label>
  )
}

