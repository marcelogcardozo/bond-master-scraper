from decimal import Decimal
from io import BytesIO
from urllib.parse import quote_plus

import pandas as pd
from requests import post

from app.anbima_parametros_ettj.config import (
    COLUNAS_CSV,
    DOWNLOAD_URL,
    HEADERS,
    TEMPLATE_PAYLOAD,
)
from app.db.base import Base
from app.db.models.anbima_parametros_ettj import ANBIMAParametrosETTJ
from app.db.session import Session, engine
from app.utils.dates import get_n_ultimos_dias_uteis


class Scraper:
    def __init__(self) -> None: ...

    def run(self) -> None:
        print("\nIniciando o processo de scraping...")

        self.download_file()
        self.formatar_dados()
        self.atualiza_db()

        print("Processo de scraping finalizado com sucesso!\n")

    def download_file(self) -> None:
        datas = get_n_ultimos_dias_uteis(5, D0=True)

        df_parametros_historico = pd.DataFrame()

        print("Buscando dados de:")

        for data in datas:
            print(f"\t{data.strftime('%d/%m/%Y')} - ", end="")

            payload = TEMPLATE_PAYLOAD.replace(
                "{data}", quote_plus(data.strftime("%d/%m/%Y"))
            )

            r = post(DOWNLOAD_URL, headers=HEADERS, data=payload)

            if not r.ok:
                print("ERRO")
                continue

            print("OK")

            buffer = BytesIO(r.content)
            df_curva = pd.read_csv(buffer, sep=";", encoding="latin1")

            df_parametros = df_curva.loc[:1].copy()
            df_parametros["Data"] = data

            df_parametros.rename(
                columns={data.strftime("%d/%m/%Y"): "Nome Taxa"}, inplace=True
            )

            df_parametros_historico = pd.concat(
                [df_parametros_historico, df_parametros], ignore_index=True
            )

        self.df_parametros_historico = df_parametros_historico

    def formatar_dados(self) -> None:
        print("Formatando dados...")

        self.df_parametros_historico.columns = COLUNAS_CSV

        colunas_float = [
            col
            for col in self.df_parametros_historico.columns
            if col not in ("nome_taxa", "data")
        ]

        self.df_parametros_historico[colunas_float] = self.df_parametros_historico[
            colunas_float
        ].map(lambda x: Decimal(str(x).replace(",", ".")) if pd.notnull(x) else None)

        print("Dados formatados com sucesso!")

    def atualiza_db(self) -> None:
        print("Atualizando banco de dados...")

        with Session() as s:
            for row in self.df_parametros_historico.itertuples(index=False):
                data = row.data
                nome_taxa = row.nome_taxa
                beta1 = row.beta1
                beta2 = row.beta2
                beta3 = row.beta3
                beta4 = row.beta4
                lambda1 = row.lambda1
                lambda2 = row.lambda2

                registro = ANBIMAParametrosETTJ(
                    data=data,
                    nome_taxa=nome_taxa,
                    beta1=beta1,
                    beta2=beta2,
                    beta3=beta3,
                    beta4=beta4,
                    lambda1=lambda1,
                    lambda2=lambda2,
                )

                s.merge(registro)

            s.commit()

        print("Banco de dados atualizado com sucesso!")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    s = Scraper()
    s.run()
