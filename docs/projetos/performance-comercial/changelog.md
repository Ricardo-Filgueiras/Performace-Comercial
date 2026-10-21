# Changelog

Mudanças relevantes do painel e da documentação deste projeto. Mudanças do portal inteiro estão no [changelog do portal](../../changelog.md).

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). O changelog registra **o que mudou**; toda entrada cita pelo nome as medidas afetadas. Cada versão recebe uma tag `performance-comercial/vX.Y.Z`.

## [Não publicado]

Reescrita da documentação e reorganização das pastas, em 21/10/2026. **Nenhuma medida DAX foi alterada.**

!!! pendente "Linha de base e tags"
    Ponto de partida previsto: a tag `performance-comercial/baseline-pre-documentacao`. Ela **ainda não foi criada**. O repositório também não tem a tag `performance-comercial/v2.0.0`. As datas e os commits abaixo vêm do histórico do Git.

### Adicionado

- Documentação do projeto no padrão da skill `documentacao-bi` 0.1.0, em `docs/projetos/performance-comercial/`: [escopo](escopo.md), [regras de negócio](regras-de-negocio.md), [guias do relatório](guias-do-relatorio/index.md) (8 páginas), [modelo de dados](modelo-de-dados.md), [medidas DAX](medidas-dax/index.md) (50 medidas, com "depende de" e "é usada por"), [fontes de dados](fontes-de-dados.md), [decisões técnicas](decisoes-tecnicas.md) (13 decisões), [guia do desenvolvedor](guia-do-desenvolvedor.md) e [guias anteriores](arquivo/guias-anteriores.md).
- Portal de documentação com menu por pasta, metodologia ([DataOps](../../metodologia/dataops.md) e [versionamento com Git](../../metodologia/versionamento-git.md)) e aviso de pendência. Kit e skill em `.agents/` (`6cf9c4c`).
- Guia de como atualizar o valor dos três parâmetros de caminho depois de clonar o repositório (em [Fontes de dados](fontes-de-dados.md#como-atualizar-o-valor-dos-parametros)).
- Arquivo `LICENSE` (MIT), citado pelo `README.md` mas que não existia (`148ba4d`).
- Grupo de consultas **Parâmetros de dados**, que reúne `Caminho_Extracao`, `Caminho_Dimensoes` e `Caminho_Meta` (`c116cef`).

### Alterado

- Projeto Power BI movido para `src/projeto/performance-comercial/` e renomeado de "Performace Comercial" para "Performance Comercial" (arquivo `.pbip` e pastas `.Report` e `.SemanticModel`) em `c116cef` e `2d2af2d`.
- Dados movidos de `src/data/` para `data/`, na raiz (`3578022`). Os valores dos três parâmetros passaram a apontar para a nova pasta (`2d2af2d`). As consultas das tabelas `fVendas`, `fMetas`, `dClientes`, `dProdutos`, `dVendedores`, `dUnidades`, `dStatus` e `dPagamento` e a consulta `dCidades` não mudaram.
- `README.md`: árvore de pastas, passo de abertura do projeto e endereço de clone corrigido.
- Dependências de `mkdocs.yml` e `pyproject.toml`: plugins `awesome-nav`, `git-revision-date-localized` e `panzoom`, com o MkDocs fixado abaixo da versão 2.
- Anotação `PBI_ResultType` das tabelas voltou de `Exception` para `Table` (`56b7cb6`), desfazendo a mudança de `2f2c698`, de 23/04/2026. Página ativa do relatório trocada de "Analítico antes" para a Capa.

### Corrigido

Correções na **documentação** (o modelo não foi alterado):

- Colunas de `dClientes` (`Cliente`, `Cidade`, `UF`, `Estado`), `dVendedores` (`Vendedor`, `URL Foto`, `Gerente`), `dProdutos` (`Produto`) e `fMetas` (`Valor Meta`), que a documentação de 30/01/2026 descrevia de outra forma.
- `dCalendario`: valores `Sem1` e `Tri1`, hierarquia `Data` (Ano, Mes Abreviado, Dia), período de 01/01/2018 a 31/12/2021 e a definição de `Datas com Venda`.
- `dStatus`: os valores são Válidas e Inválidas, e não "Efetivado" e "Cancelado".
- `42 Diferença Meta`: usa valor absoluto (`ABS`), e não "Faturamento − Meta".
- Despesa e impostos: a descrição de frete, ICMS, PIS e COFINS foi retirada, porque não está no modelo.

### Removido

- As páginas antigas `docs/01 visao geral.md`, `02 dicionario dados.md`, `03 guia medidas dax.md`, `04 relacionamentos.md`, `05 changelog.md` e `06 boas praticas.md`, mais `docs/estrutura_definition_legivel.md` e `docs/requisitos.md`, depois de migradas para as páginas do projeto. O histórico delas continua no Git.

### Problemas conhecidos (não corrigidos)

- 25 nomes antigos de medidas no relatório, como `Faturamento` no lugar de `01 Faturamento` (ver [Nomes antigos de medidas](medidas-dax/index.md#nomes-antigos-de-medidas-no-relatorio)).
- 3 botões apontam para marcadores inexistentes e 1 botão de navegação não tem destino (ver [Guias do relatório](guias-do-relatorio/index.md)).
- 9 medidas sem pasta de exibição: `52 Rank Cidade`, `53 Max Y Visual 01 pg Vendedores`, `54 Nome Vendedor` e as 6 medidas de `zMetricas`.
- O arquivo `.github/workflows/docs.yml` está vazio, e a documentação é publicada manualmente.

## [2.0.0] - 2026-01-30

Versão registrada na documentação anterior. No Git, o modelo dessa versão está no commit `23c7839`, de 02/02/2026. Não existe tag. Os itens abaixo vêm do changelog anterior e foram conferidos contra o modelo atual; o Git não permite separar essas mudanças das outras do mesmo commit.

### Adicionado

- `03 Lucro Bruto` (faturamento menos custo) e `04 Margem Bruta` (essa diferença dividida pelo faturamento), na pasta `01.Principais`.
- Documentação em seis páginas numeradas (visão geral, dicionário de dados, guia de medidas DAX, relacionamentos, changelog e boas práticas).
- Prefixo numérico nos nomes das medidas, nas faixas descritas no [Guia do desenvolvedor](guia-do-desenvolvedor.md#nomes).

### Alterado

- Medidas renomeadas com prefixo numérico, por exemplo `Faturamento` para `01 Faturamento`, `Meta` para `40 Meta` e `rank cidade` para `52 Rank Cidade`. Hoje a tabela `_Medidas` tem 44 medidas, todas numeradas. A documentação anterior falava em 48 medidas renomeadas, número que não bate com o modelo.
- Medidas de variação no tempo reescritas com variáveis (`VAR`): `23 Faturamento YoY %`, `24 Faturamento MoM %`, `27 Margem YoY %`, `28 Margem MoM %`, `31 Resultado YoY %`, `32 Resultado MoM %`, `34 Comissao YoY %` e `35 Comissao MoM %`.
- Descrição (`///`) acrescentada às medidas `03 Lucro Bruto`, `04 Margem Bruta`, `10 Margem`, `12 Positivação Clientes` e `13 Positivação Produtos`.
- Pastas de exibição: `01.Principais`, `02. Temporais`, `03. Formatações` e `.Visuais SVG`.

### Corrigido

- `12 Positivação Clientes` e `13 Positivação Produtos` passaram a contar só as vendas válidas (`Id Status = 1`). Segundo a documentação anterior, antes contavam todas.
- Divisões com `DIVIDE(..., ..., BLANK())`, para não dar erro quando o denominador é zero: `10 Margem`, `23 Faturamento YoY %`, `24 Faturamento MoM %`, `27 Margem YoY %`, `28 Margem MoM %`, `31 Resultado YoY %`, `32 Resultado MoM %`, `34 Comissao YoY %`, `35 Comissao MoM %` e `41 Porcentagem Meta`.

## Histórico anterior a 2.0.0

Reconstruído a partir do Git. O projeto não tinha versões nem tags antes da 2.0.0. A documentação anterior citava versões "1.0.0" e "1.5.0" com datas estimadas, que **não** foram mantidas aqui, porque o histórico não as confirma.

| Data | Commit | O que mudou |
|---|---|---|
| 2025-10-22 | `1812783`, `cd6a9ab`, `06b3f4c` | Início do repositório, com o painel em arquivo `.pbix` e os dados em `src/data/` |
| 2025-10-24 | `8703e41` | Painel passa ao formato PBIP; modelo e primeira guia Comercial, com o gráfico de evolução do faturamento |
| 2025-10-24 | `f133257` | Cartões SVG de variação contra o ano anterior |
| 2025-10-27 | `e605e67`, `c68eea1`, `ee3781d`, `0e2804a` | Ajuste das consultas das dimensões, visual de conteúdo HTML, botões que alternam tabela e ranking por cidade e primeira dica de ferramenta |
| 2025-11-03 | `4ed3100`, `f033698` | Dica de ferramenta dos vendedores por gerente (com a tabela `zMetricas`) e dica da tabela de vendedores por cidade, com uma nova página |
| 2025-11-04 | `16f76c2`, `47aca61`, `1df255a` | Guia Mapa Calor e início da guia Vendedores |
| 2025-11-05 | `fb30781`, `34c0567` | Guia Vendedores e Capa finalizadas; menu lateral e navegação |
| 2025-11-11 | `e0dd518`, `fb3fb1b` | Versão "completa" do painel, com as imagens e as guias "antes"; ajuste do README e da seção de portfólio |
| 2026-02-02 | `63872c7`, `23c7839` | Modelo removido e recolocado no mesmo dia; renomeação das medidas e documentação em seis páginas (ver 2.0.0) |
| 2026-04-23 | `0773ea2` | MkDocs Material, `.gitattributes` e documentação movida para `docs/`; `.pbix` original removido |
| 2026-04-23 | `2f2c698` | Página ativa do relatório e anotação `PBI_ResultType` das tabelas |

## Planejado

Sem data prevista, ver [Escopo](escopo.md#planejado-ainda-nao-implementado): ticket médio, curva ABC de produtos, produtividade por vendedor e projeção de meta.
