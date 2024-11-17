from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

# Створення екземпляру FastAPI
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Створення Моделі
# class Book(BaseModel):
#     # id: Optional[UUID] = None
#     title: str
#     pages: int = Field(..., gt=10)
#     author: str = Field(..., min_length=3, max_length=30)


# library = []


# Створення книги
@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


# Показ книг
@app.get("/book/get-all", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


# Книги по Title
@app.get("/book/{book_title}", response_model=schemas.Book)
def read_book(book_title: str, db: Session = Depends(get_db)):
    db_book = crud.read_book(db, book_title=book_title)
    if db_book is None:
        raise HTTPException(status_code=400, detail="Book not found")
    return db_book


# Видалення книги
@app.delete("/book/{book_title}", response_model=schemas.Book)
def delete_book(book_title: str, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_title=book_title)
    if db_book is None:
        raise HTTPException(status_code=400, detail="Book not found")
    return db_book


# Редагування книги по Tittle
@app.put("/book/{book_title}", response_model=schemas.Book)
def update_book(book_title: str, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_title=book_title, book_update=book_update)
    if db_book is None:
        raise HTTPException(status_code=400, detail="Book not found")
    return db_book


# Показ книг по автору
@app.get("/book/author/{author_name}", response_model=List[schemas.Book])
def get_books_by_author(author_name: str, db: Session = Depends(get_db)):
    books = crud.get_books_by_author(db, author_name=author_name)
    if books is None:
        raise HTTPException(status_code=400, detail="Author not found")
    return books


# Видалення автора по ID
@app.delete("/book/author/{author_name}", response_model=schemas.Author)
def delete_author(author_name: int, db: Session = Depends(get_db)):
    db_author = crud.delete_author(db, author_name=author_name)
    if db_author is None:
        raise HTTPException(status_code=400, detail="Author not found")
