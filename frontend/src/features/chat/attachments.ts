import type { AttachmentKind } from '@/shared/api/types'

export interface PendingAttachment {
  id: string
  file: File
  kind: AttachmentKind
  previewUrl?: string
}

export interface FileValidationResult {
  accepted: PendingAttachment[]
  errors: string[]
}

const MAX_FILES = 5
const MAX_FILE_SIZE = 10 * 1024 * 1024

const EXTENSIONS: Record<AttachmentKind, string[]> = {
  document: ['txt', 'md', 'py', 'json', 'pdf'],
  image: ['png', 'jpg', 'jpeg', 'webp'],
  audio: ['webm', 'wav', 'mp3'],
}

export function detectAttachmentKind(file: File): AttachmentKind | null {
  const extension = file.name.split('.').pop()?.toLowerCase()
  if (!extension) return null

  for (const [kind, extensions] of Object.entries(EXTENSIONS)) {
    if (extensions.includes(extension)) {
      return kind as AttachmentKind
    }
  }

  if (file.type.startsWith('image/')) return 'image'
  if (file.type.startsWith('audio/') || file.type === 'video/webm') return 'audio'
  if (file.type.startsWith('text/') || file.type === 'application/pdf') {
    return 'document'
  }

  return null
}

export function validateFiles(
  files: File[],
  existingCount = 0,
): FileValidationResult {
  const accepted: PendingAttachment[] = []
  const errors: string[] = []

  for (const file of files) {
    if (existingCount + accepted.length >= MAX_FILES) {
      errors.push('Limite de 5 arquivos por mensagem.')
      break
    }

    if (file.size > MAX_FILE_SIZE) {
      errors.push(`${file.name} excede 10 MB.`)
      continue
    }

    const kind = detectAttachmentKind(file)
    if (!kind) {
      errors.push(`${file.name} não é um tipo de arquivo permitido.`)
      continue
    }

    accepted.push({
      id: crypto.randomUUID(),
      file,
      kind,
      previewUrl: kind === 'image' ? URL.createObjectURL(file) : undefined,
    })
  }

  return { accepted, errors }
}

export function revokePendingAttachment(attachment: PendingAttachment) {
  if (attachment.previewUrl) {
    URL.revokeObjectURL(attachment.previewUrl)
  }
}
