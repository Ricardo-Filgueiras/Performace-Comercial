# Changelog da skill documentacao-bi

## [0.3.0] - 2026-10-23

Distribuição e escopo (prioridade 3 da avaliação da skill).

### Adicionado

- **Plugin com versão e atualização:** `.claude-plugin/plugin.json` (versão em um único lugar) e `.claude-plugin/marketplace.json` na raiz do kit. A skill passa a ser instalável com `claude plugin marketplace add` e `claude plugin install`. Validado com `claude plugin validate`, e a skill é descoberta com `claude --plugin-dir`.
- `SKILL.md` usa `${CLAUDE_SKILL_DIR}` nos comandos; as referências usam `<pasta-da-skill>`. Nenhum caminho depende de onde a skill foi instalada.
- `referencias/distribuicao.md`: como instalar, atualizar, publicar uma versão nova (checklist de release) e por que plugin e não `copier`.
- `scripts/comparar_portal.py`: compara um portal já criado com os modelos desta versão (só leitura), para levar mudanças de `mkdocs.yml`, CSS e metodologia a portais antigos.
- `scripts/extrair_etl.py` e `modelos/projeto/etl-python.md`: página de ETL em Python gerada das docstrings por análise estática (`ast`), sem executar nada. Extrai docstrings de módulo, funções e classes, argumentos `argparse`, bibliotecas de terceiros, variáveis de ambiente e leituras e escritas de arquivo, banco e HTTP. Credencial literal, URL com senha e caminho absoluto viram ALERTA sem copiar o valor. Mesmas regras de marcadores, `--check` e preservação do texto manual das outras páginas geradas.
- `referencias/decisao-mkdocs.md`: critérios, fatos conhecidos e roteiro de teste para decidir entre manter o MkDocs 1.x e migrar. A decisão continua adiada para depois do segundo projeto, com prazo máximo.
- `scripts/tests/test_plugin.py`: versão igual em plugin, `SKILL.md`, CHANGELOG, `README` e relatório; manifestos corretos; caminhos sem dependência do local de instalação; e uma lista de termos proibidos guardada só como hashes SHA-256, para nenhum nome de projeto anterior voltar ao kit sem a lista revelá-lo.

### Alterado

- `LEIA-ME.md` renomeado para `README.md` (convenção de repositório Git) e reescrito: instalação por plugin como opção recomendada; copiar a pasta continua possível.
- `modelos/projeto/.nav.yml`: inclui `etl-python.md` (a página é opcional; sem Python, apague-a e a linha do menu).
- `padrao-estrutura.md`, `padrao-paginas.md`, `niveis.md`, `educacao-mantenedores.md`, `armadilhas.md` e os dois modos descrevem o ETL e o plugin.

### Verificado

- 59 testes passando, 1 opcional (fixture de ETL com credenciais falsas: nenhum valor aparece na página nem na saída).
- O CLI listou a skill como `documentacao-bi:documentacao-bi` com `--plugin-dir`.

## [0.2.0] - 2026-10-23

Gerador de páginas (prioridade 2 da avaliação da skill). Nenhuma regra do padrão mudou; o que é mecânico passou do agente para o código.

### Adicionado

- `scripts/gerar_paginas.py`: gera `modelo-de-dados.md` (visão geral, diagrama ER em Mermaid dividido em visões acima de 15 relacionamentos, tabelas e colunas, expressões de colunas e tabelas calculadas, hierarquias, grupos de cálculo e papéis de segurança) e `medidas-dax/` (índice com catálogo A–Z, uma página por pasta de exibição, `sem-pasta.md`, "depende de" e "é usada por" com links entre páginas).
- Conteúdo gerado entre marcadores `gerado`: o texto escrito à mão é preservado; item que saiu do modelo vira aviso de pendência em vez de ser apagado; a URL de cada pasta de exibição é fixada pelo marcador `<!-- pasta: NOME -->`.
- `--check` (sai com 1 se alguma página estiver desatualizada) e `--dry-run`. O gerador nunca escreve dentro das pastas do Power BI.
- `levantamento.py` lê hierarquias, grupos de cálculo (com itens e precedência), papéis de segurança (RLS, inclusive filtro em várias linhas), expressão de colunas calculadas e passou a expor `carregar_projeto()` para reuso. Indicadores novos: hierarquias, grupos de cálculo e papéis de segurança.
- `scripts/tests/`: 28 testes (`unittest`, sem dependências) sobre um PBIP de exemplo com RLS, grupo de cálculo, hierarquia, relacionamento inativo e bidirecional; teste opcional contra um projeto real (`BI_PROJETO_REAL`).
- Modelos `modelo-de-dados.md`, `medidas-dax/index.md` e `medidas-dax/sem-pasta.md` ganharam marca de topo: cópia intacta é assumida pelo gerador; página antiga sem marcadores não é tocada.

### Alterado

- `SKILL.md`, `modo-projeto-novo.md`, `modo-projeto-existente.md`, `padrao-paginas.md`, `niveis.md`, `educacao-mantenedores.md`, `armadilhas.md` e `relatorio-de-teste.md` descrevem o fluxo com o gerador.
- `modelos/portal/mkdocs.yml`: `validation.links.anchors: warn`, para o `--strict` pegar link de medida quebrado.

### Verificado

- 28 testes passando; contra um projeto real, em teste local opcional, a geração é idempotente e não altera nada no projeto.
- Portal de teste (modelos da skill + PBIP de exemplo + páginas geradas) compila com `mkdocs build --strict` (MkDocs 1.6), com validação de âncoras ligada; um link de âncora errado faz o build falhar.
- Os anchors gerados coincidem com o `slugify` do MkDocs para nomes com acento, `%`, `&` e `_`.

## [0.1.1] - 2026-10-23

Correções de prioridade 1 da avaliação da skill. Nenhuma regra do padrão mudou.

### Adicionado

- `referencias/armadilhas.md`: catálogo "situação inesperada → decisão tomada", com formato para registrar novos casos.
- `levantamento.py --preflight`: verifica OneDrive, caminho longo, `.pbix` sem `.pbip` e pasta fora de `src/<slug>`.

### Alterado

- `referencias/padrao.md` virou índice; o conteúdo foi dividido em `padrao-estrutura.md`, `padrao-escrita.md`, `padrao-paginas.md`, `padrao-git.md` e `padrao-mkdocs.md`. `SKILL.md` manda ler só estrutura e escrita no início.
- Referências cruzadas em `niveis.md`, `modo-projeto-existente.md` e `educacao-mantenedores.md` apontam para os novos arquivos.
- Pasta de trabalho do agente renomeada de `.agente/` para `.agents/` em toda a skill.
- `LEIA-ME.md`: removida a referência a `../notas/`, que não existe.

## [0.1.0] - 2026-10-21

Primeira versão de teste, montada a partir do laboratório de um projeto piloto e da revisão do conselho de arquitetura da documentação (2026-10-10 a 2026-10-20).

### Adicionado

- `SKILL.md` com os dois modos (projeto novo e projeto existente), regras fixas, estrutura do portal, roteiro de sessão e checklist do pull request.
- `referencias/padrao.md`: padrão de documentação com o motivo de cada regra.
- `referencias/modo-projeto-existente.md` e `referencias/modo-projeto-novo.md`.
- `referencias/niveis.md`: nível 1 (essencial), 2 (validação e uso) e 3 (automação e publicação).
- `referencias/educacao-mantenedores.md` e `referencias/relatorio-de-teste.md`.
- `modelos/portal/`, `modelos/metodologia/` (com a referência ao DataOps Manifesto corrigida) e `modelos/projeto/`.
- `scripts/levantamento.py` com `--root` apontando para `src/<slug>/`, detecção automática do projeto e dependências entre medidas.
- `modelos/itens/`: modelos de página de guia, página de pasta de medidas e seção de medida.

### Verificado

- O script reproduz os indicadores da linha de base do projeto piloto e as dependências entre medidas conferidas à mão.
- O modelo de portal com um projeto de exemplo compila com `mkdocs build --strict` (MkDocs 1.6.1), e uma página fora do `.nav.yml` faz o build falhar.
- MkDocs fixado em `<2`, porque a versão 2.0 remove o sistema de plugins.
