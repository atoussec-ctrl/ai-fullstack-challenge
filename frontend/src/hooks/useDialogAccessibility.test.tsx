import { useState } from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import { useDialogAccessibility } from './useDialogAccessibility'

function Dialog({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const ref = useDialogAccessibility<HTMLDivElement>(isOpen, onClose)
  if (!isOpen) return null
  return (
    <div ref={ref} role="dialog" aria-modal="true">
      <button>Primeiro</button>
      <button>Meio</button>
      <button>Segundo</button>
    </div>
  )
}

function OpenableDialog() {
  const [isOpen, setIsOpen] = useState(false)
  return (
    <div>
      <button onClick={() => setIsOpen(true)}>Abrir</button>
      <Dialog isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </div>
  )
}

describe('useDialogAccessibility', () => {
  it('moves focus into the dialog when it opens', () => {
    render(<Dialog isOpen onClose={() => {}} />)

    expect(screen.getByText('Primeiro')).toHaveFocus()
  })

  it('calls onClose when Escape is pressed', () => {
    const onClose = vi.fn()
    render(<Dialog isOpen onClose={onClose} />)

    fireEvent.keyDown(document, { key: 'Escape' })

    expect(onClose).toHaveBeenCalledTimes(1)
  })

  it('wraps Tab from the last focusable element back to the first', () => {
    render(<Dialog isOpen onClose={() => {}} />)
    screen.getByText('Segundo').focus()

    fireEvent.keyDown(document, { key: 'Tab' })

    expect(screen.getByText('Primeiro')).toHaveFocus()
  })

  it('wraps Shift+Tab from the first focusable element back to the last', () => {
    render(<Dialog isOpen onClose={() => {}} />)

    fireEvent.keyDown(document, { key: 'Tab', shiftKey: true })

    expect(screen.getByText('Segundo')).toHaveFocus()
  })

  it('does not intercept Tab when focus is not on an edge element', () => {
    render(<Dialog isOpen onClose={() => {}} />)
    screen.getByText('Meio').focus()
    const event = new KeyboardEvent('keydown', { key: 'Tab', bubbles: true, cancelable: true })
    const preventDefaultSpy = vi.spyOn(event, 'preventDefault')

    document.dispatchEvent(event)

    expect(preventDefaultSpy).not.toHaveBeenCalled()
  })

  it('restores focus to the element that opened it once closed', () => {
    render(<OpenableDialog />)
    const openButton = screen.getByText('Abrir')
    openButton.focus()

    fireEvent.click(openButton)
    expect(screen.getByText('Primeiro')).toHaveFocus()

    fireEvent.keyDown(document, { key: 'Escape' })

    expect(openButton).toHaveFocus()
  })

  it('does nothing while closed', () => {
    const onClose = vi.fn()
    render(<Dialog isOpen={false} onClose={onClose} />)

    fireEvent.keyDown(document, { key: 'Escape' })

    expect(onClose).not.toHaveBeenCalled()
  })
})
