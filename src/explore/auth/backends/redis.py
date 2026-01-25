import redis.asyncio
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    RedisStrategy,
)

from ... import settings

transport = BearerTransport(tokenUrl="auth/redis/login")


def get_strategy() -> RedisStrategy:
    return RedisStrategy(
        redis=redis.asyncio.from_url(settings.AUTH_REDIS_URL, decode_responses=True),
        lifetime_seconds=3600,
    )


backend = AuthenticationBackend(
    name="redis", transport=transport, get_strategy=get_strategy
)
