# Modo: projeto novo

Use quando o projeto Power BI ainda não tem documentação. A documentação nasce já no padrão.

## Etapa 1: Linha de base no Git

1. `git status`. Se houver mudanças pendentes além da própria skill e do `.agents/`, pare e pergunte: a linha de base precisa ser um estado commitado.
2. Confirme com o usuário o **slug** do projeto e que os arquivos do Power BI estão em `src/<slug>/`. Se não estiverem, oriente a mudança de lugar como passo separado (ver `modo-projeto-existente.md`, etapa 2, passo 3).
3. Com autorização, crie a tag anotada: `git tag -a <slug>/baseline-pre-documentacao -m "<Projeto> antes da documentação"`. Anote o hash e a data (`git log -1 --format="%h %ad" --date=short`).

## Etapa 2: Foto do projeto

Rode o script de levantamento e salve o retrato em `.agents/linha-de-base-<slug>.md`:

1. Identificação: tag, hash, data, nome das pastas do Power BI.
2. Modelo: tabelas (colunas, medidas, oculta, calculada), classificação provável fato/dimensão/auxiliar (marcada como *inferida*), relacionamentos, fontes e parâmetros.
3. Medidas: total, por pasta de exibição (incluindo "sem pasta"), quantas têm `///` e `/* */`.
4. Relatório: guias com nome, ordem e se estão ocultas.
5. Pendências observadas no modelo e no relatório (sem corrigir).
6. Indicadores `Indicador | Antes | Depois`, com *Depois* vazio.
7. Como reproduzir: os comandos exatos usados.

## Etapa 3: Estrutura e páginas

1. Se a raiz do portal ainda não existir, copie `modelos/portal/` para a raiz e `modelos/metodologia/` para `docs/metodologia/`.
2. Copie `modelos/projeto/` para `docs/projetos/<slug>/` e rode `python <pasta-da-skill>/scripts/gerar_paginas.py --root src/<slug> --docs docs/projetos/<slug>`: o gerador assume `modelo-de-dados.md`, `medidas-dax/index.md` e `medidas-dax/sem-pasta.md` (cópias intactas do modelo, marcadas no topo) e cria uma página por pasta de exibição. Preencha as demais páginas só com o que dá para ler nos arquivos. Ordem sugerida: `fontes-de-dados.md`, `guias-do-relatorio/`, `regras-de-negocio.md`, `escopo.md`, `readme.md`, `decisoes-tecnicas.md`, `guia-do-desenvolvedor.md`, `pendencias.md`, `arquivo/`, `changelog.md`.
3. Uma página por guia do relatório, escrita à mão a partir de `modelos/itens/guia.md`. As páginas de `medidas-dax/` já vêm do gerador; escreva a descrição de cada medida acima do bloco `gerado`, no lugar do aviso `!!! pendente`. Se o projeto tem scripts Python, pergunte a pasta e rode `extrair_etl.py --etl <pasta> --docs docs/projetos/<slug>` (gera `etl-python.md`); se não tem, apague `etl-python.md` e a linha dele no `.nav.yml`.
4. Guias ocultas, rascunhos, medidas de teste e medidas sem uso: listadas em `arquivo/index.md` (as guias ocultas continuam com página própria, ligada a partir do arquivo).
5. Atualize o `.nav.yml` do projeto com todas as páginas criadas. Acrescente o projeto em `docs/projetos/.nav.yml` e em `docs/index.md`.
6. `como-usar.md` fica com o modelo vazio até a conversa com a área de negócio.

## Etapa 4: Validação e entrega

1. `uv sync` e `uv run mkdocs build --strict` sem avisos, e `gerar_paginas.py --check` com código 0.
2. `git status --porcelain -- src/<slug>` vazio.
3. Refaça as contagens e preencha a coluna *Depois*: só o número de páginas de documentação deve mudar.
4. Resumo para o usuário: arquivos criados, indicadores antes × depois, pendências por página, pendências observadas no modelo, checklist do PR, pauta da sessão de validação de negócio.
5. Relatório de teste (`relatorio-de-teste.md`).
