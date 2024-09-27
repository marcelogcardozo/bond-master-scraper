from datetime import datetime as dt
from datetime import timedelta as td
from typing import List

import pandas as pd

import app.utils.dates.config as cfg


def get_calendario(data_referencia: dt):
    if data_referencia >= cfg.DATA_DECLARACAO_FERIADO_NACIONAL_CONSCIENCIA_NEGRA:
        return cfg.CALENDARIO_COM_FERIADO
    return cfg.CALENDARIO_SEM_FERIADO


def eh_dia_util(data: dt, data_referencia: dt = dt.now()) -> bool:
    """
    Verifica se a data é um dia útil no Brasil.

    Args:
        data (dt): Data a ser verificada.
        data_referencia (dt): Data de referência para a verificação do feriado da consciência negra.

    Returns:
        bool: True se a data for um dia útil, False caso contrário.

    Exemplo:
        >>> eh_dia_util(dt(2023, 7, 10))
        True
        >>> eh_dia_util(dt(2023, 7, 8))
        False
        >>> eh_dia_util(dt(2024, 11, 20), dt(2023, 12, 25))
        False
        >>> eh_dia_util(dt(2024, 11, 20), dt(2023, 12, 27))
        False
    """

    cal = get_calendario(data_referencia)

    return cal.is_working_day(data)


def get_data_util_ajustada(
    data: dt,
    data_posterior: bool = True,
    forcar_ajuste: bool = False,
    data_referencia: dt = dt.now(),
) -> dt:
    """
    Retorna a data útil ajustada para o dia útil anterior ou posterior, caso a data informada seja um feriado ou final de semana.

    Args:
        data (dt): Data a ser ajustada.
        data_posterior (bool, optional): Se True, retorna a data útil posterior. Se False, retorna a data útil anterior. Defaults to True.
        forcar_ajuste (bool, optional): Se True, força o ajuste da data útil, mesmo que a data informada seja um dia útil. Defaults to False.
        data_referencia (dt, optional): Data de referência para a verificação do feriado da consciência negra. Defaults to dt.now().

    Returns:
        dt: Data útil ajustada.

    Exemplo:
        >>> data = dt.strptime('2023-01-01', '%Y-%m-%d')
        >>> data_ajustada = get_data_util_ajustada(data, True)
        >>> data_ajustada
        datetime.datetime(2023, 1, 2, 0, 0)

        >>> data = dt.strptime('2023-01-01', '%Y-%m-%d')
        >>> data_ajustada = get_data_util_ajustada(data, False)
        >>> data_ajustada
        datetime.datetime(2022, 12, 30, 0, 0)
    """

    if eh_dia_util(data, data_referencia) and not forcar_ajuste:
        return data
    elif data_posterior:
        delta = 1
    else:
        delta = -1

    cal = get_calendario(data_referencia)
    data_ajustada = cal.add_working_days(data, delta)

    return dt.combine(data_ajustada, dt.min.time())


def get_range_datas_uteis(
    data_inicial: dt,
    data_final: dt,
    intervalo_aberto: bool = True,
    data_referencia: dt = dt.today(),
) -> List[dt]:
    """
    Retorna uma lista de datetimes com os dias úteis entre as datas de e até.

    Args:
        data_inicial (dt): Data de início.
        data_final (dt): Data de fim.
        intervalo_aberto (bool, optional): Se True, o último dia da lista será ate - 1 dia caso o último dia da lista
            seja a data_final. Defaults to True.

    Returns:
        list: Lista de datetime com os dias úteis entre as datas de e até.

    """

    dias_uteis = []
    data_loop = data_inicial

    while data_loop <= data_final:
        if eh_dia_util(data_loop, data_referencia):
            dias_uteis.append(data_loop)

        data_loop += pd.Timedelta(days=1)

    return (
        dias_uteis[:-1]
        if intervalo_aberto and dias_uteis[-1] == data_final
        else dias_uteis
    )


def get_n_ultimos_dias_uteis(
    n: int, D0: bool = False, today: dt = None, data_referencia: dt = dt.now()
) -> List[dt]:
    """
    Retorna uma lista com os n últimos dias úteis, incluindo o dia atual, se for dia útil e D0 = True.

    Args:
        n (int): Quantidade de dias úteis a serem retornados.
        D0 (bool, optional): Inclui o dia atual na lista se for útil. Defaults to False.

    Returns:
        list: Lista com os n últimos dias úteis.

    Exemplo:
        >>> get_n_ultimos_dias_uteis(5, True)
            [datetime.datetime(2023, 7, 11, 10, 21, 37, 15291), datetime.datetime(2023, 7, 10, 10, 21, 37, 15291), datetime.datetime(2023, 7, 7, 10, 21, 37, 15291), datetime.datetime(2023, 7, 6, 10, 21, 37, 15291), datetime.datetime(2023, 7, 5, 10, 21, 37, 15291), datetime.datetime(2023, 7, 4, 10, 21, 37, 15291)]
        >>> get_n_ultimos_dias_uteis(5, False)
            [datetime.datetime(2023, 7, 10, 10, 21, 37, 15291), datetime.datetime(2023, 7, 7, 10, 21, 37, 15291), datetime.datetime(2023, 7, 6, 10, 21, 37, 15291), datetime.datetime(2023, 7, 5, 10, 21, 37, 15291), datetime.datetime(2023, 7, 4, 10, 21, 37, 15291)]
    """

    data = today or dt.today()
    quantidade = n + 1 if D0 else n

    ultimas_datas_uteis = []

    if D0 and eh_dia_util(data, data_referencia):
        ultimas_datas_uteis.append(data)

    while len(ultimas_datas_uteis) < quantidade:
        data += td(days=-1)
        if eh_dia_util(data, data_referencia):
            ultimas_datas_uteis.append(data)

    return [dt.combine(data, dt.min.time()) for data in ultimas_datas_uteis]
