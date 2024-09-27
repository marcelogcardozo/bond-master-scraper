from decimal import Decimal


def formata_numero(numero: str, casas_decimais: int):
    if int(numero) == 0:
        return None

    return Decimal(f"{numero[:-casas_decimais]}.{numero[-casas_decimais:]}")
