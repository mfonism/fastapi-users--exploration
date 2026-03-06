import asyncio
import time
from .config import ensure_database


def main() -> None:
    start = time.perf_counter()
    asyncio.run(ensure_database())
    end = time.perf_counter()
    print(f"Database is ready ✅ (took {(end - start):.2f}s)")
