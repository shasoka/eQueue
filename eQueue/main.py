from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

from api import router as api_router
from core.config import settings
from core.models import db_helper


@asynccontextmanager
async def lifespan(_app: FastAPI) -> None:
    # On __aenter__ do nothing
    # After __aenter__ yield
    yield
    # On __aexit__ dispose
    await db_helper.dispsose()


# noinspection PyTypeChecker
app = FastAPI(
    lifespan=lifespan,
)

app.include_router(
    api_router,
    prefix=settings.api.prefix,
)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)
