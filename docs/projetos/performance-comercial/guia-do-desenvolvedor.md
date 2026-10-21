# Guia do desenvolvedor

Convenções práticas para trabalhar no painel e na documentação. Para instalar e rodar o site, veja o `README.md` na raiz do repositório.

## Primeiros passos depois de clonar

1. Instale o [uv](https://docs.astral.sh/uv/) e rode `uv sync` na raiz para instalar as dependências da documentação.
2. Para ver a documentação no navegador: `uv run mkdocs serve` (endereço `http://127.0.0.1:8000`).
3. Para abrir o painel no Power BI Desktop, atualize antes o valor dos três parâmetros de caminho dos dados. O passo a passo está em [Como atualizar o valor dos parâmetros](fontes-de-dados.md#como-atualizar-o-valor-dos-parametros).

## Onde está cada coisa

| Quero mexer em… | Arquivo |
|---|---|
| Uma medida ou coluna | `src/projeto/performance-comercial/Performance Comercial.SemanticModel/definition/tables/<Tabela>.tmdl` |
| Um relacionamento | `src/projeto/performance-comercial/Performance Comercial.SemanticModel/definition/relationships.tmdl` |
| Uma consulta compartilhada ou parâmetro | `src/projeto/performance-comercial/Performance Comercial.SemanticModel/definition/expressions.tmdl` |
| Uma guia do relatório | `src/projeto/performance-comercial/Performance Comercial.Report/definition/pages/<id>/page.json` |
| A ordem das guias | `src/projeto/performance-comercial/Performance Comercial.Report/definition/pages/pages.json` |
| Um visual | `src/projeto/performance-comercial/Performance Comercial.Report/definition/pages/<id>/visuals/<id>/visual.json` |
| Os dados | `data/` (na raiz do repositório) |
| A documentação deste projeto | `docs/projetos/performance-comercial/` |

Prefira editar pelo Power BI Desktop e salvar. Editar o TMDL à mão funciona, mas confira no Desktop antes de commitar.

!!! warning "Renomear medidas fora do Power BI Desktop"
    O Power BI Desktop atualiza os visuais do relatório quando você renomeia uma medida. Se a renomeação for feita editando o TMDL ou por uma ferramenta externa, os visuais continuam apontando para o nome antigo. Hoje o relatório tem 25 nomes antigos desse tipo (ver [Nomes antigos de medidas](medidas-dax/index.md#nomes-antigos-de-medidas-no-relatorio)). Depois de renomear, abra o relatório e confira se algum visual mostra campo não encontrado.

## Regras para o modelo

- **Nenhuma medida fica sem pasta de exibição ao final de uma tarefa.** Antes do commit, toda medida nova ou alterada está numa pasta. Hoje 9 medidas estão sem pasta (ver [Sem pasta de exibição](medidas-dax/sem-pasta.md)); a documentação só registra isso.
- **Não renomeie pastas de exibição nem guias sem necessidade.** Renomear quebra o vínculo com a documentação sem avisar. Se precisar reorganizar, crie uma pasta nova, mova as medidas e registre no changelog.
- **Documente a medida no próprio modelo.** No TMDL, `///` antes de `measure` vira a descrição exibida no Power BI, e um comentário `//` na primeira linha da expressão explica a conta. Exemplo real do projeto:

    ```tmdl
    /// Lucro Bruto em R$ = Faturamento - Custo
    measure '03 Lucro Bruto' =

            // Lucro Bruto = Faturamento - Custo
            [01 Faturamento] - [02 Custo]
        formatString: "R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00
        displayFolder: 01.Principais
    ```

    Hoje só 8 das 50 medidas têm `///` e 9 têm comentário `//`.

## Nomes

**Tabelas.** O prefixo diz o papel da tabela.

| Prefixo | Papel | Exemplos |
|---|---|---|
| `f` | Fato | `fVendas`, `fMetas` |
| `d` | Dimensão | `dClientes`, `dProdutos`, `dCalendario` |
| `_` | Só medidas | `_Medidas` |
| `z` | Auxiliar | `zMetricas` |

**Colunas.** Nomes em português, com espaços e acentos. As chaves começam com `Id` (por exemplo, `Id Cliente`) e são números inteiros, exceto `dCalendario[Id Data]`, que é uma data. A única coluna com nome em minúsculas é `fMetas[data]`.

**Medidas.** O nome tem um número e uma descrição, por exemplo `01 Faturamento`. A faixa do número diz o tipo da medida, como está hoje no modelo:

| Faixa | Tipo | Exemplos |
|---|---|---|
| 01 a 13 | Principais | `01 Faturamento`, `10 Margem`, `12 Positivação Clientes` |
| 20 a 35 | Comparações no tempo | `22 Faturamento LY`, `23 Faturamento YoY %` |
| 40 a 42 | Metas | `40 Meta`, `41 Porcentagem Meta` |
| 50 a 54 | Auxiliares e formatação | `50 Eixo Y max Grafico Comercial`, `52 Rank Cidade` |
| 60 a 66 | Visuais SVG e cores | `60 SVG Cartao Faturamento v1`, `66 Meta Cor` |
| sem número | Tabela `zMetricas` | `Linha Atual`, `Seta para Cima` |

Sufixos de tempo: `LY` (mesmo período do ano anterior), `LM` (mês anterior), `YoY` (variação contra o ano anterior) e `MoM` (variação contra o mês anterior). O acumulado no ano (YTD) é `Acumulado`, sem sufixo.

**Pastas de exibição.** `01.Principais`, `02. Temporais`, `03. Formatações` e `.Visuais SVG`. Repare que `01.Principais` não tem espaço depois do ponto e as outras têm.

!!! pendente "A confirmar"
    A documentação anterior reservava as faixas 80 a 89 para rankings e 90 a 99 para testes. Hoje nenhuma medida usa essas faixas, e o ranking (`52 Rank Cidade`) está na faixa 50. As faixas 80 a 99 continuam reservadas?

## Padrões de DAX usados no projeto

O que o código do modelo faz hoje (conferido nas 50 medidas):

- **Divisão com `DIVIDE`:** as 11 medidas que dividem usam `DIVIDE(..., ..., BLANK())`, e nenhuma usa o operador `/`. Com denominador zero, o resultado fica em branco.
- **Variáveis (`VAR`):** 22 medidas usam variáveis, entre elas todas as de variação (`YoY` e `MoM`), a `04 Margem Bruta` e as de SVG. As medidas curtas (soma, subtração) não usam.
- **Filtro de status explícito:** as medidas de valor filtram `dStatus[Id Status] = 1` dentro de `CALCULATE`.
- **Comparações no tempo:** usam `SAMEPERIODLASTYEAR`, `DATEADD` e `DATESYTD`, com o filtro `dCalendario[Datas com Venda] = TRUE()` (ver [Comparações no tempo](regras-de-negocio.md#comparacoes-no-tempo)).
- **Sem `FILTER`:** nenhuma medida usa a função `FILTER`.
- **Colunas calculadas:** só existem em `dCalendario` (`Datas com Venda`, `Semana dia Num` e `Semana dia Nome`). Valores de linha, como o total de uma venda, são calculados por medida (`SUMX`), não por coluna.
- **Formatos de exibição:** moeda `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00` (algumas medidas sem centavos), percentual `0.00%;-0.00%;0.00%` e inteiros `#,0` ou `0`.

## Conceitos do modelo

| Termo | Significado |
|---|---|
| Granularidade | O nível de detalhe de uma tabela, ou seja, o que uma linha representa. Em `fVendas`, uma linha é um item vendido |
| Cardinalidade | O tipo de relacionamento entre duas tabelas. No modelo, todos são de muitos para um (do fato para a dimensão) |
| Filtro de contexto | Os filtros ativos no momento do cálculo (filtros do relatório, linhas e colunas do visual). Uma medida é recalculada em cada contexto |
| Medida | Cálculo em DAX feito na hora, no contexto do visual (ver [Medidas DAX](medidas-dax/index.md)) |
| Coluna calculada | Coluna em DAX gravada na tabela no momento da carga (ver `dCalendario` em [Modelo de dados](modelo-de-dados.md)) |
| Dimensão com vários papéis (*role-playing*) | Uma dimensão ligada ao fato por mais de uma coluna, com significados diferentes. Aqui, `dCalendario` liga com `Data Pedido` e `Data Envio` |

### Relacionamento inativo e `USERELATIONSHIP`

O Power BI só permite um relacionamento **ativo** entre duas tabelas. Por isso `fVendas[Data Envio]` está ligado a `dCalendario` como inativo, e só `Data Pedido` filtra por padrão. Para calcular por data de envio, uma medida precisa ativar o relacionamento com `USERELATIONSHIP`. O desenvolvedor decidiu manter esse relacionamento, mas hoje nenhuma medida o usa.

Exemplo de como seria (não existe no modelo):

```dax
Faturamento por Envio =
CALCULATE(
    [01 Faturamento],
    USERELATIONSHIP( fVendas[Data Envio], dCalendario[Id Data] )
)
```

## O que o modelo já respeita

| Prática | Situação no projeto |
|---|---|
| Esquema estrela | Sim: 2 fatos e 7 dimensões, sem dimensões ligadas a outras dimensões |
| Chaves inteiras | Sim: todas as colunas `Id` são `int64`, exceto `dCalendario[Id Data]`, que é uma data |
| Relacionamentos em uma só direção | Sim: os 10 relacionamentos filtram da dimensão para o fato |
| Calendário contínuo e marcado como tabela de datas | Sim: `dCalendario` não tem dias faltando e está marcada como data (`dataCategory: Time`, chave `Id Data`) |
| Dimensões com chave única | Esperado, mas **não conferido** nesta documentação (os dados não foram lidos) |

## Solução de problemas

Dicas gerais para problemas comuns de modelo. As consultas abaixo são diagnósticos que você pode rodar na visão de consulta DAX do Power BI Desktop.

**Totais maiores que o esperado.** Uma dimensão com a mesma chave repetida duplica as linhas do fato. Confira:

```dax
EVALUATE
ROW( "Duplicatas", COUNTROWS( dClientes ) - DISTINCTCOUNT( dClientes[Id Cliente] ) )
```

O resultado deve ser `0`. Faça o mesmo para as outras dimensões.

**Linhas "(Em branco)" nos visuais.** O fato tem uma chave que não existe na dimensão, ou uma chave vazia. Confira as vendas sem cliente correspondente:

```dax
EVALUATE
ROW( "Sem cliente", COUNTROWS( FILTER( fVendas, ISBLANK( RELATED( dClientes[Id Cliente] ) ) ) ) )
```

Se houver linhas, corrija a planilha de origem ou acrescente uma linha "Desconhecido" na dimensão.

**Um filtro (segmentação) não filtra o visual.** Verifique, no modelo, se o relacionamento existe, se está ativo e se aponta no sentido certo. Lembre que `Data Envio` está inativo.

**Comparação com o ano anterior volta em branco.** Confira se o relacionamento de `fVendas[Data Pedido]` com `dCalendario` está ativo, se o calendário cobre o período do dado (vai de 01/01/2018 a 31/12/2021) e se a coluna `Datas com Venda` está sendo usada como o modelo espera.

!!! pendente "A confirmar"
    As consultas DAX de diagnóstico desta seção são sugestões gerais e **não foram executadas** neste projeto. Rode cada uma no Power BI Desktop e ajuste, se for o caso.

## Ao alterar o painel

1. Faça a mudança no Power BI Desktop e salve o PBIP.
2. Confira o diff só nas pastas que você esperava mudar.
3. Atualize a página afetada: medida → [Medidas DAX](medidas-dax/index.md) (incluindo "depende de" e "é usada por"); tabela ou relacionamento → [Modelo de dados](modelo-de-dados.md); guia → página da guia.
4. Decisão de arquitetura → [Decisões técnicas](decisoes-tecnicas.md), com data e commit.
5. Anote no [Changelog](changelog.md), em `[Não publicado]`, citando as medidas pelo nome.
6. Rode `uv run mkdocs build --strict`. O build só passa depois que as páginas novas estão commitadas.
7. Publique a documentação com `uv run mkdocs gh-deploy` (o repositório ainda não tem publicação automática) e abra o pull request com o checklist.

## Checklist do pull request

- [ ] `uv run mkdocs build --strict` passou sem avisos.
- [ ] O diff do Power BI mexe só nas pastas esperadas.
- [ ] O changelog foi atualizado, citando as medidas pelo nome.
- [ ] As páginas das medidas alteradas têm "depende de" e "é usada por" atualizados.
- [ ] Toda página nova está no `.nav.yml` do projeto.
- [ ] Se uma regra de negócio mudou, a validação de negócio foi pedida.
- [ ] O que o agente escreveu foi revisado linha a linha.
