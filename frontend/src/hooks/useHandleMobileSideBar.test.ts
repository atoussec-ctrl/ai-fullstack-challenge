import { act, renderHook } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { useHandleMobileSideBar } from './useHandleMobileSideBar'

describe('useHandleMobileSideBar', () => {
  it('starts with sidebar closed', () => {
    const { result } = renderHook(() => useHandleMobileSideBar())
    expect(result.current.isOpen).toBe(false)
  })

  it('toggles sidebar open and closed', () => {
    const { result } = renderHook(() => useHandleMobileSideBar())

    act(() => result.current.handleOpen())
    expect(result.current.isOpen).toBe(true)

    act(() => result.current.handleOpen())
    expect(result.current.isOpen).toBe(false)
  })

  it('closes sidebar explicitly', () => {
    const { result } = renderHook(() => useHandleMobileSideBar())

    act(() => result.current.handleOpen())
    act(() => result.current.handleClose())

    expect(result.current.isOpen).toBe(false)
  })
})
