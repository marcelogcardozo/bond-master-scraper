import re
from datetime import datetime as dt
from io import BytesIO

import pandas as pd
from requests import get

from app.anbima_vna.config import DE_PARA_COLUNAS, TEMPLATE_DOWNLOAD_URL
from app.db.base import Base
from app.db.models.anbima_vna import ANBIMAVNA
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

        df_vna_historico = pd.DataFrame()

        print("Buscando dados de:")

        for data in datas:
            print(f"\t{data.strftime('%d/%m/%Y')} - ", end="")

            url = TEMPLATE_DOWNLOAD_URL.replace("[ddmmyyyy]", data.strftime("%d%m%Y"))

            r = get(url)
            r.raise_for_status()

            if not r.ok:
                print("ERRO")
                continue

            print("OK")

            search_dt = re.search(r"Data de Referência :  (\d{2}/\d{2}/\d{4})", r.text)

            if search_dt is not None:
                data_referencia = dt.strptime(search_dt.groups(0)[0], "%d/%m/%Y")
            else:
                raise ValueError("Data de referência não encontrada.")

            buffer = BytesIO(r.content)
            df = pd.read_csv(
                buffer,
                skiprows=7,
                sep=";",
                decimal=",",
                thousands=".",
                encoding="latin1",
            )
            df["data"] = data_referencia

            df_vna_historico = pd.concat([df_vna_historico, df], ignore_index=True)

        self.df_vna_historico = df_vna_historico

    def formatar_dados(self) -> None:
        print("Formatando dados...")

        self.df_vna_historico = self.df_vna_historico.filter(
            items=DE_PARA_COLUNAS.keys(), axis=1
        )
        self.df_vna_historico.rename(columns=DE_PARA_COLUNAS, inplace=True)

        print("Dados formatados com sucesso!")

    def atualiza_db(self) -> None:
        print("Atualizando banco de dados...")

        with Session() as s:
            for row in self.df_vna_historico.itertuples(index=False):
                titulo = row.titulo
                codigo_selic = row.codigo_selic
                data = row.data
                vna = row.vna

                registro = ANBIMAVNA(
                    titulo=titulo,
                    codigo_selic=codigo_selic,
                    data=data,
                    vna=vna,
                    updated=dt.now(),
                )

                s.merge(registro)

            s.commit()

        print("Banco de dados atualizado com sucesso!")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    s = Scraper()
    s.run()
