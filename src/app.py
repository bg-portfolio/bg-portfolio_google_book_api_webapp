from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .schemas import BookEntry
from .database import get_db
from .models import Book


app = FastAPI()


@app.post("/")
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


@app.get("/")
def get_record_by_isbn(isbn: int, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.isbn_13 == isbn).first()
