DOWNLOAD_URL = "https://www.anbima.com.br/informacoes/est-termo/CZ-down.asp"

TEMPLATE_PAYLOAD = "Idioma=PT&Dt_Ref={data}&saida=csv"

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "priority": "u=0, i",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}

COLUNAS_CSV = [
    "nome_taxa",
    "beta1",
    "beta2",
    "beta3",
    "beta4",
    "lambda1",
    "lambda2",
    "data",
]
