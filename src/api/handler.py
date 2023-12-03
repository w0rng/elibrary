import math

from fastapi import APIRouter, Request

from api.schemas import Response, ResponseSearch, Article
from elibrary import ELibrarySearcher
from google_scholar import GoogleSearcher

from elibrary.exceptions import CaptchaError, ELibraryProblem

router = APIRouter()


@router.get("/elibrary", response_model=Response[ResponseSearch])
async def search(request: Request, text: str, page: int = 1) -> Response[ResponseSearch]:
    log_extra: dict = request.state.log_extra
    log_extra.update({"search": text, "page": page})

    try:
        searcher = ELibrarySearcher(text, page, log_extra=log_extra)
        articles = searcher.articles()
    except CaptchaError:
        return Response[ResponseSearch](
            error="Captcha detected",
            status=500,
        )
    except ELibraryProblem:
        return Response[ResponseSearch](
            error="Server error",
            status=500,
        )

    result = []
    for article in articles:
        result.append(
            Article(
                title=article.title,
                url=article.url,
                authors=article.authors,
                date=article.date,
            )
        )
    response = ResponseSearch(
        articles=result,
        page=page,
        count_pages=math.ceil(searcher.count_articles() / 100),
        count_articles=len(result),
    )

    return Response[ResponseSearch](data=response)


@router.get("/google", response_model=Response[ResponseSearch])
async def search_all(request: Request, text: str, page: int = 1) -> Response[ResponseSearch]:
    log_extra: dict = request.state.log_extra
    log_extra.update({"search": text, "page": page})

    try:
        searcher = GoogleSearcher(text, page, log_extra=log_extra)
    except CaptchaError:
        return Response[ResponseSearch](
            error="Captcha detected",
            status=500,
        )

    articles = []
    for article in searcher.articles():
        articles.append(
            Article(
                title=article.title,
                url=article.url,
                authors=article.authors,
                date=article.date,
            )
        )
    response = ResponseSearch(
        articles=articles,
        page=page,
        count_pages=math.ceil(searcher.count_articles() / 10),
        count_articles=len(articles),
    )
    return Response[ResponseSearch](data=response)
