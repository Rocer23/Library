from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.database import SessionLocal, engine
import uvicorn


models.Base.metadata.create_all(bind=engine)

# Створення екземпляру FastAPI
app = FastAPI()


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/books/", response_class=HTMLResponse)
async def show_books(request: Request, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=0, limit=50)
    return templates.TemplateResponse("books.html", {"request": request, "books": books})


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
@app.get("/author/{author_name}", response_model=List[schemas.Book])
def get_books_by_author(author_name: str, db: Session = Depends(get_db)):
    books = crud.get_books_by_author(db, author_name=author_name)
    if books is None:
        raise HTTPException(status_code=400, detail="Author not found")
    return books


# Видалення автора по ID
@app.delete("/author/{author_name}", response_model=schemas.Author)
def delete_author(author_name: str, db: Session = Depends(get_db)):
    db_author = crud.delete_author(db, author_name=author_name)
    if db_author is None:
        raise HTTPException(status_code=400, detail="Author not found")


# Редагування автора
@app.put("/author/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author_update: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    db_author = crud.update_author(db, author_id=author_id, author_update=author_update)
    if db_author is None:
        raise HTTPException(status_code=400, detail="Author not found")

    return db_author


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
