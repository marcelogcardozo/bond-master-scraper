from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from requests import post

from app.bcb_selic.config import COLUNAS_CSV, DOWNLOAD_URL, HEADERS, TEMPLATE_PAYLOAD
from app.bcb_selic.utils import get_range_datas
from app.db.base import Base
from app.db.models.bcb_selic import BCBSelic
from app.db.session import Session, engine


class Scraper:
    def __init__(self) -> None:
        self.df_historico = pd.DataFrame()

    def run(self) -> None:
        print("\nIniciando o processo de scraping...")
        print("Threads de busca:")

        ranges_datas = get_range_datas()

        with ThreadPoolExecutor() as executor:
            executor.map(self.download_file, enumerate(ranges_datas))

        self.formatar_dados()
        self.atualiza_db()

        print("Processo de scraping finalizado com sucesso!\n")

    def download_file(self, iterable) -> None:
        index, range_busca = iterable

        de, ate = range_busca

        print(
            f"\t[Thread {index}] Baixando arquivo de: {de.strftime('%d/%m/%Y')} até {ate.strftime('%d/%m/%Y')}..."
        )

        payload = TEMPLATE_PAYLOAD.replace("{de}", de.strftime("%d/%m/%Y")).replace(
            "{ate}", ate.strftime("%d/%m/%Y")
        )

        r = post(DOWNLOAD_URL, headers=HEADERS, data=payload)

        if not r.ok:
            print(f"\t[Thread {index}] ERRO ao baixar arquivo.")
            return

        registros = r.json()["registros"]

        df = pd.DataFrame(registros)
        df.columns = COLUNAS_CSV

        df["data_cotacao"] = pd.to_datetime(df["data_cotacao"], format="%d/%m/%Y")

        self.df_historico = pd.concat([self.df_historico, df])

        print(f"\t[Thread {index}] Arquivo baixado com sucesso!")

    def formatar_dados(self) -> None:
        print("Formatando dados...")

        self.df_historico.sort_values(
            by=["data_cotacao", "fator_diario"], ascending=True, inplace=True
        )
        self.df_historico.drop_duplicates(
            subset=["data_cotacao"], keep="last", inplace=True
        )

        self.df_historico = self.df_historico[self.df_historico["fator_diario"] > 0.0]

        self.df_historico.drop(columns=["id"], inplace=True)

        print("Dados formatados com sucesso!")

    def atualiza_db(self) -> None:
        print("Atualizando banco de dados...")
        with Session() as s:
            for row in self.df_historico.itertuples(index=False):
                data_cotacao = row.data_cotacao
                fator_diario = float(row.fator_diario)
                taxa_anual = float(row.taxa_anual)

                registro = BCBSelic(
                    data=data_cotacao, fator_diario=fator_diario, taxa_anual=taxa_anual
                )

                s.merge(registro)

            s.commit()

        print("Banco de dados atualizado com sucesso!")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    s = Scraper()
    s.run()
