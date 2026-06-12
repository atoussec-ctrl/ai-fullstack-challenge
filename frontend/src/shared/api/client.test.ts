import { afterEach, describe, expect, it, vi } from 'vitest'

import {
  createBook,
  createSession,
  deleteSession,
  listBooks,
  listMessages,
  listSessions,
  sendMessage,
  updateSessionPin,
} from './client'

describe('chat session client', () => {
  it('lists sessions from API', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        Response.json([
          {
            id: 'session_1',
            title: 'Conversa',
            pinned: false,
            pinned_at: null,
            created_at: '2026-06-12T00:00:00Z',
            updated_at: '2026-06-12T01:00:00Z',
          },
        ]),
      ),
    )

    const sessions = await listSessions()
    expect(sessions).toHaveLength(1)
    expect(sessions[0].title).toBe('Conversa')
  })

  it('lists messages for a session', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        Response.json([
          {
            id: 'msg_1',
            session_id: 'session_1',
            role: 'user',
            content: 'Pergunta',
            created_at: '2026-06-12T00:00:00Z',
          },
        ]),
      ),
    )

    const messages = await listMessages('session_1')
    expect(messages[0].content).toBe('Pergunta')
  })

  it('creates a book', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        Response.json({
          id: 'book_1',
          title: 'Clean Code',
          author: 'Robert Martin',
          category: 'tech',
          publication_date: '2008-01-01',
          publication_year: 2008,
          summary: 'Princípios de código limpo.',
          created_at: '2026-06-12T00:00:00Z',
        }),
      ),
    )

    const book = await createBook({
      title: 'Clean Code',
      author: 'Robert Martin',
      category: 'tech',
      publication_year: '2008',
      summary: 'Princípios de código limpo.',
    })

    expect(book.id).toBe('book_1')
  })

  it('lists books with optional filters', async () => {
    const fetchMock = vi.fn(async () => Response.json([]))
    vi.stubGlobal('fetch', fetchMock)

    await listBooks({ q: 'python', category: 'tech' })

    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining('/books?q=python&category=tech'),
      expect.any(Object),
    )
  })

  it('sends a chat message', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        Response.json({
          user_message_id: 'msg_user',
          assistant_message_id: 'msg_1',
          status: 'completed',
          assistant_message: {
            id: 'msg_1',
            session_id: 'session_1',
            role: 'assistant',
            content: 'Olá',
            status: 'completed',
            attachments: [],
            created_at: '2026-06-12T00:00:00Z',
          },
        }),
      ),
    )

    const response = await sendMessage({
      session_id: 'session_1',
      content: 'Oi',
      thinking_mode: 'balanced',
    })

    expect(response.assistant_message.content).toBe('Olá')
  })

  it('creates a session with default title', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        Response.json({
          id: 'session_new',
          title: 'Nova conversa',
          pinned: false,
          pinned_at: null,
          created_at: '2026-06-12T00:00:00Z',
          updated_at: '2026-06-12T00:00:00Z',
        }),
      ),
    )

    const session = await createSession()
    expect(session.id).toBe('session_new')
  })
})

describe('deleteSession', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('resolves when API returns 204', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => new Response(null, { status: 204 })),
    )

    await expect(deleteSession('session_1')).resolves.toBeUndefined()
  })

  it('throws API error message when delete fails', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        Response.json(
          { error: { message: 'Conversa não encontrada.' } },
          { status: 404 },
        ),
      ),
    )

    await expect(deleteSession('missing')).rejects.toThrow('Conversa não encontrada.')
  })
})

describe('updateSessionPin', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('patches pinned state on the session', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        Response.json({
          id: 'session_1',
          title: 'Conversa',
          pinned: true,
          pinned_at: '2026-06-12T02:00:00Z',
          created_at: '2026-06-12T00:00:00Z',
          updated_at: '2026-06-12T02:00:00Z',
        }),
      ),
    )

    const session = await updateSessionPin('session_1', true)
    expect(session.pinned).toBe(true)
  })
})
