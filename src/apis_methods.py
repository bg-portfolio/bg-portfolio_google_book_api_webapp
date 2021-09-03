from sqlalchemy.orm import Session
from src.models import BookEntry
from src.database import get_db
from src.schemas import Book
from src.data_validation import validate_record_existance


def create_record(details: BookEntry, db: Session) -> tuple:
    """
    returns <bool>,<Book>; True if Book already exists, False otherwise
    """
    to_create = Book(
        isbn_13=details.isbn_13,
        title=details.title,
        publish_date=details.publish_date,
        author=details.author,
        page_count=details.page_count,
        thumbnail_url=details.thumbnail_url,
        language=details.language
    )
    if (record := validate_record_existance(db, to_create.isbn_13))[0]:
        return record
    db.add(to_create)
    db.commit()
    return (False, to_create)


def get_record_by_isbn(isbn_13: int, db: Session) -> tuple:
    """
    returns validate_record_existance, that is, a record by isbn
    """
    return validate_record_existance(db, isbn_13)


def get_all_records(db: Session) -> list:
    """
    returns a list of all records
    """
    return db.query(Book).all()


def delete_record_by_isbn(isbn_13: int, db: Session) -> None:
    """
    deletes a record by isbn
    """
    db.query(Book).filter(Book.isbn_13 == isbn_13).delete()
    db.commit()


def update_record(db: Session, update: BookEntry) -> None:
    """
    update a record with PUT, data from updated record required.
    """
    record = validate_record_existance(db, update.isbn_13)
    if record:
        delete_record_by_isbn(update.isbn_13, db)
    create_record(update, db)


def get_all_records_by_query_params(details: dict, db: Session) -> list:
    """
    returns a list of records, filtered with details from <dict>
    """
    author = details["author"]
    title = details["title"]
    language = details["language"]
    publish_date = details["publish_date"]

    records = db.query(Book).filter(Book.author == )
    return records
