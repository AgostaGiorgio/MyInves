import logging
import tomli
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.di import Container
from src.routers import router
from src.clients.orbit_client import OrbitClient
from src.config.app_config import app_config

logger = logging.getLogger(__name__)

_pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
APP_VERSION = tomli.loads(_pyproject.read_text())["tool"]["poetry"]["version"]

if app_config.orbit_api_url:
    orbit_client = OrbitClient(
        orbit_api_url=app_config.orbit_api_url,
        name="MyInves",
        version=APP_VERSION,
        description="Investment tracker",
        app_url=app_config.app_url
    )
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    if app_config.orbit_api_url:
        orbit_client.start()
        yield
        orbit_client.stop()

container = Container()
container.wire(modules=[router])

app = FastAPI(lifespan=lifespan, title="MyInves API", version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors_origins,
    allow_credentials=app_config.cors_allow_credentials,
    allow_methods=app_config.cors_allow_methods,
    allow_headers=app_config.cors_allow_headers,
)

app.include_router(router.api_router, prefix="/api/v1")