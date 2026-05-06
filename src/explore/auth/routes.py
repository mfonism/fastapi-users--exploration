import uuid

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers

from .backends.redis import backend as redis_backend
from .models import User, get_user_manager
from .schemas import UserCreate, UserRead, UserUpdate

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [redis_backend])


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

current_user = fastapi_users.current_user(active=True, verified=True)


@router.get("/whoami", response_model=UserRead, tags=["users"])
async def whoami(user: User = Depends(current_user)):
    return user
