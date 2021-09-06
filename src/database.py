from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

try:
    HEROKU_DATABASE_URL = os.environ["DATABASE_URL"]
    HEROKU_DATABASE_URL = HEROKU_DATABASE_URL.replace("postgres", "postgresql")
except KeyError:
    HEROKU_DATABASE_URL = None

SQLALCHEMY_DATABASE_URL = HEROKU_DATABASE_URL or "postgresql://postgres:password@localhost/google_book_api"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
