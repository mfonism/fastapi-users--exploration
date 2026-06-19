from fastapi import APIRouter

from .dependencies import fastapi_users
from .email_changes.routes import router as email_changes_router
from .passwords.routes import router as passwords_router
from .reactivation.routes import router as reactivation_router
from .sessions.routes import router as sessions_router
from .users.routes import router as users_router
from .users.schemas import CurrentUserRead, UserCreate

router = APIRouter()

router.include_router(sessions_router)
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
router.include_router(reactivation_router)
router.include_router(users_router)
