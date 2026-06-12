import type { ButtonHTMLAttributes } from 'react'
import { cn } from '@/shared/lib/utils'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'ghost' | 'soft' | 'danger'
  size?: 'sm' | 'md' | 'icon'
}

export function Button({
  className,
  variant = 'default',
  size = 'md',
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex shrink-0 items-center justify-center gap-2 rounded-md text-sm font-medium transition outline-none',
        'focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background',
        'disabled:pointer-events-none disabled:opacity-50',
        variant === 'default' &&
          'bg-primary text-primary-foreground hover:bg-primary/90',
        variant === 'ghost' && 'hover:bg-accent hover:text-accent-foreground',
        variant === 'soft' && 'bg-secondary text-secondary-foreground hover:bg-accent',
        variant === 'danger' &&
          'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        size === 'sm' && 'h-8 px-3',
        size === 'md' && 'h-10 px-4',
        size === 'icon' && 'h-9 w-9 p-0',
        className,
      )}
      {...props}
    />
  )
}
