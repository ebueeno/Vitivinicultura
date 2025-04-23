from bs4 import BeautifulSoup
import requests


def scraping_pagina(subopcao, opcao):
    # URL da página a ser raspada
    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_{subopcao}&opcao=opt_{opcao}'
    
    # Fazendo a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    
    # Verificando se a requisição foi bem-sucedida (código 200)
    if response.status_code == 200:
        # Criando um objeto BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrando o elemento desejado (exemplo: título da página)
        title = soup.title.string
        
        # Retornando o título da página
        return title
    else:
        return None