#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from fastapi import APIRouter

from core.config import settings

from .users import router as users_router
from .groups import router as groups_router
from .workspaces import router as workspaces_router
from .subjects import router as subjects_router
from .queue_websocket import router as websocket_router

v1_router = APIRouter(prefix=settings.api.v1.prefix)

v1_router.include_router(
    users_router,
    prefix=settings.api.v1.users_prefix,
)

v1_router.include_router(
    groups_router,
    prefix=settings.api.v1.groups_prefix,
)

v1_router.include_router(
    workspaces_router,
    prefix=settings.api.v1.workspaces_prefix,
)

v1_router.include_router(
    subjects_router,
    prefix=settings.api.v1.subjects_prefix,
)

v1_router.include_router(
    websocket_router,
    prefix=settings.api.v1.websocket_prefix,
)
