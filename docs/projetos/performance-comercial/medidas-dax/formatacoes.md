# Formatações

Medidas da pasta de exibição `03. Formatações`: **2**. Medidas auxiliares de formatação e de escala de gráficos. Veja o [catálogo](index.md) para as outras pastas.

As descrições marcadas como *deduzidas do código* foram escritas a partir da expressão DAX. As demais vêm do texto `///` do modelo. "Depende de" e "É usada por" vêm do script de levantamento. Em "Usada nas guias", cada guia aparece uma vez, inclusive as ocultas, as de dica de ferramenta e as versões "antes".

## `50 Eixo Y max Grafico Comercial`

Maior faturamento mensal no contexto selecionado, multiplicado por 1,5. Pelo nome, define o limite do eixo Y do gráfico da guia Comercial. *(descrição deduzida do código)*

```dax
VAR _tab = 
    ALLSELECTED( dCalendario[Mes Abreviado] , dCalendario[Mês] )

VAR _MaiorValor = 
    MAXX( _tab , [01 Faturamento] )

RETURN 
    _MaiorValor * 1.50
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** pelo nome antigo `Eixo Y max Grafico Comercial` em [Comercial](../guias-do-relatorio/comercial.md), [Comercial antes](../arquivo/guias-anteriores.md)
- **Depende de:** `01 Faturamento`
- **É usada por:** nenhuma medida

## `51 Faturamento formatação de texto`

Faturamento em texto abreviado: bilhões (`B`), milhões (`M`), milhares (`K`) ou o número inteiro. *(descrição deduzida do código)*

```dax
VAR _valor =[01 Faturamento]

RETURN
        SWITCH( TRUE(),
            ABS( _valor ) >=  1E9, FORMAT( _valor , "##,,,.00 B; -#,,,.0  B; -"),
            ABS( _valor ) >=  1E6, FORMAT( _valor , "##,,.00 M; -#,,.0  M; -"),
            ABS( _valor ) >=  1E3, FORMAT( _valor , "##,.00 K; -#,.0  K; -"),
            FORMAT( _valor , "#;-#;-")
            )
```

- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** nenhum visual
- **Depende de:** `01 Faturamento`
- **É usada por:** `64 SVG Tabela HTML Content Lite v1`
