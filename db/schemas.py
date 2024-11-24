from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    author: str = Field(..., min_length=3, max_length=30)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


# Створення Моделі
class BookBase(BaseModel):
    title: str
    pages: int = Field(..., gt=10)


class BookCreate(BookBase):
    author_name: str


class BookDelete(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int
    author: Author

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
