from fastapi import APIRouter
from models import WrapperRequest
from typing import Optional, List
from dependencies import scraping_pagina, lista_scraping_pagina


router = APIRouter(prefix="/importacao", tags=["importacao"])


@router.post(
    "/vinho_de_mesa",
    summary="Retorna a listagem dos dados do ano vigente",
    description="Retorna valores para listafem dos dados do ano vigente",
)
async def vinho_de_mesa(conditions: Optional[WrapperRequest] = None):
    ano = None
    if conditions and hasattr(conditions, "conditions") and conditions.conditions:
        for condition in conditions.conditions:
            if "ano" in condition:
                ano = condition["ano"]

    if isinstance(ano, list):
        print("lista na chamada")
        resultado = lista_scraping_pagina(subopcao="01", opcao="05", conditions=ano)
    else:
        print("string na chamada")
        resultado = scraping_pagina(subopcao="01", opcao="05", conditions=ano)

    # print("ano",ano)
    # print("conditions",conditions)
    return resultado
