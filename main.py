from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from typing import List
from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.crud import pwd_context
from db.database import SessionLocal, engine
import uvicorn


models.Base.metadata.create_all(bind=engine)

# Створення екземпляру FastAPI
app = FastAPI()


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@app.post("/register/")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already registered")
    return crud.create_user(db=db, user=user)


@app.post("/token/")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_login(db, login=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": user.login, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = crud.get_user_by_login(db, login=token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


@app.get("/protected-route/")
def read_protected_data(current_user: schemas.User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.login}"}


# Створення книги
@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_current_user)):
    return crud.create_book(db=db, book=book)


# Показ книг
@app.get("/book/get-all", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


# Книги по Title
@app.get("/book/{book_title}", response_model=schemas.Book)
def read_book(book_title: str, db: Session = Depends(get_db),
              current_user: schemas.User = Depends(get_current_user)):
    db_book = crud.read_book(db, book_title=book_title)
    if db_book is None:
        raise HTTPException(status_code=400, detail="Book not found")
    return db_book


# Видалення книги
@app.delete("/book/{book_title}", response_model=schemas.Book)
def delete_book(book_title: str, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_current_user)):
    db_book = crud.delete_book(db, book_title=book_title)
    if db_book is None:
        raise HTTPException(status_code=400, detail="Book not found")
    return RedirectResponse("/books/", status_code=303)


# Редагування книги по Tittle
@app.put("/book/{book_title}", response_model=schemas.Book)
def update_book(book_title: str, book_update: schemas.BookUpdate, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_current_user)):
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
def delete_author(author_name: str, db: Session = Depends(get_db),
                  current_user: schemas.User = Depends(get_current_user)):
    db_author = crud.delete_author(db, author_name=author_name)
    if db_author is None:
        raise HTTPException(status_code=400, detail="Author not found")

    return RedirectResponse("/books/", status_code=303)


# Редагування автора
@app.put("/author/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author_update: schemas.AuthorUpdate, db: Session = Depends(get_db),
                  current_user: schemas.User = Depends(get_current_user)):
    db_author = crud.update_author(db, author_id=author_id, author_update=author_update)
    if db_author is None:
        raise HTTPException(status_code=400, detail="Author not found")

    return db_author


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
