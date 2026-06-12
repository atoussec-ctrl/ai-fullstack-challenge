import { useCallback, useRef, useState } from 'react'

export const SESSION_DELETE_LONG_PRESS_MS = 550

export function useSessionDeleteGesture(longPressMs = SESSION_DELETE_LONG_PRESS_MS) {
  const [armedSessionId, setArmedSessionId] = useState<string | null>(null)
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const clearTimer = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current)
      timerRef.current = null
    }
  }, [])

  const armDelete = useCallback((sessionId: string) => {
    clearTimer()
    setArmedSessionId(sessionId)
  }, [clearTimer])

  const disarmDelete = useCallback(() => {
    clearTimer()
    setArmedSessionId(null)
  }, [clearTimer])

  const getRowHandlers = useCallback(
    (sessionId: string) => ({
      onPointerDown: () => {
        clearTimer()
        timerRef.current = setTimeout(() => armDelete(sessionId), longPressMs)
      },
      onPointerUp: clearTimer,
      onPointerLeave: clearTimer,
      onPointerCancel: clearTimer,
      onDoubleClick: (event: React.MouseEvent) => {
        event.preventDefault()
        armDelete(sessionId)
      },
    }),
    [armDelete, clearTimer, longPressMs],
  )

  return { armedSessionId, armDelete, disarmDelete, getRowHandlers }
}
