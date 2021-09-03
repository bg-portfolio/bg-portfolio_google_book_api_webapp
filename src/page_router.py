from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.apis_methods import get_all_records, update_record, create_record
from src.database import get_db
from src.models import GoogleBookRequest, BookEditionForm, BookEntry, BookDownloadForm
from src.google_wrapper import get_google_books


templates = Jinja2Templates(directory="templates")
page_router = APIRouter(include_in_schema=False)  # won't be visible in /docs


@page_router.get("/", response_class=HTMLResponse)
async def home(request: Request, msg: str = None):
    return templates.TemplateResponse("index.html", {"request": request, "msg": msg})


@page_router.get("/view1-2a", response_class=HTMLResponse)
async def view1_2a(request: Request, db: Session = Depends(get_db)):
    data = get_all_records(db)
    return templates.TemplateResponse("view1-2a.html", {"request": request, "data": data, "page_title": "view1-2a"})


@page_router.get("/view1-2b", response_class=HTMLResponse)
async def view1_2b(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("view1-2b.html", {"request": request, "page_title": "view1-2b"})


@page_router.post("/view1-2b", response_class=HTMLResponse)
async def view1_2b(request: Request, db: Session = Depends(get_db)):
    form = BookEditionForm(request)
    await form.load_data()
    if await form.is_valid():
        book = BookEntry(
            isbn_13=form.isbn_13,
            title=form.title,
            publish_date=form.publish_date,
            author=form.author,
            page_count=form.page_count,
            thumbnail_url=form.thumbnail_url,
            language=form.language
        )
        try:
            updated = update_record(db, book)
            return RedirectResponse("/?msg=Successfully-Updated-A-Book", status_code=status.HTTP_302_FOUND)
        except IntegrityError:
            form.__dict__get("errors").append("some error")

            return templates.TemplateResponse("view1-2b.html", form.__dict__)
    return templates.TemplateResponse("view1-2b.html", form.__dict__)


@ page_router.get("/view2-1", response_class=HTMLResponse)
async def view1_2b(request: Request, db: Session = Depends(get_db)):
    placeholder = {
        "req_placeholder": "search phrase",
        "intitle_placeholder": "Returns results where the text following this keyword is found in the title.",
        "inauthor_placeholder": "Returns results where the text following this keyword is found in the author.",
        "inpublisher_placeholder": "Returns results where the text following this keyword is found in the publisher.",
        "subject_placeholder": "Returns results where the text following this keyword is listed in the category list of the volume.",
        "isbn_placeholder": "Returns results where the text following this keyword is the ISBN number.",
        "lccn_placeholder": "Returns results where the text following this keyword is the Library of Congress Control Number.",
        "oclc_placeholder": "Retur"
    }
    return templates.TemplateResponse("view2-1.html", {"request": request, "page_title": "view2-1", **placeholder})


@page_router.post("/view2-1", response_class=HTMLResponse)
async def view1_2b(request: Request, db: Session = Depends(get_db)):
    form = BookDownloadForm(request)
    await form.load_data()
    if await form.is_valid():
        google_query = GoogleBookRequest(
            req=form.req,
            intitle=form.intitle,
            inauthor=form.inauthor,
            inpublisher=form.inpublisher,
            subject=form.subject,
            isbn=form.isbn,
            lccn=form.lccn,
            oclc=form.oclc
        )

        book_list = await get_google_books(google_query)

        for book in book_list:
            try:
                create_record(book, db)
            except IntegrityError:
                form.__dict__get("errors").append(
                    f"{book.isbn_13} Duplicate Record")
                return templates.TemplateResponse("/view2-1.html", form.__dict__)
        return RedirectResponse("/?msg=Successfully-Downloaded-Books-From-Google-Book-API", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("/view2-1.html", form.__dict__)


@page_router.get("/view3-1")
async def view3_1(request: Request, db: Session = Depends(get_db), title: Optional[str] = None, author: Optional[str] = None,
                  language: Optional[str] = None, publish_date: Optional[str] = None):
    details = {
        "author": [author],
        "title": title,
        "language": language,
        "publish_date": publish_date
    }
    data = []
    return templates.TemplateResponse("view3-1.html", {"request": request, "data": data, "page_title": "view3-1"})
