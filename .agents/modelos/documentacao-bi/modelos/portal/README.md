# Portal de documentação de BI

Repositório dos projetos Power BI (formato PBIP) e da documentação deles, publicada como site [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

Este arquivo cobre só como instalar e rodar o portal. O conteúdo sobre os painéis está no site, a partir de [`docs/index.md`](docs/index.md).

## Estrutura

| Caminho | O que é |
|---|---|
| `docs/` | Toda a documentação do portal |
| `docs/projetos/<slug>/` | Documentação de um projeto |
| `docs/metodologia/` | Metodologia, igual para todos os projetos |
| `src/<slug>/` | Arquivos do Power BI de um projeto (`.pbip`, `.SemanticModel/`, `.Report/`) |
| `.claude/skills/documentacao-bi/` | Skill que conduz a documentação com o agente |
| `.agente/` | Arquivos de trabalho (diagnósticos, planos, relatórios de teste da skill) |
| `mkdocs.yml` | Configuração do site |
| `pyproject.toml` / `uv.lock` | Dependências Python do site |

O `<slug>` de um projeto é o mesmo em `src/` e em `docs/projetos/`.

## Pré-requisitos

- **Power BI Desktop** com suporte a PBIP e TMDL.
- **Git**, com o histórico completo. O plugin de datas do site lê o `git log`.
- **[uv](https://docs.astral.sh/uv/)**, que instala o Python e as dependências do site.
- O repositório num **caminho curto, fora do OneDrive** (por exemplo `C:\repos\`). Caminhos longos passam do limite de 260 caracteres do Windows.

## Rodar o site

```bash
# instala as dependências (cria .venv/ a partir do uv.lock)
uv sync

# servidor local com recarga automática em http://127.0.0.1:8000
uv run mkdocs serve

# gera o site em site/ e falha se houver qualquer aviso
uv run mkdocs build --strict
```

## Abrir um painel

Abra `src/<slug>/<Projeto>.pbip` no Power BI Desktop.
