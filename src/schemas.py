from sqlalchemy import Integer, String, ARRAY, BigInteger
from sqlalchemy.sql.schema import Column
from src.database import Base


class Book(Base):
    """
    SQLAlchemy model for sql schema
    """
    __tablename__ = "books"

    isbn_13 = Column(BigInteger, primary_key=True)
    title = Column(String)
    publish_date = Column(String)
    # change later to solve many to many problem in sql schema
    author = Column(ARRAY(String))
    page_count = Column(Integer)
    thumbnail_url = Column(String)
    language = Column(String)
