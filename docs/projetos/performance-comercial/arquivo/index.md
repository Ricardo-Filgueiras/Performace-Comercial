# Arquivo

O que existe no projeto, mas não está em uso ou não é oficial. Continua documentado para consulta, sem disputar atenção com o que está em uso.

## Guias ocultas e rascunhos

| Guia | Situação | Página |
|---|---|---|
| Comercial antes | versão anterior, mantida de propósito | [Guias anteriores](guias-anteriores.md) |
| Analítico antes | versão anterior, mantida de propósito | [Guias anteriores](guias-anteriores.md) |
| Mapa Calor antes | versão anterior, mantida de propósito | [Guias anteriores](guias-anteriores.md) |
| Vendedores antes | versão anterior, mantida de propósito | [Guias anteriores](guias-anteriores.md) |

As outras guias ocultas (Comercial, Analítico, Mapa Calor, Vendedores e as três dicas de ferramenta) **estão em uso** e ficam em [Guias do relatório](../guias-do-relatorio/index.md). "Oculta" nesse caso só quer dizer que a guia não aparece na barra de guias.

## Medidas de teste

Não há medidas de teste no modelo. A faixa de numeração 90 a 99 está reservada para testes e desenvolvimento, mas nenhuma medida a usa (ver [Guia do desenvolvedor](../guia-do-desenvolvedor.md#nomes)).

## Medidas sem uso em visuais

Medidas que nenhum visual do relatório usa diretamente: **19** das 50. Uma medida sem visual pode ser a base de outra que aparece no relatório, por isso a tabela diz se ela chega a algum visual por meio de outras medidas.

A conta considera os nomes antigos usados nos visuais (por exemplo, `Qtde Vendas` no lugar de `11 Qtde Vendas`), ligados à medida atual pelo nome (ver [Nomes antigos de medidas](../medidas-dax/index.md#nomes-antigos-de-medidas-no-relatorio)). O script de levantamento não reconhece esses nomes e por isso lista 21 medidas sem uso; esta página descarta as que o relatório usa pelo nome antigo.

| Medida | Tabela | Usada por outra medida? | Chega a algum visual? |
|---|---|---|---|
| [`02 Custo`](../medidas-dax/principais.md#02-custo) | `_Medidas` | `03 Lucro Bruto`, `04 Margem Bruta`, `08 Abatimento` | sim, por outras medidas |
| [`03 Lucro Bruto`](../medidas-dax/principais.md#03-lucro-bruto) | `_Medidas` | não | **não** |
| [`04 Margem Bruta`](../medidas-dax/principais.md#04-margem-bruta) | `_Medidas` | não | **não** |
| [`05 Despesa`](../medidas-dax/principais.md#05-despesa) | `_Medidas` | `08 Abatimento` | sim, por outras medidas |
| [`06 Impostos`](../medidas-dax/principais.md#06-impostos) | `_Medidas` | `08 Abatimento` | sim, por outras medidas |
| [`23 Faturamento YoY %`](../medidas-dax/temporais.md#23-faturamento-yoy) | `_Medidas` | `60 SVG Cartao Faturamento v1` | sim, por outras medidas |
| [`25 Margem LM`](../medidas-dax/temporais.md#25-margem-lm) | `_Medidas` | `28 Margem MoM %` | **não** |
| [`26 Margem LY`](../medidas-dax/temporais.md#26-margem-ly) | `_Medidas` | `27 Margem YoY %` | sim, por outras medidas |
| [`27 Margem YoY %`](../medidas-dax/temporais.md#27-margem-yoy) | `_Medidas` | `61 SVG Cartao Margem v1`, `64 SVG Tabela HTML Content Lite v1` | sim, por outras medidas |
| [`28 Margem MoM %`](../medidas-dax/temporais.md#28-margem-mom) | `_Medidas` | não | **não** |
| [`29 Resultado LM`](../medidas-dax/temporais.md#29-resultado-lm) | `_Medidas` | `32 Resultado MoM %` | **não** |
| [`30 Resultado LY`](../medidas-dax/temporais.md#30-resultado-ly) | `_Medidas` | `31 Resultado YoY %` | sim, por outras medidas |
| [`31 Resultado YoY %`](../medidas-dax/temporais.md#31-resultado-yoy) | `_Medidas` | `62 SVG Cartao Resultado v1` | sim, por outras medidas |
| [`32 Resultado MoM %`](../medidas-dax/temporais.md#32-resultado-mom) | `_Medidas` | não | **não** |
| [`33 Comissao LY`](../medidas-dax/temporais.md#33-comissao-ly) | `_Medidas` | `34 Comissao YoY %` | sim, por outras medidas |
| [`34 Comissao YoY %`](../medidas-dax/temporais.md#34-comissao-yoy) | `_Medidas` | `63 SVG Cartao Comissao v1` | sim, por outras medidas |
| [`35 Comissao MoM %`](../medidas-dax/temporais.md#35-comissao-mom) | `_Medidas` | não | **não** |
| [`51 Faturamento formatação de texto`](../medidas-dax/formatacoes.md#51-faturamento-formatacao-de-texto) | `_Medidas` | `64 SVG Tabela HTML Content Lite v1` | sim, por outras medidas |
| [`65 SVG Percentual Meta Velocimetro`](../medidas-dax/visuais-svg.md#65-svg-percentual-meta-velocimetro) | `_Medidas` | não | **não** |

### Sem nenhum uso

Estas 8 medidas não aparecem em nenhum visual, nem direta nem indiretamente: `03 Lucro Bruto`, `04 Margem Bruta`, `25 Margem LM`, `28 Margem MoM %`, `29 Resultado LM`, `32 Resultado MoM %`, `35 Comissao MoM %`, `65 SVG Percentual Meta Velocimetro`.

Elas continuam no modelo e na documentação, e é decisão do desenvolvedor mantê-las ou removê-las. Nenhuma foi removida.

## Outros itens sem uso

| Item | Situação |
|---|---|
| Relacionamento inativo `fVendas[Data Envio]` para `dCalendario[Id Data]` | Nenhuma medida usa `USERELATIONSHIP`. O desenvolvedor decidiu mantê-lo ([ADR-010](../decisoes-tecnicas.md#adr-010-manter-o-relacionamento-inativo-por-data-envio)) |
| `data/Metas/Catalogo.pdf` e a pasta `data/imagens/` | Estão no repositório, mas nenhuma consulta do modelo os lê ([Fontes de dados](../fontes-de-dados.md#consultas-sem-uso-aparente)) |
| Colunas `Nome Vendedor`, `Nome Cliente`, `Nome Unidade`, `Faturamento Total` e `Custo Total` da planilha de vendas | A consulta de `fVendas` as descarta |
