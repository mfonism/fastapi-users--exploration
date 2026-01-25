from pathlib import Path

from pydantic import SecretStr

BASE_DIR = Path(__file__).parent.parent.resolve()

DATA_DIR = BASE_DIR / ".data"
DATA_DIR.mkdir(exist_ok=True)

CORE_DB_URL = f"sqlite+aiosqlite:///{DATA_DIR / 'db.sqlite'}"
AUTH_REDIS_URL = "redis://localhost:6379/0"

RESET_PASSWORD_TOKEN_SECRET = SecretStr("EXPLORE: RESET PASSWORD TOKEN SECRET")
VERIFICATION_TOKEN_SECRET = SecretStr("EXPLORE: VERIFICATION TOKEN SECRET")
