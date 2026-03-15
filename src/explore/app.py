from contextlib import asynccontextmanager

from fastapi import FastAPI

from .auth.routes import router as auth_router
from .db.config import init_db
from .settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, debug=settings.debug)

app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}
