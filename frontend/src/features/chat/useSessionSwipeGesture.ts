import { useCallback, useRef, useState } from 'react'

export const SESSION_SWIPE_ARM_MS = 550
export const SESSION_SWIPE_THRESHOLD_PX = 72

export type SwipeAction = 'delete' | 'pin' | 'none'

/** Pure decision logic for the swipe gesture — kept separate from the
 * component's onDragEnd handler so it's testable without touching Framer
 * Motion/React internals (onDragEnd is a synthetic Framer Motion prop, not a
 * real DOM event, so it can't be exercised via fireEvent in tests). */
export function resolveSwipeAction(offsetX: number, threshold: number): SwipeAction {
  if (offsetX <= -threshold) return 'delete'
  if (offsetX >= threshold) return 'pin'
  return 'none'
}

export function useSessionSwipeGesture(armDelayMs = SESSION_SWIPE_ARM_MS) {
  const [armedSessionId, setArmedSessionId] = useState<string | null>(null)
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const clearTimer = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current)
      timerRef.current = null
    }
  }, [])

  const armSwipe = useCallback(
    (sessionId: string) => {
      clearTimer()
      setArmedSessionId(sessionId)
    },
    [clearTimer],
  )

  const disarmSwipe = useCallback(() => {
    clearTimer()
    setArmedSessionId(null)
  }, [clearTimer])

  const getRowHandlers = useCallback(
    (sessionId: string) => ({
      onPointerDown: () => {
        clearTimer()
        timerRef.current = setTimeout(() => armSwipe(sessionId), armDelayMs)
      },
      onPointerUp: clearTimer,
      onPointerLeave: clearTimer,
      onPointerCancel: clearTimer,
    }),
    [armSwipe, clearTimer, armDelayMs],
  )

  return { armedSessionId, armSwipe, disarmSwipe, getRowHandlers }
}
