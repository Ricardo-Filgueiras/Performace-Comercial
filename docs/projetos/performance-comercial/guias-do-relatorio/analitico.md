# Analítico

## Para que serve

Detalhamento dos números em uma matriz, para consulta linha a linha por cidade, estado, subcategoria e unidade (*deduzido dos visuais*).

## Como ler

- Uma **matriz** com as dimensões cidade, estado, subcategoria e unidade e sete indicadores: abatimento, faturamento, margem, positivação de clientes, positivação de produtos, quantidade de vendas e resultado.
- **Filtros:** unidade, ano, mês, vendedor e forma de pagamento.

## Navegação

| Botão | Destino |
|---|---|
| Botão de menu | [Capa](capa.md) |
| Botão de menu | [Comercial](comercial.md) |
| Botão de menu | [Mapa Calor](mapa-calor.md) |
| Botão de menu | [Vendedores](vendedores.md) |
| Botão de marcador | marcador `AnaMenuOculto` |
| Botão de marcador | marcador `AnaMenuVisivel` |

Também existem: 1 botão(ões) sem ação definida, usado(s) apenas como rótulo ou moldura; 1 botão(ões) que apontam para a própria guia (indicam a guia atual no menu).

??? info "Detalhes técnicos"

    | Propriedade | Valor |
    |---|---|
    | Nome de exibição | Analítico |
    | Ordem no relatório | 3 de 12 |
    | Oculta | sim (`HiddenInViewMode`) |
    | Tipo | página |
    | Tamanho | 1280 × 720 |
    | Identificador | `91dc89d8077e5d4c9ee1` |
    | Visuais | 15 (mais 1 grupos) |

    **Tipos de visual:** `actionButton` (8), `slicer` (5), `group` (1), `image` (1), `pivotTable` (1).

    **Medidas usadas:** [`01 Faturamento`](../medidas-dax/01-principais.md#01-faturamento) (no relatório, pelo nome antigo `Faturamento`), [`08 Abatimento`](../medidas-dax/01-principais.md#08-abatimento) (no relatório, pelo nome antigo `Abatimento`), [`09 Resultado`](../medidas-dax/01-principais.md#09-resultado) (no relatório, pelo nome antigo `Resultado`), [`10 Margem`](../medidas-dax/01-principais.md#10-margem) (no relatório, pelo nome antigo `Margem`), [`11 Qtde Vendas`](../medidas-dax/01-principais.md#11-qtde-vendas) (no relatório, pelo nome antigo `Qtde Vendas`), [`12 Positivação Clientes`](../medidas-dax/01-principais.md#12-positivacao-clientes) (no relatório, pelo nome antigo `Positivação Clientes`), [`13 Positivação Produtos`](../medidas-dax/01-principais.md#13-positivacao-produtos) (no relatório, pelo nome antigo `Positivação Produtos`).

    **Colunas usadas:**

    | Tabela | Colunas |
    |---|---|
    | `dCalendario` | `Ano`, `Nome do Mês` |
    | `dClientes` | `Cidade`, `Estado` |
    | `dPagamento` | `Forma de Pagamento` |
    | `dProdutos` | `Subcategoria` |
    | `dUnidades` | `Unidade` |
    | `dVendedores` | `Vendedor` |

    **Regras específicas da guia:** segmentações de dados (filtros) por `Ano`, `Forma de Pagamento`, `Nome do Mês`, `Unidade`, `Vendedor`.
