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

describe('ChatSessionRow', () => {
  it('shows pin and delete actions when armed', () => {
    render(
      <ChatSessionRow
        session={session}
        isSelected={false}
        isArmed
        isDeleting={false}
        isPinning={false}
        onSelect={vi.fn()}
        onDelete={vi.fn()}
        onPin={vi.fn()}
        onDisarm={vi.fn()}
        rowHandlers={rowHandlers}
      />,
    )

    expect(screen.getByText('Fixar')).toBeInTheDocument()
    expect(screen.getByText('Excluir')).toBeInTheDocument()
  })

  it('applies selected styles when active', () => {
    const { container } = render(
      <ChatSessionRow
        session={session}
        isSelected
        isArmed={false}
        isDeleting={false}
        isPinning={false}
        onSelect={vi.fn()}
        onDelete={vi.fn()}
        onPin={vi.fn()}
        onDisarm={vi.fn()}
        rowHandlers={rowHandlers}
      />,
    )

    expect(container.querySelector('.bg-sidebar-accent')).toBeInTheDocument()
  })

  it('calls onSelect when row is clicked', () => {
    const onSelect = vi.fn()

    render(
      <ChatSessionRow
        session={session}
        isSelected={false}
        isArmed={false}
        isDeleting={false}
        isPinning={false}
        onSelect={onSelect}
        onDelete={vi.fn()}
        onPin={vi.fn()}
        onDisarm={vi.fn()}
        rowHandlers={rowHandlers}
      />,
    )

    fireEvent.click(screen.getByText('Conversa de teste'))
    expect(onSelect).toHaveBeenCalledTimes(1)
  })
})
