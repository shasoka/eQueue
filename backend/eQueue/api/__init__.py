#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from fastapi import APIRouter

from core.config import settings
from .api_v1 import v1_router

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(v1_router)


__all__ = ("router",)
