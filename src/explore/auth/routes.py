from fastapi import APIRouter, Depends

from .backends.redis import backend as redis_backend
from .dependencies import current_user, fastapi_users
from .models import User
from .schemas import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(redis_backend, requires_verification=True),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.get("/whoami", response_model=UserRead, tags=["users"])
async def whoami(user: User = Depends(current_user)):
    return user
