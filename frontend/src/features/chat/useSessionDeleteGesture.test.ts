import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { useSessionDeleteGesture } from './useSessionDeleteGesture'

describe('useSessionDeleteGesture', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('arms delete after long press', () => {
    const { result } = renderHook(() => useSessionDeleteGesture(400))
    const handlers = result.current.getRowHandlers('session_a')

    act(() => handlers.onPointerDown())
    expect(result.current.armedSessionId).toBeNull()

    act(() => vi.advanceTimersByTime(400))
    expect(result.current.armedSessionId).toBe('session_a')
  })

  it('cancels long press when pointer is released early', () => {
    const { result } = renderHook(() => useSessionDeleteGesture(400))
    const handlers = result.current.getRowHandlers('session_a')

    act(() => {
      handlers.onPointerDown()
      vi.advanceTimersByTime(200)
      handlers.onPointerUp()
      vi.advanceTimersByTime(400)
    })

    expect(result.current.armedSessionId).toBeNull()
  })

  it('arms delete on double click', () => {
    const { result } = renderHook(() => useSessionDeleteGesture())
    const handlers = result.current.getRowHandlers('session_b')
    const event = { preventDefault: vi.fn() } as unknown as React.MouseEvent

    act(() => handlers.onDoubleClick(event))

    expect(event.preventDefault).toHaveBeenCalled()
    expect(result.current.armedSessionId).toBe('session_b')
  })

  it('cancels long press when pointer is cancelled', () => {
    const { result } = renderHook(() => useSessionDeleteGesture(400))
    const handlers = result.current.getRowHandlers('session_a')

    act(() => {
      handlers.onPointerDown()
      vi.advanceTimersByTime(200)
      handlers.onPointerCancel()
      vi.advanceTimersByTime(400)
    })

    expect(result.current.armedSessionId).toBeNull()
  })

  it('cancels long press when pointer leaves the row', () => {
    const { result } = renderHook(() => useSessionDeleteGesture(400))
    const handlers = result.current.getRowHandlers('session_a')

    act(() => {
      handlers.onPointerDown()
      vi.advanceTimersByTime(200)
      handlers.onPointerLeave()
      vi.advanceTimersByTime(400)
    })

    expect(result.current.armedSessionId).toBeNull()
  })

  it('disarms delete explicitly', () => {
    const { result } = renderHook(() => useSessionDeleteGesture())

    act(() => result.current.armDelete('session_c'))
    expect(result.current.armedSessionId).toBe('session_c')

    act(() => result.current.disarmDelete())
    expect(result.current.armedSessionId).toBeNull()
  })
})
