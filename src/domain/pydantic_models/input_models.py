from pydantic import BaseModel
from typing import List, Optional


class InputDocument(BaseModel):
    title: str
    subtitles: List[str]
    folders: List[str]
    content: str
    tags: List[str]
    obsidian_references: List[str]
    bibliographic_references: List[str]
    raw_content: str


class EnhancedDocumentMetadata(InputDocument):
    summary: Optional[str]
    vector1: List[float]
    is_used: bool
    used_in: List[str]
