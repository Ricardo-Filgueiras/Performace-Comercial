# Decisões técnicas

Registro de decisões de arquitetura do painel no formato ADR (*Architecture Decision Record*). Cada decisão tem:

- **Data e Commit:** quando a decisão entrou no repositório (`git log -1 --format="%h %ad" --date=short`). Preencha no momento em que escrever a decisão.
- **Contexto:** o problema ou a restrição que levou à decisão.
- **Decisão:** o que foi escolhido.
- **Consequências:** o que muda, para o bem e para o mal.

!!! pendente "Motivos não registrados"
    Estas decisões foram reconstruídas em 21/10/2026 a partir dos arquivos e do histórico do Git. A data e o commit são o **primeiro commit em que a decisão aparece** nos arquivos. O histórico não guarda o **motivo** das decisões mais antigas, então o "Contexto" delas só descreve o que se vê nos arquivos. O desenvolvedor deve completar os motivos que lembrar. As decisões tomadas durante a reescrita da documentação (21/10/2026) trazem o motivo dado pelo desenvolvedor.

---

## ADR-001: Projeto Power BI no formato PBIP, versionado com Git

- **Data:** 2025-10-24
- **Commit:** `8703e41`

**Contexto.** O repositório começou em 22/10/2025 com o painel em um arquivo `.pbix` (commit `cd6a9ab`). Dois dias depois, o commit `8703e41` trocou o `.pbix` pelo formato PBIP, em que o modelo e o relatório são arquivos de texto. Arquivos `.pbix` ainda apareceram e sumiram do repositório em outros commits, até o `0773ea2` (2026-04-23). Hoje não há nenhum `.pbix`.

**Decisão.** Manter o painel como projeto PBIP (pastas `.SemanticModel` e `.Report`) e versionar tudo com Git.

**Consequências.** Mudanças no modelo e no relatório aparecem como diferenças de texto no Git e podem ser conferidas por script. Não é possível abrir o projeto sem o Power BI Desktop em uma versão que leia PBIP (o README pede a 2.146 ou superior). Os arquivos `.pbi/cache.abf` e `.pbi/localSettings.json` ficam fora do histórico, pelo `.gitignore`.

## ADR-002: Esquema estrela com dois fatos e sete dimensões, em modo Import

- **Data:** 2025-10-24
- **Commit:** `8703e41` (as tabelas foram removidas no commit `63872c7` e recolocadas no `23c7839`, em 2026-02-02)

**Contexto.** O primeiro commit com o modelo semântico já traz as tabelas de vendas e de metas, as dimensões e as medidas, todas carregadas a partir de planilhas.

**Decisão.** Modelar em esquema estrela, com `fVendas` e `fMetas` como fatos e sete dimensões (`dCalendario`, `dClientes`, `dProdutos`, `dVendedores`, `dUnidades`, `dStatus` e `dPagamento`). Todos os relacionamentos são de muitos para um e filtram em uma só direção. Todas as tabelas usam o modo Import.

**Consequências.** O modelo é simples de ler e de documentar (ver [Modelo de dados](modelo-de-dados.md)). Os dados ficam dentro do arquivo do modelo e só mudam quando alguém atualiza no Power BI Desktop. `fVendas` e `fMetas` não se ligam diretamente: encontram-se por `dVendedores` e `dCalendario`.

## ADR-003: Dados em planilhas Excel na pasta `data/`, com caminhos em parâmetros

- **Data:** 2025-10-24 (parâmetros de caminho); 2026-10-21 (grupo "Parâmetros de dados" e pasta `data/` na raiz)
- **Commit:** `8703e41` (parâmetros), `c116cef` (grupo de parâmetros) e `3578022` (pasta `data/` na raiz)

**Contexto.** Os dados do projeto são fictícios e ficam no próprio repositório. Quem clonar o projeto precisa apontar o modelo para a pasta de dados da sua cópia.

**Decisão.** Guardar os dados em planilhas Excel na pasta `data/`, na raiz do repositório, e ler cada pasta por um parâmetro do Power Query (`Caminho_Extracao`, `Caminho_Dimensoes` e `Caminho_Meta`), reunidos no grupo de consultas "Parâmetros de dados". A documentação traz o guia de como atualizar o valor dos parâmetros (ver [Fontes de dados](fontes-de-dados.md#como-atualizar-o-valor-dos-parametros)).

**Alternativa descartada.** Ler os dados em CSV pelo endereço "raw" do GitHub, porque o link "raw" de um `.xlsx` baixa o arquivo em vez de mostrá-lo. O desenvolvedor esclareceu em 21/10/2026 que o projeto **não usa CSV**: os dados continuam em Excel, junto com o projeto.

**Consequências.** Os valores dos parâmetros são caminhos absolutos, então cada pessoa que clonar o projeto precisa atualizá-los antes da primeira atualização dos dados. A consulta `fMetas` depende do nome `Meta 2018.xlsx` (ver [Fontes de dados](fontes-de-dados.md#transformacoes-no-power-query)).

## ADR-004: Valores só das vendas válidas (`Id Status = 1`)

- **Data:** 2025-10-24
- **Commit:** `8703e41`

**Contexto.** A planilha de vendas tem vendas com dois status, "Válidas" (`Id Status = 1`) e "Inválidas" (`Id Status = 2`).

**Decisão.** As medidas de valor (faturamento, custo, despesa, impostos e comissão) e de positivação filtram `dStatus[Id Status] = 1` dentro de `CALCULATE`. A quantidade de vendas (`11 Qtde Vendas`) é a exceção e conta vendas de qualquer status, o que o desenvolvedor confirmou ser intencional em 21/10/2026.

**Consequências.** O faturamento não inclui vendas inválidas. A quantidade de vendas e o faturamento não se referem ao mesmo conjunto de vendas (ver [Regras de negócio](regras-de-negocio.md#vendas-validas)).

## ADR-005: Calendário gerado no Power Query, marcado como tabela de datas, com `Datas com Venda`

- **Data:** 2025-10-24
- **Commit:** `8703e41`

**Contexto.** As comparações no tempo (ano anterior, mês anterior e acumulado no ano) precisam de uma dimensão de datas contínua.

**Decisão.** Gerar `dCalendario` dentro do Power Query (1.461 dias a partir de 01/01/2018, ou seja, até 31/12/2021), marcá-la como tabela de datas e criar a coluna calculada `Datas com Venda`, usada como filtro nas comparações no tempo. A data final fixa é intencional: o projeto não receberá dados depois de 31/12/2021.

**Consequências.** Não há arquivo de calendário para manter. Se algum dia entrarem vendas depois de 2021, o calendário precisa ser estendido na consulta. As medidas de tempo dependem da coluna `Datas com Venda` (ver [Regras de negócio](regras-de-negocio.md#comparacoes-no-tempo)).

## ADR-006: Nomes com prefixo, medidas numeradas e pastas de exibição

- **Data:** 2026-02-02
- **Commit:** `23c7839`

**Contexto.** As medidas tinham nomes sem numeração (por exemplo, `Faturamento`). A documentação da época, de 30/01/2026, descreve o sistema de numeração como parte da versão 2.0.

**Decisão.** Nomear tabelas pelo prefixo do papel (`f`, `d`, `_` e `z`) e as medidas com número e descrição (`01 Faturamento`), organizadas nas pastas de exibição `01.Principais`, `02. Temporais`, `03. Formatações` e `.Visuais SVG`. As faixas 80 a 89 (rankings) e 90 a 99 (testes) ficam reservadas, por decisão do desenvolvedor em 21/10/2026, embora nenhuma medida as use. Os detalhes estão no [Guia do desenvolvedor](guia-do-desenvolvedor.md#nomes).

**Consequências.** As medidas ficam fáceis de achar e de ordenar. Mas a renomeação não chegou a todos os visuais do relatório: 25 nomes antigos continuam em uso (ver [Nomes antigos de medidas](medidas-dax/index.md#nomes-antigos-de-medidas-no-relatorio)), e 9 medidas ficaram sem pasta de exibição.

## ADR-007: Cartões e tabelas desenhados com medidas SVG e visual HTML

- **Data:** 2025-10-24 (cartões SVG) e 2025-10-27 (visual de conteúdo HTML)
- **Commit:** `f133257` (cartões SVG) e `e605e67` (visual HTML)

**Contexto.** Os cartões de resumo mostram a variação contra o ano anterior com seta e cor, e a guia Comercial tem uma tabela por cidade que alterna dois valores ao passar o mouse. Esses efeitos não existem nos visuais padrão.

**Decisão.** Desenhar esses elementos com medidas DAX que devolvem imagens SVG (`60` a `64`) e usar um visual personalizado de conteúdo HTML. O relatório também usa um visual personalizado de infográfico na guia Vendedores.

**Consequências.** O visual fica mais rico, mas depende de visuais personalizados (o relatório guarda ao menos um na pasta `CustomVisuals`) e de medidas longas, difíceis de ler (ver [Visuais SVG](medidas-dax/visuais-svg.md)). A medida `65 SVG Percentual Meta Velocimetro` tem só o valor `1` como expressão.

## ADR-008: Dicas de ferramenta com tabela auxiliar `zMetricas`

- **Data:** 2025-11-03
- **Commit:** `4ed3100`

**Contexto.** A rosca de faturamento por gerente da guia Comercial precisa mostrar, ao passar o mouse, a comparação entre o faturamento atual e o do ano anterior por vendedor.

**Decisão.** Criar a tabela auxiliar `zMetricas` (digitada no Power Query) e seis medidas que alternam o valor mostrado conforme a métrica selecionada, usadas na dica de ferramenta `TooltipRosca`. O desenvolvedor confirmou em 21/10/2026 que esse uso é intencional. O relatório tem ainda as dicas `TooltiposGrafico01` e `TooltiposTabela`.

**Consequências.** A tabela `zMetricas` não se liga a nenhuma outra e só serve a essa dica de ferramenta (ver [Dicas de ferramenta](guias-do-relatorio/dica-gerente-vendedores.md)).

## ADR-009: Manter as guias "antes" como histórico

- **Data:** 2025-11-11 (as guias "antes" aparecem no repositório); 2026-10-21 (decisão de mantê-las)
- **Commit:** `e0dd518` (guias) e `56b7cb6` (decisão registrada)

**Contexto.** O relatório guarda quatro guias com a versão anterior das guias de análise: "Comercial antes", "Analítico antes", "Mapa Calor antes" e "Vendedores antes". Elas ficam fora do navegador de páginas da Capa.

**Decisão.** Manter essas guias no relatório, de propósito, para que o desenvolvedor acompanhe a evolução do projeto. A documentação as trata como histórico (ver [Guias anteriores](arquivo/guias-anteriores.md)).

**Consequências.** O relatório fica maior (72 dos 171 visuais estão nas guias "antes") e as guias anteriores usam os nomes antigos de medidas e dois marcadores inexistentes (ver [Guias do relatório](guias-do-relatorio/index.md)).

## ADR-010: Manter o relacionamento inativo por `Data Envio`

- **Data:** 2025-10-24 (relacionamento criado); 2026-10-21 (decisão de mantê-lo)
- **Commit:** `8703e41`

**Contexto.** `fVendas` tem duas colunas de data ligadas a `dCalendario`. Só `Data Pedido` pode ser o relacionamento ativo. Nenhuma medida usa `USERELATIONSHIP`.

**Decisão.** Manter o relacionamento por `Data Envio` como inativo, mesmo sem uso hoje. O desenvolvedor confirmou em 21/10/2026 que ele não deve ser removido.

**Consequências.** O modelo fica pronto para uma análise por data de envio, que exige uma medida com `USERELATIONSHIP` (ver o exemplo no [Guia do desenvolvedor](guia-do-desenvolvedor.md#relacionamento-inativo-e-userelationship)).

## ADR-011: Projeto de portfólio com dados fixos, sem RLS e sem atualização automática

- **Data:** 2026-10-21
- **Commit:** `56b7cb6`

**Contexto.** O Performance Comercial é um projeto de portfólio, com dados fictícios e sem usuários reais.

**Decisão.** Os dados cobrem 2018 a 2021 e não serão atualizados. Não haverá segurança por linha (RLS), nem atualização agendada, nem validação por uma área de negócio. O texto original dos requisitos pedia RLS, atualização automática e metas de desempenho; esses itens foram retirados do escopo (ver [Escopo](escopo.md)).

**Consequências.** O modelo não tem papéis (roles) e a atualização é manual. As regras de negócio descrevem o que o código faz, sem confirmação de uma área de negócio.

## ADR-012: Documentação com MkDocs Material, em um portal por projeto

- **Data:** 2026-04-23 (MkDocs); 2026-10-21 (estrutura de portal)
- **Commit:** `0773ea2` (MkDocs Material) e `08ea67e` (menu por pasta e estrutura de portal)

**Contexto.** A documentação em seis páginas numeradas, de 30/01/2026, tinha um menu central no `mkdocs.yml` e tinha divergências em relação ao modelo.

**Decisão.** Reescrever a documentação em 21/10/2026 no padrão do kit `documentacao-bi` (em `.agents/modelos/`, commit `6cf9c4c`): `docs/projetos/performance-comercial/`, menu por pasta (`.nav.yml`) com os blocos "Para quem usa", "Para quem mantém" e "Arquivo", pendências marcadas, e `mkdocs build --strict` como validação. A reescrita foi feita passo a passo e registrada no diário da migração.

**Consequências.** Toda página nova precisa entrar no menu, senão o build falha. O plugin de datas só funciona com os arquivos commitados. A publicação continua manual, por `mkdocs gh-deploy`, porque o arquivo `.github/workflows/docs.yml` está vazio.

## ADR-013: Organização das pastas do repositório

- **Data:** 2026-10-21
- **Commit:** `c116cef` (projeto Power BI em `src/projeto/performance-comercial/`) e `3578022` (dados em `data/`)

**Contexto.** O padrão do kit de documentação pede `src/<slug>/` para os arquivos do Power BI e `docs/projetos/<slug>/` para a documentação, com o mesmo nome. Os dados estavam em `src/data/` e o projeto em `src/projeto/` com o nome "Performace".

**Decisão.** Mover o projeto Power BI para `src/projeto/performance-comercial/`, corrigir o nome do projeto para "Performance Comercial" e mover os dados para `data/`, na raiz. O slug da documentação é `performance-comercial`.

**Consequências.** O caminho tem um nível a mais que o padrão do kit (`src/projeto/<slug>/` em vez de `src/<slug>/`). O nome do repositório no GitHub e o da pasta local ainda usam a grafia antiga, "Performace-Comercial". O resto do projeto usa "Performance".
