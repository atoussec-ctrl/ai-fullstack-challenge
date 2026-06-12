import { describe, expect, it, vi } from 'vitest'
import {
  detectAttachmentKind,
  revokePendingAttachment,
  validateFiles,
} from './attachments'

vi.stubGlobal('crypto', { randomUUID: () => 'test-id' })

describe('attachment validation', () => {
  it('detects supported file kinds', () => {
    expect(detectAttachmentKind(new File(['x'], 'main.py'))).toBe('document')
    expect(detectAttachmentKind(new File(['x'], 'error.png', { type: 'image/png' }))).toBe('image')
    expect(detectAttachmentKind(new File(['x'], 'voice.webm', { type: 'video/webm' }))).toBe('audio')
  })

  it('rejects dangerous files before upload', () => {
    const result = validateFiles([new File(['x'], 'payload.exe')])

    expect(result.accepted).toHaveLength(0)
    expect(result.errors[0]).toContain('não é um tipo')
  })

  it('accepts images with preview urls', () => {
    const createObjectURL = vi.fn(() => 'blob:preview')
    vi.stubGlobal('URL', { createObjectURL, revokeObjectURL: vi.fn() })

    const result = validateFiles([new File(['x'], 'photo.png', { type: 'image/png' })])

    expect(result.accepted).toHaveLength(1)
    expect(result.accepted[0].previewUrl).toBe('blob:preview')
    vi.unstubAllGlobals()
  })

  it('rejects files above 10 MB', () => {
    const oversized = new File([new Uint8Array(10 * 1024 * 1024 + 1)], 'big.pdf', {
      type: 'application/pdf',
    })

    const result = validateFiles([oversized])

    expect(result.accepted).toHaveLength(0)
    expect(result.errors[0]).toContain('excede 10 MB')
  })

  it('enforces the five attachment limit', () => {
    const files = Array.from({ length: 6 }, (_, index) => new File(['x'], `note-${index}.txt`))

    const result = validateFiles(files)

    expect(result.accepted).toHaveLength(5)
    expect(result.errors[0]).toContain('Limite de 5 arquivos')
  })

  it('detects mime types when extension is missing', () => {
    expect(detectAttachmentKind(new File(['x'], 'blob', { type: 'image/gif' }))).toBe('image')
    expect(detectAttachmentKind(new File(['x'], 'blob', { type: 'audio/mpeg' }))).toBe('audio')
    expect(detectAttachmentKind(new File(['x'], 'blob', { type: 'text/plain' }))).toBe('document')
  })

  it('revokes preview urls on cleanup', () => {
    const revokeObjectURL = vi.fn()
    vi.stubGlobal('URL', { createObjectURL: vi.fn(), revokeObjectURL })

    revokePendingAttachment({
      id: 'att-1',
      file: new File(['x'], 'photo.png'),
      kind: 'image',
      previewUrl: 'blob:preview',
    })

    expect(revokeObjectURL).toHaveBeenCalledWith('blob:preview')
    vi.unstubAllGlobals()
  })
})
