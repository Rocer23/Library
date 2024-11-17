from sqlalchemy.orm import Session
from . import models, schemas


def get_author_by_name(db: Session, author: str):
    return db.query(models.Author).filter(models.Author.author == author).first()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books_by_author(db: Session, author_name: str):
    db_author = db.query(models.Author).filter(models.Author.author == author_name).first()
    if db_author:
        return db_author.books
    return None


def read_book(db: Session, book_title: str):
    return db.query(models.Book).filter(models.Book.title == book_title).first()


def get_books(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_author(db: Session, author: str):
    db_author = models.Author(author=author)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def create_book(db: Session, book: schemas.BookCreate):
    db_author = get_author_by_name(db, book.author_name)
    if not db_author:
        db_author = create_author(db, book.author_name)

    db_book = models.Book(
        title=book.title,
        pages=book.pages,
        author=db_author
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def delete_author(db: Session, author_name: int):
    db_author = db.query(models.Author).filter(models.Author.author == author_name).first()
    if db_author:
        db.query(models.Book).filter(models.Book.author_id == author_name).delete()
        db.delete(db_author)
        db.commit()

    return db_author


def delete_book(db: Session, book_title: str):
    db_book = db.query(models.Book).filter(models.Book.title == book_title).first()
    if db_book:
        db.delete(db_book)
        db.commit()

    return db_book


def update_book(db: Session, book_title: str, book_update: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.title == book_title).first()
    if db_book:
        for key, value in book_update.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)

    return db_book
