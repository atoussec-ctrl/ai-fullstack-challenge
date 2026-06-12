import { fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import AssistantMarkdown from './AssistantMarkdown'

describe('AssistantMarkdown', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('renders inline and fenced markdown', async () => {
    render(
      <AssistantMarkdown content={'Texto **negrito**\n\n```python\nprint("oi")\n```'} />,
    )

    expect(screen.getByText('negrito')).toBeInTheDocument()
    expect(await screen.findByText('python')).toBeInTheDocument()
    expect(screen.getByText(/print/)).toBeInTheDocument()
  })

  it('renders inline code without a copy button', () => {
    render(<AssistantMarkdown content={'Use `const x = 1` inline.'} />)

    // No copy button for inline code — only fenced blocks get CodeBlock
    expect(screen.queryByRole('button', { name: 'Copiar' })).not.toBeInTheDocument()
    expect(screen.getByText(/const x = 1/)).toBeInTheDocument()
  })

  it('copies fenced code block content via clipboard API', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined)
    vi.stubGlobal('navigator', { clipboard: { writeText } })

    render(<AssistantMarkdown content={'```js\nconst x = 1\n```'} />)

    fireEvent.click(await screen.findByRole('button', { name: 'Copiar' }))
    expect(writeText).toHaveBeenCalledWith('const x = 1')
    expect(await screen.findByRole('button', { name: 'Copiado!' })).toBeInTheDocument()
  })

  it('falls back to execCommand when clipboard API is unavailable', async () => {
    // Remove clipboard API to force execCommand fallback path
    vi.stubGlobal('navigator', { clipboard: undefined })

    // jsdom doesn't define execCommand — define it so we can spy on it
    const execCommand = vi.fn().mockReturnValue(true)
    Object.defineProperty(document, 'execCommand', {
      value: execCommand,
      writable: true,
      configurable: true,
    })

    render(<AssistantMarkdown content={'```sh\necho hello\n```'} />)

    fireEvent.click(await screen.findByRole('button', { name: 'Copiar' }))

    // Wait for async copy to complete and button to switch to "Copiado!"
    await screen.findByRole('button', { name: 'Copiado!' })

    expect(execCommand).toHaveBeenCalledWith('copy')

    // Cleanup
    Object.defineProperty(document, 'execCommand', {
      value: undefined,
      writable: true,
      configurable: true,
    })
  })

  it('shows plain text content without any markdown', () => {
    render(<AssistantMarkdown content={'Simples texto sem formatação.'} />)
    expect(screen.getByText('Simples texto sem formatação.')).toBeInTheDocument()
  })
})

