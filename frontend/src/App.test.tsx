import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { fireEvent, render, screen } from '@testing-library/react'
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
