from pydantic import BaseModel, Field


# Створення Моделі
class BookBase(BaseModel):
    title: str
    pages: int = Field(..., gt=10)
    author: str = Field(..., min_length=3, max_length=30)


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
