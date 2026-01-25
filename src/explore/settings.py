from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()

DATA_DIR = BASE_DIR / ".data"
DATA_DIR.mkdir(exist_ok=True)

CORE_DB_URL = f"sqlite+aiosqlite:///{DATA_DIR / 'db.sqlite'}"
AUTH_REDIS_URL = "redis://localhost:6379/0"
