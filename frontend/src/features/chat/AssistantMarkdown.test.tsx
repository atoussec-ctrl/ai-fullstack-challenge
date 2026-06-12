import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import AssistantMarkdown from './AssistantMarkdown'

describe('AssistantMarkdown', () => {
  it('renders inline and fenced markdown', async () => {
    render(
      <AssistantMarkdown content={'Texto **negrito**\n\n```python\nprint("oi")\n```'} />,
    )

    expect(screen.getByText('negrito')).toBeInTheDocument()
    expect(await screen.findByText('python')).toBeInTheDocument()
    expect(screen.getByText(/print/)).toBeInTheDocument()
  })

  it('copies fenced code block content', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined)
    vi.stubGlobal('navigator', { clipboard: { writeText } })

    render(<AssistantMarkdown content={'```js\nconst x = 1\n```'} />)

    fireEvent.click(await screen.findByRole('button', { name: 'Copiar' }))
    expect(writeText).toHaveBeenCalledWith('const x = 1')

    vi.unstubAllGlobals()
  })
})
