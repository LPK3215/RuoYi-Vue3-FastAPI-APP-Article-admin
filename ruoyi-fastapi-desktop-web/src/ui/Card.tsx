import clsx from 'clsx'
import type { HTMLAttributes, ReactNode } from 'react'

export function Card({
  className,
  ...props
}: HTMLAttributes<HTMLDivElement>) {
  return <div className={clsx('ds-card', className)} {...props} />
}

export function CardHeader(props: { title: string; subtitle?: string; right?: ReactNode }) {
  return (
    <div className="ds-cardHeader">
      <div className="ds-cardHeaderText">
        <div className="ds-cardTitle">{props.title}</div>
        {props.subtitle ? (
          <div className="ds-cardSubtitle">{props.subtitle}</div>
        ) : null}
      </div>
      {props.right ? <div className="ds-cardHeaderRight">{props.right}</div> : null}
    </div>
  )
}

