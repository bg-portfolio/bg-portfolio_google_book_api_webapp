from sqlalchemy import Integer, String
from sqlalchemy.sql.schema import Column
from .database import Base


class Book(Base):
    __tablename__ = "books"

    isbn_13 = Column(Integer, primary_key=True)
    title = Column(String)
    publish_date = Column(String)  # change into <date> type when displayed
    # change later to solve many to many problem in sql model
    author = Column(String)
    page_count = Column(Integer)
    thumbnail_url = Column(String)
    language = Column(String)
