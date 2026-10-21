# Escopo

O conteúdo desta página vem dos requisitos levantados com o desenvolvedor, conferidos contra os nomes das guias e medidas e o código DAX e M. O que não dá para confirmar está marcado como pendência.

!!! info "Projeto de portfólio"
    O Performance Comercial é um projeto de **portfólio**, com dados fictícios e sem usuários reais. O escopo abaixo descreve o cenário para o qual o painel foi desenhado e serve para demonstrar o trabalho de modelagem, DAX e visualização.

## O que o painel resolve

Permite acompanhar o desempenho comercial de uma empresa de vendas (faturamento, margem, resultado, comissão e metas) em um único relatório interativo, por período, produto, cliente, cidade, unidade e vendedor, no lugar de consultas manuais a planilhas.

## Objetivo

Responder à pergunta "como estamos indo?" em poucos cliques: o gerente vê o resultado do período, compara com o ano anterior e confere o atingimento das metas.

Não há objetivo mensurável definido. Os indicadores de sucesso do texto anterior (tempo de resposta, engajamento dos usuários e opinião dos gestores) não se aplicam a um projeto sem usuários reais.

!!! pendente "A confirmar"
    Definir uma meta de tempo de resposta do relatório. O texto anterior falava em menos de 5 segundos, mas isso nunca foi medido.

## Público

O usuário de referência é o **gerente de equipe**, que acompanha a equipe e as metas. Como o projeto é de portfólio, não há como simular o uso por vários usuários, e a frequência de uso não se aplica.

Outros perfis são cenários possíveis, vindos da documentação anterior e **não validados com usuários**. A coluna "Guias que atendem" é deduzida dos visuais.

| Perfil | O que precisa ver | Guias que atendem |
|---|---|---|
| Diretoria comercial | Visão geral do resultado: faturamento, margem, resultado e evolução contra o ano anterior | [Comercial](guias-do-relatorio/comercial.md) |
| Gerência de vendas | Atingimento das metas e desempenho de cada vendedor e equipe | [Vendedores](guias-do-relatorio/vendedores.md), [Comercial](guias-do-relatorio/comercial.md) |
| Equipe comercial | Seu próprio desempenho: vendas, comissão e meta | [Vendedores](guias-do-relatorio/vendedores.md) |
| Controladoria | Rentabilidade: custo, despesa, impostos, comissão e margem | [Analítico](guias-do-relatorio/analitico.md), [Comercial](guias-do-relatorio/comercial.md) |

## Processos cobertos

| Processo | Onde aparece |
|---|---|
| Acompanhamento de faturamento e resultado | [Comercial](guias-do-relatorio/comercial.md): cartões e evolução no tempo |
| Análise de margem e rentabilidade | [Comercial](guias-do-relatorio/comercial.md) e [Analítico](guias-do-relatorio/analitico.md) |
| Acompanhamento de metas | [Vendedores](guias-do-relatorio/vendedores.md) e dica de ferramenta da [evolução do faturamento](guias-do-relatorio/dica-evolucao-faturamento.md) |
| Desempenho por vendedor e comissão | [Vendedores](guias-do-relatorio/vendedores.md) |
| Análise por produto, gerente e cidade | [Comercial](guias-do-relatorio/comercial.md) |
| Detalhamento por cidade, estado, subcategoria e unidade | [Analítico](guias-do-relatorio/analitico.md) |
| Sazonalidade (mês por dia da semana) e comparação com o ano anterior | [Mapa Calor](guias-do-relatorio/mapa-calor.md) |
| Positivação de clientes e de produtos | [Analítico](guias-do-relatorio/analitico.md) e [Vendedores](guias-do-relatorio/vendedores.md) |

## Dentro do escopo

- **Indicadores** (ver [regras de negócio](regras-de-negocio.md) e [medidas DAX](medidas-dax/index.md)): faturamento, custo, despesa, impostos, comissão, lucro bruto, margem bruta, resultado, margem, quantidade de vendas, positivação de clientes e de produtos, meta, porcentagem da meta e diferença para a meta.
- **Comparações no tempo:** ano anterior (YoY), mês anterior (MoM) e acumulado no ano, aplicadas a faturamento, margem, resultado e comissão. O acumulado existe só para o faturamento.
- **Dimensões de análise:** tempo (ano, semestre, trimestre, mês e dia), produto (categoria, subcategoria e produto), cliente (cliente e cidade), vendedor (vendedor e gerente), unidade e forma de pagamento.
- **Relatório** (ver [guias do relatório](guias-do-relatorio/index.md)): Capa, Comercial, Analítico, Mapa Calor, Vendedores e três dicas de ferramenta.
- **Interatividade:** filtros por unidade, ano, mês, vendedor e forma de pagamento, botões de navegação em menu recolhível, dicas de ferramenta e visuais personalizados (cartões e tabelas em SVG e HTML).
- **Dados** (ver [fontes de dados](fontes-de-dados.md)): planilhas Excel guardadas junto com o projeto, em `data/`, no período de 2018 a 2021, em modo Import, com os caminhos em três parâmetros do Power Query.
- **Modelo** (ver [modelo de dados](modelo-de-dados.md)): esquema estrela com duas tabelas fato (`fVendas` e `fMetas`) e sete dimensões.

### Planejado, ainda não implementado

- Ticket médio (faturamento por venda).
- Mix de produtos (curva ABC), produtividade por vendedor e projeção de meta.

Não há data prevista para essas análises.

## Fora do escopo

- **Controle de acesso por usuário (RLS).** O modelo não tem papéis.
- **Análise geográfica em mapa.** O relatório não tem visual de mapa. A guia Mapa Calor é uma matriz de mês por dia da semana.
- **Previsão de vendas, análise RFM e análise de perda de clientes (churn).**
- **Atualização automática dos dados.** Os dados são fixos e não haverá valores depois de 31/12/2021.
- **Validação por uma área de negócio.** Não existe área de negócio por trás do projeto.
- **Sistema de origem ou pipeline de dados.** O modelo lê as planilhas direto.
