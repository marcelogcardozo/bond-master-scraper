from datetime import date

from workalendar.america.brazil import WesternCalendar


class BrazilFeriado(WesternCalendar):
    "Brazil"

    FIXED_HOLIDAYS = WesternCalendar.FIXED_HOLIDAYS + (
        (4, 21, "Tiradentes' Day"),
        (9, 7, "Independence Day"),
        (10, 12, "Our Lady of Aparecida"),
        (11, 2, "All Souls' Day"),
        (11, 15, "Republic Day"),
    )
    include_sao_jose = False
    sao_jose_label = "São José"
    include_sao_pedro = False
    sao_pedro_label = "São Pedro"
    include_sao_joao = False
    sao_joao_label = "São João"
    # Civil holidays
    include_labour_day = True
    include_servidor_publico = False
    servidor_publico_label = "Dia do Servidor Público"
    # Consciência Negra day
    include_consciencia_negra = False
    # There are two dates for the Consciência Negra day
    # The most common is November, 20th
    consciencia_negra_day = (11, 20)
    consciencia_negra_label = "Consciência Negra"

    # Christian holidays
    include_easter_sunday = True
    # Dia de Nossa Senhora da Conceição is the Immaculate Conception.
    include_immaculate_conception = False
    immaculate_conception_label = "Dia de Nossa Senhora da Conceição"

    def get_variable_days(self, year):
        days = super().get_variable_days(year)
        if self.include_sao_jose:
            days.append((date(year, 3, 19), self.sao_jose_label))
        if self.include_sao_pedro:
            days.append((date(year, 6, 29), self.sao_pedro_label))
        if self.include_sao_joao:
            days.append((date(year, 6, 24), self.sao_joao_label))
        if self.include_servidor_publico:
            days.append((date(year, 10, 28), self.servidor_publico_label))
        if self.include_consciencia_negra and year >= 2024:
            month, day = self.consciencia_negra_day
            days.append((date(year, month, day), self.consciencia_negra_label))
        return days
