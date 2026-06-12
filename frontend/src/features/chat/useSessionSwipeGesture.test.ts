import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { useSessionSwipeGesture } from './useSessionSwipeGesture'

describe('useSessionSwipeGesture', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('arms swipe after long press', () => {
    const { result } = renderHook(() => useSessionSwipeGesture(400))
    const handlers = result.current.getRowHandlers('session_a')

    act(() => handlers.onPointerDown())
    expect(result.current.armedSessionId).toBeNull()

    act(() => vi.advanceTimersByTime(400))
    expect(result.current.armedSessionId).toBe('session_a')
  })

  it('cancels long press when pointer is released early', () => {
    const { result } = renderHook(() => useSessionSwipeGesture(400))
    const handlers = result.current.getRowHandlers('session_a')

    act(() => {
      handlers.onPointerDown()
      vi.advanceTimersByTime(200)
      handlers.onPointerUp()
      vi.advanceTimersByTime(400)
    })

    expect(result.current.armedSessionId).toBeNull()
  })

  it('disarms swipe explicitly', () => {
    const { result } = renderHook(() => useSessionSwipeGesture())

    act(() => result.current.armSwipe('session_c'))
    expect(result.current.armedSessionId).toBe('session_c')

    act(() => result.current.disarmSwipe())
    expect(result.current.armedSessionId).toBeNull()
  })
})
