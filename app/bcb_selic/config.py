import os
from datetime import datetime as dt

MINIMA_DATA_DADOS_SELIC = dt(1986, 6, 4)

data_inicial_param = os.environ.get("DATA_INICIAL")

DATA_INICIAL = (
    dt.strptime(data_inicial_param, "%d/%m/%Y")
    if data_inicial_param is not None
    else MINIMA_DATA_DADOS_SELIC
)

DOWNLOAD_URL = "https://www3.bcb.gov.br/novoselic/rest/taxaSelicApurada/pub/search?parametrosOrdenacao=%5B%5D&page=1&pageSize=200000"

TEMPLATE_PAYLOAD = '{"dataInicial":"{de}","dataFinal":"{ate}"}'  # %d/%m/%Y

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/json;charset=UTF-8",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-dtpc": "-7$327342404_206h38vUMARUTWJUMFHMLQHAJECCPCIBDUDFGBF-0e0",
    "x-requested-with": "XMLHttpRequest",
}


COLUNAS_CSV = [
    "id",
    "data_cotacao",
    "fator_diario",
    "media",
    "mediana",
    "moda",
    "desvio_padrao",
    "indice_curtose",
    "financeiro",
    "qtd_operacoes",
    "taxa_anual",
]
