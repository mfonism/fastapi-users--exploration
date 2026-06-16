from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_users.router.common import ErrorCode

from .auth.exceptions import UserDeleted
from .auth.routes import router as auth_router
from .db.config import init_db
from .exceptions import AppAPIError
from .settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, debug=settings.debug)

app.include_router(auth_router)


@app.exception_handler(AppAPIError)
async def app_api_error_exception_handler(request: Request, exc: AppAPIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(UserDeleted)
async def user_deleted_exception_handler(request: Request, exc: UserDeleted):
    return JSONResponse(
        status_code=400,
        content={"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
    )


@app.get("/health")
def health():
    return {"status": "ok"}
