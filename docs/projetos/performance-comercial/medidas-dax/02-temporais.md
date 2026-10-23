<!-- pasta: 02. Temporais -->
# 02. Temporais

<!-- gerado:inicio resumo -->
Medidas da pasta de exibição `02. Temporais`: **16**. Veja o [catálogo](index.md) para as outras pastas.
<!-- gerado:fim resumo -->

## 20 Faturamento Acumulado

Faturamento acumulado desde o início do ano até a data (YTD), limitado às datas até a última venda. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)
- **Observação:** Usa `dCalendario[Datas com Venda]`, que marca as datas até a última venda (ver [Modelo de dados](../modelo-de-dados.md)).

<!-- gerado:inicio medida:20 Faturamento Acumulado -->
- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento)
- **É usada por:** nenhuma medida

```dax
    CALCULATE(
        [01 Faturamento],
        CALCULATETABLE(
            DATESYTD(dCalendario[Id Data]),
            dCalendario[Datas com Venda] = TRUE()
        )
    )
```
<!-- gerado:fim medida:20 Faturamento Acumulado -->

## 21 Faturamento Acumulado LY

Faturamento acumulado no ano, no mesmo período do ano anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:21 Faturamento Acumulado LY -->
- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento)
- **É usada por:** nenhuma medida

```dax
    CALCULATE(
        [01 Faturamento],
        CALCULATETABLE(
            DATESYTD( SAMEPERIODLASTYEAR( dCalendario[Id Data]) ),
            dCalendario[Datas com Venda] = TRUE()
        )
    )
```
<!-- gerado:fim medida:21 Faturamento Acumulado LY -->

## 22 Faturamento LY

Faturamento do mesmo período do ano anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:22 Faturamento LY -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento)
- **É usada por:** [`23 Faturamento YoY %`](#23-faturamento-yoy), [`Context Medida z`](sem-pasta.md#context-medida-z), [`Linha Anterior`](sem-pasta.md#linha-anterior), [`Seta para Cima`](sem-pasta.md#seta-para-cima), [`Seta para baixo  ( limit Inferior )`](sem-pasta.md#seta-para-baixo-limit-inferior), [`Seta para baixo  ( limit sup )`](sem-pasta.md#seta-para-baixo-limit-sup)

```dax
CALCULATE(
    [01 Faturamento],
    CALCULATETABLE(
        SAMEPERIODLASTYEAR( dCalendario[Id Data] ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```
<!-- gerado:fim medida:22 Faturamento LY -->

## 23 Faturamento YoY %

Variação percentual Year-over-Year do Faturamento

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:23 Faturamento YoY % -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento), [`22 Faturamento LY`](#22-faturamento-ly)
- **É usada por:** [`60 SVG Cartao Faturamento v1`](visuais-svg.md#60-svg-cartao-faturamento-v1)

```dax
// Variação Year over Year do Faturamento
VAR FaturamentoAtual = [01 Faturamento]
VAR FaturamentoLY = [22 Faturamento LY]

RETURN 
    DIVIDE(
        FaturamentoAtual - FaturamentoLY,
        FaturamentoLY,
        BLANK()
    )
```
<!-- gerado:fim medida:23 Faturamento YoY % -->

## 24 Faturamento MoM %

Variação percentual Month-over-Month do Faturamento

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)
- **Observação:** O mês anterior é calculado dentro da própria medida, sem uma medida `LM` separada.

<!-- gerado:inicio medida:24 Faturamento MoM % -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento)
- **É usada por:** nenhuma medida

```dax
// Variação Month over Month do Faturamento
VAR FaturamentoAtual = [01 Faturamento]
VAR FaturamentoLM = 
    CALCULATE(
        [01 Faturamento],
        CALCULATETABLE(
            DATEADD(dCalendario[Id Data], -1, MONTH),
            dCalendario[Datas com Venda] = TRUE()
        )
    )

RETURN 
    DIVIDE(
        FaturamentoAtual - FaturamentoLM,
        FaturamentoLM,
        BLANK()
    )
```
<!-- gerado:fim medida:24 Faturamento MoM % -->

## 25 Margem LM

Margem líquida do mês anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:25 Margem LM -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`10 Margem`](01-principais.md#10-margem)
- **É usada por:** [`28 Margem MoM %`](#28-margem-mom)

```dax
CALCULATE(
    [10 Margem],
    CALCULATETABLE(
        DATEADD( dCalendario[Id Data], -1, MONTH ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```
<!-- gerado:fim medida:25 Margem LM -->

## 26 Margem LY

Margem líquida do mesmo período do ano anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:26 Margem LY -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`10 Margem`](01-principais.md#10-margem)
- **É usada por:** [`27 Margem YoY %`](#27-margem-yoy)

```dax
CALCULATE(
    [10 Margem],
    CALCULATETABLE(
        SAMEPERIODLASTYEAR( dCalendario[Id Data] ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```
<!-- gerado:fim medida:26 Margem LY -->

## 27 Margem YoY %

Variação percentual da margem líquida em relação ao mesmo período do ano anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)
- **Observação:** É a variação **relativa** entre duas margens (a diferença dividida pela margem do ano anterior), e não a diferença em pontos percentuais.

<!-- gerado:inicio medida:27 Margem YoY % -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`10 Margem`](01-principais.md#10-margem), [`26 Margem LY`](#26-margem-ly)
- **É usada por:** [`61 SVG Cartao Margem v1`](visuais-svg.md#61-svg-cartao-margem-v1), [`64 SVG Tabela HTML Content Lite v1`](visuais-svg.md#64-svg-tabela-html-content-lite-v1)

```dax
VAR MargemAtual = [10 Margem]
VAR MargemLY = [26 Margem LY]

RETURN 
    DIVIDE(
        MargemAtual - MargemLY,
        MargemLY,
        BLANK()
    )
```
<!-- gerado:fim medida:27 Margem YoY % -->

## 28 Margem MoM %

Variação percentual da margem líquida em relação ao mês anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:28 Margem MoM % -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`10 Margem`](01-principais.md#10-margem), [`25 Margem LM`](#25-margem-lm)
- **É usada por:** nenhuma medida

```dax
VAR MargemAtual = [10 Margem]
VAR MargemLM = [25 Margem LM]

RETURN 
    DIVIDE(
        MargemAtual - MargemLM,
        MargemLM,
        BLANK()
    )
```
<!-- gerado:fim medida:28 Margem MoM % -->

## 29 Resultado LM

Resultado do mês anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:29 Resultado LM -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`09 Resultado`](01-principais.md#09-resultado)
- **É usada por:** [`32 Resultado MoM %`](#32-resultado-mom)

```dax
CALCULATE(
    [09 Resultado],
    CALCULATETABLE(
        DATEADD( dCalendario[Id Data], -1, MONTH ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```
<!-- gerado:fim medida:29 Resultado LM -->

## 30 Resultado LY

Resultado do mesmo período do ano anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:30 Resultado LY -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`09 Resultado`](01-principais.md#09-resultado)
- **É usada por:** [`31 Resultado YoY %`](#31-resultado-yoy)

```dax
CALCULATE(
    [09 Resultado],
    CALCULATETABLE(
        SAMEPERIODLASTYEAR( dCalendario[Id Data] ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```
<!-- gerado:fim medida:30 Resultado LY -->

## 31 Resultado YoY %

Variação percentual do resultado em relação ao mesmo período do ano anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:31 Resultado YoY % -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`09 Resultado`](01-principais.md#09-resultado), [`30 Resultado LY`](#30-resultado-ly)
- **É usada por:** [`62 SVG Cartao Resultado v1`](visuais-svg.md#62-svg-cartao-resultado-v1)

```dax
VAR ResultadoAtual = [09 Resultado]
VAR ResultadoLY = [30 Resultado LY]

RETURN 
    DIVIDE(
        ResultadoAtual - ResultadoLY,
        ResultadoLY,
        BLANK()
    )
```
<!-- gerado:fim medida:31 Resultado YoY % -->

## 32 Resultado MoM %

Variação percentual do resultado em relação ao mês anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:32 Resultado MoM % -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`09 Resultado`](01-principais.md#09-resultado), [`29 Resultado LM`](#29-resultado-lm)
- **É usada por:** nenhuma medida

```dax
VAR ResultadoAtual = [09 Resultado]
VAR ResultadoLM = [29 Resultado LM]

RETURN 
    DIVIDE(
        ResultadoAtual - ResultadoLM,
        ResultadoLM,
        BLANK()
    )
```
<!-- gerado:fim medida:32 Resultado MoM % -->

## 33 Comissao LY

Comissão do mesmo período do ano anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:33 Comissao LY -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`07 Comissao`](01-principais.md#07-comissao)
- **É usada por:** [`34 Comissao YoY %`](#34-comissao-yoy)

```dax
CALCULATE(
    [07 Comissao],
    CALCULATETABLE(
        SAMEPERIODLASTYEAR( dCalendario[Id Data] ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```
<!-- gerado:fim medida:33 Comissao LY -->

## 34 Comissao YoY %

Variação percentual da comissão em relação ao mesmo período do ano anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)

<!-- gerado:inicio medida:34 Comissao YoY % -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`07 Comissao`](01-principais.md#07-comissao), [`33 Comissao LY`](#33-comissao-ly)
- **É usada por:** [`63 SVG Cartao Comissao v1`](visuais-svg.md#63-svg-cartao-comissao-v1)

```dax
VAR ComissaoAtual = [07 Comissao]
VAR ComissaoLY = [33 Comissao LY]

RETURN 
    DIVIDE(
        ComissaoAtual - ComissaoLY,
        ComissaoLY,
        BLANK()
    )
```
<!-- gerado:fim medida:34 Comissao YoY % -->

## 35 Comissao MoM %

Variação percentual da comissão em relação ao mês anterior. *(descrição deduzida do código)*

- **Regra de negócio:** [Comparações no tempo](../regras-de-negocio.md#comparacoes-no-tempo)
- **Observação:** Diferente das outras medidas do mês anterior, o cálculo do mês anterior **não** usa o filtro `dCalendario[Datas com Venda] = TRUE()`. Intencional, confirmado pelo desenvolvedor.

<!-- gerado:inicio medida:35 Comissao MoM % -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`07 Comissao`](01-principais.md#07-comissao)
- **É usada por:** nenhuma medida

```dax
VAR ComissaoAtual = [07 Comissao]
VAR ComissaoLM = 
    CALCULATE(
        [07 Comissao],
        DATEADD(dCalendario[Id Data], -1, MONTH)
    )

RETURN 
    DIVIDE(
        ComissaoAtual - ComissaoLM,
        ComissaoLM,
        BLANK()
    )
```
<!-- gerado:fim medida:35 Comissao MoM % -->
