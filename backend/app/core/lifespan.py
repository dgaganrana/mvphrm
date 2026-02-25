from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (DB pool, queues, caches)
    print("Starting MVPHRM backend...")
    yield
    # Shutdown logic (close DB, flush queues)
    print("Shutting down MVPHRM backend...")
