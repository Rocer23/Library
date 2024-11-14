from sqlalchemy.orm import Session
from . import models, schemas


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def read_book(db: Session, book_title: str):
    return db.query(models.Book).filter(models.Book.title == book_title).first()


def get_books(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        pages=book.pages,
        author=book.author
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


