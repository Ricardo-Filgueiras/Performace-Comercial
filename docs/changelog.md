# Changelog do portal

Mudanças que afetam o portal inteiro: estrutura, metodologia, padrão de documentação e entrada de projetos. Cada projeto tem o seu changelog na própria pasta.

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/). Cada versão recebe uma tag `portal/vX.Y.Z`.

## [Não publicado]

### Adicionado

- Estrutura inicial do portal, seguindo a skill `documentacao-bi` 0.1.0.
- Entrada do projeto **Performance Comercial** no portal, em `docs/projetos/performance-comercial/`. Veja o [changelog do projeto](projetos/performance-comercial/changelog.md).
- Metodologia do portal: [DataOps](metodologia/dataops.md) e [versionamento com Git](metodologia/versionamento-git.md).
- Menu por pasta (`awesome-nav`), datas de revisão das páginas, zoom nos diagramas e aviso de pendência.

### Alterado

- A página inicial do portal passou a ser a entrada geral, e a documentação antiga do projeto, em seis páginas numeradas, foi removida depois de migrada.
- A pasta `site/` deixou de ser versionada. A publicação é feita por `mkdocs gh-deploy`, na branch `gh-pages`.
