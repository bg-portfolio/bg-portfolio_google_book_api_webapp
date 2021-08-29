from pydantic import BaseModel
from typing import Optional


class BookEntry(BaseModel):
    isbn_13: int
    title: Optional[str] = None
    publish_date: Optional[str] = None
    author: Optional[str] = None
    page_count: Optional[int] = None
    thumbnail_url: Optional[str] = None
    language: Optional[str] = None
