from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/{filename}", response_class=FileResponse)
async def get_pdf(filename: str):
    logger.info(f"Requisição recebida para arquivo: {filename}")

    if ".." in filename or "/" in filename or "\\" in filename:
        logger.warning(f"Tentativa de acesso inválido: {filename}")
        raise HTTPException(status_code=400, detail="Nome de arquivo inválido.")

    pdf_path = os.path.join(os.path.dirname(__file__), '..', 'static', filename)

    if not os.path.exists(pdf_path):
        logger.error(f"Arquivo não encontrado: {pdf_path}")
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")

    logger.info(f"Servindo arquivo: {pdf_path}")
    return FileResponse(
        path=pdf_path,
        media_type='application/pdf',
        filename=filename,
        headers={
            "Content-Disposition": f"inline; filename={filename}"
        }
    )
