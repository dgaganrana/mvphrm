import importlib
import pkgutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.lifespan import lifespan
from app.core.config import settings
from app.core.logging import setup_logging, app_logger
from app.core.middleware import LoggingMiddleware
import app.api as api_pkg

# Setup logging
setup_logging()

app = FastAPI(
    title="MVPHRM Backend",
    lifespan=lifespan
)

# Add logging middleware first (so it wraps all other middleware)
app.add_middleware(LoggingMiddleware)

# Add CORS middleware using Settings
origins = [
    settings.FRONTEND_URL,
    settings.FRONTEND_URL_PROD,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dynamically discover and register all routers in app/api
for _, module_name, _ in pkgutil.iter_modules(api_pkg.__path__):
    module = importlib.import_module(f"app.api.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)
