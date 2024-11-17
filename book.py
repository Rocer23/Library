from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

# Створення екземпляру FastAPI
app = FastAPI()


# Створення Моделі
class Book(BaseModel):
    # id: Optional[UUID] = None
    title: str
    pages: int = Field(..., gt=10)
    author: str = Field(..., min_length=3, max_length=30)


library = []


# Створення книги
@app.post("/books/", response_model=Book)
def create_book(book: Book):
    library.append(book)
    return book


# Показ книг
@app.get("/books/", response_model=List[Book])
def read_books():
    return library


# Книги по Title
@app.get("/books/{book_title}", response_model=Book)
def read_book(title: Book):
    for book in library:
        if book.title == title:
            return book

    raise HTTPException(status_code=400, detail="Book not found")


# Показ книг по автору
@app.get("/books/author/{author}", response_model=List[Book])
def get_books_on_author(author: str):
    books_by_author = [book for book in library if book.author == author]
    if not books_by_author:
        raise HTTPException(status_code=400, detail="Author not found")
    return books_by_author


# Редагування книги по Title
@app.put("/books/{book_title}", response_model=Book)
def update_book(title: Book, book_update: Book):
    for idx, book in enumerate(library):
        if book.title == title:
            updated_book = book.copy(update=book_update.dict(exclude_unset=True))
            library[idx] = updated_book
            return updated_book

    raise HTTPException(status_code=400, detail="Book not found")


# Видалення книги
@app.delete("/books/{book_title}", response_model=Book)
def delete_book(title: Book):
    for idx, book in enumerate(library):
        if book.title == title:
            return library.pop(idx)

    raise HTTPException(status_code=400, detail="Book not found")
