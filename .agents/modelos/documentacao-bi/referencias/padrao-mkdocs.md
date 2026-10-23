<!-- Parte do padrão. Índice em padrao.md. -->
# 5. Setup do MkDocs

O modelo completo está em `modelos/portal/mkdocs.yml`. O essencial:

- Tema `material` com `navigation.tabs` (abas de topo) e `navigation.indexes` (pastas com `index.md`).
- Plugins: `search`, `awesome-nav` (menu por pasta), `git-revision-date-localized` (data de cada página) e `panzoom` (zoom nos diagramas).
- `validation.nav.omitted_files: warn` e `not_found: warn`: com `--strict`, o build falha se uma página ficar fora do menu.
- Extensões: `admonition`, `pymdownx.details`, `pymdownx.superfences` (Mermaid), `toc` com `permalink`.
- `extra_css` com o aviso `pendente`.

Dependências (`pyproject.toml`): `mkdocs` (fixado em `>=1.6,<2`), `mkdocs-material`, `mkdocs-awesome-nav`, `mkdocs-git-revision-date-localized-plugin`, `mkdocs-panzoom-plugin`.

!!! warning "MkDocs 2.0"
    O MkDocs 2.0 remove o sistema de plugins e não tem caminho de migração (aviso da equipe do Material for MkDocs, fev. 2026). Todo o portal depende de plugins (`awesome-nav`, datas, `panzoom`). Por isso o MkDocs fica fixado na série 1.x até haver uma decisão sobre o futuro da ferramenta.

Testado em 2026-10-21 com MkDocs 1.6.1: o modelo de portal com um projeto de exemplo compila com `--strict`, e uma página fora do `.nav.yml` faz o build falhar, como esperado.

# 6. O que ficou para depois

Ideias decididas mas adiadas estão em `niveis.md` (níveis 2 e 3): validação de negócio formal, glossário corporativo, changelog do portal ligado aos projetos, CI, blocos-fonte por medida, números por variável, rodapé com link do changelog, formulário "Sugerir correção", identidade visual, indicadores e publicação com login.
