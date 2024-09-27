import os
from datetime import datetime as dt

from app.utils.dates import get_n_ultimos_dias_uteis

data_inicial_param = os.environ.get("DATA_INICIAL")

DATA_INICIAL = (
    dt.strptime(data_inicial_param, "%d/%m/%Y")
    if data_inicial_param is not None
    else get_n_ultimos_dias_uteis(n=5)[-1]
)


TEMPLATE_DOWNLOAD_URL = "https://www3.bcb.gov.br/novoselic/rest/arquivosDiarios/pub/download/4/{data}ASEL007"  # %Y%m%d

PASTA_ARQUIVOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
TEMPLATE_CAMINHO_ARQUIVO = os.path.join(PASTA_ARQUIVOS, "{data}.csv")

FILTRO_TITULOS = [
    "LTN",  # Letra do Tesouro Nacional
    "NTN-B",  # Nota do Tesouro Nacional série B
    # "NTN-C", # Nota do Tesouro Nacional série C
    "NTN-F",  # Nota do Tesouro Nacional série F
    "LFT",  # Letra Financeira do Tesouro
]

COLUNAS_CSV = [
    "tipo_registro",
    "codigo_titulo",
    "data_vencimento",
    "codigo_isin",
    "sigla_titulo",
    "ind_possibilidade_negociacao",
    "ind_bloqueio",
    "data_primeira_emissao",
    "posicao_geral_custodia",
    "tipo_rendimento",
    "valor_resgate",
    "data_base",
    "valor_nominal_data_base",
    "indice_atualizacao_valor_nominal",
    "indicador_pagamento_cupom_juros",
    "periodicidade_pgto_juros",
    "taxa_juros",
    "regime_capitalizacao_juros",
    "indicador_possibilidade_desmembramento",
    "preco_unitario_pagamento_juros",
    "indicador_amortizacao_principal",
    "periodicidade_amortizacao",
    "percentual_amortizacao",
    "numero_parcelas",
    "preco_unitario_pagamento_amortizacao",
    "preco_unitario_lastro_550",
    "valor_nominal_atualizado",
    "preco_unitario_retorno_resgate",
    "preco_unitario_pagamento_resgate",
    "data_base_juros",
]

COLUNAS_DATA = [
    "data_vencimento",
    "data_primeira_emissao",
    # "data_base",
    # "data_base_juros",
]

COLUNAS_DECIMAL_8_CASAS = [
    "valor_resgate",
    "valor_nominal_data_base",
    "preco_unitario_pagamento_juros",
    "preco_unitario_pagamento_amortizacao",
    "preco_unitario_lastro_550",
    "valor_nominal_atualizado",
    "preco_unitario_retorno_resgate",
    "preco_unitario_pagamento_resgate",
]

COLUNAS_DECIMAL_2_CASAS = [
    "taxa_juros",
]

COLUNAS_BOOLEANAS = [
    "indicador_pagamento_cupom_juros",
]

COLUNAS_UTEIS = [
    "codigo_isin",
    "sigla_titulo",
    "codigo_titulo",
    "data_primeira_emissao",
    "data_vencimento",
    "valor_nominal_data_base",
    "valor_resgate",
    "indicador_pagamento_cupom_juros",
    "periodicidade_pgto_juros",
    "taxa_juros",
]
