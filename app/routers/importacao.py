from fastapi import APIRouter
from models import WrapperRequest
from typing import Optional


router = APIRouter(prefix="/importacao", tags=["importacao"])


@router.post(
    "/vinho_de_mesa",
    summary="Retorna a listagem dos dados do ano vigente",
    description="Retorna valores para listafem dos dados do ano vigente",
)
def vinho_de_mesa(conditions: Optional[WrapperRequest] = None):
    return ""
