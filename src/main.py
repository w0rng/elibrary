import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.handler import router
from api.schemas import Response
from logger import logger

app = FastAPI()
app.include_router(router, prefix="/search")


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request.state.log_extra = {
        "source_path": f"{request.method} {request.url.path}",
        "trace_id": request.headers.get("trace-id", str(uuid.uuid4())),
    }

    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(str(e))
        return JSONResponse(content=Response(error=str(e), status=500).dict(), status_code=500)
