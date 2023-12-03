from typing import TypeVar, Generic, Optional

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


DataT = TypeVar('DataT')


class Response(BaseModel, Generic[DataT]):
    error: Optional[str] = None
    status: int = 200
    data: Optional[DataT] = None
