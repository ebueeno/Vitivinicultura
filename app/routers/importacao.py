from fastapi import APIRouter
from models import WrapperRequest
from typing import Optional, List
from dependencies import scraping_pagina, lista_scraping_pagina


router = APIRouter(prefix="/importacao", tags=["importacao"])


@router.post(
    "/vinho_de_mesa",
    summary="Retorna a listagem dos dados do ano vigente",
    description="Retorna valores para listagem dos dados do ano vigente",
)
async def vinho_de_mesa(conditions: Optional[WrapperRequest] = None):
    ano = None

    if conditions and hasattr(conditions, "conditions") and conditions.conditions:

        for condition in conditions.conditions:
            if "ano" in condition:
                ano = condition["ano"]

    if isinstance(ano, list):
        resultado = lista_scraping_pagina(subopcao="01", opcao="05", conditions=ano)
    else:
        resultado = scraping_pagina(subopcao="01", opcao="05", conditions=ano)

    return resultado


@router.post(
    "/espumantes",
    summary="Retorna a listagem dos dados do ano vigente",
    description="Retorna valores para listagem dos dados do ano vigente",
)
async def espumantes(conditions: Optional[WrapperRequest] = None):
    ano = None
    if conditions and hasattr(conditions, "conditions") and conditions.conditions:
        for condition in conditions.conditions:
            if "ano" in condition:
                ano = condition["ano"]

    if isinstance(ano, list):
        resultado = lista_scraping_pagina(subopcao="02", opcao="05", conditions=ano)
    else:
        resultado = scraping_pagina(subopcao="02", opcao="05", conditions=ano)

    return resultado


@router.post(
    "/uvas_frescas",
    summary="Retorna a listagem dos dados do ano vigente",
    description="Retorna valores para listagem dos dados do ano vigente",
)
async def uvas_frescas(conditions: Optional[WrapperRequest] = None):
    ano = None
    if conditions and hasattr(conditions, "conditions") and conditions.conditions:
        for condition in conditions.conditions:
            if "ano" in condition:
                ano = condition["ano"]

    if isinstance(ano, list):
        resultado = lista_scraping_pagina(subopcao="03", opcao="05", conditions=ano)
    else:
        resultado = scraping_pagina(subopcao="03", opcao="05", conditions=ano)

    return resultado


@router.post(
    "/uvas_passas",
    summary="Retorna a listagem dos dados do ano vigente",
    description="Retorna valores para listagem dos dados do ano vigente",
)
async def uvas_passas(conditions: Optional[WrapperRequest] = None):
    ano = None
    if conditions and hasattr(conditions, "conditions") and conditions.conditions:
        for condition in conditions.conditions:
            if "ano" in condition:
                ano = condition["ano"]

    if isinstance(ano, list):
        resultado = lista_scraping_pagina(subopcao="04", opcao="05", conditions=ano)
    else:
        resultado = scraping_pagina(subopcao="04", opcao="05", conditions=ano)

    return resultado


@router.post(
    "/suco_de_uva",
    summary="Retorna a listagem dos dados do ano vigente",
    description="Retorna valores para listagem dos dados do ano vigente",
)
async def suco_de_uva(conditions: Optional[WrapperRequest] = None):
    ano = None
    if conditions and hasattr(conditions, "conditions") and conditions.conditions:
        for condition in conditions.conditions:
            if "ano" in condition:
                ano = condition["ano"]

    if isinstance(ano, list):
        resultado = lista_scraping_pagina(subopcao="05", opcao="05", conditions=ano)
    else:
        resultado = scraping_pagina(subopcao="05", opcao="05", conditions=ano)

    return resultado
