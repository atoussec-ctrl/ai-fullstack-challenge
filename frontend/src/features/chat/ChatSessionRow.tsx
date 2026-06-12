import { AnimatePresence, motion } from 'framer-motion'
import { Trash2 } from 'lucide-react'

import { cn, formatRelativeTime } from '@/shared/lib/utils'
import type { ChatSession } from '@/shared/api/types'

export interface ChatSessionRowProps {
  session: ChatSession
  isSelected: boolean
  showDelete: boolean
  isDeleting: boolean
  onSelect: () => void
  onDelete: () => void
  rowHandlers: {
    onPointerDown: () => void
    onPointerUp: () => void
    onPointerLeave: () => void
    onPointerCancel: () => void
    onDoubleClick: (event: React.MouseEvent) => void
  }
}

export function ChatSessionRow({
  session,
  isSelected,
  showDelete,
  isDeleting,
  onSelect,
  onDelete,
  rowHandlers,
}: ChatSessionRowProps) {
  return (
    <div
      className={cn(
        'group relative mb-1 flex h-9 w-full items-center rounded-md transition',
        isSelected && 'bg-sidebar-accent text-sidebar-accent-foreground',
      )}
      {...rowHandlers}
    >
      <button
        type="button"
        className={cn(
          'flex min-w-0 flex-1 items-center justify-between rounded-md px-2 text-left text-sm text-sidebar-foreground transition hover:bg-sidebar-accent',
          isSelected && 'text-sidebar-accent-foreground',
        )}
        onClick={onSelect}
      >
        <span className="min-w-0 truncate pr-2">{session.title}</span>
        <span className="shrink-0 text-xs text-muted-foreground">
          {formatRelativeTime(session.updated_at)}
        </span>
      </button>

      <AnimatePresence>
        {showDelete && (
          <motion.button
            type="button"
            initial={{ opacity: 0, scale: 0.5, x: 8 }}
            animate={{ opacity: 1, scale: 1, x: 0 }}
            exit={{ opacity: 0, scale: 0.5, x: 8 }}
            transition={{ type: 'spring', stiffness: 420, damping: 24 }}
            aria-label={`Excluir conversa ${session.title}`}
            className="absolute right-1 grid h-7 w-7 place-items-center rounded-md bg-destructive text-destructive-foreground shadow-sm disabled:opacity-60"
            disabled={isDeleting}
            onClick={event => {
              event.stopPropagation()
              onDelete()
            }}
          >
            <Trash2 size={14} />
          </motion.button>
        )}
      </AnimatePresence>
    </div>
  )
}
