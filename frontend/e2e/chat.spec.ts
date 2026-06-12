import { expect, test } from '@playwright/test'

test.beforeEach(async ({ page }) => {
  await page.route('**/api/v1/books**', async route => {
    if (route.request().method() === 'GET') {
      await route.fulfill({
        json: [
          {
            id: 'book_1',
            title: 'Python Fluente',
            category: 'Programação',
            author: 'Luciano Ramalho',
            publication_date: '2015-01-01',
            publication_year: 2015,
            summary: 'Livro avançado sobre Python idiomático.',
          },
        ],
      })
      return
    }

    await route.fulfill({
      status: 201,
      json: {
        id: 'book_2',
        title: 'Novo livro',
        category: 'Programação',
        author: 'Autora',
        publication_date: '2024-01-01',
        publication_year: 2024,
        summary: 'Resumo.',
      },
    })
  })

  await page.route('**/api/v1/chat/sessions', async route => {
    if (route.request().method() === 'GET') {
      await route.fulfill({
        json: [
          {
            id: 'session_1',
            title: 'Como criar listas em Python',
            created_at: '2026-06-11T14:21:00Z',
            updated_at: '2026-06-11T14:25:00Z',
          },
        ],
      })
      return
    }

    await route.fulfill({
      status: 201,
      json: {
        id: 'session_new',
        title: 'Nova conversa',
        created_at: '2026-06-11T14:21:00Z',
        updated_at: '2026-06-11T14:21:00Z',
      },
    })
  })

  await page.route('**/api/v1/chat/sessions/session_1/messages', async route => {
    await route.fulfill({
      json: [
        {
          id: 'msg_1',
          session_id: 'session_1',
          role: 'assistant',
          content: 'Em Python, listas usam colchetes: `items = [1, 2, 3]`.',
          thinking_mode: 'balanced',
          status: 'completed',
          attachments: [],
          created_at: '2026-06-11T14:21:05Z',
        },
      ],
    })
  })
})

test('loads chat shell and supports theme/thinking controls', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByText('MindSight AI')).toBeVisible()
  await expect(page.getByPlaceholder('Pergunte alguma coisa')).toBeVisible()

  await page.getByLabel('Alternar tema').click()
  await expect(page.locator('html')).toHaveClass(/dark/)

  await page.getByLabel(/Thinking/i).selectOption('deep')
  await expect(page.getByLabel(/Thinking/i)).toHaveValue('deep')
})

test('mobile shell opens sidebar drawer', async ({ page, isMobile }) => {
  test.skip(!isMobile, 'mobile-only assertion')

  await page.goto('/')
  await page.getByLabel('Abrir menu').click()

  await expect(page.getByRole('button', { name: 'Novo chat' })).toBeVisible()
})

test('opens the book administration screen', async ({ page, isMobile }) => {
  await page.goto('/')

  if (isMobile) {
    await page.getByLabel('Abrir menu').click()
  }
  await page.getByRole('button', { name: 'Biblioteca' }).click()

  await expect(page.getByText('Administração')).toBeVisible()
  await expect(page.getByLabel('Upload de livro')).toBeVisible()
  await expect(page.getByText('Python Fluente')).toBeVisible()
})
