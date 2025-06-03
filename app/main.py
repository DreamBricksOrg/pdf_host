from fastapi import FastAPI
from app.api import routes
from app.core.code_registry import load_used_codes
from app.core.logging_config import setup_logging
import logging
from contextlib import asynccontextmanager
from app.services.log_sender import LogSender
import app.core.parameters as param

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Aplicação iniciando...")

    load_used_codes()

    log_sender_instance = LogSender(param.LOG_API, param.LOG_PROJECT_ID, upload_delay=120)
    app.state.log_sender = log_sender_instance

    yield

    logger.info("Aplicação finalizando...")

app = FastAPI(lifespan=lifespan)

app.include_router(routes.router)
