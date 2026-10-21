# Visuais SVG

Medidas da pasta de exibição `.Visuais SVG`: **7**. Medidas que devolvem imagens SVG ou textos de cor, usadas por visuais do relatório. Veja o [catálogo](index.md) para as outras pastas.

As descrições marcadas como *deduzidas do código* foram escritas a partir da expressão DAX. As demais vêm do texto `///` do modelo. "Depende de" e "É usada por" vêm do script de levantamento. Em "Usada nas guias", cada guia aparece uma vez, inclusive as ocultas, as de dica de ferramenta e as versões "antes".

## `60 SVG Cartao Faturamento v1`

Desenha, em SVG, a variação do faturamento contra o ano anterior (`23 Faturamento YoY %`), com seta e cor. *(descrição deduzida do código)*

```dax
VAR _percent = [23 Faturamento YoY %]
VAR _format = FORMAT( _percent + 0 , " +0.00 %; -0.00 %; -")
VAR _seta = 
SWITCH(
    TRUE(),
    _percent > 0 , "▲",
    _percent < 0 , "▼",
    " - "
)
VAR _cor_seta = 
SWITCH(
    TRUE(),
    _percent > 0 , "Green",
    _percent < 0 , "red",
    "#ffffff"
)

VAR _text =
    "data:image/svg+xml,
    <svg  viewBox='0 0 190 50' fill='none' xmlns='http://www.w3.org/2000/svg'>
        <g id='varia&#195;&#167;&#195;&#163;o'>
            <text id='rot_cat' fill='white' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='12' font-weight='400' letter-spacing='0em'>
                <tspan x='88' y='40.9688'>Vs. Ano Anterior</tspan>
            </text>
            <text id='rot_dados' fill='"& _cor_seta &"' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='14' font-weight='600' letter-spacing='0em'>
                <tspan x='88' y='21.2969'>"& _format &"</tspan>
            </text>
            <text id='seta' fill='"& _cor_seta &"' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='14' font-weight='600' letter-spacing='0em'>
                <tspan x='68' y='31.2969'>"& _seta &"</tspan>
            </text>
        </g>
    </svg>
    "

RETURN 
    _text
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** [Comercial](../guias-do-relatorio/comercial.md); pelo nome antigo `cartao  faturamento svg v1` em [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md)
- **Depende de:** `23 Faturamento YoY %`
- **É usada por:** nenhuma medida

## `61 SVG Cartao Margem v1`

Desenha, em SVG, a variação da margem contra o ano anterior (`27 Margem YoY %`), com seta e cor. *(descrição deduzida do código)*

```dax
VAR _percent = [27 Margem YoY %]
VAR _format = FORMAT( _percent + 0 , "+0.00 %;-0.00 %;-")
VAR _seta = 
SWITCH(
    TRUE(),
    _percent > 0 , "▲",
    _percent < 0 , "▼",
    " - "
)
VAR _cor_seta = 
SWITCH(
    TRUE(),
    _percent > 0 , "Green",
    _percent < 0 , "red",
    "#ffffff"
)

VAR _text =
    "data:image/svg+xml,
    <svg  viewBox='0 0 190 50' fill='none' xmlns='http://www.w3.org/2000/svg'>
        <g id='varia&#195;&#167;&#195;&#163;o'>
            <text id='rot_cat' fill='white' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='12' font-weight='400' letter-spacing='0em'>
                <tspan x='88' y='40.9688'>Vs. Ano Anterior</tspan>
            </text>
            <text id='rot_dados' fill='"& _cor_seta &"' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='14' font-weight='600' letter-spacing='0em'>
                <tspan x='88' y='21.2969'>"& _format &"</tspan>
            </text>
            <text id='seta' fill='"& _cor_seta &"' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='14' font-weight='600' letter-spacing='0em'>
                <tspan x='68' y='31.2969'>"& _seta &"</tspan>
            </text>
        </g>
    </svg>
    "

RETURN 
    _text
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** pelo nome antigo `cartao  margem svg v1` em [Comercial](../guias-do-relatorio/comercial.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md)
- **Depende de:** `27 Margem YoY %`
- **É usada por:** nenhuma medida

## `62 SVG Cartao Resultado v1`

Desenha, em SVG, a variação do resultado contra o ano anterior (`31 Resultado YoY %`), com seta e cor. *(descrição deduzida do código)*

```dax
VAR _percent = [31 Resultado YoY %]
VAR _format = FORMAT( _percent + 0 , "+0.00 %;-0.00 %;-")
VAR _seta = 
SWITCH(
    TRUE(),
    _percent > 0 , "▲",
    _percent < 0 , "▼",
    " - "
)
VAR _cor_seta = 
SWITCH(
    TRUE(),
    _percent > 0 , "Green",
    _percent < 0 , "red",
    "#ffffff"
)

VAR _text =
    "data:image/svg+xml,
    <svg  viewBox='0 0 190 50' fill='none' xmlns='http://www.w3.org/2000/svg'>
        <g id='varia&#195;&#167;&#195;&#163;o'>
            <text id='rot_cat' fill='white' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='12' font-weight='400' letter-spacing='0em'>
                <tspan x='88' y='40.9688'>Vs. Ano Anterior</tspan>
            </text>
            <text id='rot_dados' fill='"& _cor_seta &"' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='14' font-weight='600' letter-spacing='0em'>
                <tspan x='88' y='21.2969'>"& _format &"</tspan>
            </text>
            <text id='seta' fill='"& _cor_seta &"' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='14' font-weight='600' letter-spacing='0em'>
                <tspan x='68' y='31.2969'>"& _seta &"</tspan>
            </text>
        </g>
    </svg>
    "

RETURN 
    _text
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** pelo nome antigo `cartao  resultado svg v1` em [Comercial](../guias-do-relatorio/comercial.md), [Vendedores](../guias-do-relatorio/vendedores.md), [Comercial antes](../arquivo/guias-anteriores.md), [Vendedores antes](../arquivo/guias-anteriores.md)
- **Depende de:** `31 Resultado YoY %`
- **É usada por:** nenhuma medida

## `63 SVG Cartao Comissao v1`

Desenha, em SVG, a variação da comissão contra o ano anterior (`34 Comissao YoY %`), com seta e cor. *(descrição deduzida do código)*

```dax
VAR _percent = [34 Comissao YoY %]
VAR _format = FORMAT( _percent + 0 , " +0.00 %; -0.00 %; -")
VAR _seta = 
SWITCH(
    TRUE(),
    _percent > 0 , "▲",
    _percent < 0 , "▼",
    " - "
)
VAR _cor_seta = 
SWITCH(
    TRUE(),
    _percent > 0 , "Green",
    _percent < 0 , "red",
    "#ffffff"
)

VAR _text =
    "data:image/svg+xml,
    <svg  viewBox='0 0 190 50' fill='none' xmlns='http://www.w3.org/2000/svg'>
        <g id='varia&#195;&#167;&#195;&#163;o'>
            <text id='rot_cat' fill='white' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='12' font-weight='400' letter-spacing='0em'>
                <tspan x='88' y='40.9688'>Vs. Ano Anterior</tspan>
            </text>
            <text id='rot_dados' fill='"& _cor_seta &"' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='14' font-weight='600' letter-spacing='0em'>
                <tspan x='88' y='21.2969'>"& _format &"</tspan>
            </text>
            <text id='seta' fill='"& _cor_seta &"' xml:space='preserve' style='white-space: pre' font-family='Segoe UI' font-size='14' font-weight='600' letter-spacing='0em'>
                <tspan x='68' y='31.2969'>"& _seta &"</tspan>
            </text>
        </g>
    </svg>
    "

RETURN 
    _text
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** pelo nome antigo `cartao comissao svg v1` em [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md)
- **Depende de:** `34 Comissao YoY %`
- **É usada por:** nenhuma medida

## `64 SVG Tabela HTML Content Lite v1`

Desenha, em SVG, uma linha de tabela por cidade, com o faturamento abreviado e a variação da margem contra o ano anterior. Alterna entre os dois ao passar o mouse. *(descrição deduzida do código)*

```dax
VAR _cidade = SELECTEDVALUE( dClientes[Cidade] )

VAR _valor = [51 Faturamento formatação de texto]

VAR _margem = FORMAT(  [27 Margem YoY %], "#.0 %")
-----------------------------------
--- Formatação                 ----
-----------------------------------
var __cor_fonte =  "#D6D7E3"

VAR _cores = 
SWITCH(
    TRUE(),
    [27 Margem YoY %] > 0 , "green",
    [27 Margem YoY %] < 0 , "red",
    "#ffffff"
)

RETURN
    "
    <svg width='255' height='79' viewBox='0 0 255 65' fill='none' xmlns='http://www.w3.org/2000/svg'>

        <defs>
            <style>
                #txt_margem, #txt_cidade, #txt_faturamento  {
                    transition: .7s
                }


                svg:hover #txt_faturamento  {
                    transform: translateX( -126px)
                }
                svg:hover #txt_cidade {
                    transform: translateX(126px)
                }
                svg:hover  #txt_margem {
                    transform: translateX( -126px)
                }

            </style>
        </defs>

        <g id='tabela_cidades'>
            <line id='divisor' x1='127.5' y1='14' x2='127.5' y2='50' stroke='white' stroke-opacity='0.1'/>
            <text id='txt_cidade' fill='"& __cor_fonte &"' font-family='Segoe UI' font-size='11' font-weight='600'>
                <tspan x='28' y='34.0547'> " & _cidade & " </tspan>
            </text>
            <text id='txt_faturamento' fill='"& __cor_fonte &"' font-family='Segoe UI' font-size='15' font-weight='600'>
                <tspan x='155' y='26.2109'> R$ "& _valor &" </tspan>
            </text>
            <text id='txt_margem' fill='"& _cores &"' font-family='Segoe UI' font-size='15' font-weight='600'>
                <tspan x='155' y='53.2109'> "& _margem &" </tspan>
            </text>
        </g>
    </svg>
    "
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** [Comercial](../guias-do-relatorio/comercial.md); pelo nome antigo `tabela hml contente lite v1` em [Comercial antes](../arquivo/guias-anteriores.md)
- **Depende de:** `27 Margem YoY %`, `51 Faturamento formatação de texto`
- **É usada por:** nenhuma medida

## `65 SVG Percentual Meta Velocimetro`

Medida de nome "velocímetro", cuja expressão é apenas o valor `1`. *(descrição deduzida do código)*

```dax
1
```

- **Tabela:** `_Medidas`
- **Formato:** `0`
- **Usada nas guias:** nenhum visual
- **Depende de:** nenhuma medida
- **É usada por:** nenhuma medida
- **Observação:** O formato de exibição é `0` e a expressão é o valor fixo `1`.

## `66 Meta Cor`

Cor da meta conforme o percentual atingido: verde a partir de 60%, vermelho abaixo de 10% e cinza entre os dois. *(descrição deduzida do código)*

```dax
SWITCH(
    TRUE(),
    [41 Porcentagem Meta] >= 0.6, "green",
    [41 Porcentagem Meta] < 0.10 , "red",
    "grey"
)
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** pelo nome antigo `Meta Cor` em [Vendedores](../guias-do-relatorio/vendedores.md), [Vendedores antes](../arquivo/guias-anteriores.md)
- **Depende de:** `41 Porcentagem Meta`
- **É usada por:** nenhuma medida
- **Regra de negócio:** [Metas](../regras-de-negocio.md#metas)
