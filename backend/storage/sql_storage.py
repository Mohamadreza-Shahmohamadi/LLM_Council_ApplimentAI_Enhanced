"""SQL-based storage for conversations."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db_engine
from .models import Conversation

def _get_session() -> Session:
    """Helper to get a new session."""
    if SessionLocal is None:
        init_db_engine()
        if SessionLocal is None:
             raise RuntimeError("Database not initialized")
    return SessionLocal()

def create_conversation(conversation_id: str) -> Dict[str, Any]:
    """Create a new conversation."""
    session = _get_session()
    try:
        db_conversation = Conversation(
            id=conversation_id,
            title="New Conversation",
            messages=[]
        )
        session.add(db_conversation)
        session.commit()
        return db_conversation.to_dict()
    finally:
        session.close()

def get_conversation(conversation_id: str) -> Optional[Dict[str, Any]]:
    """Load a conversation from storage."""
    session = _get_session()
    try:
        db_conversation = session.query(Conversation).filter(Conversation.id == conversation_id).first()
        return db_conversation.to_dict() if db_conversation else None
    finally:
        session.close()

def save_conversation(conversation: Dict[str, Any]):
    """Save a conversation to storage."""
    session = _get_session()
    try:
        db_conversation = session.query(Conversation).filter(Conversation.id == conversation['id']).first()
        if db_conversation:
            db_conversation.title = conversation.get('title', db_conversation.title)
            db_conversation.messages = conversation.get('messages', [])
            # updated_at is handled automatically by onupdate
            session.commit()
    finally:
        session.close()

def list_conversations() -> List[Dict[str, Any]]:
    """List all conversations (metadata only)."""
    session = _get_session()
    try:
        conversations = session.query(Conversation).order_by(Conversation.created_at.desc()).all()
        return [{
            "id": c.id,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "title": c.title,
            "message_count": len(c.messages or [])
        } for c in conversations]
    finally:
        session.close()

def add_user_message(conversation_id: str, content: str):
    """Add a user message to a conversation."""
    session = _get_session()
    try:
        db_conversation = session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not db_conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        # We need to create a new list to trigger SQLAlchemy change detection for JSON
        messages = list(db_conversation.messages)
        messages.append({
            "role": "user",
            "content": content
        })
        db_conversation.messages = messages
        session.commit()
    finally:
        session.close()

def add_assistant_message(
    conversation_id: str,
    stage1: List[Dict[str, Any]],
    stage2: Optional[List[Dict[str, Any]]] = None,
    stage3: Optional[Dict[str,Any]] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """Add an assistant message to a conversation."""
    session = _get_session()
    try:
        db_conversation = session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not db_conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        message = {
            "role": "assistant",
            "stage1": stage1,
        }
        
        if stage2 is not None:
            message["stage2"] = stage2
        if stage3 is not None:
            message["stage3"] = stage3
        if metadata:
            message["metadata"] = metadata

        messages = list(db_conversation.messages)
        messages.append(message)
        db_conversation.messages = messages
        session.commit()
    finally:
        session.close()

def add_error_message(conversation_id: str, error_text: str):
    """Add an error message to a conversation."""
    session = _get_session()
    try:
        db_conversation = session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not db_conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        message = {
            "role": "assistant",
            "content": None,
            "error": error_text,
            "stage1": [],
            "stage2": [],
            "stage3": None
        }

        messages = list(db_conversation.messages)
        messages.append(message)
        db_conversation.messages = messages
        session.commit()
    finally:
        session.close()

def update_conversation_title(conversation_id: str, title: str):
    """Update the title of a conversation."""
    session = _get_session()
    try:
        db_conversation = session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not db_conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        db_conversation.title = title
        session.commit()
    finally:
        session.close()

def delete_conversation(conversation_id: str) -> bool:
    """Delete a conversation."""
    session = _get_session()
    try:
        db_conversation = session.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not db_conversation:
            return False
        
        session.delete(db_conversation)
        session.commit()
        return True
    finally:
        session.close()
