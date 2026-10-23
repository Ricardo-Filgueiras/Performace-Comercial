# Dica de ferramenta: evolução do faturamento

## Para que serve

Dica de ferramenta do gráfico de área "Evolução Faturamento" da guia [Comercial](comercial.md): detalha o mês sob o mouse (*deduzido dos visuais*).

## Como ler

- Um cartão com o nome do mês, o faturamento, a meta e a porcentagem da meta.
- A página tem um filtro fixo por `dCalendario[Mes-Ano]`, que recebe o mês do ponto sobre o qual o mouse está.

## Navegação

Dica de ferramenta: não tem navegação. Aparece quando o mouse passa sobre um visual da guia [Comercial](comercial.md).

??? info "Detalhes técnicos"

    | Propriedade | Valor |
    |---|---|
    | Nome de exibição | TooltiposGrafico01 |
    | Ordem no relatório | 10 de 12 |
    | Oculta | sim (`HiddenInViewMode`) |
    | Tipo | dica de ferramenta |
    | Tamanho | 180 × 270 |
    | Identificador | `f8b9922666ba8d85bb97` |
    | Visuais | 1 (mais 0 grupos) |

    **Tipos de visual:** `cardVisual` (1).

    **Medidas usadas:** [`01 Faturamento`](../medidas-dax/01-principais.md#01-faturamento) (no relatório, pelo nome antigo `Faturamento`), [`40 Meta`](../medidas-dax/01-principais.md#40-meta) (no relatório, pelo nome antigo `Meta`), [`41 Porcentagem Meta`](../medidas-dax/01-principais.md#41-porcentagem-meta) (no relatório, pelo nome antigo `Porcentagem Meta`).

    **Colunas usadas:**

    | Tabela | Colunas |
    |---|---|
    | `dCalendario` | `Nome do Mês` |

    **Regras específicas da guia:** filtro de página fixo por `dCalendario[Mes-Ano]`.
