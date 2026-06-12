import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { beforeEach, expect, it, vi } from 'vitest'
import App from './App'

function renderApp() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  })

  return render(
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>,
  )
}

beforeEach(() => {
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string) => {
      if (url.includes('/books')) {
        return Response.json([])
      }
      if (url.includes('/chat/sessions')) {
        return Response.json([])
      }
      return Response.json([])
    }),
  )
})

it('renders the chat shell and composer', async () => {
  renderApp()

  expect(await screen.findByText('MindSight AI')).toBeInTheDocument()
  expect(screen.getByPlaceholderText('Pergunte alguma coisa')).toBeInTheDocument()
  expect(screen.getByLabelText('Anexar arquivo')).toBeInTheDocument()
})

it('renders the book administration screen', async () => {
  renderApp()

  fireEvent.click(await screen.findByRole('button', { name: 'Biblioteca' }))

  expect(await screen.findByText('Administração')).toBeInTheDocument()
  expect(screen.getByLabelText('Upload de livro')).toBeInTheDocument()
  expect(screen.getByLabelText('Buscar livros')).toBeInTheDocument()
})

it('reuses the same session when a failed send is retried', async () => {
  let createSessionCalls = 0
  let messageAttempts = 0

  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string, init?: RequestInit) => {
      const method = init?.method ?? 'GET'
      if (url.includes('/chat/sessions') && method === 'POST') {
        createSessionCalls += 1
        return Response.json({
          id: 'session_fixed',
          title: 'Conversa',
          created_at: '2026-06-11T00:00:00Z',
          updated_at: '2026-06-11T00:00:00Z',
        })
      }
      if (url.includes('/chat/messages') && method === 'POST') {
        messageAttempts += 1
        if (messageAttempts === 1) {
          return new Response(
            JSON.stringify({ error: { message: 'Falha temporária' } }),
            { status: 500 },
          )
        }
        return Response.json({
          user_message_id: 'msg_user',
          assistant_message_id: 'msg_assistant',
          status: 'completed',
          assistant_message: {
            id: 'msg_assistant',
            session_id: 'session_fixed',
            role: 'assistant',
            content: 'ok',
            thinking_mode: 'balanced',
            status: 'completed',
            trace_id: null,
            attachments: [],
            created_at: '2026-06-11T00:00:00Z',
          },
        })
      }
      return Response.json([])
    }),
  )

  renderApp()

  const composer = await screen.findByPlaceholderText('Pergunte alguma coisa')
  fireEvent.change(composer, { target: { value: 'primeira pergunta' } })
  fireEvent.click(screen.getByLabelText('Enviar mensagem'))

  await waitFor(() => expect(messageAttempts).toBe(1))

  fireEvent.change(composer, { target: { value: 'primeira pergunta' } })
  fireEvent.click(screen.getByLabelText('Enviar mensagem'))

  await waitFor(() => expect(messageAttempts).toBe(2))
  expect(createSessionCalls).toBe(1)
})
