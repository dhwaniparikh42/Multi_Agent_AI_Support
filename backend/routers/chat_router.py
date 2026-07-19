from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import get_db
import models
import auth
from agents.router import get_agent_response

router = APIRouter(prefix="/chat", tags=["chat"])


class MessageOut(BaseModel):
    id: str
    role: str
    content: str
    agent_type: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class SessionOut(BaseModel):
    id: str
    title: str
    agent_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CreateSessionRequest(BaseModel):
    title: str = "New Conversation"


class SendMessageRequest(BaseModel):
    session_id: str
    message: str


class SendMessageResponse(BaseModel):
    message: MessageOut
    session: SessionOut


@router.post("/sessions", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def create_session(
    req: CreateSessionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    session = models.ChatSession(user_id=current_user.id, title=req.title[:200])
    db.add(session)
    db.commit()
    db.refresh(session)
    return SessionOut.model_validate(session)


@router.get("/sessions", response_model=list[SessionOut])
def list_sessions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    sessions = (
        db.query(models.ChatSession)
        .filter(models.ChatSession.user_id == current_user.id)
        .order_by(models.ChatSession.updated_at.desc())
        .all()
    )
    return [SessionOut.model_validate(s) for s in sessions]


@router.get("/sessions/{session_id}/messages", response_model=list[MessageOut])
def get_messages(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return [MessageOut.model_validate(m) for m in session.messages]


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == session_id,
        models.ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()


@router.post("/message", response_model=SendMessageResponse)
def send_message(
    req: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    session = db.query(models.ChatSession).filter(
        models.ChatSession.id == req.session_id,
        models.ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Get previous messages for conversation context
    previous_messages = [
        {"role": m.role, "content": m.content}
        for m in session.messages
    ]

    # Persist user message
    user_msg = models.Message(
        session_id=session.id,
        role="user",
        content=req.message.strip()
    )
    db.add(user_msg)
    db.flush()

    # Get AI response with conversation history
    agent_type, reply_text = get_agent_response(req.message, previous_messages)

    # Persist AI reply
    ai_msg = models.Message(
        session_id=session.id,
        role="assistant",
        content=reply_text,
        agent_type=agent_type
    )
    db.add(ai_msg)

    session.agent_type = agent_type
    session.updated_at = func.now()

    db.commit()
    db.refresh(ai_msg)
    db.refresh(session)

    return SendMessageResponse(
        message=MessageOut.model_validate(ai_msg),
        session=SessionOut.model_validate(session)
    )
