# Medidas DAX

Catálogo das medidas do modelo, com uma página para cada **pasta de exibição** que já existe no `.tmdl`. As medidas sem pasta ficam em [Sem pasta de exibição](sem-pasta.md). Medidas de teste e sem uso em visuais estão listadas no [Arquivo](../arquivo/index.md).

Para cada medida: tabela onde está, formato, guias em que aparece, de quais medidas depende, quais medidas a usam e o código DAX copiado do modelo.

| Pasta de exibição | Medidas | Página |
|---|---:|---|
| `01.Principais` | 16 | [Principais](principais.md) |
| `02. Temporais` | 16 | [Temporais](temporais.md) |
| `03. Formatações` | 2 | [Formatações](formatacoes.md) |
| `.Visuais SVG` | 7 | [Visuais SVG](visuais-svg.md) |
| *Sem pasta de exibição* | 9 | [Sem pasta de exibição](sem-pasta.md) |
| **Total** | **50** | |

As medidas ficam em duas tabelas: `_Medidas` (44) e `zMetricas` (6).

## Todas as medidas

| Medida | Pasta de exibição |
|---|---|
| [`01 Faturamento`](principais.md#01-faturamento) | `01.Principais` |
| [`02 Custo`](principais.md#02-custo) | `01.Principais` |
| [`03 Lucro Bruto`](principais.md#03-lucro-bruto) | `01.Principais` |
| [`04 Margem Bruta`](principais.md#04-margem-bruta) | `01.Principais` |
| [`05 Despesa`](principais.md#05-despesa) | `01.Principais` |
| [`06 Impostos`](principais.md#06-impostos) | `01.Principais` |
| [`07 Comissao`](principais.md#07-comissao) | `01.Principais` |
| [`08 Abatimento`](principais.md#08-abatimento) | `01.Principais` |
| [`09 Resultado`](principais.md#09-resultado) | `01.Principais` |
| [`10 Margem`](principais.md#10-margem) | `01.Principais` |
| [`11 Qtde Vendas`](principais.md#11-qtde-vendas) | `01.Principais` |
| [`12 Positivação Clientes`](principais.md#12-positivacao-clientes) | `01.Principais` |
| [`13 Positivação Produtos`](principais.md#13-positivacao-produtos) | `01.Principais` |
| [`20 Faturamento Acumulado`](temporais.md#20-faturamento-acumulado) | `02. Temporais` |
| [`21 Faturamento Acumulado LY`](temporais.md#21-faturamento-acumulado-ly) | `02. Temporais` |
| [`22 Faturamento LY`](temporais.md#22-faturamento-ly) | `02. Temporais` |
| [`23 Faturamento YoY %`](temporais.md#23-faturamento-yoy) | `02. Temporais` |
| [`24 Faturamento MoM %`](temporais.md#24-faturamento-mom) | `02. Temporais` |
| [`25 Margem LM`](temporais.md#25-margem-lm) | `02. Temporais` |
| [`26 Margem LY`](temporais.md#26-margem-ly) | `02. Temporais` |
| [`27 Margem YoY %`](temporais.md#27-margem-yoy) | `02. Temporais` |
| [`28 Margem MoM %`](temporais.md#28-margem-mom) | `02. Temporais` |
| [`29 Resultado LM`](temporais.md#29-resultado-lm) | `02. Temporais` |
| [`30 Resultado LY`](temporais.md#30-resultado-ly) | `02. Temporais` |
| [`31 Resultado YoY %`](temporais.md#31-resultado-yoy) | `02. Temporais` |
| [`32 Resultado MoM %`](temporais.md#32-resultado-mom) | `02. Temporais` |
| [`33 Comissao LY`](temporais.md#33-comissao-ly) | `02. Temporais` |
| [`34 Comissao YoY %`](temporais.md#34-comissao-yoy) | `02. Temporais` |
| [`35 Comissao MoM %`](temporais.md#35-comissao-mom) | `02. Temporais` |
| [`40 Meta`](principais.md#40-meta) | `01.Principais` |
| [`41 Porcentagem Meta`](principais.md#41-porcentagem-meta) | `01.Principais` |
| [`42 Diferença Meta`](principais.md#42-diferenca-meta) | `01.Principais` |
| [`50 Eixo Y max Grafico Comercial`](formatacoes.md#50-eixo-y-max-grafico-comercial) | `03. Formatações` |
| [`51 Faturamento formatação de texto`](formatacoes.md#51-faturamento-formatacao-de-texto) | `03. Formatações` |
| [`52 Rank Cidade`](sem-pasta.md#52-rank-cidade) | *sem pasta* |
| [`53 Max Y Visual 01 pg Vendedores`](sem-pasta.md#53-max-y-visual-01-pg-vendedores) | *sem pasta* |
| [`54 Nome Vendedor`](sem-pasta.md#54-nome-vendedor) | *sem pasta* |
| [`60 SVG Cartao Faturamento v1`](visuais-svg.md#60-svg-cartao-faturamento-v1) | `.Visuais SVG` |
| [`61 SVG Cartao Margem v1`](visuais-svg.md#61-svg-cartao-margem-v1) | `.Visuais SVG` |
| [`62 SVG Cartao Resultado v1`](visuais-svg.md#62-svg-cartao-resultado-v1) | `.Visuais SVG` |
| [`63 SVG Cartao Comissao v1`](visuais-svg.md#63-svg-cartao-comissao-v1) | `.Visuais SVG` |
| [`64 SVG Tabela HTML Content Lite v1`](visuais-svg.md#64-svg-tabela-html-content-lite-v1) | `.Visuais SVG` |
| [`65 SVG Percentual Meta Velocimetro`](visuais-svg.md#65-svg-percentual-meta-velocimetro) | `.Visuais SVG` |
| [`66 Meta Cor`](visuais-svg.md#66-meta-cor) | `.Visuais SVG` |
| [`Context Medida z`](sem-pasta.md#context-medida-z) | *sem pasta* |
| [`Linha Anterior`](sem-pasta.md#linha-anterior) | *sem pasta* |
| [`Linha Atual`](sem-pasta.md#linha-atual) | *sem pasta* |
| [`Seta para Cima`](sem-pasta.md#seta-para-cima) | *sem pasta* |
| [`Seta para baixo  ( limit Inferior )`](sem-pasta.md#seta-para-baixo-limit-inferior) | *sem pasta* |
| [`Seta para baixo  ( limit sup )`](sem-pasta.md#seta-para-baixo-limit-sup) | *sem pasta* |

## Nomes antigos de medidas no relatório

O modelo renomeou as medidas com prefixo numérico (por exemplo, `Faturamento` virou `01 Faturamento`) no commit `23c7839`, de 02/02/2026. A maior parte dos visuais do relatório ainda aponta para o nome antigo. A tabela mostra cada nome antigo, a medida atual correspondente (inferida pelo nome) e as guias em que aparece.

| Nome no relatório | Medida atual (inferida) | Guias |
|---|---|---|
| `Abatimento` | `08 Abatimento` | [Analítico](../guias-do-relatorio/analitico.md), [Analítico antes](../arquivo/guias-anteriores.md) |
| `cartao  faturamento svg v1` | `60 SVG Cartao Faturamento v1` | [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md) |
| `cartao  margem svg v1` | `61 SVG Cartao Margem v1` | [Comercial](../guias-do-relatorio/comercial.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md) |
| `cartao  resultado svg v1` | `62 SVG Cartao Resultado v1` | [Comercial](../guias-do-relatorio/comercial.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md) |
| `cartao comissao svg v1` | `63 SVG Cartao Comissao v1` | [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md) |
| `Comissao` | `07 Comissao` | [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md) |
| `Diferença Meta` | `42 Diferença Meta` | [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md) |
| `Eixo Y max Grafico Comercial` | `50 Eixo Y max Grafico Comercial` | [Comercial](../guias-do-relatorio/comercial.md), [Comercial antes](../arquivo/guias-anteriores.md) |
| `Faturamento` | `01 Faturamento` | [Comercial](../guias-do-relatorio/comercial.md), [Analítico](../guias-do-relatorio/analitico.md), [Mapa Calor](../guias-do-relatorio/mapa-calor.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Analítico antes](../arquivo/guias-anteriores.md), [Mapa Calor antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md), [TooltiposGrafico01](../guias-do-relatorio/dica-evolucao-faturamento.md), [TooltiposTabela](../guias-do-relatorio/dica-tabela-vendedores.md) |
| `Faturamento Acumulado` | `20 Faturamento Acumulado` | [Mapa Calor](../guias-do-relatorio/mapa-calor.md), [Mapa Calor antes](../arquivo/guias-anteriores.md) |
| `Faturamento Acumulado LY` | `21 Faturamento Acumulado LY` | [Mapa Calor](../guias-do-relatorio/mapa-calor.md), [Mapa Calor antes](../arquivo/guias-anteriores.md) |
| `Faturamento LY` | `22 Faturamento LY` | [Mapa Calor](../guias-do-relatorio/mapa-calor.md), [Mapa Calor antes](../arquivo/guias-anteriores.md) |
| `Faturamento MoM %` | `24 Faturamento MoM %` | [Comercial](../guias-do-relatorio/comercial.md), [Comercial antes](../arquivo/guias-anteriores.md) |
| `Margem` | `10 Margem` | [Comercial](../guias-do-relatorio/comercial.md), [Analítico](../guias-do-relatorio/analitico.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Analítico antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md) |
| `max Y visual 01 pg Vendedores` | `53 Max Y Visual 01 pg Vendedores` | [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md) |
| `Meta` | `40 Meta` | [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md), [TooltiposGrafico01](../guias-do-relatorio/dica-evolucao-faturamento.md) |
| `Meta Cor` | `66 Meta Cor` | [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md) |
| `nome vendedor` | `54 Nome Vendedor` | [TooltipRosca](../guias-do-relatorio/dica-gerente-vendedores.md) |
| `Porcentagem Meta` | `41 Porcentagem Meta` | [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md), [TooltiposGrafico01](../guias-do-relatorio/dica-evolucao-faturamento.md), [TooltiposTabela](../guias-do-relatorio/dica-tabela-vendedores.md) |
| `Positivação Clientes` | `12 Positivação Clientes` | [Analítico](../guias-do-relatorio/analitico.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Analítico antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md) |
| `Positivação Produtos` | `13 Positivação Produtos` | [Analítico](../guias-do-relatorio/analitico.md), [Analítico antes](../arquivo/guias-anteriores.md) |
| `Qtde Vendas` | `11 Qtde Vendas` | [Analítico](../guias-do-relatorio/analitico.md), [Analítico antes](../arquivo/guias-anteriores.md) |
| `rank cidade` | `52 Rank Cidade` | [Comercial](../guias-do-relatorio/comercial.md), [Comercial antes](../arquivo/guias-anteriores.md) |
| `Resultado` | `09 Resultado` | [Analítico](../guias-do-relatorio/analitico.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Analítico antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md) |
| `tabela hml contente lite v1` | `64 SVG Tabela HTML Content Lite v1` | [Comercial antes](../arquivo/guias-anteriores.md) |

!!! pendente "Relatório com nomes antigos de medidas"
    25 nomes de medida usados em visuais do relatório não existem no modelo atual. Isso aparece no Power BI como campo não encontrado. As páginas desta documentação ligam cada nome antigo à medida atual pelo nome, mas essa ligação é uma dedução. Confirme abrindo o relatório no Power BI Desktop e, se for o caso, reaponte os visuais para as medidas atuais.
