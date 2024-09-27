from concurrent.futures import ThreadPoolExecutor
from datetime import datetime as dt
from io import BytesIO

import pandas as pd
from requests import get

from app.db.base import Base
from app.db.models.bcb_titulos_publicos import BCBTitulosPublicos
from app.db.session import Session, engine
from app.utils.dates import get_range_datas_uteis

from .config import (
    COLUNAS_BOOLEANAS,
    COLUNAS_CSV,
    COLUNAS_DATA,
    COLUNAS_DECIMAL_2_CASAS,
    COLUNAS_DECIMAL_8_CASAS,
    COLUNAS_UTEIS,
    DATA_INICIAL,
    FILTRO_TITULOS,
    TEMPLATE_CAMINHO_ARQUIVO,
    TEMPLATE_DOWNLOAD_URL,
)
from .utils import formata_numero


class Scraper:
    def __init__(self) -> None: ...

    def run(self) -> None:
        print("\nIniciando o processo de scraping...")

        datas_download = get_range_datas_uteis(DATA_INICIAL, dt.today())

        self.download_file(datas_download[0])

        with ThreadPoolExecutor() as executor:
            executor.map(self.download_file, datas_download)

        print("Processo de scraping finalizado com sucesso!\n")

    def download_file(self, data: dt) -> None:
        print(f"Baixando arquivo de: {data.strftime('%d/%m/%Y')}...")

        url = TEMPLATE_DOWNLOAD_URL.format(data=data.strftime("%Y%m%d"))

        r = get(url)

        if not r.ok:
            print("ERRO ao baixar arquivo.")
            return

        buffer = BytesIO(r.content)

        df = pd.read_csv(buffer, skiprows=1, sep=";", dtype=str, encoding="latin1")

        print("Arquivo baixado com sucesso!")

        df.columns = COLUNAS_CSV

        df["sigla_titulo"] = df["sigla_titulo"].str.strip()

        df = df[df["sigla_titulo"].isin(FILTRO_TITULOS)]
        df.reset_index(drop=True, inplace=True)

        df[COLUNAS_DATA] = df[COLUNAS_DATA].apply(pd.to_datetime, format="%Y%m%d")

        df[COLUNAS_DECIMAL_2_CASAS] = df[COLUNAS_DECIMAL_2_CASAS].map(
            lambda x: formata_numero(x, 2)
        )
        df[COLUNAS_DECIMAL_8_CASAS] = df[COLUNAS_DECIMAL_8_CASAS].map(
            lambda x: formata_numero(x, 8)
        )

        df[COLUNAS_BOOLEANAS] = df[COLUNAS_BOOLEANAS].map(
            lambda x: True if x == "S" else False
        )

        df["periodicidade_pgto_juros"] = (
            df["periodicidade_pgto_juros"].str.strip().replace("", None)
        )

        df = df[COLUNAS_UTEIS]

        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        df.to_csv(
            TEMPLATE_CAMINHO_ARQUIVO.replace("{data}", data.strftime("%Y%m%d")),
            index=False,
            sep=";",
            decimal=",",
        )

        self.atualiza_db(data, df)

    def atualiza_db(self, data_arquivo: dt, df: pd.DataFrame) -> None:
        print("Atualizando db...")

        with Session() as session:
            for row in df.itertuples():
                titulo = BCBTitulosPublicos(
                    codigo_isin=row.codigo_isin,
                    sigla_titulo=row.sigla_titulo,
                    codigo_titulo=row.codigo_titulo,
                    data_vencimento=row.data_vencimento,
                    data_primeira_emissao=row.data_primeira_emissao,
                    valor_nominal_data_base=row.valor_nominal_data_base,
                    valor_resgate=row.valor_resgate,
                    paga_cupom=row.indicador_pagamento_cupom_juros,
                    frequencia_cupom=row.periodicidade_pgto_juros,
                    taxa_cupom=row.taxa_juros,
                    updated=data_arquivo,
                )

                session.merge(titulo)
            session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    s = Scraper()
    s.run()
