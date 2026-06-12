import type { Meta, StoryObj } from '@storybook/react-vite'
import App from './App'

const meta = {
  title: 'MindSight/App',
  component: App,
  parameters: {
    docs: {
      description: {
        component:
          'Aplicação principal com chat, biblioteca, upload de livros, áudio, anexos e tema claro/escuro.',
      },
    },
  },
} satisfies Meta<typeof App>

export default meta

type Story = StoryObj<typeof meta>

export const Shell: Story = {}
