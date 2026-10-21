# Como usar o painel

Esta página descreve as jornadas de quem usa o painel: em que momento da rotina, para tomar qual decisão e por quais guias passar.

!!! info "Jornadas deduzidas dos visuais"
    O Performance Comercial é um projeto de portfólio, sem usuários reais e sem área de negócio para validar. As jornadas abaixo foram **deduzidas dos visuais das guias e do [escopo](escopo.md)** e não foram testadas com usuários. O "Quando" de cada uma é um cenário possível, não uma rotina observada.

## Antes de começar

- **Abrir o relatório:** use o [painel publicado](readme.md#links) ou abra o arquivo `.pbip` no Power BI Desktop (ver [Como atualizar o valor dos parâmetros](fontes-de-dados.md#como-atualizar-o-valor-dos-parametros)).
- **Navegar:** comece pela [Capa](guias-do-relatorio/capa.md). O navegador de páginas leva às quatro guias de análise, e cada guia tem um menu de botões para as outras.
- **Filtrar:** as guias de análise têm filtros por unidade, ano, mês, vendedor e forma de pagamento. Os filtros valem para os visuais da guia.
- **Período dos dados:** de 2018 a 2021. Escolha o ano antes de ler os números.

## Conferir o resultado do período

- **Quem:** gerente de equipe ou diretoria comercial.
- **Quando:** ao fechar um mês ou um ano.
- **Decisão:** se o período foi bom e se o resultado se sustenta contra o ano anterior.

1. Abra a guia [Comercial](guias-do-relatorio/comercial.md).
2. Filtre por **ano** e **mês** (e por unidade, se quiser).
3. Olhe os cartões de **faturamento, resultado e margem**. Cada um mostra a variação contra o ano anterior, com seta e cor.
4. Olhe o gráfico **Evolução Faturamento**. Passe o mouse sobre um ponto para ver o mês, o faturamento, a meta e a porcentagem da meta.
5. Para entender de onde veio o faturamento, olhe a rosca por gerente e as barras por categoria, produto e subcategoria.

## Acompanhar a meta de um vendedor

- **Quem:** gerente de equipe.
- **Quando:** durante o mês, para ver quem está perto da meta.
- **Decisão:** com quem conversar e onde agir.

1. Abra a guia [Vendedores](guias-do-relatorio/vendedores.md).
2. Escolha o **vendedor** no filtro, e o ano e o mês.
3. Veja os cartões de **comissão, faturamento, margem e resultado**.
4. Veja a **meta** e a diferença para a meta, e o visual com a porcentagem da meta. A cor indica a situação: verde a partir de 60% da meta, vermelho abaixo de 10% e cinza no meio.
5. Olhe os gráficos por dia para ver em que dias o vendedor vendeu e comissionou mais.

!!! warning "Diferença para a meta"
    O valor da diferença para a meta é sempre positivo, porque usa valor absoluto. Ele **não diz** se o faturamento está acima ou abaixo da meta. Use a porcentagem da meta e a cor para saber a situação (ver [Metas](regras-de-negocio.md#metas)).

## Ver quais cidades e produtos vendem mais

- **Quem:** gerente de equipe ou diretoria comercial.
- **Quando:** ao planejar visitas ou campanhas.
- **Decisão:** onde concentrar esforço.

1. Abra a guia [Comercial](guias-do-relatorio/comercial.md).
2. Na área das cidades, use os botões para alternar entre as visões de **ranking** e de **desempenho** por cidade (alguns desses botões têm problemas, ver [Guias do relatório](guias-do-relatorio/index.md#problemas-encontrados-nos-botoes)). A tabela personalizada alterna, ao passar o mouse, entre o faturamento e a variação da margem.
3. Passe o mouse sobre uma cidade ou um produto para ver, na dica de ferramenta, os vendedores com faturamento, margem e porcentagem da meta.
4. Nas barras por produto, compare categorias, produtos e subcategorias.

## Descobrir quando as vendas acontecem

- **Quem:** gerente de equipe.
- **Quando:** ao dimensionar a equipe ou planejar promoções.
- **Decisão:** em que meses e dias da semana reforçar a equipe.

1. Abra a guia [Mapa Calor](guias-do-relatorio/mapa-calor.md).
2. Escolha o ano.
3. Leia a **matriz** de mês por dia da semana e compare o faturamento entre os meses e entre os dias da semana.
4. Compare o ano atual com o ano anterior nos gráficos de linha, mês a mês e acumulado no ano.

## Detalhar os números

- **Quem:** controladoria ou gerência.
- **Quando:** quando um número chamou atenção em outra guia.
- **Decisão:** onde está a causa de uma variação.

1. Abra a guia [Analítico](guias-do-relatorio/analitico.md).
2. Aplique os filtros (ano, mês, unidade, vendedor, forma de pagamento).
3. Na **matriz**, abra os níveis (cidade, estado, subcategoria, unidade) e leia abatimento, faturamento, margem, positivação de clientes e de produtos, quantidade de vendas e resultado.

## Cuidados ao ler os números

- Os valores consideram só as **vendas válidas**. A **quantidade de vendas** conta vendas válidas e inválidas, então não se refere ao mesmo conjunto que o faturamento (ver [Vendas válidas](regras-de-negocio.md#vendas-validas)).
- As margens são **razões** em porcentagem. A variação da margem contra o ano anterior é relativa, e não a diferença em pontos percentuais.
- Os dados são fictícios e vão só até 31/12/2021.
- Alguns visuais do relatório ainda apontam para nomes antigos de medidas e podem mostrar campo não encontrado (ver [Nomes antigos de medidas](medidas-dax/index.md#nomes-antigos-de-medidas-no-relatorio)).
