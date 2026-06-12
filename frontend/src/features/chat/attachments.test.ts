import { describe, expect, it, vi } from 'vitest'
import { detectAttachmentKind, validateFiles } from './attachments'

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
})
