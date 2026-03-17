import clsx from 'clsx'

export function StatusPill(props: { value?: string }) {
  const v = props.value
  const tone = v === '0' ? 'ok' : v === '1' ? 'muted' : 'neutral'
  const text = v === '0' ? '启用' : v === '1' ? '停用' : '-'

  return <span className={clsx('ds-pill', `ds-pill--${tone}`)}>{text}</span>
}

