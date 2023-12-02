from typing import Optional, Any

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    url: str
    authors: list[str]
    date: str


class ResponseSearch(BaseModel):
    page: int
    count_pages: int
    count_articles: int
    articles: list[Article]


class Error(BaseModel):
    message: str


class Task(BaseModel):
    id: str
    status: str
    result: Optional[Any] = None
