#  Copyright (c) 2024 Arkady Schoenberg <shasoka@yandex.ru>

from core.config import settings

proxies = {
    "http": settings.proxy.http,
    "https": settings.proxy.https,
}
