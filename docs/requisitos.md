# Requisitos

Este documento descreve para que serve o painel **Performance Comercial**, quem o usa e o que ele precisa entregar. Foi reescrito a partir do que existe hoje no projeto (modelo semântico, relatório e documentação anterior). O texto anterior era um modelo genérico de requisitos, com itens que o projeto nunca implementou.

## Contexto do projeto

Este é um **projeto de portfólio**. Os dados são fictícios e o painel não tem usuários reais. O cenário de uso descrito abaixo é o que o painel foi desenhado para atender e serve para demonstrar o trabalho de modelagem, DAX e visualização.

!!! pendente "Rascunho para validação"
    Os itens marcados como pendentes não puderam ser confirmados e dependem de resposta do responsável pelo projeto. A lista completa está no fim da página.

## 1. Propósito

O painel permite acompanhar o desempenho de vendas da empresa: quanto se vendeu, com que margem e resultado, quanto se pagou de comissão e se a meta foi atingida. Os resultados podem ser vistos por período, produto, cliente, cidade, unidade e vendedor.

O objetivo é trocar a consulta manual a planilhas por uma visão única e interativa, para que a pergunta "como estamos indo?" seja respondida em poucos cliques.

## 2. Usuários

| Usuário | O que precisa ver |
|---|---|
| Diretoria comercial | Visão geral do resultado: faturamento, margem, resultado e evolução contra o ano anterior |
| Gerência de vendas | Atingimento das metas e desempenho de cada vendedor e equipe |
| Equipe comercial | Seu próprio desempenho: vendas, comissão e meta |
| Controladoria | Rentabilidade: custo, despesa, impostos, comissão e margem |

O usuário de referência é o **gerente de equipe**, que acompanha a equipe e as metas. Por ser um projeto de portfólio, não há como simular o uso por vários usuários diferentes. Os demais perfis da tabela são cenários possíveis, vindos da documentação anterior, e não foram validados com usuários.

## 3. Requisitos funcionais

### 3.1 Indicadores

| Indicador | Definição | Situação |
|---|---|---|
| Faturamento | Receita das vendas efetivadas | Implementado |
| Custo, despesa, impostos e comissão | Valores unitários multiplicados pela quantidade vendida | Implementado |
| Lucro bruto e margem bruta | Faturamento menos custo, e esse valor dividido pelo faturamento | Implementado |
| Resultado e margem | Faturamento menos custo, despesa, impostos e comissão, e esse valor dividido pelo faturamento | Implementado |
| Quantidade de vendas | Contagem de vendas distintas | Implementado |
| Positivação de clientes e de produtos | Clientes e produtos distintos que compraram no período | Implementado |
| Comparação com o ano anterior (YoY), mês anterior (MoM) e acumulado no ano | Aplicada ao faturamento, à margem, ao resultado e à comissão | Implementado (acumulado só para faturamento) |
| Meta, porcentagem da meta e diferença para a meta | Meta por vendedor e mês contra o faturamento | Implementado |
| Ticket médio | Faturamento por venda | Planejado, ainda não implementado |
| Mix de produtos (ABC), produtividade por vendedor, projeção de meta | Análises avançadas | Planejado, sem data |

### 3.2 Dimensões de análise

- **Tempo:** ano, semestre, trimestre, mês e dia.
- **Produto:** categoria, subcategoria e produto.
- **Cliente:** cliente e cidade.
- **Vendedor:** vendedor e gerente.
- **Unidade:** filial ou unidade de negócio.
- **Forma de pagamento.**

### 3.3 Páginas do relatório

| Página | Para que serve |
|---|---|
| Capa | Entrada e navegação entre as páginas |
| Comercial | Visão geral: cartões de faturamento, margem, resultado e comissão, evolução no tempo, ranking e distribuição |
| Analítico | Detalhamento em tabela dinâmica |
| Mapa Calor | Desempenho por período e dimensão em matriz |
| Vendedores | Desempenho individual contra a meta |

O relatório também guarda três páginas de dica de ferramenta (tooltip) e quatro páginas com o sufixo "antes". Estas últimas são versões anteriores das páginas principais e **são mantidas de propósito**, para que o desenvolvedor possa ver a evolução do relatório. A documentação deve tratá-las como histórico, não como parte da entrega atual.

### 3.4 Interatividade

- Segmentações de dados (filtros) em todas as páginas de análise.
- Botões de navegação entre páginas, em menu lateral.
- Dicas de ferramenta com detalhes ao passar o mouse.
- Cartões e tabelas desenhados com medidas SVG e HTML (visuais personalizados).

## 4. Requisitos de dados

- **Natureza dos dados:** fictícios, criados para o portfólio.
- **Origem:** arquivos guardados no próprio repositório, em `src/data/`: vendas (uma linha por item vendido), cadastros (dimensões) e metas por ano (2018 a 2021).
- **Formato:** CSV. O Excel foi descartado como formato de entrada porque o link "raw" do GitHub baixa o arquivo `.xlsx` em vez de exibir o conteúdo, e o CSV pode ser lido direto.
- **Parâmetros:** os caminhos dos dados ficam em parâmetros do Power Query, reunidos em um grupo próprio de consultas, separado de fatos, dimensões e auxiliares. Quem clonar o repositório deve precisar **atualizar um único caminho**, o da pasta onde estão os dados.
- **Carga:** modo Import, com tratamento no Power Query.
- **Modelo:** esquema estrela com duas tabelas fato (`fVendas` e `fMetas`) e sete dimensões. Detalhes em [Relacionamentos](04 relacionamentos.md).
- **Granularidade:** `fVendas` tem uma linha por item vendido. `fMetas` tem uma linha por vendedor e mês.
- **Regra de negócio central:** os indicadores de venda consideram apenas vendas efetivadas (`Id Status = 1`).
- **Cultura:** pt-BR.

!!! pendente "Caminho único dos dados"
    Falta definir o que o parâmetro guarda: o caminho da pasta `src/data` na cópia local do repositório, ou o endereço base dos arquivos "raw" no GitHub. Falta também converter os arquivos de Excel para CSV e adaptar as consultas, porque hoje o modelo ainda lê `.xlsx` por três parâmetros (`Caminho_Extracao`, `Caminho_Dimensoes` e `Caminho_Meta`).

!!! pendente "Período dos dados"
    Falta confirmar o período coberto pelos dados de vendas. Os arquivos de meta vão só até 2021.

## 5. Requisitos não funcionais

| Tema | Situação hoje |
|---|---|
| Atualização | Manual. Os dados vêm de planilhas locais e não há atualização agendada. Como os dados são fictícios e fixos, não há necessidade de atualização periódica |
| Segurança por linha (RLS) | Não é requisito. O projeto é de portfólio, sem usuários reais, e o modelo não tem papéis (roles) |
| Versionamento | Projeto em formato `.pbip`, versionado com Git |
| Documentação | MkDocs Material, publicada pelo GitHub Actions |
| Desempenho | Sem meta definida |
| Publicação | Há um link público do painel no Power BI Service |

!!! pendente "Meta de desempenho"
    Falta definir uma meta de tempo de resposta. O texto anterior falava em menos de 5 segundos, mas isso nunca foi medido.

## 6. Fora do escopo atual

- Controle de acesso por usuário (RLS).
- Análise geográfica em mapa. O texto anterior pedia mapas, mas o relatório não tem visual de mapa. A página "Mapa Calor" é uma matriz.
- Previsão de vendas, análise RFM e churn de clientes.
- Atualização automática dos dados.

## 7. Pendências para validação

1. O parâmetro único guarda o caminho local da pasta de dados ou o endereço base "raw" do GitHub? (ver seção 4)
2. Qual é o período coberto pelos dados de vendas?
3. Qual meta de tempo de resposta adotar?
