import { motion, useMotionValue, useTransform } from 'framer-motion'
import { Pin, Trash2 } from 'lucide-react'
import { useEffect } from 'react'

import { cn, formatRelativeTime } from '@/shared/lib/utils'
import type { ChatSession } from '@/shared/api/types'
import { resolveSwipeAction, SESSION_SWIPE_THRESHOLD_PX } from './useSessionSwipeGesture'

export interface ChatSessionRowProps {
  session: ChatSession
  isSelected: boolean
  isArmed: boolean
  isDeleting: boolean
  isPinning: boolean
  onSelect: () => void
  onDelete: () => void
  onPin: () => void
  onDisarm: () => void
  rowHandlers: {
    onPointerDown: () => void
    onPointerUp: () => void
    onPointerLeave: () => void
    onPointerCancel: () => void
  }
}

export function ChatSessionRow({
  session,
  isSelected,
  isArmed,
  isDeleting,
  isPinning,
  onSelect,
  onDelete,
  onPin,
  onDisarm,
  rowHandlers,
}: ChatSessionRowProps) {
  const x = useMotionValue(0)
  const pinOpacity = useTransform(x, [0, SESSION_SWIPE_THRESHOLD_PX], [0, 1])
  const deleteOpacity = useTransform(x, [0, -SESSION_SWIPE_THRESHOLD_PX], [0, 1])

  useEffect(() => {
    if (!isArmed) {
      x.set(0)
    }
  }, [isArmed, x])

  function handleDragEnd(_: unknown, info: { offset: { x: number } }) {
    if (!isArmed) return

    const action = resolveSwipeAction(info.offset.x, SESSION_SWIPE_THRESHOLD_PX)
    if (action === 'delete') {
      onDelete()
      return
    }
    if (action === 'pin') {
      onPin()
      return
    }
    onDisarm()
  }

  return (
    <div className="group relative mb-1 h-9 overflow-hidden rounded-md">
      <div className="absolute inset-0 flex items-stretch">
        <motion.div
          style={{ opacity: pinOpacity }}
          className="flex w-1/2 items-center gap-1 bg-emerald-600 px-3 text-xs font-medium text-white"
        >
          <Pin size={14} />
          Fixar
        </motion.div>
        <motion.div
          style={{ opacity: deleteOpacity }}
          className="ml-auto flex w-1/2 items-center justify-end gap-1 bg-destructive px-3 text-xs font-medium text-destructive-foreground"
        >
          Excluir
          <Trash2 size={14} />
        </motion.div>
      </div>

      {/* Ação acessível por teclado/leitor de tela — o swipe é só um atalho.
          Sempre presente no DOM (nunca display:none) para permanecer no tab
          order; só fica visível no hover/foco via opacity + pointer-events. */}
      <div
        className={cn(
          'absolute inset-y-0 right-1 z-20 flex items-center gap-0.5 opacity-0 pointer-events-none transition-opacity',
          'group-hover:opacity-100 group-hover:pointer-events-auto',
          'group-focus-within:opacity-100 group-focus-within:pointer-events-auto',
        )}
      >
        <button
          type="button"
          aria-label={session.pinned ? 'Desafixar conversa' : 'Fixar conversa'}
          className="rounded p-1 text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-1 focus-visible:ring-sidebar-ring"
          onClick={onPin}
        >
          <Pin size={14} />
        </button>
        <button
          type="button"
          aria-label="Excluir conversa"
          className="rounded p-1 text-muted-foreground hover:bg-destructive hover:text-destructive-foreground focus-visible:ring-1 focus-visible:ring-sidebar-ring"
          onClick={onDelete}
        >
          <Trash2 size={14} />
        </button>
      </div>

      <motion.div
        className={cn(
          'relative flex h-9 w-full items-center rounded-md bg-sidebar transition-shadow',
          isSelected && 'bg-sidebar-accent text-sidebar-accent-foreground',
          isArmed && 'z-10 cursor-grab select-none shadow-md ring-1 ring-sidebar-border active:cursor-grabbing',
        )}
        drag={isArmed ? 'x' : false}
        dragConstraints={{ left: -120, right: 120 }}
        dragElastic={0.12}
        dragMomentum={false}
        style={{ x, touchAction: isArmed ? 'none' : 'pan-y' }}
        onDragEnd={handleDragEnd}
        onContextMenu={event => {
          if (isArmed) event.preventDefault()
        }}
        {...rowHandlers}
      >
        <button
          type="button"
          className={cn(
            'flex min-w-0 flex-1 items-center justify-between rounded-md px-2 text-left text-sm text-sidebar-foreground transition hover:bg-sidebar-accent',
            isSelected && 'text-sidebar-accent-foreground',
            isArmed && 'pointer-events-none',
          )}
          onClick={onSelect}
        >
          <span className="flex min-w-0 items-center gap-1.5 truncate pr-2">
            {session.pinned ? <Pin size={12} className="shrink-0 text-emerald-500" /> : null}
            <span className="truncate">{session.title}</span>
          </span>
          <span className="shrink-0 text-xs text-muted-foreground">
            {formatRelativeTime(session.updated_at)}
          </span>
        </button>
      </motion.div>

      {(isDeleting || isPinning) && (
        <div className="pointer-events-none absolute inset-0 rounded-md bg-sidebar/40" />
      )}
    </div>
  )
}
