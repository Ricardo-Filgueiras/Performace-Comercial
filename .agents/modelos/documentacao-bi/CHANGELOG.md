# Changelog da skill documentacao-bi

## [0.1.0] - 2026-10-21

Primeira versão de teste, montada a partir do laboratório do Gestão de compras e da revisão do conselho de arquitetura da documentação (2026-10-10 a 2026-10-20).

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

- O script reproduz os indicadores da linha de base do Gestão de compras (121 medidas, 65 sem pasta, 21 guias, 354 visuais) e as dependências de `mFaturameto` conferidas à mão.
- O modelo de portal com um projeto de exemplo compila com `mkdocs build --strict` (MkDocs 1.6.1), e uma página fora do `.nav.yml` faz o build falhar.
- MkDocs fixado em `<2`, porque a versão 2.0 remove o sistema de plugins.
