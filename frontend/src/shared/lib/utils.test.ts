import { describe, expect, it, vi } from 'vitest'

import {
  formatFileSize,
  formatRelativeTime,
  generateId,
  groupSessionsByDate,
  groupSessionsForSidebar,
  truncate,
} from './utils'

describe('utils', () => {
  it('formats file sizes', () => {
    expect(formatFileSize(0)).toBe('0 B')
    expect(formatFileSize(1536)).toBe('1.5 KB')
  })

  it('formats relative time buckets', () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-06-12T12:00:00Z'))

    expect(formatRelativeTime('2026-06-12T11:59:30Z')).toBe('just now')
    expect(formatRelativeTime('2026-06-12T11:30:00Z')).toBe('30m ago')
    expect(formatRelativeTime('2026-06-12T11:00:00Z')).toBe('1h ago')
    expect(formatRelativeTime('2026-06-10T12:00:00Z')).toBe('2d ago')

    vi.useRealTimers()
  })

  it('falls back to a localized date for anything a week or older', () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-06-12T12:00:00Z'))

    const oldDate = new Date('2026-04-01T12:00:00Z')

    expect(formatRelativeTime(oldDate.toISOString())).toBe(oldDate.toLocaleDateString())

    vi.useRealTimers()
  })

  it('groups sessions by recency', () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-06-12T12:00:00Z'))

    const groups = groupSessionsByDate([
      { updated_at: '2026-06-12T10:00:00Z' },
      { updated_at: '2026-06-11T10:00:00Z' },
      { updated_at: '2026-06-08T10:00:00Z' },
      { updated_at: '2026-05-01T10:00:00Z' },
    ])

    expect(groups.map(group => group.label)).toEqual([
      'Today',
      'Yesterday',
      'Previous 7 Days',
      'Older',
    ])

    vi.useRealTimers()
  })

  it('assigns sessions to Previous 30 Days bucket', () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-06-12T12:00:00Z'))

    // 15 days ago: older than 7 days but within 30 days
    const groups = groupSessionsByDate([{ updated_at: '2026-05-28T12:00:00Z' }])

    expect(groups).toHaveLength(1)
    expect(groups[0].label).toBe('Previous 30 Days')

    vi.useRealTimers()
  })

  it('separates pinned sessions from recent groups', () => {
    const layout = groupSessionsForSidebar([
      {
        updated_at: '2026-06-12T10:00:00Z',
        pinned: true,
        pinned_at: '2026-06-12T09:00:00Z',
      },
      {
        updated_at: '2026-06-11T10:00:00Z',
        pinned: false,
        pinned_at: null,
      },
    ])

    expect(layout.pinned).toHaveLength(1)
    expect(layout.groups).toHaveLength(1)
    expect(layout.groups[0].items).toHaveLength(1)
  })

  it('sorts pinned sessions by pinned_at, falling back to updated_at when null', () => {
    const layout = groupSessionsForSidebar([
      {
        updated_at: '2026-06-10T10:00:00Z',
        pinned: true,
        pinned_at: null, // falls back to updated_at for sort
      },
      {
        updated_at: '2026-06-12T10:00:00Z',
        pinned: true,
        pinned_at: '2026-06-12T08:00:00Z',
      },
    ])

    expect(layout.pinned).toHaveLength(2)
    // Most recently pinned should come first (2026-06-12 > 2026-06-10)
    expect(layout.pinned[0].updated_at).toBe('2026-06-12T10:00:00Z')
  })

  it('truncates long strings', () => {
    expect(truncate('abcdef', 10)).toBe('abcdef')
    expect(truncate('abcdefghijklmnop', 10)).toBe('abcdefg...')
  })

  it('generates ids', () => {
    vi.stubGlobal('crypto', { randomUUID: () => 'uuid-test' })
    expect(generateId()).toBe('uuid-test')
    vi.unstubAllGlobals()
  })
})
