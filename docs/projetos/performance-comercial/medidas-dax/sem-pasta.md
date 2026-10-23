# Sem pasta de exibição

Medidas sem `displayFolder` no modelo, agrupadas pela tabela onde estão. Pela regra do [guia do desenvolvedor](../guia-do-desenvolvedor.md), nenhuma medida deveria ficar sem pasta ao final de uma tarefa no modelo; esta página registra o que existe.

<!-- gerado:inicio resumo -->
Medidas sem pasta de exibição: **9**. Veja o [catálogo](index.md) para as outras pastas.
<!-- gerado:fim resumo -->

## 52 Rank Cidade

Posição da cidade no ranking de faturamento, entre todas as cidades de `dClientes`. *(descrição deduzida do código)*

<!-- gerado:inicio medida:52 Rank Cidade -->
- **Tabela:** `_Medidas`
- **Formato:** `0`
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento)
- **É usada por:** nenhuma medida

```dax
RANKX(
    ALL( dClientes[Cidade] ) , [01 Faturamento] 
)
```
<!-- gerado:fim medida:52 Rank Cidade -->

## 53 Max Y Visual 01 pg Vendedores

Maior faturamento diário no contexto selecionado, multiplicado por 1,5. Pelo nome, define o limite do eixo Y do visual 01 da guia Vendedores. *(descrição deduzida do código)*

<!-- gerado:inicio medida:53 Max Y Visual 01 pg Vendedores -->
- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento)
- **É usada por:** nenhuma medida

```dax
MAXX(
    ALLSELECTED(
        dCalendario[Dia]
    ), [01 Faturamento] * 1.5

)
```
<!-- gerado:fim medida:53 Max Y Visual 01 pg Vendedores -->

## 54 Nome Vendedor

Nome do vendedor selecionado no filtro (vazio se houver mais de um). *(descrição deduzida do código)*

<!-- gerado:inicio medida:54 Nome Vendedor -->
- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** nenhuma medida

```dax
SELECTEDVALUE( dVendedores[Vendedor] )
```
<!-- gerado:fim medida:54 Nome Vendedor -->

## Context Medida z

Devolve o faturamento atual ou o do ano anterior, conforme o valor de `zMetricas[Metrica]` ("Atual" ou "Anterior"). *(descrição deduzida do código)*

<!-- gerado:inicio medida:Context Medida z -->
- **Tabela:** `zMetricas`
- **Formato:** padrão
- **Usada nas guias:** *TooltipRosca*
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento), [`22 Faturamento LY`](02-temporais.md#22-faturamento-ly)
- **É usada por:** nenhuma medida

```dax
VAR _contexto = SELECTEDVALUE( zMetricas[Metrica] )

VAR _selecao = 
SWITCH(
    TRUE(),
    _contexto = "Atual", [01 Faturamento] ,
    _contexto = "Anterior", [22 Faturamento LY],
    BLANK()

)

RETURN
    _selecao
```
<!-- gerado:fim medida:Context Medida z -->

## Linha Anterior

Faturamento do mesmo período do ano anterior (repete `22 Faturamento LY`). *(descrição deduzida do código)*

<!-- gerado:inicio medida:Linha Anterior -->
- **Tabela:** `zMetricas`
- **Formato:** padrão
- **Usada nas guias:** *TooltipRosca*
- **Depende de:** [`22 Faturamento LY`](02-temporais.md#22-faturamento-ly)
- **É usada por:** nenhuma medida

```dax
[22 Faturamento LY]
```
<!-- gerado:fim medida:Linha Anterior -->

## Linha Atual

Faturamento atual, quando a métrica selecionada é "Atual" ou não há seleção. *(descrição deduzida do código)*

<!-- gerado:inicio medida:Linha Atual -->
- **Tabela:** `zMetricas`
- **Formato:** padrão
- **Usada nas guias:** *TooltipRosca*
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento)
- **É usada por:** nenhuma medida

```dax
VAR _selecao = SELECTEDVALUE( zMetricas[Metrica] )

RETURN
    IF(  _selecao in {"Atual", ""} , [01 Faturamento] )
```
<!-- gerado:fim medida:Linha Atual -->

## Seta para baixo  ( limit Inferior )

Faturamento atual, quando não há métrica selecionada e o atual é menor que o do ano anterior. *(descrição deduzida do código)*

<!-- gerado:inicio medida:Seta para baixo  ( limit Inferior ) -->
- **Tabela:** `zMetricas`
- **Formato:** padrão
- **Usada nas guias:** *TooltipRosca*
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento), [`22 Faturamento LY`](02-temporais.md#22-faturamento-ly)
- **É usada por:** nenhuma medida

```dax
VAR _context = SELECTEDVALUE( zMetricas[Metrica] )
VAR _atual = [01 Faturamento]
VAR _anterio = [22 Faturamento LY] 

RETURN
    IF(
        _context = ""
        && _atual < _anterio,
        _atual 
    )
```
<!-- gerado:fim medida:Seta para baixo  ( limit Inferior ) -->

## Seta para baixo  ( limit sup )

Faturamento do ano anterior, quando não há métrica selecionada e o atual é menor. *(descrição deduzida do código)*

<!-- gerado:inicio medida:Seta para baixo  ( limit sup ) -->
- **Tabela:** `zMetricas`
- **Formato:** `0`
- **Usada nas guias:** *TooltipRosca*
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento), [`22 Faturamento LY`](02-temporais.md#22-faturamento-ly)
- **É usada por:** nenhuma medida

```dax
VAR _context = SELECTEDVALUE( zMetricas[Metrica] )
VAR _atual = [01 Faturamento]
VAR _anterio = [22 Faturamento LY] 

RETURN
    IF(
        _context = ""
        && _atual < _anterio,
        _anterio 
    )
```
<!-- gerado:fim medida:Seta para baixo  ( limit sup ) -->

## Seta para Cima

Faturamento atual, quando não há métrica selecionada e o atual é maior ou igual ao do ano anterior. *(descrição deduzida do código)*

<!-- gerado:inicio medida:Seta para Cima -->
- **Tabela:** `zMetricas`
- **Formato:** padrão
- **Usada nas guias:** *TooltipRosca*
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento), [`22 Faturamento LY`](02-temporais.md#22-faturamento-ly)
- **É usada por:** nenhuma medida

```dax
VAR _context = SELECTEDVALUE( zMetricas[Metrica] )
VAR _atual = [01 Faturamento]
VAR _anterio = [22 Faturamento LY] 

RETURN
    IF(
        _context = ""
        && _atual >= _anterio,
        _atual 
    )
```
<!-- gerado:fim medida:Seta para Cima -->
