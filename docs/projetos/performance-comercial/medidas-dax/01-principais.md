<!-- pasta: 01.Principais -->
# 01.Principais

<!-- gerado:inicio resumo -->
Medidas da pasta de exibição `01.Principais`: **16**. Veja o [catálogo](index.md) para as outras pastas.
<!-- gerado:fim resumo -->

## 01 Faturamento

Soma de `Qtde × Valor Unit` das vendas válidas (`Id Status = 1`). *(descrição deduzida do código)*

- **Regra de negócio:** [Faturamento, custo, despesa, impostos e comissão](../regras-de-negocio.md#faturamento-custo-despesa-impostos-e-comissao)
- **Observação:** Confirma que os valores unitários são multiplicados por `Qtde`: o cálculo é feito linha a linha (`SUMX`) e só considera vendas com `Id Status = 1` (válidas). O mesmo vale para `02 Custo`, `05 Despesa`, `06 Impostos` e `07 Comissao`.

<!-- gerado:inicio medida:01 Faturamento -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`
- **Usada nas guias:** [Comercial ](../guias-do-relatorio/comercial.md), *TooltiposTabela*
- **Depende de:** nenhuma medida
- **É usada por:** [`03 Lucro Bruto`](#03-lucro-bruto), [`04 Margem Bruta`](#04-margem-bruta), [`09 Resultado`](#09-resultado), [`10 Margem`](#10-margem), [`20 Faturamento Acumulado`](02-temporais.md#20-faturamento-acumulado), [`21 Faturamento Acumulado LY`](02-temporais.md#21-faturamento-acumulado-ly), [`22 Faturamento LY`](02-temporais.md#22-faturamento-ly), [`23 Faturamento YoY %`](02-temporais.md#23-faturamento-yoy), [`24 Faturamento MoM %`](02-temporais.md#24-faturamento-mom), [`41 Porcentagem Meta`](#41-porcentagem-meta), [`42 Diferença Meta`](#42-diferenca-meta), [`50 Eixo Y max Grafico Comercial`](03-formatacoes.md#50-eixo-y-max-grafico-comercial), [`51 Faturamento formatação de texto`](03-formatacoes.md#51-faturamento-formatacao-de-texto), [`52 Rank Cidade`](sem-pasta.md#52-rank-cidade), [`53 Max Y Visual 01 pg Vendedores`](sem-pasta.md#53-max-y-visual-01-pg-vendedores), [`Context Medida z`](sem-pasta.md#context-medida-z), [`Linha Atual`](sem-pasta.md#linha-atual), [`Seta para Cima`](sem-pasta.md#seta-para-cima), [`Seta para baixo  ( limit Inferior )`](sem-pasta.md#seta-para-baixo-limit-inferior), [`Seta para baixo  ( limit sup )`](sem-pasta.md#seta-para-baixo-limit-sup)

```dax
    CALCULATE(
        SUMX(
            fVendas,
            fVendas[Qtde] * fVendas[Valor Unit]
        ),
        dStatus[Id Status] = 1
    )
```
<!-- gerado:fim medida:01 Faturamento -->

## 02 Custo

Soma de `Qtde × Custo Unit` das vendas válidas. *(descrição deduzida do código)*

- **Regra de negócio:** [Faturamento, custo, despesa, impostos e comissão](../regras-de-negocio.md#faturamento-custo-despesa-impostos-e-comissao)

<!-- gerado:inicio medida:02 Custo -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** [`03 Lucro Bruto`](#03-lucro-bruto), [`04 Margem Bruta`](#04-margem-bruta), [`08 Abatimento`](#08-abatimento)

```dax
    CALCULATE(
        SUMX(
            fVendas,
            fVendas[Qtde] * fVendas[Custo Unit]
        ),
        dStatus[Id Status] = 1 
    )
```
<!-- gerado:fim medida:02 Custo -->

## 03 Lucro Bruto

Lucro Bruto em R$ = Faturamento - Custo

- **Regra de negócio:** [Resultado e margens](../regras-de-negocio.md#resultado-e-margens)

<!-- gerado:inicio medida:03 Lucro Bruto -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](#01-faturamento), [`02 Custo`](#02-custo)
- **É usada por:** nenhuma medida

```dax
// Lucro Bruto = Faturamento - Custo
[01 Faturamento] - [02 Custo]
```
<!-- gerado:fim medida:03 Lucro Bruto -->

## 04 Margem Bruta

Margem Bruta (%) = (Faturamento - Custo) / Faturamento

- **Regra de negócio:** [Resultado e margens](../regras-de-negocio.md#resultado-e-margens)

<!-- gerado:inicio medida:04 Margem Bruta -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](#01-faturamento), [`02 Custo`](#02-custo)
- **É usada por:** nenhuma medida

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
<!-- gerado:fim medida:04 Margem Bruta -->

## 05 Despesa

Soma de `Qtde × Despesa Unit` das vendas válidas. *(descrição deduzida do código)*

- **Regra de negócio:** [Faturamento, custo, despesa, impostos e comissão](../regras-de-negocio.md#faturamento-custo-despesa-impostos-e-comissao)

<!-- gerado:inicio medida:05 Despesa -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** [`08 Abatimento`](#08-abatimento)

```dax
    CALCULATE(
        SUMX(
            fVendas,
            fVendas[Qtde] * fVendas[Despesa Unit]
        ),
        dStatus[Id Status] = 1 
    )
```
<!-- gerado:fim medida:05 Despesa -->

## 06 Impostos

Soma de `Qtde × Impostos Unit` das vendas válidas. *(descrição deduzida do código)*

- **Regra de negócio:** [Faturamento, custo, despesa, impostos e comissão](../regras-de-negocio.md#faturamento-custo-despesa-impostos-e-comissao)

<!-- gerado:inicio medida:06 Impostos -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** [`08 Abatimento`](#08-abatimento)

```dax
    CALCULATE(
        SUMX(
            fVendas,
            fVendas[Qtde] * fVendas[Impostos Unit]
        ),
        dStatus[Id Status] = 1 
    )
```
<!-- gerado:fim medida:06 Impostos -->

## 07 Comissao

Soma de `Qtde × Comissão Unit` das vendas válidas. *(descrição deduzida do código)*

- **Regra de negócio:** [Faturamento, custo, despesa, impostos e comissão](../regras-de-negocio.md#faturamento-custo-despesa-impostos-e-comissao)

<!-- gerado:inicio medida:07 Comissao -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** [`08 Abatimento`](#08-abatimento), [`33 Comissao LY`](02-temporais.md#33-comissao-ly), [`34 Comissao YoY %`](02-temporais.md#34-comissao-yoy), [`35 Comissao MoM %`](02-temporais.md#35-comissao-mom)

```dax
    CALCULATE(
           SUMX(
            fVendas,
            fVendas[Qtde] * fVendas[Comissão Unit]
        ),
        dStatus[Id Status] = 1 
    )
```
<!-- gerado:fim medida:07 Comissao -->

## 08 Abatimento

Soma de custo, despesa, impostos e comissão. *(descrição deduzida do código)*

- **Regra de negócio:** [Resultado e margens](../regras-de-negocio.md#resultado-e-margens)

<!-- gerado:inicio medida:08 Abatimento -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`02 Custo`](#02-custo), [`05 Despesa`](#05-despesa), [`06 Impostos`](#06-impostos), [`07 Comissao`](#07-comissao)
- **É usada por:** [`09 Resultado`](#09-resultado)

```dax
    [02 Custo] + [05 Despesa] + [06 Impostos] + [07 Comissao]
```
<!-- gerado:fim medida:08 Abatimento -->

## 09 Resultado

Faturamento menos o abatimento (custo, despesa, impostos e comissão). *(descrição deduzida do código)*

- **Regra de negócio:** [Resultado e margens](../regras-de-negocio.md#resultado-e-margens)

<!-- gerado:inicio medida:09 Resultado -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** [Comercial ](../guias-do-relatorio/comercial.md)
- **Depende de:** [`01 Faturamento`](#01-faturamento), [`08 Abatimento`](#08-abatimento)
- **É usada por:** [`10 Margem`](#10-margem), [`29 Resultado LM`](02-temporais.md#29-resultado-lm), [`30 Resultado LY`](02-temporais.md#30-resultado-ly), [`31 Resultado YoY %`](02-temporais.md#31-resultado-yoy), [`32 Resultado MoM %`](02-temporais.md#32-resultado-mom)

```dax
    [01 Faturamento] - [08 Abatimento]
```
<!-- gerado:fim medida:09 Resultado -->

## 10 Margem

Margem Líquida (%) = (Resultado / Faturamento) com tratamento de divisão por zero

- **Regra de negócio:** [Resultado e margens](../regras-de-negocio.md#resultado-e-margens)

<!-- gerado:inicio medida:10 Margem -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** [Comercial ](../guias-do-relatorio/comercial.md), *TooltiposTabela*
- **Depende de:** [`01 Faturamento`](#01-faturamento), [`09 Resultado`](#09-resultado)
- **É usada por:** [`25 Margem LM`](02-temporais.md#25-margem-lm), [`26 Margem LY`](02-temporais.md#26-margem-ly), [`27 Margem YoY %`](02-temporais.md#27-margem-yoy), [`28 Margem MoM %`](02-temporais.md#28-margem-mom)

```dax
// Margem Líquida = Resultado / Faturamento
DIVIDE(
    [09 Resultado],
    [01 Faturamento],
    BLANK()
)
```
<!-- gerado:fim medida:10 Margem -->

## 11 Qtde Vendas

Contagem de números de venda distintos (`Num Venda`). *(descrição deduzida do código)*

- **Regra de negócio:** [Quantidade de vendas e positivação](../regras-de-negocio.md#quantidade-de-vendas-e-positivacao)
- **Observação:** **Não filtra o status:** conta as vendas válidas e as inválidas. As medidas de valor consideram só as válidas. Intencional, confirmado pelo desenvolvedor.

<!-- gerado:inicio medida:11 Qtde Vendas -->
- **Tabela:** `_Medidas`
- **Formato:** `#,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** nenhuma medida

```dax
DISTINCTCOUNT(fVendas[Num Venda])
```
<!-- gerado:fim medida:11 Qtde Vendas -->

## 12 Positivação Clientes

Quantidade de clientes únicos com vendas efetivadas (Status = 1)

- **Regra de negócio:** [Quantidade de vendas e positivação](../regras-de-negocio.md#quantidade-de-vendas-e-positivacao)
- **Observação:** Considera só vendas válidas (`Id Status = 1`).

<!-- gerado:inicio medida:12 Positivação Clientes -->
- **Tabela:** `_Medidas`
- **Formato:** `0`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** nenhuma medida

```dax
// Refere-se a Qtde de clientes que efetuaram compras efetivadas
CALCULATE(
    DISTINCTCOUNT(fVendas[Id Cliente]),
    dStatus[Id Status] = 1
)
```
<!-- gerado:fim medida:12 Positivação Clientes -->

## 13 Positivação Produtos

Quantidade de produtos únicos vendidos (Status = 1)

- **Regra de negócio:** [Quantidade de vendas e positivação](../regras-de-negocio.md#quantidade-de-vendas-e-positivacao)
- **Observação:** Considera só vendas válidas (`Id Status = 1`).

<!-- gerado:inicio medida:13 Positivação Produtos -->
- **Tabela:** `_Medidas`
- **Formato:** `0`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** nenhuma medida

```dax
// Refere-se a Qtde de produtos vendidos efetivamente
CALCULATE(
    DISTINCTCOUNT(fVendas[Id Produto]),
    dStatus[Id Status] = 1
)
```
<!-- gerado:fim medida:13 Positivação Produtos -->

## 40 Meta

Soma de `Valor Meta`, a meta de vendas dos vendedores. *(descrição deduzida do código)*

- **Regra de negócio:** [Metas](../regras-de-negocio.md#metas)

<!-- gerado:inicio medida:40 Meta -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** [`41 Porcentagem Meta`](#41-porcentagem-meta), [`42 Diferença Meta`](#42-diferenca-meta)

```dax
SUM(fMetas[Valor Meta])
```
<!-- gerado:fim medida:40 Meta -->

## 41 Porcentagem Meta

Percentual de atingimento: Faturamento / Meta

- **Regra de negócio:** [Metas](../regras-de-negocio.md#metas)

<!-- gerado:inicio medida:41 Porcentagem Meta -->
- **Tabela:** `_Medidas`
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usada nas guias:** *TooltiposTabela*
- **Depende de:** [`01 Faturamento`](#01-faturamento), [`40 Meta`](#40-meta)
- **É usada por:** [`66 Meta Cor`](visuais-svg.md#66-meta-cor)

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
<!-- gerado:fim medida:41 Porcentagem Meta -->

## 42 Diferença Meta

Diferença, em valor absoluto, entre a meta e o faturamento. *(descrição deduzida do código)*

- **Regra de negócio:** [Metas](../regras-de-negocio.md#metas)
- **Observação:** Usa `ABS`: o resultado é sempre positivo e não diz se o faturamento ficou acima ou abaixo da meta. A documentação anterior descrevia a medida como "Faturamento − Meta".

<!-- gerado:inicio medida:42 Diferença Meta -->
- **Tabela:** `_Medidas`
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](#01-faturamento), [`40 Meta`](#40-meta)
- **É usada por:** nenhuma medida

```dax
ABS( [40 Meta] - [01 Faturamento] )
```
<!-- gerado:fim medida:42 Diferença Meta -->
