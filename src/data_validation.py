from sqlalchemy.orm import Session
from src.schemas import Book


def validate_record_existance(db: Session, isbn_13: int) -> tuple:
    """
    (<bool>; <query> if True, otherwise <None>)
    """
    query = db.query(Book).filter(Book.isbn_13 == isbn_13).first()
    if query is None:
        return (False, None)
    return (True, query)
