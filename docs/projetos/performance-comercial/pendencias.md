# Pendências

Todas as perguntas em aberto da documentação deste projeto, num lugar só. Cada pendência também aparece na página de origem, como aviso `!!! pendente` ou, nas revisões de texto deduzido, como marca no próprio texto (por exemplo, "descrição deduzida do código").

Ao responder uma pendência: atualize a página de origem, tire o aviso e mova a linha para *Resolvidas*, com a data e a resposta resumida.

## Em aberto

"Afeta números?" quer dizer que a resposta pode mudar um resultado do painel (regra, filtro, cálculo). Essas vêm primeiro. O dono de todas é o desenvolvedor do projeto, porque não há área de negócio por trás do painel.

| # | Pendência | Página | Afeta números? | Dono | Prioridade |
|---:|---|---|---|---|---|
| 1 | Os visuais do relatório usam 25 nomes antigos de medidas que não existem no modelo (por exemplo, `Faturamento`). Abrir o relatório no Power BI Desktop, conferir os campos não encontrados e reapontar os visuais para as medidas atuais | [Medidas DAX](medidas-dax/index.md#nomes-antigos-de-medidas-no-relatorio) | sim | Desenvolvedor | alta |
| 2 | Confirmar que todas as planilhas de meta têm o mesmo formato: 15 colunas, com o Id do vendedor, o nome do vendedor e os 12 meses | [Fontes de dados](fontes-de-dados.md#transformacoes-no-power-query) | sim | Desenvolvedor | média |
| 3 | Conferir os botões do relatório: 3 apontam para marcadores inexistentes (`b665145e7737d486954d` e `51958de021a70cbce700`) e 1 botão de navegação da guia Comercial não tem destino | [Guias do relatório](guias-do-relatorio/index.md#problemas-encontrados-nos-botoes) | não | Desenvolvedor | média |
| 4 | Criar a tag de linha de base `performance-comercial/baseline-pre-documentacao` e a tag `performance-comercial/v2.0.0`. Nenhuma das duas existe | [Changelog](changelog.md) | não | Desenvolvedor | média |
| 5 | Revisar a descrição das 42 medidas escritas a partir do código (as 8 medidas com `///` usam o texto do modelo), em especial `50 Eixo Y max Grafico Comercial`, `53 Max Y Visual 01 pg Vendedores` e `65 SVG Percentual Meta Velocimetro` | [Medidas DAX](medidas-dax/index.md) | não | Desenvolvedor | média |
| 6 | Revisar os textos "Para que serve" e "Como ler" das 8 páginas de guia, deduzidos dos visuais | [Guias do relatório](guias-do-relatorio/index.md) | não | Desenvolvedor | baixa |
| 7 | Revisar as jornadas de uso, deduzidas dos visuais e não testadas com usuários | [Como usar](como-usar.md) | não | Desenvolvedor | baixa |
| 8 | Conferir os nomes dos botões do Power BI Desktop no guia de atualizar os parâmetros, que não foi executado na escrita | [Fontes de dados](fontes-de-dados.md#como-atualizar-o-valor-dos-parametros) | não | Desenvolvedor | baixa |
| 9 | Definir uma meta de tempo de resposta do relatório. O texto anterior falava em menos de 5 segundos, mas isso nunca foi medido | [Escopo](escopo.md) | não | Desenvolvedor | baixa |
| 10 | Completar os motivos das decisões mais antigas, que o histórico do Git não registra | [Decisões técnicas](decisoes-tecnicas.md) | não | Desenvolvedor | baixa |
| 11 | Rodar, no Power BI Desktop, as consultas DAX de diagnóstico sugeridas e conferir se as dimensões têm chave única. Os dados não foram lidos | [Guia do desenvolvedor](guia-do-desenvolvedor.md#solucao-de-problemas) | sim | Desenvolvedor | baixa |
| 12 | Conferir o titular (Ricardo Filgueiras) e o ano (2025) escolhidos para a licença MIT | `LICENSE`, na raiz do repositório | não | Desenvolvedor | baixa |

## Pendências observadas no modelo

Problemas notados no modelo ou no relatório que a documentação não corrige (princípio: a documentação se adapta ao modelo). Nada abaixo foi alterado.

| # | Observação | Onde |
|---:|---|---|
| 1 | 9 medidas estão sem pasta de exibição: `52 Rank Cidade`, `53 Max Y Visual 01 pg Vendedores`, `54 Nome Vendedor` e as 6 medidas de `zMetricas` | [Sem pasta de exibição](medidas-dax/sem-pasta.md) |
| 2 | 8 medidas não têm nenhum uso, nem em visuais nem em outras medidas: `03 Lucro Bruto`, `04 Margem Bruta`, `25 Margem LM`, `28 Margem MoM %`, `29 Resultado LM`, `32 Resultado MoM %`, `35 Comissao MoM %` e `65 SVG Percentual Meta Velocimetro`. Manter ou remover é decisão do desenvolvedor | [Arquivo](arquivo/index.md#medidas-sem-uso-em-visuais) |
| 3 | A medida `65 SVG Percentual Meta Velocimetro` tem como expressão apenas o valor `1` | [Visuais SVG](medidas-dax/visuais-svg.md#65-svg-percentual-meta-velocimetro) |
| 4 | A consulta `fMetas` depende do nome do arquivo `Meta 2018.xlsx` e só entende arquivos nomeados `Meta AAAA.xlsx` | [Fontes de dados](fontes-de-dados.md#transformacoes-no-power-query) |
| 5 | O calendário tem data final fixa (31/12/2021). Vendas posteriores ficariam sem data. Hoje não existem, e isso é intencional | [Modelo de dados](modelo-de-dados.md#dcalendario) |
| 6 | A pasta `01.Principais` não tem espaço depois do ponto, e `02. Temporais` e `03. Formatações` têm | [Guia do desenvolvedor](guia-do-desenvolvedor.md#nomes) |
| 7 | O arquivo `.github/workflows/docs.yml` está vazio. A documentação é publicada manualmente, com `mkdocs gh-deploy` | [Decisões técnicas](decisoes-tecnicas.md#adr-012-documentacao-com-mkdocs-material-em-um-portal-por-projeto) |
| 8 | O nome do repositório no GitHub e o da pasta local ainda usam a grafia antiga "Performace-Comercial" | [Decisões técnicas](decisoes-tecnicas.md#adr-013-organizacao-das-pastas-do-repositorio) |
| 9 | `Catalogo.pdf` e a pasta `data/imagens/` estão no repositório, mas nenhuma consulta os usa | [Fontes de dados](fontes-de-dados.md#consultas-sem-uso-aparente) |
| 10 | As 4 guias "antes" e a documentação anterior usam os nomes antigos de medidas. É um histórico mantido de propósito | [Guias anteriores](arquivo/guias-anteriores.md) |

## Resolvidas

Respostas do desenvolvedor durante a reescrita da documentação.

| # | Pendência | Resposta | Data |
|---:|---|---|---|
| 1 | O projeto é de uso real, estudo ou portfólio? | Portfólio, com dados fictícios | 2026-10-21 |
| 2 | Quem usa o painel? | O gerente de equipe é o usuário de referência. Não há como simular vários usuários | 2026-10-21 |
| 3 | De onde vêm os dados? Excel ou CSV? | Planilhas Excel na pasta `data/`, junto com o projeto. O projeto não usa CSV | 2026-10-21 |
| 4 | As guias "antes" podem sair do relatório? | Não, ficam para mostrar a evolução do projeto | 2026-10-21 |
| 5 | É preciso RLS? | Não | 2026-10-21 |
| 6 | Ticket médio e as análises avançadas continuam no plano? | Sim, como planejado, sem data | 2026-10-21 |
| 7 | Os valores unitários são multiplicados por `Qtde`? | Sim. Conferido no código das medidas | 2026-10-21 |
| 8 | O relacionamento inativo por `Data Envio` pode sair? | Não, deve ficar | 2026-10-21 |
| 9 | O período das vendas coincide com o calendário? | Sim, de 2018 a 2021. Não haverá dados depois de 31/12/2021 | 2026-10-21 |
| 10 | Quais são os valores de `Status`? | Válidas (`1`) e Inválidas (`2`), lidos da planilha | 2026-10-21 |
| 11 | O uso de `zMetricas` na dica `TooltipRosca` é intencional? | Sim | 2026-10-21 |
| 12 | A numeração 80 a 99 continua reservada? | Sim | 2026-10-21 |
| 13 | A composição de despesa, impostos e comissão precisa ser definida? | Não, porque é um projeto de portfólio | 2026-10-21 |
| 14 | `11 Qtde Vendas` deve contar vendas de qualquer status? | Sim, é intencional | 2026-10-21 |
| 15 | A cor da meta (60% e 10%) e o uso de `ABS` na diferença para a meta são intencionais? | Sim | 2026-10-21 |
| 16 | `35 Comissao MoM %` sem o filtro `Datas com Venda` é intencional? | Sim | 2026-10-21 |
| 17 | É preciso validação de negócio? | Não: o projeto é de portfólio | 2026-10-21 |
| 18 | O arquivo `LICENSE` deve ser criado? | Sim, criado com a licença MIT | 2026-10-21 |
| 19 | As páginas antigas podem ser apagadas depois de migradas? | Sim, inclusive `docs/requisitos.md` | 2026-10-21 |
| 20 | Slug e estrutura de pastas | Slug `performance-comercial`; projeto em `src/projeto/performance-comercial/`; dados em `data/` | 2026-10-21 |
