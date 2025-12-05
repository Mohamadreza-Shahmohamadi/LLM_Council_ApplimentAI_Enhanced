"""
Storage package for LLM Council.
Handles switching between JSON file storage and Database storage.
"""

from typing import List, Dict, Any, Optional
from ..config import get_database_config
from .database import init_database

# Import implementations
from . import json_storage
from . import sql_storage

def _get_backend():
    """Get the active storage backend based on config."""
    config = get_database_config()
    if config["type"] in ["postgresql", "mysql"]:
        return sql_storage
    return json_storage

# Facade functions that delegate to the active backend

def create_conversation(conversation_id: str) -> Dict[str, Any]:
    return _get_backend().create_conversation(conversation_id)

def get_conversation(conversation_id: str) -> Optional[Dict[str, Any]]:
    return _get_backend().get_conversation(conversation_id)

def save_conversation(conversation: Dict[str, Any]):
    return _get_backend().save_conversation(conversation)

def list_conversations() -> List[Dict[str, Any]]:
    return _get_backend().list_conversations()

def add_user_message(conversation_id: str, content: str):
    return _get_backend().add_user_message(conversation_id, content)

def add_assistant_message(conversation_id: str, stage1: List[Dict[str, Any]], stage2: Optional[List[Dict[str, Any]]] = None, stage3: Optional[Dict[str,Any]] = None, metadata: Optional[Dict[str, Any]] = None):
    return _get_backend().add_assistant_message(conversation_id, stage1, stage2, stage3, metadata)

def add_error_message(conversation_id: str, error_text: str):
    return _get_backend().add_error_message(conversation_id, error_text)

def update_conversation_title(conversation_id: str, title: str):
    return _get_backend().update_conversation_title(conversation_id, title)

def delete_conversation(conversation_id: str) -> bool:
    return _get_backend().delete_conversation(conversation_id)
