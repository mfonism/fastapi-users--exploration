import redis.asyncio
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    RedisStrategy,
)

from ...settings import get_settings

settings = get_settings()

transport = BearerTransport(tokenUrl="auth/login")


def get_strategy() -> RedisStrategy:
    return RedisStrategy(
        redis=redis.asyncio.from_url(settings.auth_redis_url, decode_responses=True),
        lifetime_seconds=3600,
        key_prefix=settings.redis_key_prefix,
    )


backend = AuthenticationBackend(
    name="redis", transport=transport, get_strategy=get_strategy
)
