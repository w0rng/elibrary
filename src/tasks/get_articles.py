import math

import dramatiq

from api.schemas import Error, Article, ResponseSearch
from elibrary import ELibrarySearcher
from elibrary.exceptions import CaptchaError
from redis_client import redis


@dramatiq.actor
def get_articles(task_id: str, text: str, page: int, *, log_extra: dict):
    redis.set(task_id, "started")
    try:
        searcher = ELibrarySearcher(text, page, log_extra=log_extra)
    except CaptchaError:
        redis.set(task_id, Error(message="Captcha detected").json())
        return

    result = []
    for article in searcher.articles():
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

    redis.set(task_id, response.json())
