"""Schema-level tests for cascade behavior between models.

Attachment.message_id declares ondelete="CASCADE" to match the ORM-level
cascade="all, delete-orphan" already set on ChatMessage.attachments — an
attachment without its message has no reason to exist. This test exercises
the ORM cascade directly (deleting a ChatMessage, not a whole ChatSession),
since that's the path the ondelete/cascade declarations actually describe,
even though no current service method deletes a single message on its own.
"""

from __future__ import annotations

from app.extensions import db
from app.models import Attachment, ChatMessage, ChatSession


def test_deleting_a_message_cascades_to_its_attachments(app):
    with app.app_context():
        session = ChatSession(title="Sessão de teste")
        db.session.add(session)
        db.session.flush()

        message = ChatMessage(session_id=session.id, role="user", content="oi")
        db.session.add(message)
        db.session.flush()

        attachment = Attachment(
            session_id=session.id,
            message_id=message.id,
            filename="nota.txt",
            mime_type="text/plain",
            size=3,
            kind="document",
            storage_path="/tmp/nota.txt",
        )
        db.session.add(attachment)
        db.session.commit()
        attachment_id = attachment.id

        db.session.delete(message)
        db.session.commit()

        assert db.session.get(Attachment, attachment_id) is None
