from fastapi import Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas import Book
from src.models import BookEntry
from src.data_validation import validate_record_existance
from src import apis_methods


api_router = APIRouter()


@api_router.post("/create-record")
def api_create_record(details: BookEntry, db: Session = Depends(get_db)):
    to_create = apis_methods.create_record(details, db)
    if not to_create[0]:  # bool
        return {
            "success": True,
            "created_id": to_create[1].isbn_13  # query/record -> Book
        }
    # Book
    return {"success": False, "info": f"isbn {to_create[1].isbn_13} already exists"}


@api_router.get("/get-record-by-isbn/{isbn_13}")
def api_get_record_by_isbn(isbn_13: int, db: Session = Depends(get_db)):
    if not (record := (apis_methods.get_record_by_isbn(isbn_13, db)))[0]:
        return {"success": False, "info": f"isbn {isbn_13} do not exists"}
    return record[1]  # the query


@ api_router.get("/get-all-records")
def api_get_all_records(db: Session = Depends(get_db)):
    return db.query(Book).all()


@api_router.get("/get-all-records-by-query-params")
def api_get_all_records_by_query_params(title: Optional[str] = None, author: Optional[str] = None,
                                        language: Optional[str] = None, publish_date: Optional[str] = None, db: Session = Depends(get_db)):
    details = {
        "author": author,
        "title": title,
        "language": language,
        "publish_date": publish_date
    }
    records = apis_methods.get_all_records_by_query_params(details, db)
    return records


@api_router.put("/update-record")
def api_update_record(update: BookEntry, db: Session = Depends(get_db)):
    apis_methods.update_record(db, update)
    return {"success": True, "created_id": f"{update.isbn_13}"}


@ api_router.delete("/delete-record-by-isbn/{isbn_13}")
def api_delete_record_by_isbn(isbn_13: int, db: Session = Depends(get_db)):
    if (validate_record_existance(db, isbn_13))[0]:
        apis_methods.delete_record_by_isbn(isbn_13)
        return {"success": True, "deleted_id": isbn_13}
    return {"success": False, "info": f"isbn {isbn_13} do not exists"}
