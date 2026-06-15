from fastapi import APIRouter, status

from .backends.redis import backend as redis_backend
from .dependencies import fastapi_users
from .email_changes.routes import router as email_changes_router
from .passwords.routes import router as passwords_router
from .schemas import (
    UserCreate,
)
from .users.routes import router as users_router
from .users.schemas import CurrentUserRead

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
router.include_router(
    fastapi_users.get_register_router(CurrentUserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(CurrentUserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(email_changes_router)
router.include_router(passwords_router)
router.include_router(users_router)
