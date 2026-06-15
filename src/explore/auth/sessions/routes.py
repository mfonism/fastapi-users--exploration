from fastapi import APIRouter, status

from ..backends.redis import backend as redis_backend
from ..dependencies import fastapi_users

router = APIRouter()

auth_router = fastapi_users.get_auth_router(
    redis_backend,
    requires_verification=True,
)

logout_route = next(
    (route for route in auth_router.routes if route.name == "auth:redis.logout"),
    None,
)

if logout_route:
    logout_route.status_code = status.HTTP_204_NO_CONTENT

router.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)
