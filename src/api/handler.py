import uuid

from fastapi import APIRouter, Request

from api.schemas import Task
from redis_client import redis
from tasks.get_articles import get_articles

router = APIRouter()


@router.get("/search")
async def search(request: Request, text: str, page: int = 1) -> Task:
    log_extra: dict = request.state.log_extra
    log_extra.update({"search": text, "page": page})

    task_id = str(uuid.uuid4())
    get_articles.send(task_id, text, page, log_extra=log_extra)

    return Task(id=task_id, status="started")


@router.get("/search/{task_id}")
async def search_result(request: Request, task_id: str) -> Task:
    log_extra: dict = request.state.log_extra
    log_extra.update({"search": task_id})

    result = redis.get(task_id)
    if not result:
        return Task(id=task_id, status="not found")

    return Task(id=task_id, status="success", result=result)


@router.get("/tasks")
async def tasks():
    return redis.keys()
