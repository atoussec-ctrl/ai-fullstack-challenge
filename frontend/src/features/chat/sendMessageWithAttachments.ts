import { deleteAttachment, sendMessage, uploadAttachment } from '@/shared/api/client'

import type { PendingAttachment } from './attachments'
import type { Attachment, SendMessageResponse, ThinkingMode } from '@/shared/api/types'

interface SendMessageWithAttachmentsInput {
  sessionId: string
  content: string
  thinkingMode: ThinkingMode | string
  attachments: PendingAttachment[]
  model?: string
  signal?: AbortSignal
}

/**
 * Uploads pending attachments and sends the message as one logical unit.
 *
 * The backend only links an attachment to a message once /chat/messages
 * succeeds, so a failure anywhere in this sequence — a partial upload batch
 * or the send itself — would otherwise leave already-uploaded files orphaned
 * in storage. This compensates by deleting whatever was uploaded before
 * re-throwing, so callers see the original failure either way.
 */
export async function sendMessageWithAttachments({
  sessionId,
  content,
  thinkingMode,
  attachments,
  model,
  signal,
}: SendMessageWithAttachmentsInput): Promise<SendMessageResponse> {
  const uploaded: Attachment[] = []
  try {
    for (const attachment of attachments) {
      uploaded.push(await uploadAttachment(sessionId, attachment.file, attachment.kind, signal))
    }
    return await sendMessage(
      {
        session_id: sessionId,
        content,
        thinking_mode: thinkingMode as ThinkingMode,
        attachment_ids: uploaded.map(item => item.id),
        model,
      },
      signal,
    )
  } catch (error) {
    await Promise.allSettled(uploaded.map(item => deleteAttachment(item.id)))
    throw error
  }
}
