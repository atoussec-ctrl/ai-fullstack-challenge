export type ThinkingMode = 'fast' | 'balanced' | 'deep'

export interface ChatSession {
  id: string
  title: string
  created_at: string
  updated_at: string
}

export interface Book {
  id: string
  title: string
  category: string
  author: string
  publication_date: string
  publication_year: number
  summary: string
  created_at?: string
}

export interface CreateBookInput {
  title: string
  category: string
  author: string
  publication_year: string
  summary: string
}

export interface ImportBookResponse {
  book: Book
  extracted: {
    title: string
    category: string
    author: string
    publication_year: number
    summary: string
  }
}

export interface Attachment {
  id: string
  filename: string
  mime_type: string
  size: number
  kind: AttachmentKind
  url: string
  created_at?: string
}

export type AttachmentKind = 'document' | 'image' | 'audio'

export interface ChatMessage {
  id: string
  session_id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  thinking_mode?: ThinkingMode
  status: 'pending' | 'streaming' | 'completed' | 'error'
  attachments: Attachment[]
  created_at: string
}

export interface SendMessageInput {
  session_id: string
  content: string
  thinking_mode: ThinkingMode
  attachment_ids?: string[]
  model?: string
}

export interface SendMessageResponse {
  user_message_id: string
  assistant_message_id: string
  status: string
  assistant_message: ChatMessage
}

export interface SemanticSearchResult {
  document_id: string
  title: string
  score: number
  excerpt: string
}
