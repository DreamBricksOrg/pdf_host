from fastapi import FastAPI
from app.api import routes
from app.core.logging_config import setup_logging
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Aplicação iniciando...")

    yield

    logger.info("Aplicação finalizando...")

app = FastAPI(lifespan=lifespan)

app.include_router(routes.router)
