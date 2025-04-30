from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout
import re
import logging
from fastapi import HTTPException, Body
from typing import Optional
from models import WrapperRequest

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("scraping.log", encoding="utf-8"),  # grava em arquivo
        logging.StreamHandler(),  # e também no console
    ],
)
logger = logging.getLogger(__name__)


def common_request_body():
    """
    Retorna o objeto que será injetado em openapi_extra["requestBody"]
    com o schema referenciando WrapperRequest e exemplos.
    """
    return {
        "description": "Filtro opcional de anos para a importação",
        "required": False,  # torna o body opcional
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/WrapperRequest"},
                "examples": {
                    "multiplos_anos": {
                        "summary": "Vários anos num array",
                        "value": {"conditions": [{"ano": ["2027", "2024", "2003"]}]},
                    },
                    "ano_unico": {
                        "summary": "Ano único como string",
                        "value": {"conditions": [{"ano": "2027"}]},
                    },
                },
            }
        },
    }


def valida_ano(soup):
    nav = soup.find("p", id="p_ano")
    texto = nav.find("label", class_="lbl_pesq").text.strip()
    busca = re.search(r"\[(.*?)\]", texto)
    if not busca:
        return []
    valor = busca.group(1)
    ano = valor.split("-")

    return ano


def scraping_pagina(subopcao, opcao, conditions=None):
    condit = None
    if conditions and conditions is not None:
        condit = conditions
    con_ano = []

    if isinstance(condit, str):
        ano = [condit]
    else:
        ano = condit

    for a in ano or [None]:
        if ano is not None:
            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={a}&opcao=opt_{opcao}&subopcao=subopt_{subopcao}"
        else:
            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_{subopcao}&opcao=opt_{opcao}"

        try:
            response = requests.get(url, timeout=10)

        except Timeout as e:
            logger.error("Ano %s: timeout na requisição (%s)", a, e)
            # para tudo e devolve 504
            raise HTTPException(
                status_code=504, detail=f"Timeout ao consultar o ano {a}"
            )

        except ConnectionError as e:
            logger.error("Ano %s: erro de conexão (%s)", a, e)
            # para tudo e devolve 502
            raise HTTPException(
                status_code=502, detail=f"Serviço indisponível para o ano {a}"
            )

        except HTTPError as e:
            status = getattr(e.response, "status_code", 500)
            logger.error("Ano %s: erro HTTP %s (%s)", a, status, e)
            # para tudo e devolve o próprio status retornado
            raise HTTPException(
                status_code=status, detail=f"Erro HTTP {status} ao consultar o ano {a}"
            )

        except Exception as e:
            logger.warning("Ano %s: erro inesperado (%s)", a, e)
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        try:
            if a < valida_ano(soup)[0] or a > valida_ano(soup)[1]:
                continue
        except Exception as e:
            logger.warning("Ano %s: erro ao validar ano (%s)", a, e)
            continue
        try:
            container = soup.find("div", class_="content_center")
            title = container.find("p").text.strip()

            # pegar o cabecalho
            thead = container.find("thead")
            cabecalho = []
            for th in thead.find_all("th"):
                th.string = th.text.strip()
                cabecalho.append(th.string)
        except Exception as e:
            logger.warning(
                "Ano %s: erro ao processar o HTML para recupera o cabeçalho (%s)",
                a,
                e,
            )
            continue

        try:
            corpo = []
            tbody = container.find("tbody")
            for tr in tbody.find_all("tr"):
                linha = []
                for td in tr.find_all("td"):
                    td.string = td.text.strip()
                    linha.append(td.string)
                corpo.append(linha)
        except Exception as e:
            logger.warning(
                "Ano %s: erro ao processar o HTML para recupera o corpo (%s)",
                e,
            )

        result = []
        try:
            for tr in tbody.find_all("tr"):
                valores = []
                for td in tr.find_all("td"):
                    td.string = td.text.strip()
                    valores.append(td.string)
                linha = dict(zip(cabecalho, valores))
                result.append(linha)
            tfoot = container.find("tfoot")
            rodape = []
            for tr in tfoot.find_all("tr"):

                for td in tr.find_all("td"):
                    td.string = td.text.strip()
                    rodape.append(td.string)
                rodape = dict(zip(cabecalho, rodape))
            result.append(rodape)

            output = {title: result}
            con_ano.append(output)
        except Exception as e:
            logger.warning(
                "Ano %s: erro ao processar o HTML para recupera o rodape (%s)",
                a,
                e,
            )
            continue
    logger.info("Total de anos processados: %s", len(con_ano))
    return con_ano
