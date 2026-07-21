import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import { ChatSessionRow } from './ChatSessionRow'

const session = {
  id: 'session_1',
  title: 'Conversa de teste',
  pinned: false,
  pinned_at: null,
  created_at: '2026-06-12T00:00:00Z',
  updated_at: '2026-06-12T01:00:00Z',
}

const rowHandlers = {
  onPointerDown: vi.fn(),
  onPointerUp: vi.fn(),
  onPointerLeave: vi.fn(),
  onPointerCancel: vi.fn(),
}

function renderRow(overrides: Partial<Parameters<typeof ChatSessionRow>[0]> = {}) {
  const props = {
    session,
    isSelected: false,
    isArmed: false,
    isDeleting: false,
    isPinning: false,
    onSelect: vi.fn(),
    onDelete: vi.fn(),
    onPin: vi.fn(),
    onDisarm: vi.fn(),
    rowHandlers,
    ...overrides,
  }
  return { ...render(<ChatSessionRow {...props} />), props }
}

describe('ChatSessionRow', () => {
  it('shows pin and delete actions when armed', () => {
    renderRow({ isArmed: true })

    expect(screen.getByText('Fixar')).toBeInTheDocument()
    expect(screen.getByText('Excluir')).toBeInTheDocument()
  })

  it('applies selected styles when active', () => {
    const { container } = renderRow({ isSelected: true })
    expect(container.querySelector('.bg-sidebar-accent')).toBeInTheDocument()
  })

  it('calls onSelect when row is clicked', () => {
    const onSelect = vi.fn()
    renderRow({ onSelect })

    fireEvent.click(screen.getByText('Conversa de teste'))
    expect(onSelect).toHaveBeenCalledTimes(1)
  })

  it('shows the pin icon when session is pinned', () => {
    const { container } = renderRow({ session: { ...session, pinned: true } })
    // Pin icon is rendered as an SVG via lucide-react — check the svg presence
    expect(container.querySelector('svg')).toBeInTheDocument()
  })

  it('renders loading overlay when isDeleting', () => {
    const { container } = renderRow({ isDeleting: true })
    expect(container.querySelector('.bg-sidebar\\/40')).toBeInTheDocument()
  })

  it('renders loading overlay when isPinning', () => {
    const { container } = renderRow({ isPinning: true })
    expect(container.querySelector('.bg-sidebar\\/40')).toBeInTheDocument()
  })

  it('does not render overlay when neither deleting nor pinning', () => {
    const { container } = renderRow({ isDeleting: false, isPinning: false })
    expect(container.querySelector('.bg-sidebar\\/40')).not.toBeInTheDocument()
  })

  it('calls onPin when the accessible pin button is clicked', () => {
    const onPin = vi.fn()
    renderRow({ onPin })

    fireEvent.click(screen.getByRole('button', { name: 'Fixar conversa' }))

    expect(onPin).toHaveBeenCalledTimes(1)
  })

  it('calls onDelete when the accessible delete button is clicked', () => {
    const onDelete = vi.fn()
    renderRow({ onDelete })

    fireEvent.click(screen.getByRole('button', { name: 'Excluir conversa' }))

    expect(onDelete).toHaveBeenCalledTimes(1)
  })

  it('labels the pin button as "Desafixar" for an already-pinned session', () => {
    renderRow({ session: { ...session, pinned: true } })

    expect(screen.getByRole('button', { name: 'Desafixar conversa' })).toBeInTheDocument()
  })

  it('accessible actions stay reachable by keyboard regardless of hover state', () => {
    renderRow()

    // Real DOM elements (not display:none) are what keeps them in the tab order.
    expect(screen.getByRole('button', { name: 'Fixar conversa' })).toBeVisible()
    expect(screen.getByRole('button', { name: 'Excluir conversa' })).toBeVisible()
  })

  it('prevents contextMenu when armed', () => {
    const { container } = renderRow({ isArmed: true })

    // Find the motion.div that has the onContextMenu handler (it has a style attribute)
    const motionDivs = container.querySelectorAll('[style]')
    // The draggable motion.div is the one with x transform — pick last one
    const draggableDiv = motionDivs[motionDivs.length - 1] as HTMLElement

    // fireEvent correctly triggers React synthetic event handlers
    const prevented = fireEvent.contextMenu(draggableDiv)

    // Returns false when preventDefault() was called
    expect(prevented).toBe(false)
  })

  it('does not prevent contextMenu when not armed', () => {
    const { container } = renderRow({ isArmed: false })

    const motionDivs = container.querySelectorAll('[style]')
    const draggableDiv = motionDivs[motionDivs.length - 1] as HTMLElement

    const prevented = fireEvent.contextMenu(draggableDiv)

    // Returns true when preventDefault() was NOT called
    expect(prevented).toBe(true)
  })
})

