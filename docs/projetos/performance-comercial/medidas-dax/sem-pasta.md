# Sem pasta de exibição

Medidas sem `displayFolder` no modelo, agrupadas pela tabela onde estão: **9**. Pela regra do [guia do desenvolvedor](../guia-do-desenvolvedor.md), nenhuma medida deveria ficar sem pasta ao final de uma tarefa no modelo; esta página registra o que existe.

As descrições marcadas como *deduzidas do código* foram escritas a partir da expressão DAX. As demais vêm do texto `///` do modelo. "Depende de" e "É usada por" vêm do script de levantamento. Em "Usada nas guias", cada guia aparece uma vez, inclusive as ocultas, as de dica de ferramenta e as versões "antes".

## Tabela `_Medidas`

3 medidas.

### `52 Rank Cidade`

Posição da cidade no ranking de faturamento, entre todas as cidades de `dClientes`. *(descrição deduzida do código)*

```dax
RANKX(
    ALL( dClientes[Cidade] ) , [01 Faturamento] 
)
```

- **Tabela:** `_Medidas`
- **Formato:** `0`
- **Usada nas guias:** pelo nome antigo `rank cidade` em [Comercial](../guias-do-relatorio/comercial.md), [Comercial antes](../arquivo/guias-anteriores.md)
- **Depende de:** `01 Faturamento`
- **É usada por:** nenhuma medida

### `53 Max Y Visual 01 pg Vendedores`

Maior faturamento diário no contexto selecionado, multiplicado por 1,5. Pelo nome, define o limite do eixo Y do visual 01 da guia Vendedores. *(descrição deduzida do código)*

```dax
MAXX(
    ALLSELECTED(
        dCalendario[Dia]
    ), [01 Faturamento] * 1.5

)
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** pelo nome antigo `max Y visual 01 pg Vendedores` em [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md)
- **Depende de:** `01 Faturamento`
- **É usada por:** nenhuma medida

### `54 Nome Vendedor`

Nome do vendedor selecionado no filtro (vazio se houver mais de um). *(descrição deduzida do código)*

```dax
SELECTEDVALUE( dVendedores[Vendedor] )
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** pelo nome antigo `nome vendedor` em [TooltipRosca](../guias-do-relatorio/dica-gerente-vendedores.md)
- **Depende de:** nenhuma medida
- **É usada por:** nenhuma medida

## Tabela `zMetricas`

6 medidas.

### `Context Medida z`

Devolve o faturamento atual ou o do ano anterior, conforme o valor de `zMetricas[Metrica]` ("Atual" ou "Anterior"). *(descrição deduzida do código)*

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

- **Tabela:** `zMetricas`
- **Formato:** padrão
- **Usada nas guias:** [TooltipRosca](../guias-do-relatorio/dica-gerente-vendedores.md)
- **Depende de:** `01 Faturamento`, `22 Faturamento LY`
- **É usada por:** nenhuma medida

### `Linha Anterior`

Faturamento do mesmo período do ano anterior (repete `22 Faturamento LY`). *(descrição deduzida do código)*

```dax
[22 Faturamento LY]
```

- **Tabela:** `zMetricas`
- **Formato:** padrão
- **Usada nas guias:** [TooltipRosca](../guias-do-relatorio/dica-gerente-vendedores.md)
- **Depende de:** `22 Faturamento LY`
- **É usada por:** nenhuma medida

### `Linha Atual`

Faturamento atual, quando a métrica selecionada é "Atual" ou não há seleção. *(descrição deduzida do código)*

```dax
VAR _selecao = SELECTEDVALUE( zMetricas[Metrica] )

RETURN
    IF(  _selecao in {"Atual", ""} , [01 Faturamento] )
```

- **Tabela:** `zMetricas`
- **Formato:** padrão
- **Usada nas guias:** [TooltipRosca](../guias-do-relatorio/dica-gerente-vendedores.md)
- **Depende de:** `01 Faturamento`
- **É usada por:** nenhuma medida

### `Seta para Cima`

Faturamento atual, quando não há métrica selecionada e o atual é maior ou igual ao do ano anterior. *(descrição deduzida do código)*

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

- **Tabela:** `zMetricas`
- **Formato:** padrão
- **Usada nas guias:** [TooltipRosca](../guias-do-relatorio/dica-gerente-vendedores.md)
- **Depende de:** `01 Faturamento`, `22 Faturamento LY`
- **É usada por:** nenhuma medida

### `Seta para baixo  ( limit Inferior )`

Faturamento atual, quando não há métrica selecionada e o atual é menor que o do ano anterior. *(descrição deduzida do código)*

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

- **Tabela:** `zMetricas`
- **Formato:** padrão
- **Usada nas guias:** [TooltipRosca](../guias-do-relatorio/dica-gerente-vendedores.md)
- **Depende de:** `01 Faturamento`, `22 Faturamento LY`
- **É usada por:** nenhuma medida

### `Seta para baixo  ( limit sup )`

Faturamento do ano anterior, quando não há métrica selecionada e o atual é menor. *(descrição deduzida do código)*

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

- **Tabela:** `zMetricas`
- **Formato:** `0`
- **Usada nas guias:** [TooltipRosca](../guias-do-relatorio/dica-gerente-vendedores.md)
- **Depende de:** `01 Faturamento`, `22 Faturamento LY`
- **É usada por:** nenhuma medida

