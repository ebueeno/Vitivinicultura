from bs4 import BeautifulSoup
import requests


def scraping_pagina(subopcao, opcao, conditions=None):
    # URL da página a ser raspada
    ano = None
    if conditions and conditions is not None:
        ano = conditions

    if ano == None or isinstance(ano, str) and ano == "todos":
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_{subopcao}&opcao=opt_{opcao}"
    elif isinstance(ano, str) and ano != "todos":
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_{opcao}&subopcao=subopt_{subopcao}"

    # Fazendo a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)

    # Verificando se a requisição foi bem-sucedida (código 200)
    if response.status_code == 200:
        # Criando um objeto BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(response.content, "html.parser")
        container = soup.find("div", class_="content_center")
        title = container.find("p").text.strip()

        # pegar o cabecalho
        thead = container.find("thead")
        cabecalho = []
        for th in thead.find_all("th"):
            th.string = th.text.strip()
            cabecalho.append(th.string)

        corpo = []
        tbody = container.find("tbody")
        for tr in tbody.find_all("tr"):
            linha = []
            for td in tr.find_all("td"):
                td.string = td.text.strip()
                linha.append(td.string)
            corpo.append(linha)

        result = []

        for tr in tbody.find_all("tr"):
            # extrai todos os <td> da linha
            valores = []
            for td in tr.find_all("td"):
                td.string = td.text.strip()
                valores.append(td.string)
            # cria o dicionário mapeando header → valor
            linha = dict(zip(cabecalho, valores))
            result.append(linha)

        # Retornando o título da página
        output = {title: result}
        return output
    else:
        return None


def lista_scraping_pagina(subopcao, opcao, conditions=None):
    ano = None
    if conditions and conditions is not None:
        ano = conditions
    con_ano = []
    if isinstance(ano, list):
        for a in ano:
            url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={a}&opcao=opt_{opcao}&subopcao=subopt_{subopcao}"
            # Fazendo a requisição HTTP para obter o conteúdo da página
            response = requests.get(url)

            # Verificando se a requisição foi bem-sucedida (código 200)
            if response.status_code == 200:
                # Criando um objeto BeautifulSoup para analisar o HTML
                soup = BeautifulSoup(response.content, "html.parser")
                container = soup.find("div", class_="content_center")
                title = container.find("p").text.strip()
                # pegar o cabecalho
                thead = container.find("thead")
                cabecalho = []
                for th in thead.find_all("th"):
                    th.string = th.text.strip()
                    cabecalho.append(th.string)

                corpo = []
                tbody = container.find("tbody")
                for tr in tbody.find_all("tr"):
                    linha = []
                    for td in tr.find_all("td"):
                        td.string = td.text.strip()
                        linha.append(td.string)
                    corpo.append(linha)

                result = []

                for tr in tbody.find_all("tr"):
                    # extrai todos os <td> da linha
                    valores = []
                    for td in tr.find_all("td"):
                        td.string = td.text.strip()
                        valores.append(td.string)
                    # cria o dicionário mapeando header → valor
                    linha = dict(zip(cabecalho, valores))
                    result.append(linha)

                # Retornando o título da página
                output = {title: result}
                con_ano.append(output)
    return con_ano
