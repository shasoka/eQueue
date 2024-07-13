#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from api import router as api_router
from core.config import settings
from core.models import db_helper

templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> None:
    # On __aenter__ do nothing
    # After __aenter__ yield
    yield
    # On __aexit__ dispose
    await db_helper.dispose()


# noinspection PyTypeChecker
app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

# For debugger
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
)


@app.get("/", tags=["Test template for queue"])
async def get(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="queue_test.html",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)
