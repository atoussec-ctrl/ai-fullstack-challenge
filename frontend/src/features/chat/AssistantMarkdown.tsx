import { Copy } from 'lucide-react'
import type { ReactNode } from 'react'
import ReactMarkdown from 'react-markdown'
import rehypeHighlight from 'rehype-highlight'
import remarkGfm from 'remark-gfm'

function toText(children: ReactNode): string {
  if (typeof children === 'string' || typeof children === 'number') {
    return String(children)
  }
  if (Array.isArray(children)) {
    return children.map(toText).join('')
  }
  if (children && typeof children === 'object' && 'props' in children) {
    return toText((children as { props?: { children?: React.ReactNode } }).props?.children)
  }
  return ''
}

function CodeBlock({
  children,
  className,
}: {
  children: ReactNode
  className?: string
}) {
  const code = toText(children).replace(/\n$/, '')
  const language = className?.match(/language-(\w+)/)?.[1] ?? 'texto'

  return (
    <div className="my-4 overflow-hidden rounded-lg border border-border bg-zinc-950 text-zinc-50">
      <div className="flex h-9 items-center justify-between border-b border-white/10 px-3 text-xs text-zinc-400">
        <span>{language}</span>
        <button
          className="inline-flex items-center gap-1 rounded px-2 py-1 hover:bg-white/10"
          onClick={() => navigator.clipboard?.writeText(code)}
          type="button"
        >
          <Copy size={13} />
          Copiar
        </button>
      </div>
      <pre className="overflow-x-auto p-4 text-sm">
        <code className={className}>{children}</code>
      </pre>
    </div>
  )
}

export default function AssistantMarkdown({ content }: { content: string }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeHighlight]}
      components={{
        code: ({ children, className }) =>
          className ? (
            <CodeBlock className={className}>{children}</CodeBlock>
          ) : (
            <code>{children}</code>
          ),
        pre: ({ children }) => <>{children}</>,
      }}
    >
      {content}
    </ReactMarkdown>
  )
}
