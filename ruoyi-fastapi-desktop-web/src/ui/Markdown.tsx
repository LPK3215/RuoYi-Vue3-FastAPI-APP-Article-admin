import clsx from 'clsx'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export function Markdown(props: { className?: string; children?: string | null }) {
  const text = (props.children || '').trim()
  if (!text) return null

  return (
    <div className={clsx('ds-md', props.className)}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
    </div>
  )
}

