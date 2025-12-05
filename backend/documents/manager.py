"""
Document management module.
Handles file storage, registry, and retrieval.
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from ..config import get_document_config
from .parser import extract_text

# Constants
SUPPORTED_EXTENSIONS = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

MAX_TEXT_LENGTH = 500 * 1024  # 500KB limit for extracted text

def _get_paths():
    config = get_document_config()
    doc_dir = config["upload_dir"]
    registry_file = os.path.join(doc_dir, "registry.json")
    return doc_dir, registry_file

def ensure_documents_dir() -> None:
    doc_dir, _ = _get_paths()
    os.makedirs(doc_dir, exist_ok=True)

def load_registry() -> Dict[str, Dict]:
    _, registry_file = _get_paths()
    if not os.path.exists(registry_file):
        return {}
    try:
        with open(registry_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading registry: {e}")
        return {}

def save_registry(registry: Dict[str, Dict]) -> None:
    _, registry_file = _get_paths()
    ensure_documents_dir()
    with open(registry_file, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

async def save_document(file_content: bytes, filename: str) -> Dict:
    config = get_document_config()
    if len(file_content) > config["max_upload_size"]:
        raise ValueError(f"File too large. Maximum size is {config['max_upload_size'] / (1024*1024):.1f}MB")

    extension = Path(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    ensure_documents_dir()
    doc_dir, _ = _get_paths()
    
    doc_id = str(uuid.uuid4())
    original_file_path = os.path.join(doc_dir, f"{doc_id}{extension}")
    text_file_path = os.path.join(doc_dir, f"{doc_id}.txt")

    # Save original
    with open(original_file_path, 'wb') as f:
        f.write(file_content)

    # Extract text
    extracted_text = extract_text(original_file_path, extension)
    
    text_truncated = False
    if len(extracted_text) > MAX_TEXT_LENGTH:
        extracted_text = extracted_text[:MAX_TEXT_LENGTH] + "\n\n[... Text truncated ...]"
        text_truncated = True

    # Save text
    with open(text_file_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

    metadata = {
        "id": doc_id,
        "filename": filename,
        "extension": extension,
        "size": len(file_content),
        "uploaded_at": datetime.utcnow().isoformat(),
        "text_length": len(extracted_text),
        "text_truncated": text_truncated,
        "is_active": True
    }

    registry = load_registry()
    registry[doc_id] = metadata
    save_registry(registry)

    return metadata

def get_document_text(doc_id: str) -> Optional[str]:
    doc_dir, _ = _get_paths()
    text_file_path = os.path.join(doc_dir, f"{doc_id}.txt")
    if not os.path.exists(text_file_path):
        return None
    try:
        with open(text_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None

def list_documents() -> List[Dict]:
    registry = load_registry()
    docs = []
    for doc_id, meta in registry.items():
        doc = meta.copy()
        text = get_document_text(doc_id)
        if text:
            preview = text[:200].strip()
            if len(text) > 200: preview += "..."
            doc["preview"] = preview
        else:
            doc["preview"] = "[No preview]"
        docs.append(doc)
    docs.sort(key=lambda x: x["uploaded_at"], reverse=True)
    return docs

def delete_document(doc_id: str) -> bool:
    registry = load_registry()
    if doc_id not in registry:
        return False
    
    meta = registry[doc_id]
    doc_dir, _ = _get_paths()
    
    orig_path = os.path.join(doc_dir, f"{doc_id}{meta['extension']}")
    text_path = os.path.join(doc_dir, f"{doc_id}.txt")
    
    if os.path.exists(orig_path): os.remove(orig_path)
    if os.path.exists(text_path): os.remove(text_path)
    
    del registry[doc_id]
    save_registry(registry)
    return True

def toggle_document_active(doc_id: str, is_active: bool) -> bool:
    registry = load_registry()
    if doc_id not in registry:
        return False
    registry[doc_id]["is_active"] = is_active
    save_registry(registry)
    return True

def get_active_documents_context() -> str:
    registry = load_registry()
    active_docs = [(doc_id, meta) for doc_id, meta in registry.items() if meta.get("is_active", True)]
    
    if not active_docs:
        return ""
        
    parts = ["=== UPLOADED DOCUMENTS ===\n"]
    for doc_id, meta in active_docs:
        text = get_document_text(doc_id)
        if text:
            parts.append(f"--- Document: {meta['filename']} ---")
            parts.append(text)
            parts.append("")
    parts.append("=== END DOCUMENTS ===")
    return "\n".join(parts)
