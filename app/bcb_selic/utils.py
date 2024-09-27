from datetime import datetime as dt

from dateutil.relativedelta import relativedelta

from .config import DATA_INICIAL


def get_range_datas():
    data_final = dt.today()
    ranges_datas = []

    if (data_final - DATA_INICIAL).days < relativedelta(years=10).days:
        return [[DATA_INICIAL, data_final]]

    for i in range(5):
        data_inicial = max(data_final.replace(year=data_final.year - 10), DATA_INICIAL)

        ranges_datas.append([data_inicial, data_final])

        data_final = data_final.replace(year=data_final.year - 10)

        if data_inicial == DATA_INICIAL:
            break

    return ranges_datas
