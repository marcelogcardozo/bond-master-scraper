# Bond Master Scraper

Este projeto é uma ferramenta de web scraping para coletar dados essenciais utilizados no cálculo de preços de títulos públicos para serem utilizados na aplicação [Bond Master](https://github.com/marcelogcardozo/bond-master). Os dados são extraídos de várias fontes, como ANBIMA e Banco Central do Brasil, e são organizados em módulos específicos.

## Módulos

- **anbima_ettj/**: Realiza o scraping dos parâmetros da Estrutura a Termo da Taxa de Juros (ETTJ) da ANBIMA.
- **anbima_vna/**: Realiza o scraping do Valor Nominal Atualizado (VNA) da ANBIMA.
- **bcb_selic/**: Realiza o scraping da Taxa SELIC disponibilizada pelo Banco Central do Brasil.
- **bcb_titulos_publicos/**: Realiza o scraping dos dados de títulos públicos no Banco Central do Brasil.

Cada um desses módulos possui um README detalhado com informações sobre a fonte dos dados e os tipos de informações extraídas.

## Como Usar

1. Clone este repositório.
2. Instalar as dependências:
   ```bash
   poetry install
   ```
3. Executar os módulos dessa forma:
   ```bash
   poetry run python -m app.anbima_parametros_ettj.scraper
   ```
