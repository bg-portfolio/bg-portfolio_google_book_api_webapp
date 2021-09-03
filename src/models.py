from pydantic import BaseModel
from typing import Optional, List
from fastapi import Request


class GoogleBookRequest(BaseModel):
    """
    Pydantic model for google book api query

    intitle: Returns results where the text following this keyword is found in the title.
    inauthor: Returns results where the text following this keyword is found in the author.
    inpublisher: Returns results where the text following this keyword is found in the publisher.
    subject: Returns results where the text following this keyword is listed in the category list of the volume.
    isbn: Returns results where the text following this keyword is the ISBN number.
    lccn: Returns results where the text following this keyword is the Library of Congress Control Number.
    oclc: Retur
    """

    req: Optional[str] = "The Book"
    intitle: Optional[str] = ""
    inauthor: Optional[str] = ""
    inpublisher: Optional[str] = ""
    subject: Optional[str] = ""
    isbn: Optional[str] = ""
    lccn: Optional[str] = ""
    oclc: Optional[str] = ""


class BookEntry(BaseModel):
    """
    Pydantic model for Books
    """

    isbn_13: int
    title: Optional[str] = None
    publish_date: Optional[str] = None
    author: Optional[List[str]] = None
    page_count: Optional[int] = None
    thumbnail_url: Optional[str] = None
    language: Optional[str] = None


class BookEditionForm:
    """
    Form for book edition
    """

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.isbn_13: int
        self.title: Optional[str] = None
        self.publish_date: Optional[str] = None
        self.author: Optional[List[str]] = None
        self.page_count: Optional[int] = None
        self.thumbnail_url: Optional[str] = None
        self.language: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.isbn_13: int = form.get("isbn_13")
        self.title: Optional[str] = form.get("title")
        self.publish_date: Optional[str] = form.get("publish_date")
        self.author: Optional[List[str]] = [form.get("author")]
        self.page_count: Optional[int] = form.get("page_count")
        self.thumbnail_url: Optional[str] = form.get("thumbnail_url")
        self.language: Optional[str] = form.get("language")

    async def is_valid(self):
        if not self.isbn_13 or self.isbn_13.isnumeric() == False:
            self.errors.append("isbn should be a number")
        if not self.page_count or self.page_count.isnumeric() == False:
            self.errors.append("page_count should be a number")
        if not self.errors:
            return True
        return False


class BookDownloadForm:
    """
    Form for book downloading from google
    """

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.req: Optional[str] = "The Book"
        self.intitle: Optional[str] = ""
        self.inauthor: Optional[str] = ""
        self.inpublisher: Optional[str] = ""
        self.subject: Optional[str] = ""
        self.isbn: Optional[str] = ""
        self.lccn: Optional[str] = ""
        self.oclc: Optional[str] = ""

    async def load_data(self):
        form = await self.request.form()
        self.req: Optional[str] = form.get("req")
        self.intitle: Optional[str] = form.get("intitle")
        self.inauthor: Optional[str] = form.get("inauthor")
        self.inpublisher: Optional[str] = form.get("inpublisher")
        self.subject: Optional[int] = form.get("subject")
        self.isbn: Optional[str] = form.get("isbn")
        self.lccn: Optional[str] = form.get("lccn")
        self.oclc: Optional[str] = form.get("oclc")

    async def is_valid(self):
        if not self.errors:
            return True
        return False

# json from google book api for ref
#
#
# {
#   "kind": "books#volumes",
#   "totalItems": 525,
#   "items": [
#     {
#       "kind": "books#volume",
#       "id": "3f0NugEACAAJ",
#       "etag": "DFFzv1DzN1I",
#       "selfLink": "https://www.googleapis.com/books/v1/volumes/3f0NugEACAAJ",
#       "volumeInfo": {
#         "title": "Star Wars Ostatni Jedi",
#         "authors": [
#           "Jason Fry"
#         ],
#         "publishedDate": "2018",
#         "industryIdentifiers": [
#           {
#             "type": "ISBN_10",
#             "identifier": "8328053039"
#           },
#           {
#             "type": "ISBN_13",
#             "identifier": "9788328053038"
#           }
#         ],
#         "readingModes": {
#           "text": false,
#           "image": false
#         },
#         "pageCount": 320,
#         "printType": "BOOK",
#         "categories": [
#           "Fiction"
#         ],
#         "maturityRating": "NOT_MATURE",
#         "allowAnonLogging": false,
#         "contentVersion": "preview-1.0.0",
#         "panelizationSummary": {
#           "containsEpubBubbles": false,
#           "containsImageBubbles": false
#         },
#         "language": "pl",
#         "previewLink": "http://books.google.pl/books?id=3f0NugEACAAJ&dq=star+wars&hl=&cd=1&source=gbs_api",
#         "infoLink": "http://books.google.pl/books?id=3f0NugEACAAJ&dq=star+wars&hl=&source=gbs_api",
#         "canonicalVolumeLink": "https://books.google.com/books/about/Star_Wars_Ostatni_Jedi.html?hl=&id=3f0NugEACAAJ"
