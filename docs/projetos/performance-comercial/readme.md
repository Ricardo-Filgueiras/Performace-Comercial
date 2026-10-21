# Sobre esta documentação

Esta documentação descreve o painel **Performance Comercial** a partir dos arquivos do projeto PBIP em `src/projeto/performance-comercial/`. Ela fica no mesmo repositório que o painel, então o histórico das duas coisas é um só.

O Performance Comercial é um projeto de **portfólio**, com dados fictícios. Acompanha faturamento, margem, resultado, comissão e metas por período, produto, cliente, cidade, unidade e vendedor.

O que não dá para saber pelos arquivos está marcado como pendência e reunido em [Pendências](pendencias.md).

## O projeto em números

| Item | Quantidade |
|---|---|
| Tabelas | 11: 2 fatos (`fVendas`, `fMetas`), 7 dimensões e 2 auxiliares (`_Medidas`, `zMetricas`) |
| Relacionamentos | 10 (9 ativos e 1 inativo) |
| Medidas DAX | 50 |
| Guias do relatório | 12: 5 de análise e entrada, 3 dicas de ferramenta e 4 versões anteriores |
| Período dos dados | 2018 a 2021 |
| Formato dos dados | Planilhas Excel, na pasta `data/` do repositório |

Os números vêm do script de levantamento, rodado sobre o projeto em 21/10/2026.

## Links

- **Painel publicado** no Power BI Service: [abrir o painel](https://app.powerbi.com/view?r=eyJrIjoiNjRlNmRhYzktODY2Yy00MTI2LWIyYTYtMDczNTFjNTkyZDMzIiwidCI6ImVhNmIyNzRlLTE4MmYtNDc0Yy04YWMwLTQzOWM5ZTE1Yjg3ZSJ9)
- **Repositório:** [Performace-Comercial no GitHub](https://github.com/Ricardo-Filgueiras/Performace-Comercial)
- **Autor:** Ricardo Filgueiras, no [LinkedIn](https://www.linkedin.com/in/ricardo-filgueiras-b4607b232/)

## Termos usados

- **Página:** uma página desta documentação.
- **Guia:** uma aba do relatório no Power BI.

## Se você procura…

| Procura | Veja |
|---|---|
| O que o painel resolve e para quem | [Escopo](escopo.md) |
| Como usar o painel no dia a dia | [Como usar](como-usar.md) |
| Como se calcula cada indicador | [Regras de negócio](regras-de-negocio.md) |
| O que tem em cada aba do relatório | [Guias do relatório](guias-do-relatorio/index.md) |
| Tabelas, colunas e relacionamentos | [Modelo de dados](modelo-de-dados.md) |
| O código de uma medida | [Medidas DAX](medidas-dax/index.md) |
| De onde vêm os dados e quando atualizam | [Fontes de dados](fontes-de-dados.md) |
| Como abrir o projeto depois de clonar | [Como atualizar o valor dos parâmetros](fontes-de-dados.md#como-atualizar-o-valor-dos-parametros) |
| Por que algo foi feito de certo jeito | [Decisões técnicas](decisoes-tecnicas.md) |
| Como trabalhar no projeto | [Guia do desenvolvedor](guia-do-desenvolvedor.md) |
| O que ainda está em aberto | [Pendências](pendencias.md) |
| O que mudou e quando | [Changelog](changelog.md) |
| Guias e versões que não estão mais em uso | [Arquivo](arquivo/index.md) |

## Por que DataOps neste projeto

O projeto é versionado com Git desde 22/10/2025, e o modelo e o relatório estão no formato PBIP, que guarda tudo em arquivos de texto. Isso permite tratar a documentação como código: ela fica no mesmo repositório, muda junto com o modelo e pode ser conferida contra ele.

Antes desta reescrita, o projeto tinha seis páginas de documentação (versão 2.0, de 30/01/2026). As contagens estavam certas, mas a conferência com os arquivos do modelo encontrou diferenças, como colunas citadas que não existem e exemplos de valores que não estão nos dados. A documentação atual foi escrita a partir dos arquivos do modelo e do relatório, com um script de levantamento para conferir contagens e dependências, e o `mkdocs build --strict` impede que uma página fique fora do menu ou com link quebrado.

O histórico da documentação anterior continua disponível no Git. A metodologia está em [DataOps](../../metodologia/dataops.md) e [Versionamento com Git](../../metodologia/versionamento-git.md).
