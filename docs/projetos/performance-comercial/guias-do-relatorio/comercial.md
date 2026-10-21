# Comercial

## Para que serve

Visão geral do desempenho comercial: quanto se faturou, com que resultado e margem, como isso evoluiu no tempo e como se distribui por gerente, produto e cidade (*deduzido dos visuais*).

## Como ler

- **Cartões de resumo:** faturamento, resultado e margem, cada um com a variação contra o ano anterior desenhada por uma medida SVG, com seta e cor.
- **Evolução Faturamento:** gráfico de área do faturamento ao longo do tempo. Ao passar o mouse, a dica de ferramenta [evolução do faturamento](dica-evolucao-faturamento.md) mostra mês, faturamento, meta e porcentagem da meta.
- **Rosca por gerente:** faturamento por gerente. A dica de ferramenta [gerente e vendedores](dica-gerente-vendedores.md) compara o faturamento atual com o do ano anterior.
- **Barras por produto:** faturamento por categoria, produto e subcategoria. A dica de ferramenta [tabela de vendedores](dica-tabela-vendedores.md) detalha por vendedor.
- **Cidades:** uma tabela personalizada em HTML/SVG, que mostra faturamento abreviado e variação da margem por cidade (e alterna os dois ao passar o mouse), mais duas tabelas por cidade: uma com cidade e faturamento e outra com cidade, faturamento e margem. Botões com marcadores alternam entre as visões de ranking e de desempenho por cidade.
- **Filtros:** unidade, ano, mês, vendedor e forma de pagamento.

## Navegação

| Botão | Destino |
|---|---|
| Botão de menu | [Capa](capa.md) |
| Botão de menu | [Analítico](analitico.md) |
| Botão de menu | [Mapa Calor](mapa-calor.md) |
| Botão de menu | [Vendedores](vendedores.md) |
| Botão de marcador | marcador **inexistente** `b665145e7737d486954d` |
| Botão de marcador | marcador `GeralCidadesTab` |
| Botão de marcador | marcador `MenuComInVisivel01` |
| Botão de marcador | marcador `MenuComVisivel01` |
| Botão de marcador | marcador `RankCidVisivel` |

Também existem: 2 botão(ões) sem ação definida, usado(s) apenas como rótulo ou moldura; 1 botão de navegação sem página de destino definida.

??? info "Detalhes técnicos"

    | Propriedade | Valor |
    |---|---|
    | Nome de exibição | Comercial |
    | Ordem no relatório | 2 de 12 |
    | Oculta | sim (`HiddenInViewMode`) |
    | Tipo | página |
    | Tamanho | 1280 × 720 |
    | Identificador | `98d137a6b23a0f270828` |
    | Visuais | 26 (mais 4 grupos) |

    **Tipos de visual:** `actionButton` (13), `slicer` (5), `group` (4), `tableEx` (2), `areaChart` (1), `cardVisual` (1), `clusteredBarChart` (1), `donutChart` (1), `htmlContent443BE3AD55E043BF878BED274D3A6865` (1), `image` (1).

    **Medidas usadas:** [`01 Faturamento`](../medidas-dax/principais.md#01-faturamento) (no relatório, pelo nome antigo `Faturamento`), [`09 Resultado`](../medidas-dax/principais.md#09-resultado), [`10 Margem`](../medidas-dax/principais.md#10-margem) (no relatório, pelo nome antigo `Margem`), [`24 Faturamento MoM %`](../medidas-dax/temporais.md#24-faturamento-mom) (no relatório, pelo nome antigo `Faturamento MoM %`), [`50 Eixo Y max Grafico Comercial`](../medidas-dax/formatacoes.md#50-eixo-y-max-grafico-comercial) (no relatório, pelo nome antigo `Eixo Y max Grafico Comercial`), [`60 SVG Cartao Faturamento v1`](../medidas-dax/visuais-svg.md#60-svg-cartao-faturamento-v1), [`61 SVG Cartao Margem v1`](../medidas-dax/visuais-svg.md#61-svg-cartao-margem-v1) (no relatório, pelo nome antigo `cartao  margem svg v1`), [`62 SVG Cartao Resultado v1`](../medidas-dax/visuais-svg.md#62-svg-cartao-resultado-v1) (no relatório, pelo nome antigo `cartao  resultado svg v1`), [`64 SVG Tabela HTML Content Lite v1`](../medidas-dax/visuais-svg.md#64-svg-tabela-html-content-lite-v1).

    **Colunas usadas:**

    | Tabela | Colunas |
    |---|---|
    | `dCalendario` | `Ano`, `Dia`, `Mes Abreviado`, `Nome do Mês` |
    | `dClientes` | `Cidade` |
    | `dPagamento` | `Forma de Pagamento` |
    | `dProdutos` | `Categoria`, `Produto`, `Subcategoria` |
    | `dUnidades` | `Unidade` |
    | `dVendedores` | `Gerente`, `Vendedor` |

    **Regras específicas da guia:** segmentações de dados (filtros) por `Ano`, `Forma de Pagamento`, `Nome do Mês`, `Unidade`, `Vendedor`; dicas de ferramenta usadas: [TooltipRosca](dica-gerente-vendedores.md), [TooltiposGrafico01](dica-evolucao-faturamento.md), [TooltiposTabela](dica-tabela-vendedores.md).
