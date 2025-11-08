from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from uvicorn import run

from api import auth_router, prices_router
from core.exceptions.auth import InvalidCredentials
from core.exceptions.base import ClientError
from settings import settings
from utils.configure_logger import configure_logger
from utils.seeding.init_registry import init_registry

configure_logger(
    logger_root_name=__name__, logger_prefix_output="NEXORA FASTAPI BACKEND"
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_registry()
    yield


app = FastAPI(
    title=settings.swagger_title,
    debug=settings.debug,
    lifespan=lifespan,
)

router = APIRouter(prefix="/api")
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(prices_router, prefix="/prices", tags=["Prices"])
app.include_router(router)


@app.get("/health", tags=["Healthcheck"])
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        f'http://{settings.cms_panel_domain}',
        f'http://{settings.cms_backend_domain}',
        f'http://{settings.main_site_domain}',
        f'https://{settings.cms_panel_domain}',
        f'https://{settings.cms_backend_domain}',
        f'https://{settings.main_site_domain}',
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ClientError)
def client_error_handler(_: Request, exc: ClientError) -> JSONResponse:
    return JSONResponse({"detail": str(exc)}, status_code=400)


@app.exception_handler(InvalidCredentials)
def invalid_token_error_handler(_: Request, exc: InvalidCredentials) -> JSONResponse:
    return JSONResponse({"detail": str(exc)}, status_code=401)


if __name__ == "__main__":
    run(
        "main:app",
        host="0.0.0.0",
        reload=settings.debug,
        workers=settings.workers,
    )
