from datetime import datetime as dt

from workalendar.america import Brazil

from app.utils.dates.brazil_calendar import BrazilFeriado

DATA_DECLARACAO_FERIADO_NACIONAL_CONSCIENCIA_NEGRA = dt(2023, 12, 26)

CALENDARIO_COM_FERIADO = BrazilFeriado()
CALENDARIO_COM_FERIADO.include_fat_tuesday = True
CALENDARIO_COM_FERIADO.fat_tuesday_label = "Carnaval"
CALENDARIO_COM_FERIADO.include_good_friday = True
CALENDARIO_COM_FERIADO.include_ash_wednesday = False
CALENDARIO_COM_FERIADO.include_corpus_christi = True
CALENDARIO_COM_FERIADO.include_easter_sunday = False
CALENDARIO_COM_FERIADO.include_clean_monday = True
CALENDARIO_COM_FERIADO.include_consciencia_negra = True

CALENDARIO_SEM_FERIADO = Brazil()
CALENDARIO_SEM_FERIADO.include_fat_tuesday = True
CALENDARIO_SEM_FERIADO.fat_tuesday_label = "Carnaval"
CALENDARIO_SEM_FERIADO.include_good_friday = True
CALENDARIO_SEM_FERIADO.include_ash_wednesday = False
CALENDARIO_SEM_FERIADO.include_corpus_christi = True
CALENDARIO_SEM_FERIADO.include_easter_sunday = False
CALENDARIO_SEM_FERIADO.include_clean_monday = True
