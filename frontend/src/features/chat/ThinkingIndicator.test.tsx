import { render, screen } from '@testing-library/react'
import { expect, it } from 'vitest'

import { ThinkingIndicator } from './ThinkingIndicator'

it('renders the thinking state with mode label', () => {
  render(<ThinkingIndicator modeLabel="Equilibrado" />)

  expect(screen.getByLabelText('Assistente pensando')).toBeInTheDocument()
  expect(screen.getByText('MindSight AI')).toBeInTheDocument()
  expect(screen.getByText('Equilibrado')).toBeInTheDocument()
  expect(screen.getByText(/Pensando/)).toBeInTheDocument()
})
