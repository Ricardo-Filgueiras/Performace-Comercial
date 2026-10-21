# Vendedores

## Para que serve

Desempenho de um vendedor (escolhido no filtro): valores, meta e evolução diária (*deduzido dos visuais*).

## Como ler

- **Foto do vendedor:** um cartão exibe a imagem do endereço guardado em `dVendedores[URL Foto]`.
- **Cartões de resumo:** comissão, faturamento, margem e resultado.
- **Meta:** um cartão com a meta e a diferença para a meta, e um visual personalizado (infográfico) com faturamento, porcentagem da meta e a cor da meta (verde, vermelho ou cinza, conforme [as regras de metas](../regras-de-negocio.md#metas)).
- **Evolução diária:** três gráficos de linha (faturamento, comissão e positivação de clientes por dia) e um de colunas (resultado por dia).
- **Filtros:** unidade, ano, mês, vendedor e forma de pagamento.

## Navegação

| Botão | Destino |
|---|---|
| Botão de menu | [Capa](capa.md) |
| Botão de menu | [Comercial](comercial.md) |
| Botão de menu | [Analítico](analitico.md) |
| Botão de menu | [Mapa Calor](mapa-calor.md) |
| Botão de marcador | marcador `VendMenuOculto` |
| Botão de marcador | marcador `VendMenuVisivel` |

Também existem: 1 botão(ões) sem ação definida, usado(s) apenas como rótulo ou moldura; 1 botão(ões) que apontam para a própria guia (indicam a guia atual no menu).

??? info "Detalhes técnicos"

    | Propriedade | Valor |
    |---|---|
    | Nome de exibição | Vendedores |
    | Ordem no relatório | 5 de 12 |
    | Oculta | sim (`HiddenInViewMode`) |
    | Tipo | página |
    | Tamanho | 1280 × 720 |
    | Identificador | `690519eebc3669f09dfa` |
    | Visuais | 22 (mais 1 grupos) |

    **Tipos de visual:** `actionButton` (8), `slicer` (5), `cardVisual` (3), `lineChart` (3), `clusteredColumnChart` (1), `group` (1), `image` (1), `pureVizInfographicC9801BF222134D2D83FA9C41861F3482` (1).

    **Medidas usadas:** [`01 Faturamento`](../medidas-dax/principais.md#01-faturamento) (no relatório, pelo nome antigo `Faturamento`), [`07 Comissao`](../medidas-dax/principais.md#07-comissao) (no relatório, pelo nome antigo `Comissao`), [`09 Resultado`](../medidas-dax/principais.md#09-resultado) (no relatório, pelo nome antigo `Resultado`), [`10 Margem`](../medidas-dax/principais.md#10-margem) (no relatório, pelo nome antigo `Margem`), [`12 Positivação Clientes`](../medidas-dax/principais.md#12-positivacao-clientes) (no relatório, pelo nome antigo `Positivação Clientes`), [`40 Meta`](../medidas-dax/principais.md#40-meta) (no relatório, pelo nome antigo `Meta`), [`41 Porcentagem Meta`](../medidas-dax/principais.md#41-porcentagem-meta) (no relatório, pelo nome antigo `Porcentagem Meta`), [`42 Diferença Meta`](../medidas-dax/principais.md#42-diferenca-meta) (no relatório, pelo nome antigo `Diferença Meta`), [`53 Max Y Visual 01 pg Vendedores`](../medidas-dax/sem-pasta.md#53-max-y-visual-01-pg-vendedores) (no relatório, pelo nome antigo `max Y visual 01 pg Vendedores`), [`60 SVG Cartao Faturamento v1`](../medidas-dax/visuais-svg.md#60-svg-cartao-faturamento-v1) (no relatório, pelo nome antigo `cartao  faturamento svg v1`), [`61 SVG Cartao Margem v1`](../medidas-dax/visuais-svg.md#61-svg-cartao-margem-v1) (no relatório, pelo nome antigo `cartao  margem svg v1`), [`62 SVG Cartao Resultado v1`](../medidas-dax/visuais-svg.md#62-svg-cartao-resultado-v1) (no relatório, pelo nome antigo `cartao  resultado svg v1`), [`63 SVG Cartao Comissao v1`](../medidas-dax/visuais-svg.md#63-svg-cartao-comissao-v1) (no relatório, pelo nome antigo `cartao comissao svg v1`), [`66 Meta Cor`](../medidas-dax/visuais-svg.md#66-meta-cor) (no relatório, pelo nome antigo `Meta Cor`).

    **Colunas usadas:**

    | Tabela | Colunas |
    |---|---|
    | `dCalendario` | `Ano`, `Dia`, `Nome do Mês` |
    | `dPagamento` | `Forma de Pagamento` |
    | `dUnidades` | `Unidade` |
    | `dVendedores` | `URL Foto`, `Vendedor` |

    **Regras específicas da guia:** segmentações de dados (filtros) por `Ano`, `Forma de Pagamento`, `Nome do Mês`, `Unidade`, `Vendedor`.
