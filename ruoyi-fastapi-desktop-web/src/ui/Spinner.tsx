import clsx from 'clsx'

export function Spinner(props: { className?: string; label?: string }) {
  return (
    <div className={clsx('ds-spinnerWrap', props.className)}>
      <span className="ds-spinner" aria-hidden="true" />
      {props.label ? <span className="ds-spinnerLabel">{props.label}</span> : null}
    </div>
  )
}

