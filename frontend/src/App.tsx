import { Suspense, lazy, useEffect, useMemo, useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import {
  BookOpen,
  Bot,
  Calendar,
  ChevronDown,
  FileAudio,
  FileCode2,
  FileText,
  ImageIcon,
  Menu,
  Mic,
  Moon,
  PanelLeftClose,
  Paperclip,
  Plus,
  Search,
  SendHorizontal,
  Settings2,
  Sparkles,
  Square,
  Sun,
  UserRound,
  X,
} from 'lucide-react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import {
  type PendingAttachment,
  revokePendingAttachment,
  validateFiles,
} from '@/features/chat/attachments'
import { useAudioRecorder } from '@/features/chat/useAudioRecorder'
import {
  createBook,
  createSession,
  importBook,
  listBooks,
  listMessages,
  listSessions,
  sendMessage,
  uploadAttachment,
} from '@/shared/api/client'
import type {
  AttachmentKind,
  Book,
  ChatMessage,
  ChatSession,
  CreateBookInput,
  ThinkingMode,
} from '@/shared/api/types'
import { cn, formatFileSize, formatRelativeTime, groupSessionsByDate } from '@/shared/lib/utils'

const MODEL_OPTIONS = ['gpt-4.1-mini', 'gpt-4.1', 'gpt-5-mini', 'gpt-5'] as const

const THINKING_OPTIONS: Array<{
  value: ThinkingMode
  label: string
  detail: string
}> = [
  { value: 'fast', label: 'Rápido', detail: 'direto' },
  { value: 'balanced', label: 'Equilibrado', detail: 'exemplos' },
  { value: 'deep', label: 'Profundo', detail: 'trade-offs' },
]

const SUGGESTIONS = [
  'Como criar uma lista em Python?',
  'Explique fixtures do pytest com exemplo',
  'Como estruturar uma API Flask com SQLAlchemy?',
  'Revise este erro de tipagem em Python',
]

const AssistantMarkdown = lazy(() => import('@/features/chat/AssistantMarkdown'))

function App() {
  const queryClient = useQueryClient()
  const fileInputRef = useRef<HTMLInputElement | null>(null)
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null)
  const [composerValue, setComposerValue] = useState('')
  const [thinkingMode, setThinkingMode] = useState<ThinkingMode>(
    (import.meta.env.VITE_DEFAULT_THINKING_MODE as ThinkingMode) ?? 'balanced',
  )
  const [model, setModel] = useState<(typeof MODEL_OPTIONS)[number]>('gpt-4.1-mini')
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    return (localStorage.getItem('mindsight-theme') as 'light' | 'dark') ?? 'light'
  })
  const [activeView, setActiveView] = useState<'chat' | 'books'>('chat')
  const [isMobileSidebarOpen, setMobileSidebarOpen] = useState(false)
  const [pendingAttachments, setPendingAttachments] = useState<PendingAttachment[]>([])
  const pendingAttachmentsRef = useRef<PendingAttachment[]>([])
  const [uiError, setUiError] = useState<string | null>(null)
  const audioRecorder = useAudioRecorder()

  const sessionsQuery = useQuery({
    queryKey: ['sessions'],
    queryFn: listSessions,
  })

  const messagesQuery = useQuery({
    queryKey: ['messages', selectedSessionId],
    queryFn: () => listMessages(selectedSessionId as string),
    enabled: Boolean(selectedSessionId),
  })

  const sendMessageMutation = useMutation({
    mutationFn: async () => {
      const content = composerValue.trim()
      if (!content && pendingAttachments.length === 0) {
        throw new Error('Digite uma pergunta ou anexe um arquivo.')
      }

      let session = selectedSessionId
      if (!session) {
        session = (
          await createSession(content ? content.slice(0, 54) : 'Conversa com anexos')
        ).id
        // Persiste a sessão imediatamente para que um retry após falha de
        // upload/envio reuse a mesma conversa em vez de criar outra.
        setSelectedSessionId(session)
        queryClient.invalidateQueries({ queryKey: ['sessions'] })
      }

      const uploaded = []
      for (const attachment of pendingAttachments) {
        uploaded.push(
          await uploadAttachment(session, attachment.file, attachment.kind),
        )
      }

      return sendMessage({
        session_id: session,
        content,
        thinking_mode: thinkingMode,
        attachment_ids: uploaded.map(attachment => attachment.id),
        model,
      })
    },
    onSuccess: response => {
      setComposerValue('')
      pendingAttachments.forEach(revokePendingAttachment)
      setPendingAttachments([])
      setSelectedSessionId(response.assistant_message.session_id)
      setUiError(null)
      queryClient.invalidateQueries({ queryKey: ['sessions'] })
      queryClient.invalidateQueries({
        queryKey: ['messages', response.assistant_message.session_id],
      })
    },
    onError: error => {
      setUiError(error instanceof Error ? error.message : 'Falha ao enviar mensagem.')
    },
  })

  const askBookMutation = useMutation({
    mutationFn: async (book: Book) => {
      const session = await createSession(`Livro: ${book.title}`.slice(0, 64))
      return sendMessage({
        session_id: session.id,
        content: `Resuma o livro "${book.title}", cite autor, data de publicação e explique os pontos principais usando somente a biblioteca local.`,
        thinking_mode: 'deep',
        model,
      })
    },
    onSuccess: response => {
      setActiveView('chat')
      setSelectedSessionId(response.assistant_message.session_id)
      setUiError(null)
      queryClient.invalidateQueries({ queryKey: ['sessions'] })
      queryClient.invalidateQueries({
        queryKey: ['messages', response.assistant_message.session_id],
      })
    },
    onError: error => {
      setUiError(error instanceof Error ? error.message : 'Falha ao consultar a IA.')
    },
  })

  const sessions = useMemo(() => sessionsQuery.data ?? [], [sessionsQuery.data])
  const messages = messagesQuery.data ?? []
  const groupedSessions = useMemo(() => groupSessionsByDate(sessions), [sessions])
  const selectedSession = sessions.find(session => session.id === selectedSessionId)

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
    localStorage.setItem('mindsight-theme', theme)
  }, [theme])

  useEffect(() => {
    pendingAttachmentsRef.current = pendingAttachments
  }, [pendingAttachments])

  useEffect(() => {
    return () => pendingAttachmentsRef.current.forEach(revokePendingAttachment)
  }, [])

  function selectFiles(files: FileList | null) {
    if (!files) return
    const result = validateFiles(Array.from(files), pendingAttachments.length)
    setPendingAttachments(current => [...current, ...result.accepted])
    setUiError(result.errors[0] ?? null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  function removeAttachment(id: string) {
    setPendingAttachments(current => {
      const target = current.find(item => item.id === id)
      if (target) revokePendingAttachment(target)
      return current.filter(item => item.id !== id)
    })
  }

  async function toggleRecording() {
    try {
      if (audioRecorder.isRecording) {
        const file = await audioRecorder.stop()
        const result = validateFiles([file], pendingAttachments.length)
        setPendingAttachments(current => [...current, ...result.accepted])
        setUiError(result.errors[0] ?? null)
      } else {
        await audioRecorder.start()
        setUiError(null)
      }
    } catch (error) {
      setUiError(
        error instanceof Error
          ? error.message
          : 'Não foi possível acessar o microfone.',
      )
    }
  }

  function submit() {
    if (!sendMessageMutation.isPending) {
      sendMessageMutation.mutate()
    }
  }

  const sidebar = (
    <ChatSidebar
      sessions={sessions}
      groupedSessions={groupedSessions}
      selectedSessionId={selectedSessionId}
      isLoading={sessionsQuery.isLoading}
      onNewChat={() => {
        setActiveView('chat')
        setSelectedSessionId(null)
        setComposerValue('')
        setMobileSidebarOpen(false)
      }}
      activeView={activeView}
      onOpenBooks={() => {
        setActiveView('books')
        setMobileSidebarOpen(false)
      }}
      onSelectSession={sessionId => {
        setActiveView('chat')
        setSelectedSessionId(sessionId)
        setMobileSidebarOpen(false)
      }}
    />
  )

  return (
    <div className="min-h-dvh bg-background text-foreground">
      <div className="flex h-dvh overflow-hidden">
        <aside className="hidden w-[326px] shrink-0 border-r border-sidebar-border bg-sidebar text-sidebar-foreground lg:block">
          {sidebar}
        </aside>

        <AnimatePresence>
          {isMobileSidebarOpen && (
            <motion.div
              className="fixed inset-0 z-40 bg-black/45 lg:hidden"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileSidebarOpen(false)}
            >
              <motion.aside
                className="h-full w-[82vw] max-w-[326px] border-r border-sidebar-border bg-sidebar text-sidebar-foreground"
                initial={{ x: -340 }}
                animate={{ x: 0 }}
                exit={{ x: -340 }}
                transition={{ type: 'spring', damping: 28, stiffness: 260 }}
                onClick={event => event.stopPropagation()}
              >
                {sidebar}
              </motion.aside>
            </motion.div>
          )}
        </AnimatePresence>

        <main className="flex min-w-0 flex-1 flex-col bg-background">
          <ChatHeader
            title={
              activeView === 'books'
                ? 'Biblioteca de livros'
                : selectedSession?.title ?? 'MindSight AI'
            }
            model={model}
            thinkingMode={thinkingMode}
            theme={theme}
            onOpenSidebar={() => setMobileSidebarOpen(true)}
            onModelChange={setModel}
            onThinkingChange={setThinkingMode}
            onThemeToggle={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          />

          {activeView === 'books' ? (
            <BooksAdminView
              actionError={uiError}
              isAskingBook={askBookMutation.isPending}
              onAskBook={book => askBookMutation.mutate(book)}
            />
          ) : (
            <section className="relative min-h-0 flex-1">
              <div className="h-full overflow-y-auto px-4 pb-[180px] pt-8 sm:px-8">
                <div className="mx-auto flex w-full max-w-[960px] flex-col gap-8">
                  {messagesQuery.isLoading && selectedSessionId ? (
                    <MessageSkeleton />
                  ) : messages.length > 0 ? (
                    <MessageList messages={messages} />
                  ) : (
                    <EmptyState
                      onUseSuggestion={suggestion => setComposerValue(suggestion)}
                    />
                  )}
                </div>
              </div>

              <ChatComposer
                value={composerValue}
                thinkingMode={thinkingMode}
                model={model}
                attachments={pendingAttachments}
                error={uiError}
                isSending={sendMessageMutation.isPending}
                isRecording={audioRecorder.isRecording}
                onChange={setComposerValue}
                onSubmit={submit}
                onAttachClick={() => fileInputRef.current?.click()}
                onRemoveAttachment={removeAttachment}
                onToggleRecording={toggleRecording}
              />

              <input
                ref={fileInputRef}
                className="hidden"
                type="file"
                multiple
                accept=".txt,.md,.py,.json,.pdf,.png,.jpg,.jpeg,.webp,.webm,.wav,.mp3"
                onChange={event => selectFiles(event.target.files)}
              />
            </section>
          )}
        </main>
      </div>
    </div>
  )
}

interface ChatSidebarProps {
  sessions: ChatSession[]
  groupedSessions: Array<{ label: string; items: ChatSession[] }>
  selectedSessionId: string | null
  activeView: 'chat' | 'books'
  isLoading: boolean
  onNewChat: () => void
  onOpenBooks: () => void
  onSelectSession: (sessionId: string) => void
}

function ChatSidebar({
  groupedSessions,
  selectedSessionId,
  activeView,
  isLoading,
  onNewChat,
  onOpenBooks,
  onSelectSession,
}: ChatSidebarProps) {
  return (
    <div className="flex h-full flex-col">
      <div className="flex h-16 items-center justify-between px-5">
        <div className="flex items-center gap-2 text-lg font-semibold text-foreground">
          <span className="grid h-8 w-8 place-items-center rounded-md bg-primary text-primary-foreground">
            <Bot size={18} />
          </span>
          MindSight
        </div>
        <Button variant="ghost" size="icon" aria-label="Recolher sidebar">
          <PanelLeftClose size={18} />
        </Button>
      </div>

      <div className="space-y-1 px-3">
        <SidebarButton icon={<Plus size={18} />} label="Novo chat" onClick={onNewChat} />
        <SidebarButton icon={<Search size={18} />} label="Buscar chats" />
        <SidebarButton
          active={activeView === 'books'}
          icon={<BookOpen size={18} />}
          label="Biblioteca"
          onClick={onOpenBooks}
        />
        <SidebarButton icon={<Sparkles size={18} />} label="Python Assistant" />
        <SidebarButton icon={<Settings2 size={18} />} label="Configurações" />
      </div>

      <div className="mt-6 min-h-0 flex-1 overflow-y-auto px-3">
        <p className="mb-2 px-2 text-sm font-semibold text-foreground">Recentes</p>
        {isLoading ? (
          <div className="space-y-2">
            <div className="h-9 rounded-md bg-sidebar-accent" />
            <div className="h-9 rounded-md bg-sidebar-accent" />
          </div>
        ) : groupedSessions.length > 0 ? (
          groupedSessions.map(group => (
            <div className="mb-4" key={group.label}>
              <p className="mb-1 px-2 text-xs text-muted-foreground">{group.label}</p>
              {group.items.map(session => (
                <button
                  key={session.id}
                  className={cn(
                    'mb-1 flex h-9 w-full items-center justify-between rounded-md px-2 text-left text-sm text-sidebar-foreground transition hover:bg-sidebar-accent',
                    activeView === 'chat' &&
                      selectedSessionId === session.id &&
                      'bg-sidebar-accent text-sidebar-accent-foreground',
                  )}
                  onClick={() => onSelectSession(session.id)}
                >
                  <span className="min-w-0 truncate">{session.title}</span>
                  <span className="ml-2 shrink-0 text-xs text-muted-foreground">
                    {formatRelativeTime(session.updated_at)}
                  </span>
                </button>
              ))}
            </div>
          ))
        ) : (
          <p className="px-2 text-sm text-muted-foreground">Nenhuma conversa ainda.</p>
        )}
      </div>

      <div className="flex items-center gap-3 border-t border-sidebar-border p-4">
        <div className="grid h-9 w-9 place-items-center rounded-full bg-emerald-500 text-sm font-semibold text-white">
          MS
        </div>
        <div className="min-w-0">
          <p className="truncate text-sm font-medium text-foreground">Python Team</p>
          <p className="text-xs text-muted-foreground">Workspace local</p>
        </div>
      </div>
    </div>
  )
}

function SidebarButton({
  icon,
  label,
  active = false,
  onClick,
}: {
  icon: React.ReactNode
  label: string
  active?: boolean
  onClick?: () => void
}) {
  return (
    <button
      className={cn(
        'flex h-10 w-full items-center gap-3 rounded-md px-2 text-sm text-sidebar-foreground transition hover:bg-sidebar-accent hover:text-sidebar-accent-foreground',
        active && 'bg-sidebar-accent text-sidebar-accent-foreground',
      )}
      onClick={onClick}
    >
      {icon}
      <span>{label}</span>
    </button>
  )
}

function BooksAdminView({
  actionError,
  isAskingBook,
  onAskBook,
}: {
  actionError: string | null
  isAskingBook: boolean
  onAskBook: (book: Book) => void
}) {
  const queryClient = useQueryClient()
  const importInputRef = useRef<HTMLInputElement | null>(null)
  const [search, setSearch] = useState('')
  const [form, setForm] = useState<CreateBookInput>({
    title: '',
    category: 'Programação',
    author: '',
    publication_year: '',
    summary: '',
  })
  const [importedBookTitle, setImportedBookTitle] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const booksQuery = useQuery({
    queryKey: ['books', search],
    queryFn: () => listBooks({ q: search }),
  })

  const createBookMutation = useMutation({
    mutationFn: createBook,
    onSuccess: () => {
      setForm({
        title: '',
        category: 'Programação',
        author: '',
        publication_year: '',
        summary: '',
      })
      setError(null)
      queryClient.invalidateQueries({ queryKey: ['books'] })
    },
    onError: mutationError => {
      setError(
        mutationError instanceof Error
          ? mutationError.message
          : 'Falha ao cadastrar livro.',
      )
    },
  })

  const importBookMutation = useMutation({
    mutationFn: importBook,
    onSuccess: response => {
      setImportedBookTitle(response.book.title)
      setError(null)
      queryClient.invalidateQueries({ queryKey: ['books'] })
      if (importInputRef.current) {
        importInputRef.current.value = ''
      }
    },
    onError: mutationError => {
      setImportedBookTitle(null)
      setError(
        mutationError instanceof Error
          ? mutationError.message
          : 'Falha ao importar livro.',
      )
    },
  })

  function updateForm(field: keyof CreateBookInput, value: string) {
    setForm(current => ({ ...current, [field]: value }))
  }

  function submitBook(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    createBookMutation.mutate(form)
  }

  const books = booksQuery.data ?? []

  return (
    <section className="min-h-0 flex-1 overflow-y-auto px-4 py-6 sm:px-8">
      <div className="mx-auto grid w-full max-w-6xl gap-6 xl:grid-cols-[380px_1fr]">
        <form
          className="h-fit rounded-lg border border-border bg-card p-4 shadow-sm"
          onSubmit={submitBook}
        >
          <div className="mb-4">
            <h2 className="text-base font-semibold">Administração</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Cadastre livros manualmente ou importe um arquivo com metadados.
            </p>
          </div>

          {actionError && (
            <div
              className="mb-4 rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive"
              role="alert"
            >
              {actionError}
            </div>
          )}

          <div className="mb-5 rounded-md border border-border bg-secondary/45 p-3">
            <p className="text-sm font-medium">Importar livro com IA</p>
            <p className="mt-1 text-xs leading-5 text-muted-foreground">
              Envie `.txt`, `.md`, `.json` ou `.pdf` contendo título, autor, categoria,
              ano e resumo. O backend extrai e cadastra o livro automaticamente.
            </p>
            <div className="mt-3 flex gap-2">
              <input
                ref={importInputRef}
                aria-label="Upload de livro"
                className="min-w-0 flex-1 rounded-md border border-border bg-background px-3 py-2 text-sm"
                type="file"
                accept=".txt,.md,.json,.pdf"
                onChange={event => {
                  const file = event.target.files?.[0]
                  if (file) importBookMutation.mutate(file)
                }}
              />
            </div>
            {importBookMutation.isPending && (
              <p className="mt-2 text-xs text-muted-foreground">Extraindo metadados...</p>
            )}
            {importedBookTitle && (
              <p className="mt-2 text-xs text-emerald-600">
                Livro importado: {importedBookTitle}
              </p>
            )}
          </div>

          <label className="mb-3 block">
            <span className="mb-1 block text-sm font-medium">Título</span>
            <input
              className="h-10 w-full rounded-md border border-border bg-background px-3 text-sm outline-none focus:ring-2 focus:ring-ring"
              value={form.title}
              onChange={event => updateForm('title', event.target.value)}
              placeholder="Python Fluente"
            />
          </label>

          <label className="mb-3 block">
            <span className="mb-1 block text-sm font-medium">Categoria</span>
            <input
              className="h-10 w-full rounded-md border border-border bg-background px-3 text-sm outline-none focus:ring-2 focus:ring-ring"
              value={form.category}
              onChange={event => updateForm('category', event.target.value)}
              placeholder="Programação"
            />
          </label>

          <label className="mb-3 block">
            <span className="mb-1 block text-sm font-medium">Autor</span>
            <input
              className="h-10 w-full rounded-md border border-border bg-background px-3 text-sm outline-none focus:ring-2 focus:ring-ring"
              value={form.author}
              onChange={event => updateForm('author', event.target.value)}
              placeholder="Luciano Ramalho"
            />
          </label>

          <label className="mb-3 block">
            <span className="mb-1 block text-sm font-medium">Ano de publicação</span>
            <input
              className="h-10 w-full rounded-md border border-border bg-background px-3 text-sm outline-none focus:ring-2 focus:ring-ring"
              value={form.publication_year}
              onChange={event => updateForm('publication_year', event.target.value)}
              inputMode="numeric"
              placeholder="2015"
            />
          </label>

          <label className="mb-4 block">
            <span className="mb-1 block text-sm font-medium">Resumo</span>
            <Textarea
              className="min-h-28 rounded-md border border-border bg-background px-3 py-2 text-sm focus:ring-2 focus:ring-ring"
              value={form.summary}
              onChange={event => updateForm('summary', event.target.value)}
              placeholder="Descreva o conteúdo do livro para a IA usar como fonte."
            />
          </label>

          {error && (
            <div
              className="mb-3 rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive"
              role="alert"
            >
              {error}
            </div>
          )}

          <Button className="w-full" disabled={createBookMutation.isPending}>
            {createBookMutation.isPending ? 'Salvando...' : 'Cadastrar livro'}
          </Button>
        </form>

        <div className="min-w-0">
          <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-base font-semibold">Consulta de livros</h2>
              <p className="mt-1 text-sm text-muted-foreground">
                Busque por título, autor ou termos do resumo. A IA usa esses registros
                como contexto local.
              </p>
            </div>
            <label className="relative block sm:w-[320px]">
              <Search
                className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground"
                size={17}
              />
              <input
                aria-label="Buscar livros"
                className="h-10 w-full rounded-md border border-border bg-background pl-9 pr-3 text-sm outline-none focus:ring-2 focus:ring-ring"
                value={search}
                onChange={event => setSearch(event.target.value)}
                placeholder="Buscar livros"
              />
            </label>
          </div>

          {booksQuery.isLoading ? (
            <div className="space-y-3">
              <div className="h-28 rounded-lg bg-secondary animate-shimmer" />
              <div className="h-28 rounded-lg bg-secondary animate-shimmer" />
            </div>
          ) : books.length > 0 ? (
            <div className="grid gap-3">
              {books.map(book => (
                <BookCard
                  key={book.id}
                  book={book}
                  isAskingBook={isAskingBook}
                  onAskBook={() => onAskBook(book)}
                />
              ))}
            </div>
          ) : (
            <div className="rounded-lg border border-dashed border-border p-8 text-center">
              <BookOpen className="mx-auto mb-3 text-muted-foreground" size={28} />
              <p className="font-medium">Nenhum livro encontrado</p>
              <p className="mt-1 text-sm text-muted-foreground">
                Cadastre um livro ou ajuste a busca.
              </p>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}

function BookCard({
  book,
  isAskingBook,
  onAskBook,
}: {
  book: Book
  isAskingBook: boolean
  onAskBook: () => void
}) {
  return (
    <article className="rounded-lg border border-border bg-card p-4 shadow-sm">
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div className="min-w-0">
          <h3 className="text-lg font-semibold">{book.title}</h3>
          <div className="mt-2 flex flex-wrap gap-2 text-sm text-muted-foreground">
            <span className="inline-flex items-center gap-1">
              <UserRound size={15} />
              {book.author}
            </span>
            <span>{book.category}</span>
            <span className="inline-flex items-center gap-1">
              <Calendar size={15} />
              {book.publication_year}
            </span>
          </div>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">{book.summary}</p>
        </div>
        <Button
          className="md:w-[170px]"
          disabled={isAskingBook}
          variant="soft"
          onClick={onAskBook}
        >
          <Sparkles size={16} />
          Perguntar à IA
        </Button>
      </div>
    </article>
  )
}

interface ChatHeaderProps {
  title: string
  model: string
  thinkingMode: ThinkingMode
  theme: 'light' | 'dark'
  onOpenSidebar: () => void
  onModelChange: (model: (typeof MODEL_OPTIONS)[number]) => void
  onThinkingChange: (mode: ThinkingMode) => void
  onThemeToggle: () => void
}

function ChatHeader({
  title,
  model,
  thinkingMode,
  theme,
  onOpenSidebar,
  onModelChange,
  onThinkingChange,
  onThemeToggle,
}: ChatHeaderProps) {
  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-border px-3 sm:px-5">
      <div className="flex min-w-0 items-center gap-2">
        <Button
          variant="ghost"
          size="icon"
          className="lg:hidden"
          aria-label="Abrir menu"
          onClick={onOpenSidebar}
        >
          <Menu size={20} />
        </Button>
        <div className="min-w-0">
          <h1 className="truncate text-base font-semibold">{title}</h1>
          <p className="hidden text-xs text-muted-foreground sm:block">
            Assistente para Python, Flask, testes e arquitetura
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <label className="hidden items-center gap-2 rounded-md border border-border px-2 py-1.5 text-sm sm:flex">
          <span className="text-muted-foreground">Modelo</span>
          <select
            className="bg-transparent outline-none"
            value={model}
            onChange={event =>
              onModelChange(event.target.value as (typeof MODEL_OPTIONS)[number])
            }
          >
            {MODEL_OPTIONS.map(option => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          <ChevronDown size={14} />
        </label>

        <label className="flex items-center gap-2 rounded-md border border-border px-2 py-1.5 text-sm">
          <span className="hidden text-muted-foreground sm:inline">Thinking</span>
          <select
            className="bg-transparent outline-none"
            value={thinkingMode}
            onChange={event => onThinkingChange(event.target.value as ThinkingMode)}
          >
            {THINKING_OPTIONS.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <Button
          variant="ghost"
          size="icon"
          aria-label="Alternar tema"
          onClick={onThemeToggle}
        >
          {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
        </Button>
      </div>
    </header>
  )
}

function EmptyState({ onUseSuggestion }: { onUseSuggestion: (value: string) => void }) {
  return (
    <motion.div
      className="mx-auto flex min-h-[56vh] max-w-3xl flex-col items-center justify-center text-center"
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="mb-5 grid h-14 w-14 place-items-center rounded-xl border border-border bg-secondary">
        <Sparkles size={24} />
      </div>
      <h2 className="text-2xl font-semibold sm:text-3xl">Como posso ajudar com Python?</h2>
      <p className="mt-3 max-w-xl text-sm leading-6 text-muted-foreground sm:text-base">
        Envie uma pergunta, erro, arquivo de código, imagem ou áudio. O assistente
        responde em português com foco em boas práticas.
      </p>
      <div className="mt-8 grid w-full gap-3 sm:grid-cols-2">
        {SUGGESTIONS.map(suggestion => (
          <button
            key={suggestion}
            className="rounded-lg border border-border bg-card px-4 py-3 text-left text-sm transition hover:bg-accent"
            onClick={() => onUseSuggestion(suggestion)}
          >
            {suggestion}
          </button>
        ))}
      </div>
    </motion.div>
  )
}

function MessageList({ messages }: { messages: ChatMessage[] }) {
  return (
    <div className="space-y-8" aria-live="polite">
      {messages.map(message => (
        <motion.article
          key={message.id}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.18 }}
        >
          <MessageBubble message={message} />
        </motion.article>
      ))}
    </div>
  )
}

function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === 'user'
  return (
    <div className={cn('flex w-full', isUser ? 'justify-end' : 'justify-start')}>
      <div
        className={cn(
          'group relative max-w-[860px]',
          isUser
            ? 'rounded-2xl bg-secondary px-5 py-4 text-secondary-foreground sm:max-w-[72%]'
            : 'w-full text-foreground',
        )}
      >
        {!isUser && (
          <div className="mb-3 flex items-center gap-2 text-sm font-medium">
            <span className="grid h-7 w-7 place-items-center rounded-md bg-primary text-primary-foreground">
              <Bot size={16} />
            </span>
            MindSight AI
            {message.thinking_mode && (
              <Badge>{THINKING_OPTIONS.find(item => item.value === message.thinking_mode)?.label}</Badge>
            )}
          </div>
        )}

        {message.attachments.length > 0 && (
          <div className="mb-3 flex flex-wrap gap-2">
            {message.attachments.map(attachment => (
              <Badge key={attachment.id}>{attachment.filename}</Badge>
            ))}
          </div>
        )}

        <div className={cn(!isUser && 'prose-chat max-w-none')}>
          {isUser ? (
            <p className="whitespace-pre-wrap text-base leading-7">{message.content}</p>
          ) : (
            <Suspense
              fallback={
                <p className="text-sm text-muted-foreground">Carregando resposta...</p>
              }
            >
              <AssistantMarkdown content={message.content} />
            </Suspense>
          )}
        </div>
      </div>
    </div>
  )
}

interface ChatComposerProps {
  value: string
  thinkingMode: ThinkingMode
  model: string
  attachments: PendingAttachment[]
  error: string | null
  isSending: boolean
  isRecording: boolean
  onChange: (value: string) => void
  onSubmit: () => void
  onAttachClick: () => void
  onRemoveAttachment: (id: string) => void
  onToggleRecording: () => void
}

function ChatComposer({
  value,
  thinkingMode,
  model,
  attachments,
  error,
  isSending,
  isRecording,
  onChange,
  onSubmit,
  onAttachClick,
  onRemoveAttachment,
  onToggleRecording,
}: ChatComposerProps) {
  const activeThinking = THINKING_OPTIONS.find(item => item.value === thinkingMode)

  return (
    <div className="pointer-events-none absolute inset-x-0 bottom-0 bg-gradient-to-t from-background via-background to-background/0 px-3 pb-3 pt-10 sm:px-6">
      <div className="pointer-events-auto mx-auto w-full max-w-[960px]">
        <AnimatePresence>
          {attachments.length > 0 && (
            <motion.div
              className="mb-2 flex gap-2 overflow-x-auto"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 8 }}
            >
              {attachments.map(attachment => (
                <AttachmentPreview
                  key={attachment.id}
                  attachment={attachment}
                  onRemove={() => onRemoveAttachment(attachment.id)}
                />
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <div
            className="mb-2 rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive"
            role="alert"
          >
            {error}
          </div>
        )}

        <div className="rounded-2xl border border-border bg-composer text-composer-foreground shadow-[0_12px_45px_rgba(0,0,0,0.12)]">
          <Textarea
            value={value}
            placeholder="Pergunte alguma coisa"
            rows={1}
            className="max-h-44 px-5 pt-4"
            onChange={event => onChange(event.target.value)}
            onKeyDown={event => {
              if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault()
                onSubmit()
              }
            }}
          />
          <div className="flex items-center justify-between gap-2 px-3 pb-3">
            <div className="flex min-w-0 items-center gap-2">
              <Button
                variant="soft"
                size="icon"
                aria-label="Anexar arquivo"
                onClick={onAttachClick}
              >
                <Paperclip size={18} />
              </Button>
              <Badge className="hidden max-w-[220px] truncate sm:inline-flex">
                {model}
              </Badge>
              <Badge>{activeThinking?.label ?? 'Equilibrado'}</Badge>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant={isRecording ? 'danger' : 'soft'}
                size="icon"
                aria-label={isRecording ? 'Parar gravação' : 'Gravar áudio'}
                className={isRecording ? 'animate-pulse-recording' : undefined}
                onClick={onToggleRecording}
              >
                {isRecording ? <Square size={16} /> : <Mic size={18} />}
              </Button>
              <Button
                size="icon"
                aria-label="Enviar mensagem"
                disabled={isSending}
                onClick={onSubmit}
              >
                {isSending ? <Square size={16} /> : <SendHorizontal size={18} />}
              </Button>
            </div>
          </div>
        </div>
        <p className="mt-2 text-center text-xs text-muted-foreground">
          O MindSight pode cometer erros. Confira informações relevantes.
        </p>
      </div>
    </div>
  )
}

function AttachmentPreview({
  attachment,
  onRemove,
}: {
  attachment: PendingAttachment
  onRemove: () => void
}) {
  return (
    <div className="flex min-w-[210px] items-center gap-3 rounded-lg border border-border bg-card p-2 shadow-sm">
      <div className="grid h-10 w-10 shrink-0 place-items-center rounded-md bg-secondary">
        {attachment.kind === 'image' && attachment.previewUrl ? (
          <img
            src={attachment.previewUrl}
            alt=""
            className="h-full w-full rounded-md object-cover"
          />
        ) : (
          <AttachmentIcon kind={attachment.kind} />
        )}
      </div>
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium">{attachment.file.name}</p>
        <p className="text-xs text-muted-foreground">
          {attachment.kind} · {formatFileSize(attachment.file.size)}
        </p>
      </div>
      <Button variant="ghost" size="icon" aria-label="Remover anexo" onClick={onRemove}>
        <X size={16} />
      </Button>
    </div>
  )
}

function AttachmentIcon({ kind }: { kind: AttachmentKind }) {
  if (kind === 'image') return <ImageIcon size={18} />
  if (kind === 'audio') return <FileAudio size={18} />
  if (kind === 'document') return <FileText size={18} />
  return <FileCode2 size={18} />
}

function MessageSkeleton() {
  return (
    <div className="space-y-8">
      <div className="ml-auto h-24 max-w-[70%] rounded-2xl bg-secondary animate-shimmer" />
      <div className="h-44 rounded-lg bg-secondary animate-shimmer" />
    </div>
  )
}

export default App
