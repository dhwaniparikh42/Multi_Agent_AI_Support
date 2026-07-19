"""
Module 8 - Conversation Memory
Handles storing and retrieving conversation history from the database.

Stores per message:
  - session_id  : which conversation this message belongs to
  - role        : "user" or "assistant"
  - content     : the actual message text
  - agent_type  : which agent replied (billing, technical, etc.)
  - created_at  : timestamp (auto-set by the database)
"""

from sqlalchemy.orm import Session
import models


def save_user_message(db: Session, session_id: str, content: str) -> models.Message:
    """Store the user's message in the database."""
    message = models.Message(
        session_id=session_id,
        role="user",
        content=content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def save_ai_message(
    db: Session,
    session_id: str,
    content: str,
    agent_type: str = None,
) -> models.Message:
    """Store the AI agent's response in the database."""
    message = models.Message(
        session_id=session_id,
        role="assistant",
        content=content,
        agent_type=agent_type,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_conversation_history(db: Session, session_id: str) -> list[dict]:
    """
    Retrieve the full conversation history for a session.
    Returns a list of dicts containing all four stored fields:
      - session_id
      - role
      - content
      - agent_type
      - timestamp
    """
    messages = (
        db.query(models.Message)
        .filter(models.Message.session_id == session_id)
        .order_by(models.Message.created_at.asc())
        .all()
    )
    return [
        {
            "session_id": m.session_id,
            "role": m.role,
            "content": m.content,
            "agent_type": m.agent_type,
            "timestamp": m.created_at.isoformat() if m.created_at else None,
        }
        for m in messages
    ]


def get_recent_history(db: Session, session_id: str, last_n: int = 6) -> list[dict]:
    """
    Retrieve the last N messages for passing as context to the agent.
    Keeps the conversation window small so the LLM does not receive too many tokens.
    """
    messages = (
        db.query(models.Message)
        .filter(models.Message.session_id == session_id)
        .order_by(models.Message.created_at.desc())
        .limit(last_n)
        .all()
    )
    messages.reverse()  # put back into oldest-first order
    return [{"role": m.role, "content": m.content} for m in messages]


def clear_session_history(db: Session, session_id: str) -> None:
    """Delete all messages for a session (used when the user resets a conversation)."""
    db.query(models.Message).filter(models.Message.session_id == session_id).delete()
    db.commit()
