from fastapi import FastAPI, status, Response, Path, Query, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
import typing as t

app = FastAPI()


class Book:
    def __init__(self, id: str, title: str, author: str, date_added: datetime, rating: float):
        self.id = id
        self.title = title
        self.author = author
        self.date_added = date_added
        self.rating = rating


class BookRequest(BaseModel):
    id: t.Optional[str] = Field(default=str(uuid4()))
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    date_added: datetime = Field(default_factory=datetime.utcnow)
    rating: float = Field(default=0.0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Some Title",
                    "author": "Some Author",
                    "rating": 0.0
                },
            ]
        }
    }


BOOKS = [
    Book(id="a86704fd-52a6-44cd-80a7-501b0c51e067", title="Gulliver Travels", author="Kartik Behl", date_added=datetime(2024, 1, 8, 23, 41, 9, 5889), rating=9.5),
    Book(id="c86704fd-52a6-44cd-80a7-501b0c51e076", title="Secret of Nagas", author="Amish", date_added=datetime(2024, 1, 8, 23, 41, 9, 5889), rating=9.0),
]


@app.get("/books", response_model=t.List[BookRequest], status_code=status.HTTP_200_OK)
def get_all_books():
    return BOOKS


@app.get("/books/{book_id}", response_model=BookRequest, status_code=status.HTTP_200_OK)
def get_one_by_id(book_id: str = Path(example="c86704fd-52a6-44cd-80a7-501b0c51e076")):
    matching_books = list(filter(lambda book: book.id.casefold() == book_id.casefold(), BOOKS))
    if matching_books:
        return matching_books[0]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {book_id} not found!!!")


@app.get("/books/", response_model=t.List[BookRequest], status_code=status.HTTP_200_OK)
def get_books_by_rating_or_date_added(rating: t.Optional[float] = Query(ge=0.0, lt=10.0, example=0.0, default=None), date_added: t.Optional[str] = Query(default=None, example=datetime.utcnow())):
    matching_books = []
    if rating:
        matching_books = list(filter(lambda book: book.rating == rating, BOOKS))
    if date_added:
        matching_books = list(
            filter(lambda book: book.date_added == datetime.fromisoformat(date_added), BOOKS))
    return matching_books


@app.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)


@app.put("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_book(update_book_request: BookRequest, book_id: str = Path(example="c86704fd-52a6-44cd-80a7-501b0c51e076")):
    for book_idx in range(len(BOOKS)):
        if BOOKS[book_idx].id.casefold() == book_id:
            BOOKS[book_idx] = Book(**update_book_request.model_dump())
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {book_id} not found!!!")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: str = Path(example="c86704fd-52a6-44cd-80a7-501b0c51e076")):
    for book_idx in range(len(BOOKS)):
        if BOOKS[book_idx].id.casefold() == book_id:
            BOOKS.pop(book_idx)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {book_id} not found!!!")
