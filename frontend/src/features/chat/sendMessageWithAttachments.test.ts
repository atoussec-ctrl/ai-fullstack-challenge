import { afterEach, describe, expect, it, vi } from 'vitest'

import { sendMessageWithAttachments } from './sendMessageWithAttachments'

import * as client from '@/shared/api/client'

import type { PendingAttachment } from './attachments'
import type { Attachment, SendMessageResponse } from '@/shared/api/types'

function pendingAttachment(id: string): PendingAttachment {
  return {
    id,
    file: new File(['conteudo'], `${id}.txt`),
    kind: 'document',
  }
}

function uploadedAttachment(id: string): Attachment {
  return {
    id,
    filename: `${id}.txt`,
    mime_type: 'text/plain',
    size: 8,
    kind: 'document',
    url: `/attachments/${id}`,
  }
}

const sendMessageResponse: SendMessageResponse = {
  user_message_id: 'msg_user',
  assistant_message_id: 'msg_assistant',
  status: 'completed',
  assistant_message: {
    id: 'msg_assistant',
    session_id: 'session_1',
    role: 'assistant',
    content: 'Olá',
    status: 'completed',
    attachments: [],
    created_at: '2026-07-21T00:00:00Z',
  },
}

describe('sendMessageWithAttachments', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('sends the message directly when there are no attachments', async () => {
    const sendMessage = vi.spyOn(client, 'sendMessage').mockResolvedValue(sendMessageResponse)
    const uploadAttachment = vi.spyOn(client, 'uploadAttachment')

    const result = await sendMessageWithAttachments({
      sessionId: 'session_1',
      content: 'oi',
      thinkingMode: 'balanced',
      attachments: [],
    })

    expect(result).toBe(sendMessageResponse)
    expect(uploadAttachment).not.toHaveBeenCalled()
    expect(sendMessage).toHaveBeenCalledWith(
      expect.objectContaining({ session_id: 'session_1', content: 'oi', attachment_ids: [] }),
      undefined,
    )
  })

  it('uploads every pending attachment before sending the message', async () => {
    vi.spyOn(client, 'uploadAttachment')
      .mockResolvedValueOnce(uploadedAttachment('att_1'))
      .mockResolvedValueOnce(uploadedAttachment('att_2'))
    const sendMessage = vi.spyOn(client, 'sendMessage').mockResolvedValue(sendMessageResponse)

    await sendMessageWithAttachments({
      sessionId: 'session_1',
      content: 'veja os anexos',
      thinkingMode: 'balanced',
      attachments: [pendingAttachment('local_1'), pendingAttachment('local_2')],
    })

    expect(sendMessage).toHaveBeenCalledWith(
      expect.objectContaining({ attachment_ids: ['att_1', 'att_2'] }),
      undefined,
    )
  })

  it('deletes the uploaded attachments and rethrows when sending the message fails', async () => {
    vi.spyOn(client, 'uploadAttachment')
      .mockResolvedValueOnce(uploadedAttachment('att_1'))
      .mockResolvedValueOnce(uploadedAttachment('att_2'))
    const sendError = new Error('Falha ao enviar mensagem.')
    vi.spyOn(client, 'sendMessage').mockRejectedValue(sendError)
    const deleteAttachment = vi.spyOn(client, 'deleteAttachment').mockResolvedValue(undefined)

    await expect(
      sendMessageWithAttachments({
        sessionId: 'session_1',
        content: 'vai falhar',
        thinkingMode: 'balanced',
        attachments: [pendingAttachment('local_1'), pendingAttachment('local_2')],
      }),
    ).rejects.toThrow(sendError)

    expect(deleteAttachment).toHaveBeenCalledWith('att_1')
    expect(deleteAttachment).toHaveBeenCalledWith('att_2')
  })

  it('deletes only the attachments already uploaded when the upload batch fails partway', async () => {
    vi.spyOn(client, 'uploadAttachment')
      .mockResolvedValueOnce(uploadedAttachment('att_1'))
      .mockRejectedValueOnce(new Error('Falha ao enviar arquivo.'))
    const sendMessage = vi.spyOn(client, 'sendMessage')
    const deleteAttachment = vi.spyOn(client, 'deleteAttachment').mockResolvedValue(undefined)

    await expect(
      sendMessageWithAttachments({
        sessionId: 'session_1',
        content: 'upload vai falhar no meio',
        thinkingMode: 'balanced',
        attachments: [pendingAttachment('local_1'), pendingAttachment('local_2')],
      }),
    ).rejects.toThrow('Falha ao enviar arquivo.')

    expect(deleteAttachment).toHaveBeenCalledExactlyOnceWith('att_1')
    expect(sendMessage).not.toHaveBeenCalled()
  })

  it('does not let a compensation failure hide the original error', async () => {
    vi.spyOn(client, 'uploadAttachment').mockResolvedValueOnce(uploadedAttachment('att_1'))
    const sendError = new Error('Falha ao enviar mensagem.')
    vi.spyOn(client, 'sendMessage').mockRejectedValue(sendError)
    vi.spyOn(client, 'deleteAttachment').mockRejectedValue(new Error('cleanup indisponível'))

    await expect(
      sendMessageWithAttachments({
        sessionId: 'session_1',
        content: 'oi',
        thinkingMode: 'balanced',
        attachments: [pendingAttachment('local_1')],
      }),
    ).rejects.toThrow(sendError)
  })
})
