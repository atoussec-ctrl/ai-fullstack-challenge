import type {
  Attachment,
  AttachmentKind,
  Book,
  ChatMessage,
  ChatSession,
  CreateBookInput,
  ImportBookResponse,
  SemanticSearchResult,
  SendMessageInput,
  SendMessageResponse,
} from './types'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:5000/api/v1'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      ...(init?.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
      ...init?.headers,
    },
  })

  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    const message = payload?.error?.message ?? 'Falha ao comunicar com a API.'
    throw new Error(message)
  }

  return response.json() as Promise<T>
}

export function listSessions() {
  return request<ChatSession[]>('/chat/sessions')
}

export function listBooks(
  filters: { q?: string; title?: string; author?: string; category?: string } = {},
) {
  const params = new URLSearchParams()
  for (const [key, value] of Object.entries(filters)) {
    if (value?.trim()) {
      params.set(key, value.trim())
    }
  }
  const query = params.toString()
  return request<Book[]>(`/books${query ? `?${query}` : ''}`)
}

export function createBook(input: CreateBookInput) {
  return request<Book>('/books', {
    method: 'POST',
    body: JSON.stringify(input),
  })
}

export function importBook(file: File) {
  const formData = new FormData()
  formData.set('file', file)

  return request<ImportBookResponse>('/books/import', {
    method: 'POST',
    body: formData,
  })
}

export function createSession(title = 'Nova conversa') {
  return request<ChatSession>('/chat/sessions', {
    method: 'POST',
    body: JSON.stringify({ title }),
  })
}

export async function deleteSession(sessionId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/chat/sessions/${sessionId}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    const message = payload?.error?.message ?? 'Falha ao excluir a conversa.'
    throw new Error(message)
  }
}

export function listMessages(sessionId: string) {
  return request<ChatMessage[]>(`/chat/sessions/${sessionId}/messages`)
}

export function sendMessage(input: SendMessageInput) {
  return request<SendMessageResponse>('/chat/messages', {
    method: 'POST',
    body: JSON.stringify(input),
  })
}

export function uploadAttachment(
  sessionId: string,
  file: File,
  kind: AttachmentKind,
) {
  const formData = new FormData()
  formData.set('session_id', sessionId)
  formData.set('kind', kind)
  formData.set('file', file)

  return request<Attachment>('/attachments', {
    method: 'POST',
    body: formData,
  })
}

export function semanticSearch(query: string, k = 3) {
  return request<{ results: SemanticSearchResult[] }>('/semantic-search', {
    method: 'POST',
    body: JSON.stringify({ query, k }),
  })
}
