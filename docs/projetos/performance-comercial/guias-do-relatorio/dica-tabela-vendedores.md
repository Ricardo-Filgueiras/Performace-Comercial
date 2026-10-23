# Dica de ferramenta: tabela de vendedores

## Para que serve

Dica de ferramenta das cidades e dos produtos da guia [Comercial](comercial.md): lista os vendedores com faturamento, margem e porcentagem da meta (*deduzido dos visuais*).

## Como ler

- Uma tabela com vendedor, faturamento, margem e porcentagem da meta.
- A página tem um filtro fixo por `dCalendario[Mes-Ano]`.

## Navegação

Dica de ferramenta: não tem navegação. Aparece quando o mouse passa sobre um visual da guia [Comercial](comercial.md).

??? info "Detalhes técnicos"

    | Propriedade | Valor |
    |---|---|
    | Nome de exibição | TooltiposTabela |
    | Ordem no relatório | 12 de 12 |
    | Oculta | sim (`HiddenInViewMode`) |
    | Tipo | dica de ferramenta |
    | Tamanho | 430 × 450 |
    | Identificador | `268e7edaf0b9edd4e1db` |
    | Visuais | 2 (mais 0 grupos) |

    **Tipos de visual:** `actionButton` (1), `tableEx` (1).

    **Medidas usadas:** [`01 Faturamento`](../medidas-dax/01-principais.md#01-faturamento) (no relatório, pelo nome antigo `Faturamento`), [`10 Margem`](../medidas-dax/01-principais.md#10-margem), [`41 Porcentagem Meta`](../medidas-dax/01-principais.md#41-porcentagem-meta) (no relatório, pelo nome antigo `Porcentagem Meta`).

    **Colunas usadas:**

    | Tabela | Colunas |
    |---|---|
    | `dVendedores` | `Vendedor` |

    **Regras específicas da guia:** filtro de página fixo por `dCalendario[Mes-Ano]`.
