# Temporais

Medidas da pasta de exibição `02. Temporais`: **16**. Comparações no tempo: mês anterior (`LM`), mesmo período do ano anterior (`LY`) e variações percentuais (`MoM` e `YoY`). Veja o [catálogo](index.md) para as outras pastas.

As descrições marcadas como *deduzidas do código* foram escritas a partir da expressão DAX. As demais vêm do texto `///` do modelo. "Depende de" e "É usada por" vêm do script de levantamento. Em "Usada nas guias", cada guia aparece uma vez, inclusive as ocultas, as de dica de ferramenta e as versões "antes".

## `20 Faturamento Acumulado`

Faturamento acumulado desde o início do ano até a data (YTD), limitado às datas até a última venda. *(descrição deduzida do código)*

```dax
CALCULATE(
    [01 Faturamento],
    CALCULATETABLE(
        DATESYTD(dCalendario[Id Data]),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** pelo nome antigo `Faturamento Acumulado` em Mapa Calor, Mapa Calor antes
- **Depende de:** `01 Faturamento`
- **É usada por:** nenhuma medida
- **Observação:** Usa `dCalendario[Datas com Venda]`, que marca as datas até a última venda (ver [Modelo de dados](../modelo-de-dados.md)).

## `21 Faturamento Acumulado LY`

Faturamento acumulado no ano, no mesmo período do ano anterior. *(descrição deduzida do código)*

```dax
CALCULATE(
    [01 Faturamento],
    CALCULATETABLE(
        DATESYTD( SAMEPERIODLASTYEAR( dCalendario[Id Data]) ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** pelo nome antigo `Faturamento Acumulado LY` em Mapa Calor, Mapa Calor antes
- **Depende de:** `01 Faturamento`
- **É usada por:** nenhuma medida

## `22 Faturamento LY`

Faturamento do mesmo período do ano anterior. *(descrição deduzida do código)*

```dax
CALCULATE(
    [01 Faturamento],
    CALCULATETABLE(
        SAMEPERIODLASTYEAR( dCalendario[Id Data] ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** pelo nome antigo `Faturamento LY` em Mapa Calor, Mapa Calor antes
- **Depende de:** `01 Faturamento`
- **É usada por:** `23 Faturamento YoY %`, `Context Medida z`, `Linha Anterior`, `Seta para Cima`, `Seta para baixo  ( limit Inferior )`, `Seta para baixo  ( limit sup )`

## `23 Faturamento YoY %`

Variação percentual Year-over-Year do Faturamento

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

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** `01 Faturamento`, `22 Faturamento LY`
- **É usada por:** `60 SVG Cartao Faturamento v1`

## `24 Faturamento MoM %`

Variação percentual Month-over-Month do Faturamento

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

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** pelo nome antigo `Faturamento MoM %` em Comercial, Comercial antes
- **Depende de:** `01 Faturamento`
- **É usada por:** nenhuma medida
- **Observação:** O mês anterior é calculado dentro da própria medida, sem uma medida `LM` separada.

## `25 Margem LM`

Margem líquida do mês anterior. *(descrição deduzida do código)*

```dax
CALCULATE(
    [10 Margem],
    CALCULATETABLE(
        DATEADD( dCalendario[Id Data], -1, MONTH ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** `10 Margem`
- **É usada por:** `28 Margem MoM %`

## `26 Margem LY`

Margem líquida do mesmo período do ano anterior. *(descrição deduzida do código)*

```dax
CALCULATE(
    [10 Margem],
    CALCULATETABLE(
        SAMEPERIODLASTYEAR( dCalendario[Id Data] ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** `10 Margem`
- **É usada por:** `27 Margem YoY %`

## `27 Margem YoY %`

Variação percentual da margem líquida em relação ao mesmo período do ano anterior. *(descrição deduzida do código)*

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

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** `10 Margem`, `26 Margem LY`
- **É usada por:** `61 SVG Cartao Margem v1`, `64 SVG Tabela HTML Content Lite v1`
- **Observação:** É a variação **relativa** entre duas margens (a diferença dividida pela margem do ano anterior), e não a diferença em pontos percentuais.

## `28 Margem MoM %`

Variação percentual da margem líquida em relação ao mês anterior. *(descrição deduzida do código)*

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

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** `10 Margem`, `25 Margem LM`
- **É usada por:** nenhuma medida

## `29 Resultado LM`

Resultado do mês anterior. *(descrição deduzida do código)*

```dax
CALCULATE(
    [09 Resultado],
    CALCULATETABLE(
        DATEADD( dCalendario[Id Data], -1, MONTH ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** `09 Resultado`
- **É usada por:** `32 Resultado MoM %`

## `30 Resultado LY`

Resultado do mesmo período do ano anterior. *(descrição deduzida do código)*

```dax
CALCULATE(
    [09 Resultado],
    CALCULATETABLE(
        SAMEPERIODLASTYEAR( dCalendario[Id Data] ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** `09 Resultado`
- **É usada por:** `31 Resultado YoY %`

## `31 Resultado YoY %`

Variação percentual do resultado em relação ao mesmo período do ano anterior. *(descrição deduzida do código)*

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

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** `09 Resultado`, `30 Resultado LY`
- **É usada por:** `62 SVG Cartao Resultado v1`

## `32 Resultado MoM %`

Variação percentual do resultado em relação ao mês anterior. *(descrição deduzida do código)*

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

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** `09 Resultado`, `29 Resultado LM`
- **É usada por:** nenhuma medida

## `33 Comissao LY`

Comissão do mesmo período do ano anterior. *(descrição deduzida do código)*

```dax
CALCULATE(
    [07 Comissao],
    CALCULATETABLE(
        SAMEPERIODLASTYEAR( dCalendario[Id Data] ),
        dCalendario[Datas com Venda] = TRUE()
    )
)
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** `07 Comissao`
- **É usada por:** `34 Comissao YoY %`

## `34 Comissao YoY %`

Variação percentual da comissão em relação ao mesmo período do ano anterior. *(descrição deduzida do código)*

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

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** `07 Comissao`, `33 Comissao LY`
- **É usada por:** `63 SVG Cartao Comissao v1`

## `35 Comissao MoM %`

Variação percentual da comissão em relação ao mês anterior. *(descrição deduzida do código)*

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

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** `07 Comissao`
- **É usada por:** nenhuma medida
- **Observação:** Diferente das outras medidas do mês anterior, o cálculo do mês anterior **não** usa o filtro `dCalendario[Datas com Venda] = TRUE()`.
