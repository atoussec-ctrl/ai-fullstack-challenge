import { motion } from 'framer-motion'
import { Bot } from 'lucide-react'

import { Badge } from '@/components/ui/badge'

interface ThinkingIndicatorProps {
  modeLabel: string
}

const DOT_DELAYS = [0, 0.18, 0.36] as const

export function ThinkingIndicator({ modeLabel }: ThinkingIndicatorProps) {
  return (
    <motion.article
      aria-label="Assistente pensando"
      aria-live="polite"
      aria-busy="true"
      className="flex w-full justify-start"
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10, transition: { duration: 0.15 } }}
      transition={{ duration: 0.22, ease: 'easeOut' }}
    >
      <div className="w-full max-w-[860px] text-foreground">
        <div className="mb-3 flex items-center gap-2 text-sm font-medium">
          <motion.span
            className="relative grid h-7 w-7 place-items-center rounded-md bg-primary text-primary-foreground"
            animate={{ scale: [1, 1.04, 1] }}
            transition={{ duration: 2.2, repeat: Infinity, ease: 'easeInOut' }}
          >
            <Bot size={16} />
            <motion.span
              className="pointer-events-none absolute inset-0 rounded-md ring-2 ring-primary/40"
              animate={{ opacity: [0.35, 0.85, 0.35], scale: [1, 1.18, 1] }}
              transition={{ duration: 2.2, repeat: Infinity, ease: 'easeInOut' }}
            />
          </motion.span>
          MindSight AI
          <Badge>{modeLabel}</Badge>
        </div>

        <motion.div
          className="inline-flex items-center gap-3 rounded-2xl border border-border/70 bg-card/80 px-4 py-3 shadow-sm backdrop-blur-sm"
          initial={{ opacity: 0.6 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          <div className="flex items-center gap-1.5" aria-hidden="true">
            {DOT_DELAYS.map(delay => (
              <motion.span
                key={delay}
                className="h-2 w-2 rounded-full bg-muted-foreground"
                animate={{ y: [0, -5, 0], opacity: [0.35, 1, 0.35] }}
                transition={{
                  duration: 0.9,
                  repeat: Infinity,
                  ease: 'easeInOut',
                  delay,
                }}
              />
            ))}
          </div>

          <motion.span
            className="text-sm font-medium text-muted-foreground"
            animate={{ opacity: [0.55, 1, 0.55] }}
            transition={{ duration: 1.6, repeat: Infinity, ease: 'easeInOut' }}
          >
            Pensando
            <motion.span
              aria-hidden="true"
              animate={{ opacity: [0, 1, 0] }}
              transition={{ duration: 1.6, repeat: Infinity, ease: 'linear' }}
            >
              ...
            </motion.span>
          </motion.span>

          <motion.span
            className="hidden h-px w-16 overflow-hidden rounded-full bg-border sm:block"
            aria-hidden="true"
          >
            <motion.span
              className="block h-full w-1/2 rounded-full bg-primary/50"
              animate={{ x: ['-100%', '220%'] }}
              transition={{ duration: 1.4, repeat: Infinity, ease: 'easeInOut' }}
            />
          </motion.span>
        </motion.div>
      </div>
    </motion.article>
  )
}
