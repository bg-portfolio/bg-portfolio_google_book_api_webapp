from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .models import BookEntry
from .database import get_db
from .schemas import Book

api_router = APIRouter()


@api_router.post("/")
def create_record(details: BookEntry, db: Session = Depends(get_db)):
    to_create = Book(
        isbn_13=details.isbn_13,
        title=details.title,
        publish_date=details.publish_date,
        author=details.author,
        page_count=details.page_count,
        thumbnail_url=details.thumbnail_url,
        language=details.language
    )
    db.add(to_create)
    db.commit()
    return {
        "success": True,
        "created_id": to_create.isbn_13
    }


@api_router.get("/")
def get_record_by_isbn(isbn: int, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.isbn_13 == isbn).first()


@api_router.delete("/")
def delete_record_by_isbn(isbn: int, db: Session = Depends(get_db)):
    db.query(Book).filter(Book.isbn_13 == isbn).delete()
    db.commit()
    return {"success": True, "deleted_id": isbn}
