# Regras de negócio

Glossário e regras de cálculo que valem para o painel inteiro, lidos do código DAX e M. Regras que só se aplicam a uma guia ficam na página dela, em [Guias do relatório](guias-do-relatorio/index.md).

Cada regra indica onde está implementada, para que dê para conferir no modelo. Quando a área de negócio confirmar uma regra, registre logo abaixo do título dela: **Validado por** <nome, área>, **em** <data>, **com o exemplo** <resultado conferido>.

!!! info "Projeto de portfólio"
    Nenhuma regra desta página foi validada por uma área de negócio, e não haverá validação: o projeto é de portfólio, com dados fictícios. As regras abaixo descrevem **o que o código faz**. O desenvolvedor confirmou que os pontos de atenção listados nesta página são intencionais.

## Glossário

| Termo | Significado (como está no modelo) | Onde |
|---|---|---|
| Venda válida | Venda cujo `Id Status` é `1` ("Válidas"). Vendas com `Id Status` `2` ("Inválidas") ficam fora dos valores | `dStatus` |
| Faturamento | Soma de `Qtde × Valor Unit` das vendas válidas | [`01 Faturamento`](medidas-dax/01-principais.md#01-faturamento) |
| Custo | Soma de `Qtde × Custo Unit` das vendas válidas | [`02 Custo`](medidas-dax/01-principais.md#02-custo) |
| Despesa | Soma de `Qtde × Despesa Unit` das vendas válidas | [`05 Despesa`](medidas-dax/01-principais.md#05-despesa) |
| Impostos | Soma de `Qtde × Impostos Unit` das vendas válidas | [`06 Impostos`](medidas-dax/01-principais.md#06-impostos) |
| Comissão | Soma de `Qtde × Comissão Unit` das vendas válidas | [`07 Comissao`](medidas-dax/01-principais.md#07-comissao) |
| Abatimento | Custo + despesa + impostos + comissão | [`08 Abatimento`](medidas-dax/01-principais.md#08-abatimento) |
| Lucro bruto | Faturamento − custo | [`03 Lucro Bruto`](medidas-dax/01-principais.md#03-lucro-bruto) |
| Margem bruta | (Faturamento − custo) ÷ faturamento | [`04 Margem Bruta`](medidas-dax/01-principais.md#04-margem-bruta) |
| Resultado | Faturamento − abatimento | [`09 Resultado`](medidas-dax/01-principais.md#09-resultado) |
| Margem (líquida) | Resultado ÷ faturamento | [`10 Margem`](medidas-dax/01-principais.md#10-margem) |
| Quantidade de vendas | Número de vendas distintas (`Num Venda`), de qualquer status | [`11 Qtde Vendas`](medidas-dax/01-principais.md#11-qtde-vendas) |
| Positivação | Quantidade de clientes (ou de produtos) distintos com venda válida no contexto | [`12 Positivação Clientes`](medidas-dax/01-principais.md#12-positivacao-clientes), [`13 Positivação Produtos`](medidas-dax/01-principais.md#13-positivacao-produtos) |
| Meta | Soma de `Valor Meta`, por vendedor e mês | [`40 Meta`](medidas-dax/01-principais.md#40-meta) |
| LY (*last year*) | Mesmo período do ano anterior | [Comparações no tempo](#comparacoes-no-tempo) |
| LM (*last month*) | Mês anterior | [Comparações no tempo](#comparacoes-no-tempo) |
| YoY (*year over year*) | Variação percentual contra o mesmo período do ano anterior | [Comparações no tempo](#comparacoes-no-tempo) |
| MoM (*month over month*) | Variação percentual contra o mês anterior | [Comparações no tempo](#comparacoes-no-tempo) |
| YTD (*year to date*) | Acumulado desde o início do ano | [`20 Faturamento Acumulado`](medidas-dax/02-temporais.md#20-faturamento-acumulado) |
| Datas com venda | Datas do calendário até a data da última venda. Usada para cortar o futuro nas comparações | `dCalendario[Datas com Venda]` |

O modelo **não define** o que cada tipo de despesa contém. A documentação anterior dizia que despesa incluía frete, logística e embalagem, e que impostos incluíam ICMS, PIS e COFINS. Nada disso está no código ou nos dados lidos pelo modelo, e por isso não foi mantido.

Por ser um projeto de portfólio, a composição de `Despesa Unit`, `Impostos Unit` e `Comissão Unit` **não é definida**: o modelo só multiplica esses valores pela quantidade. O desenvolvedor confirmou que isso é intencional.

## Vendas válidas

Todo valor financeiro do painel considera só as vendas **válidas**. A tabela `dStatus` tem dois status: `1` = Válidas e `2` = Inválidas. As medidas filtram `Id Status = 1`.

| Regra | Cálculo | Onde |
|---|---|---|
| Faturamento, custo, despesa, impostos e comissão só contam vendas válidas | `CALCULATE( ..., dStatus[Id Status] = 1 )` | `01 Faturamento`, `02 Custo`, `05 Despesa`, `06 Impostos`, `07 Comissao` |
| Positivação só conta vendas válidas | `CALCULATE( DISTINCTCOUNT(...), dStatus[Id Status] = 1 )` | `12 Positivação Clientes`, `13 Positivação Produtos` |
| **Exceção:** a quantidade de vendas conta vendas de qualquer status | `DISTINCTCOUNT( fVendas[Num Venda] )`, sem filtro de status | `11 Qtde Vendas` |
| **Exceção:** a meta não depende do status | `SUM( fMetas[Valor Meta] )` | `40 Meta` |

A quantidade de vendas (`11 Qtde Vendas`) inclui vendas inválidas, ao contrário dos valores. O desenvolvedor confirmou que isso é **intencional**. Quem comparar a quantidade com o faturamento deve saber que os dois não se referem ao mesmo conjunto de vendas.

## Faturamento, custo, despesa, impostos e comissão

Os valores unitários da planilha são multiplicados pela quantidade, linha a linha, antes de somar. Isso foi confirmado pelo desenvolvedor e conferido no código.

| Regra | Cálculo | Onde |
|---|---|---|
| Faturamento | `SUMX( fVendas, fVendas[Qtde] * fVendas[Valor Unit] )` | `01 Faturamento` |
| Custo | `SUMX( fVendas, fVendas[Qtde] * fVendas[Custo Unit] )` | `02 Custo` |
| Despesa | `SUMX( fVendas, fVendas[Qtde] * fVendas[Despesa Unit] )` | `05 Despesa` |
| Impostos | `SUMX( fVendas, fVendas[Qtde] * fVendas[Impostos Unit] )` | `06 Impostos` |
| Comissão | `SUMX( fVendas, fVendas[Qtde] * fVendas[Comissão Unit] )` | `07 Comissao` |

Todas aplicam o filtro de [vendas válidas](#vendas-validas).

## Resultado e margens

| Regra | Cálculo | Onde |
|---|---|---|
| Abatimento | `[02 Custo] + [05 Despesa] + [06 Impostos] + [07 Comissao]` | `08 Abatimento` |
| Resultado | `[01 Faturamento] - [08 Abatimento]` | `09 Resultado` |
| Margem (líquida) | `DIVIDE( [09 Resultado], [01 Faturamento], BLANK() )` | `10 Margem` |
| Lucro bruto | `[01 Faturamento] - [02 Custo]` | `03 Lucro Bruto` |
| Margem bruta | `DIVIDE( faturamento − custo, faturamento, BLANK() )` | `04 Margem Bruta` |

- As divisões usam `DIVIDE` com `BLANK()` como resultado alternativo: quando o denominador é zero, a medida fica em branco em vez de dar erro.
- As margens são razões (por exemplo, `0,25`) exibidas com formato de porcentagem. A documentação anterior descrevia a conta com "× 100"; o código não multiplica por 100.
- `03 Lucro Bruto` e `04 Margem Bruta` não são usadas em nenhum visual do relatório.

## Quantidade de vendas e positivação

| Regra | Cálculo | Onde |
|---|---|---|
| Quantidade de vendas | Contagem distinta de `Num Venda`, de qualquer status | `11 Qtde Vendas` |
| Positivação de clientes | Contagem distinta de `Id Cliente` nas vendas válidas | `12 Positivação Clientes` |
| Positivação de produtos | Contagem distinta de `Id Produto` nas vendas válidas | `13 Positivação Produtos` |

As três dependem do contexto de filtro do visual: período, vendedor, cidade e assim por diante.

## Metas

| Regra | Cálculo | Onde |
|---|---|---|
| Meta | `SUM( fMetas[Valor Meta] )`. A meta é por vendedor e mês | `40 Meta` |
| Porcentagem da meta | `DIVIDE( [01 Faturamento], [40 Meta], BLANK() )` | `41 Porcentagem Meta` |
| Diferença para a meta | `ABS( [40 Meta] - [01 Faturamento] )`. O resultado é sempre positivo | `42 Diferença Meta` |
| Cor da meta | Verde se `[41 Porcentagem Meta] >= 0,6`; vermelho se for menor que `0,10`; cinza nos demais casos | `66 Meta Cor` |

- A diferença para a meta **não diz** se o faturamento ficou acima ou abaixo da meta, porque usa valor absoluto.
- A cor usa dois limites fixos no código (60% e 10%). Entre 10% e 60%, a cor é cinza.
- `42 Diferença Meta` e `66 Meta Cor` não são usadas por outras medidas. Aparecem em visuais da guia Vendedores pelo nome antigo (ver [Nomes antigos de medidas](medidas-dax/index.md#nomes-antigos-de-medidas-no-relatorio)).

Os limites de 60% e 10% da cor da meta e o uso de valor absoluto na diferença para a meta são **intencionais** (confirmado pelo desenvolvedor).

## Comparações no tempo

As comparações usam a tabela `dCalendario` e valem para faturamento, margem, resultado e comissão.

| Regra | Cálculo | Onde |
|---|---|---|
| Mesmo período do ano anterior (LY) | `SAMEPERIODLASTYEAR( dCalendario[Id Data] )`, limitado a `dCalendario[Datas com Venda] = TRUE()` | `22 Faturamento LY`, `26 Margem LY`, `30 Resultado LY`, `33 Comissao LY` |
| Mês anterior (LM) | `DATEADD( dCalendario[Id Data], -1, MONTH )`, limitado a `Datas com Venda` | `25 Margem LM`, `29 Resultado LM` |
| Variação contra o ano anterior (YoY) | `DIVIDE( atual − LY, LY, BLANK() )` | `23 Faturamento YoY %`, `27 Margem YoY %`, `31 Resultado YoY %`, `34 Comissao YoY %` |
| Variação contra o mês anterior (MoM) | `DIVIDE( atual − LM, LM, BLANK() )` | `24 Faturamento MoM %`, `28 Margem MoM %`, `32 Resultado MoM %`, `35 Comissao MoM %` |
| Acumulado no ano (YTD) | `DATESYTD( dCalendario[Id Data] )`, limitado a `Datas com Venda` | `20 Faturamento Acumulado`, `21 Faturamento Acumulado LY` (mesmo período do ano anterior) |

- A variação da **margem** é a variação relativa entre duas razões, e não a diferença em pontos percentuais.
- O filtro `Datas com Venda` impede que meses sem venda (depois da última data de venda) entrem na comparação.
- `35 Comissao MoM %` é a única comparação de mês anterior que **não** usa o filtro `Datas com Venda`.
- O mês anterior de `24 Faturamento MoM %` é calculado dentro da própria medida, sem uma medida `LM` separada.

A diferença no filtro de `35 Comissao MoM %` é **intencional** (confirmado pelo desenvolvedor).
