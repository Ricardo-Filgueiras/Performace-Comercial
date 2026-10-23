<!-- pasta: 03. Formatações -->
# 03. Formatações

<!-- gerado:inicio resumo -->
Medidas da pasta de exibição `03. Formatações`: **2**. Veja o [catálogo](index.md) para as outras pastas.
<!-- gerado:fim resumo -->

## 50 Eixo Y max Grafico Comercial

Maior faturamento mensal no contexto selecionado, multiplicado por 1,5. Pelo nome, define o limite do eixo Y do gráfico da guia Comercial. *(descrição deduzida do código)*

<!-- gerado:inicio medida:50 Eixo Y max Grafico Comercial -->
- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento)
- **É usada por:** nenhuma medida

```dax
VAR _tab = 
    ALLSELECTED( dCalendario[Mes Abreviado] , dCalendario[Mês] )

VAR _MaiorValor = 
    MAXX( _tab , [01 Faturamento] )

RETURN 
    _MaiorValor * 1.50
```
<!-- gerado:fim medida:50 Eixo Y max Grafico Comercial -->

## 51 Faturamento formatação de texto

Faturamento em texto abreviado: bilhões (`B`), milhões (`M`), milhares (`K`) ou o número inteiro. *(descrição deduzida do código)*

<!-- gerado:inicio medida:51 Faturamento formatação de texto -->
- **Tabela:** `_Medidas`
- **Formato:** padrão
- **Usada nas guias:** nenhum visual
- **Depende de:** [`01 Faturamento`](01-principais.md#01-faturamento)
- **É usada por:** [`64 SVG Tabela HTML Content Lite v1`](visuais-svg.md#64-svg-tabela-html-content-lite-v1)

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
<!-- gerado:fim medida:51 Faturamento formatação de texto -->
