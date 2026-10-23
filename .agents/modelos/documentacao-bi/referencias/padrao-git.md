<!-- Parte do padrão. Índice em padrao.md. -->
# 4. Versionamento com Git

| Regra | Por quê |
|---|---|
| **Linha de base antes de documentar:** tag anotada `<slug>/baseline-pre-documentacao` no estado commitado do projeto. | Permite comparar o antes e o depois. O prefixo evita conflito entre projetos no mesmo repositório. |
| **Tags de versão com prefixo:** `<slug>/v1.0.0`, `portal/v1.0.0`. | Mesmo motivo. Cada versão do changelog tem uma tag. |
| **Nada direto na `main`.** O agente deixa as mudanças no working tree; o autor revisa e abre o pull request. | A revisão das sessões de IA acontece no PR. |
| **Mudar um projeto de lugar num commit próprio**, com a remoção e a adição juntas e sem alterar conteúdo. | O Git reconhece a renomeação e mantém o histórico de cada arquivo (`git log --follow`). Comparações com a linha de base passam a usar `git diff -M`. |
| **Commits no formato `tipo: descrição`** (`feat`, `fix`, `docs`, `refactor`, `chore`). Mudança no modelo e mudança só de documentação em commits separados quando não dependem uma da outra. | Histórico legível. |
| **`.gitignore`:** `.pbi/localSettings.json`, `.pbi/cache.abf`, `*.pbix`, `.venv/`, `site/`, `__pycache__/`. | Caches locais e binários grandes nunca entram no histórico. |
