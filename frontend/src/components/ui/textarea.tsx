import type { TextareaHTMLAttributes } from 'react'
import { cn } from '@/shared/lib/utils'

export function Textarea({
  className,
  ...props
}: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      className={cn(
        'min-h-12 w-full resize-none bg-transparent text-base leading-6 text-foreground outline-none placeholder:text-muted-foreground',
        className,
      )}
      {...props}
    />
  )
}
