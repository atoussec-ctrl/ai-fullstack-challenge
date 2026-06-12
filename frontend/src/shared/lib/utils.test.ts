import { describe, expect, it, vi } from 'vitest'

import {
  formatFileSize,
  formatRelativeTime,
  generateId,
  groupSessionsByDate,
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
    expect(formatRelativeTime('2026-04-01T12:00:00Z')).not.toBe('2d ago')

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
