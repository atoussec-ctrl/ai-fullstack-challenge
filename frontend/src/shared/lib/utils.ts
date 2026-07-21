import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`
}

export function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffSec = Math.floor(diffMs / 1000)
  const diffMin = Math.floor(diffSec / 60)
  const diffHour = Math.floor(diffMin / 60)
  const diffDay = Math.floor(diffHour / 24)

  if (diffSec < 60) return 'just now'
  if (diffMin < 60) return `${diffMin}m ago`
  if (diffHour < 24) return `${diffHour}h ago`
  if (diffDay < 7) return `${diffDay}d ago`
  return date.toLocaleDateString()
}

export function groupSessionsByDate<T extends { updated_at: string }>(
  sessions: T[]
): { label: string; items: T[] }[] {
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const yesterday = new Date(today.getTime() - 86400000)
  const weekAgo = new Date(today.getTime() - 7 * 86400000)
  const monthAgo = new Date(today.getTime() - 30 * 86400000)

  const groups: { label: string; items: T[] }[] = [
    { label: 'Today', items: [] },
    { label: 'Yesterday', items: [] },
    { label: 'Previous 7 Days', items: [] },
    { label: 'Previous 30 Days', items: [] },
    { label: 'Older', items: [] },
  ]

  for (const session of sessions) {
    const date = new Date(session.updated_at)
    if (date >= today) {
      groups[0].items.push(session)
    } else if (date >= yesterday) {
      groups[1].items.push(session)
    } else if (date >= weekAgo) {
      groups[2].items.push(session)
    } else if (date >= monthAgo) {
      groups[3].items.push(session)
    } else {
      groups[4].items.push(session)
    }
  }

  return groups.filter(g => g.items.length > 0)
}

export function groupSessionsForSidebar<
  T extends { updated_at: string; pinned: boolean; pinned_at?: string | null },
>(sessions: T[]): { pinned: T[]; groups: { label: string; items: T[] }[] } {
  const pinned = sessions
    .filter(session => session.pinned)
    .sort(
      (left, right) =>
        new Date(right.pinned_at ?? right.updated_at).getTime() -
        new Date(left.pinned_at ?? left.updated_at).getTime(),
    )

  const groups = groupSessionsByDate(sessions.filter(session => !session.pinned))

  return { pinned, groups }
}

export function filterSessionsByQuery<T extends { title: string }>(
  sessions: T[],
  query: string,
): T[] {
  const normalized = query.trim().toLowerCase()
  if (!normalized) return sessions
  return sessions.filter(session => session.title.toLowerCase().includes(normalized))
}

export function generateId(): string {
  return crypto.randomUUID()
}

export function truncate(str: string, maxLength: number): string {
  if (str.length <= maxLength) return str
  return str.slice(0, maxLength - 3) + '...'
}
