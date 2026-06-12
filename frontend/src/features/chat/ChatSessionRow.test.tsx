import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import { ChatSessionRow } from './ChatSessionRow'

const session = {
  id: 'session_1',
  title: 'Conversa de teste',
  created_at: '2026-06-12T00:00:00Z',
  updated_at: '2026-06-12T01:00:00Z',
}

const rowHandlers = {
  onPointerDown: vi.fn(),
  onPointerUp: vi.fn(),
  onPointerLeave: vi.fn(),
  onPointerCancel: vi.fn(),
  onDoubleClick: vi.fn(),
}

describe('ChatSessionRow', () => {
  it('renders delete icon when showDelete is true', () => {
    render(
      <ChatSessionRow
        session={session}
        isSelected={false}
        showDelete
        isDeleting={false}
        onSelect={vi.fn()}
        onDelete={vi.fn()}
        rowHandlers={rowHandlers}
      />,
    )

    expect(
      screen.getByLabelText('Excluir conversa Conversa de teste'),
    ).toBeInTheDocument()
  })

  it('applies selected styles when active', () => {
    const { container } = render(
      <ChatSessionRow
        session={session}
        isSelected
        showDelete={false}
        isDeleting={false}
        onSelect={vi.fn()}
        onDelete={vi.fn()}
        rowHandlers={rowHandlers}
      />,
    )

    expect(container.firstChild).toHaveClass('bg-sidebar-accent')
  })

  it('calls onDelete when trash icon is clicked', () => {
    const onDelete = vi.fn()

    render(
      <ChatSessionRow
        session={session}
        isSelected={false}
        showDelete
        isDeleting={false}
        onSelect={vi.fn()}
        onDelete={onDelete}
        rowHandlers={rowHandlers}
      />,
    )

    fireEvent.click(screen.getByLabelText('Excluir conversa Conversa de teste'))
    expect(onDelete).toHaveBeenCalledTimes(1)
  })
})
