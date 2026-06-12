import type { Meta, StoryObj } from '@storybook/react-vite'
import { Paperclip, SendHorizontal } from 'lucide-react'
import { Button } from './button'

const meta = {
  title: 'UI/Button',
  component: Button,
} satisfies Meta<typeof Button>

export default meta

type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    children: 'Cadastrar livro',
  },
}

export const Soft: Story = {
  args: {
    variant: 'soft',
    children: 'Perguntar à IA',
  },
}

export const Icon: Story = {
  args: {
    size: 'icon',
    'aria-label': 'Enviar',
    children: <SendHorizontal size={18} />,
  },
}

export const Attachment: Story = {
  args: {
    variant: 'soft',
    size: 'icon',
    'aria-label': 'Anexar',
    children: <Paperclip size={18} />,
  },
}
