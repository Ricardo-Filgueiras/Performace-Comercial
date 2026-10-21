# Mapa Calor

## Para que serve

Mostra quando as vendas acontecem: faturamento por mês e por dia da semana, com a comparação contra o ano anterior (*deduzido dos visuais*).

## Como ler

- Uma **matriz** de mês abreviado por dia da semana, com o faturamento em cada cruzamento (o "mapa de calor").
- Um **gráfico de barras** do faturamento por mês e um **gráfico de colunas** do faturamento por dia da semana.
- Dois **gráficos de linha**: faturamento do ano atual contra o do ano anterior, mês a mês, e o mesmo comparativo acumulado no ano.
- **Filtros:** unidade, ano, mês, vendedor e forma de pagamento.

## Navegação

| Botão | Destino |
|---|---|
| Botão de menu | [Capa](capa.md) |
| Botão de menu | [Comercial](comercial.md) |
| Botão de menu | [Analítico](analitico.md) |
| Botão de menu | [Vendedores](vendedores.md) |
| Botão de marcador | marcador `MapMenuOculto` |
| Botão de marcador | marcador `MapMenuVisivel` |

Também existem: 1 botão(ões) sem ação definida, usado(s) apenas como rótulo ou moldura; 1 botão(ões) que apontam para a própria guia (indicam a guia atual no menu).

??? info "Detalhes técnicos"

    | Propriedade | Valor |
    |---|---|
    | Nome de exibição | Mapa Calor |
    | Ordem no relatório | 4 de 12 |
    | Oculta | sim (`HiddenInViewMode`) |
    | Tipo | página |
    | Tamanho | 1280 × 720 |
    | Identificador | `63e9cbba0eae4018dcf4` |
    | Visuais | 20 (mais 1 grupos) |

    **Tipos de visual:** `actionButton` (8), `slicer` (5), `image` (2), `lineChart` (2), `barChart` (1), `clusteredColumnChart` (1), `group` (1), `pivotTable` (1).

    **Medidas usadas:** [`01 Faturamento`](../medidas-dax/principais.md#01-faturamento) (no relatório, pelo nome antigo `Faturamento`), [`20 Faturamento Acumulado`](../medidas-dax/temporais.md#20-faturamento-acumulado) (no relatório, pelo nome antigo `Faturamento Acumulado`), [`21 Faturamento Acumulado LY`](../medidas-dax/temporais.md#21-faturamento-acumulado-ly) (no relatório, pelo nome antigo `Faturamento Acumulado LY`), [`22 Faturamento LY`](../medidas-dax/temporais.md#22-faturamento-ly) (no relatório, pelo nome antigo `Faturamento LY`).

    **Colunas usadas:**

    | Tabela | Colunas |
    |---|---|
    | `dCalendario` | `Ano`, `Mes Abreviado`, `Nome do Mês`, `Semana dia Nome` |
    | `dPagamento` | `Forma de Pagamento` |
    | `dUnidades` | `Unidade` |
    | `dVendedores` | `Vendedor` |

    **Regras específicas da guia:** segmentações de dados (filtros) por `Ano`, `Forma de Pagamento`, `Nome do Mês`, `Unidade`, `Vendedor`.
