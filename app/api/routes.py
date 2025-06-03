from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
import os
import logging
from app.core.code_registry import is_code_used, mark_code_used

from app.utils.log_sender_middleware import get_log_sender


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{code}/{projectid}/{filename}", response_class=FileResponse)
async def get_pdf(code: str, projectid: str, filename: str, request: Request):
    logger.info(f"Requisição recebida para arquivo: {filename} | Código: {code} | Projeto: {projectid}")

    if ".." in filename or "/" in filename or "\\" in filename:
        logger.warning(f"Tentativa de acesso inválido: {filename}")
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido.")

    pdf_path = os.path.join(os.path.dirname(__file__), '..', 'static', filename)

    if not os.path.exists(pdf_path):
        logger.error(f"Arquivo não encontrado: {pdf_path}")
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")

    if not is_code_used(projectid, code):
        get_log_sender(request).log(projectid, "ACESSOU_QRCODE", code)
        mark_code_used(projectid, code)
        logger.info(f"Log registrado para código: {code}")
    else:
        logger.info(f"Código {code} já foi utilizado para o projeto {projectid}, log ignorado.")

    return FileResponse(
        path=pdf_path,
        media_type='application/pdf',
        filename=filename,
        headers={"Content-Disposition": f"inline; filename={filename}"}
    )
