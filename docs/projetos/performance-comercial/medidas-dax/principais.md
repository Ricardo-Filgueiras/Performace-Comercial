# Principais

Medidas da pasta de exibição `01.Principais`: **16**. Valores e indicadores centrais (faturamento, custo, resultado, margem, positivação) e as medidas de meta (`40` a `42`). Veja o [catálogo](index.md) para as outras pastas.

As descrições marcadas como *deduzidas do código* foram escritas a partir da expressão DAX. As demais vêm do texto `///` do modelo. "Depende de" e "É usada por" vêm do script de levantamento. Em "Usada nas guias", cada guia aparece uma vez, inclusive as ocultas, as de dica de ferramenta e as versões "antes".

## `01 Faturamento`

Soma de `Qtde × Valor Unit` das vendas válidas (`Id Status = 1`). *(descrição deduzida do código)*

```dax
CALCULATE(
    SUMX(
        fVendas,
        fVendas[Qtde] * fVendas[Valor Unit]
    ),
    dStatus[Id Status] = 1
)
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`
- **Usada nas guias:** [Comercial](../guias-do-relatorio/comercial.md), [TooltiposTabela](../guias-do-relatorio/dica-tabela-vendedores.md); pelo nome antigo `Faturamento` em [Comercial](../guias-do-relatorio/comercial.md), [Analítico](../guias-do-relatorio/analitico.md), [Mapa Calor](../guias-do-relatorio/mapa-calor.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Analítico antes](../arquivo/guias-anteriores.md), [Mapa Calor antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md), [TooltiposGrafico01](../guias-do-relatorio/dica-evolucao-faturamento.md), [TooltiposTabela](../guias-do-relatorio/dica-tabela-vendedores.md)
- **Depende de:** nenhuma medida
- **É usada por:** `03 Lucro Bruto`, `04 Margem Bruta`, `09 Resultado`, `10 Margem`, `20 Faturamento Acumulado`, `21 Faturamento Acumulado LY`, `22 Faturamento LY`, `23 Faturamento YoY %`, `24 Faturamento MoM %`, `41 Porcentagem Meta`, `42 Diferença Meta`, `50 Eixo Y max Grafico Comercial`, `51 Faturamento formatação de texto`, `52 Rank Cidade`, `53 Max Y Visual 01 pg Vendedores`, `Context Medida z`, `Linha Atual`, `Seta para Cima`, `Seta para baixo  ( limit Inferior )`, `Seta para baixo  ( limit sup )`
- **Regra de negócio:** [Faturamento, custo, despesa, impostos e comissão](../regras-de-negocio.md#faturamento-custo-despesa-impostos-e-comissao)
- **Observação:** Confirma que os valores unitários são multiplicados por `Qtde`: o cálculo é feito linha a linha (`SUMX`) e só considera vendas com `Id Status = 1` (válidas). O mesmo vale para `02 Custo`, `05 Despesa`, `06 Impostos` e `07 Comissao`.

## `02 Custo`

Soma de `Qtde × Custo Unit` das vendas válidas. *(descrição deduzida do código)*

```dax
CALCULATE(
    SUMX(
        fVendas,
        fVendas[Qtde] * fVendas[Custo Unit]
    ),
    dStatus[Id Status] = 1 
)
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** `03 Lucro Bruto`, `04 Margem Bruta`, `08 Abatimento`
- **Regra de negócio:** [Faturamento, custo, despesa, impostos e comissão](../regras-de-negocio.md#faturamento-custo-despesa-impostos-e-comissao)

## `03 Lucro Bruto`

Lucro Bruto em R$ = Faturamento - Custo

```dax
// Lucro Bruto = Faturamento - Custo
[01 Faturamento] - [02 Custo]
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`
- **Usada nas guias:** nenhum visual
- **Depende de:** `01 Faturamento`, `02 Custo`
- **É usada por:** nenhuma medida
- **Regra de negócio:** [Resultado e margens](../regras-de-negocio.md#resultado-e-margens)

## `04 Margem Bruta`

Margem Bruta (%) = (Faturamento - Custo) / Faturamento

```dax
// Margem Bruta = (Faturamento - Custo) / Faturamento
VAR _Faturamento = [01 Faturamento]
VAR _Custo = [02 Custo]
VAR _MargemBruta = _Faturamento - _Custo

RETURN
    DIVIDE(
        _MargemBruta,
        _Faturamento,
        BLANK()
    )
```

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** `01 Faturamento`, `02 Custo`
- **É usada por:** nenhuma medida
- **Regra de negócio:** [Resultado e margens](../regras-de-negocio.md#resultado-e-margens)

## `05 Despesa`

Soma de `Qtde × Despesa Unit` das vendas válidas. *(descrição deduzida do código)*

```dax
CALCULATE(
    SUMX(
        fVendas,
        fVendas[Qtde] * fVendas[Despesa Unit]
    ),
    dStatus[Id Status] = 1 
)
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** `08 Abatimento`
- **Regra de negócio:** [Faturamento, custo, despesa, impostos e comissão](../regras-de-negocio.md#faturamento-custo-despesa-impostos-e-comissao)

## `06 Impostos`

Soma de `Qtde × Impostos Unit` das vendas válidas. *(descrição deduzida do código)*

```dax
CALCULATE(
    SUMX(
        fVendas,
        fVendas[Qtde] * fVendas[Impostos Unit]
    ),
    dStatus[Id Status] = 1 
)
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** `08 Abatimento`
- **Regra de negócio:** [Faturamento, custo, despesa, impostos e comissão](../regras-de-negocio.md#faturamento-custo-despesa-impostos-e-comissao)

## `07 Comissao`

Soma de `Qtde × Comissão Unit` das vendas válidas. *(descrição deduzida do código)*

```dax
CALCULATE(
       SUMX(
        fVendas,
        fVendas[Qtde] * fVendas[Comissão Unit]
    ),
    dStatus[Id Status] = 1 
)
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`
- **Usada nas guias:** pelo nome antigo `Comissao` em [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md)
- **Depende de:** nenhuma medida
- **É usada por:** `08 Abatimento`, `33 Comissao LY`, `34 Comissao YoY %`, `35 Comissao MoM %`
- **Regra de negócio:** [Faturamento, custo, despesa, impostos e comissão](../regras-de-negocio.md#faturamento-custo-despesa-impostos-e-comissao)

## `08 Abatimento`

Soma de custo, despesa, impostos e comissão. *(descrição deduzida do código)*

```dax
[02 Custo] + [05 Despesa] + [06 Impostos] + [07 Comissao]
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** pelo nome antigo `Abatimento` em [Analítico](../guias-do-relatorio/analitico.md), [Analítico antes](../arquivo/guias-anteriores.md)
- **Depende de:** `02 Custo`, `05 Despesa`, `06 Impostos`, `07 Comissao`
- **É usada por:** `09 Resultado`
- **Regra de negócio:** [Resultado e margens](../regras-de-negocio.md#resultado-e-margens)

## `09 Resultado`

Faturamento menos o abatimento (custo, despesa, impostos e comissão). *(descrição deduzida do código)*

```dax
[01 Faturamento] - [08 Abatimento]
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** [Comercial](../guias-do-relatorio/comercial.md); pelo nome antigo `Resultado` em [Analítico](../guias-do-relatorio/analitico.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Analítico antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md)
- **Depende de:** `01 Faturamento`, `08 Abatimento`
- **É usada por:** `10 Margem`, `29 Resultado LM`, `30 Resultado LY`, `31 Resultado YoY %`, `32 Resultado MoM %`
- **Regra de negócio:** [Resultado e margens](../regras-de-negocio.md#resultado-e-margens)

## `10 Margem`

Margem Líquida (%) = (Resultado / Faturamento) com tratamento de divisão por zero

```dax
// Margem Líquida = Resultado / Faturamento
DIVIDE(
    [09 Resultado],
    [01 Faturamento],
    BLANK()
)
```

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** [Comercial](../guias-do-relatorio/comercial.md), [TooltiposTabela](../guias-do-relatorio/dica-tabela-vendedores.md); pelo nome antigo `Margem` em [Comercial](../guias-do-relatorio/comercial.md), [Analítico](../guias-do-relatorio/analitico.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Analítico antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md)
- **Depende de:** `01 Faturamento`, `09 Resultado`
- **É usada por:** `25 Margem LM`, `26 Margem LY`, `27 Margem YoY %`, `28 Margem MoM %`
- **Regra de negócio:** [Resultado e margens](../regras-de-negocio.md#resultado-e-margens)

## `11 Qtde Vendas`

Contagem de números de venda distintos (`Num Venda`). *(descrição deduzida do código)*

```dax
DISTINCTCOUNT(fVendas[Num Venda])
```

- **Tabela:** `_Medidas`
- **Formato:** `#,0`
- **Usada nas guias:** pelo nome antigo `Qtde Vendas` em [Analítico](../guias-do-relatorio/analitico.md), [Analítico antes](../arquivo/guias-anteriores.md)
- **Depende de:** nenhuma medida
- **É usada por:** nenhuma medida
- **Regra de negócio:** [Quantidade de vendas e positivação](../regras-de-negocio.md#quantidade-de-vendas-e-positivacao)
- **Observação:** **Não filtra o status:** conta as vendas válidas e as inválidas. As medidas de valor consideram só as válidas. Intencional, confirmado pelo desenvolvedor.

## `12 Positivação Clientes`

Quantidade de clientes únicos com vendas efetivadas (Status = 1)

```dax
// Refere-se a Qtde de clientes que efetuaram compras efetivadas
CALCULATE(
    DISTINCTCOUNT(fVendas[Id Cliente]),
    dStatus[Id Status] = 1
)
```

- **Tabela:** `_Medidas`
- **Formato:** `0`
- **Usada nas guias:** pelo nome antigo `Positivação Clientes` em [Analítico](../guias-do-relatorio/analitico.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Analítico antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md)
- **Depende de:** nenhuma medida
- **É usada por:** nenhuma medida
- **Regra de negócio:** [Quantidade de vendas e positivação](../regras-de-negocio.md#quantidade-de-vendas-e-positivacao)
- **Observação:** Considera só vendas válidas (`Id Status = 1`).

## `13 Positivação Produtos`

Quantidade de produtos únicos vendidos (Status = 1)

```dax
// Refere-se a Qtde de produtos vendidos efetivamente
CALCULATE(
    DISTINCTCOUNT(fVendas[Id Produto]),
    dStatus[Id Status] = 1
)
```

- **Tabela:** `_Medidas`
- **Formato:** `0`
- **Usada nas guias:** pelo nome antigo `Positivação Produtos` em [Analítico](../guias-do-relatorio/analitico.md), [Analítico antes](../arquivo/guias-anteriores.md)
- **Depende de:** nenhuma medida
- **É usada por:** nenhuma medida
- **Regra de negócio:** [Quantidade de vendas e positivação](../regras-de-negocio.md#quantidade-de-vendas-e-positivacao)
- **Observação:** Considera só vendas válidas (`Id Status = 1`).

## `40 Meta`

Soma de `Valor Meta`, a meta de vendas dos vendedores. *(descrição deduzida do código)*

```dax
SUM(fMetas[Valor Meta])
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** pelo nome antigo `Meta` em [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md), [TooltiposGrafico01](../guias-do-relatorio/dica-evolucao-faturamento.md)
- **Depende de:** nenhuma medida
- **É usada por:** `41 Porcentagem Meta`, `42 Diferença Meta`
- **Regra de negócio:** [Metas](../regras-de-negocio.md#metas)

## `41 Porcentagem Meta`

Percentual de atingimento: Faturamento / Meta

```dax
// Percentual de atingimento da meta
VAR _Faturamento = [01 Faturamento]
VAR _Meta = [40 Meta]

RETURN
    DIVIDE(
        _Faturamento,
        _Meta,
        BLANK()
    )
```

- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** [TooltiposTabela](../guias-do-relatorio/dica-tabela-vendedores.md); pelo nome antigo `Porcentagem Meta` em [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md), [TooltiposGrafico01](../guias-do-relatorio/dica-evolucao-faturamento.md), [TooltiposTabela](../guias-do-relatorio/dica-tabela-vendedores.md)
- **Depende de:** `01 Faturamento`, `40 Meta`
- **É usada por:** `66 Meta Cor`
- **Regra de negócio:** [Metas](../regras-de-negocio.md#metas)

## `42 Diferença Meta`

Diferença, em valor absoluto, entre a meta e o faturamento. *(descrição deduzida do código)*

```dax
ABS( [40 Meta] - [01 Faturamento] )
```

- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** pelo nome antigo `Diferença Meta` em [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md)
- **Depende de:** `01 Faturamento`, `40 Meta`
- **É usada por:** nenhuma medida
- **Regra de negócio:** [Metas](../regras-de-negocio.md#metas)
- **Observação:** Usa `ABS`: o resultado é sempre positivo e não diz se o faturamento ficou acima ou abaixo da meta. A documentação anterior descrevia a medida como "Faturamento − Meta".
