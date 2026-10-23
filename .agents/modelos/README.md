# Kit de documentação de BI

Tudo o que é preciso para criar a documentação de um projeto Power BI no portal único, na forma de uma **skill** do Claude Code: `documentacao-bi/` (versão 0.3.0, em teste).

Origem: laboratório de um projeto piloto e revisão do conselho de arquitetura da documentação (2026-10).

## O que tem aqui

```
.claude-plugin/              ← plugin.json e marketplace.json
documentacao-bi/
├── SKILL.md                    ← instruções para o agente
├── CHANGELOG.md                ← versões da skill
├── referencias/
│   ├── padrao.md               ← índice do padrão
│   ├── padrao-estrutura.md, padrao-escrita.md, padrao-paginas.md,
│   │   padrao-git.md, padrao-mkdocs.md  ← o padrão por tema, com o porquê de cada regra
│   ├── armadilhas.md           ← situação inesperada → decisão tomada
│   ├── distribuicao.md         ← plugin, versão, atualização e release
│   ├── decisao-mkdocs.md       ← critérios para manter ou trocar o MkDocs
│   ├── modo-projeto-existente.md
│   ├── modo-projeto-novo.md
│   ├── niveis.md               ← o que entra agora e o que fica para depois
│   ├── educacao-mantenedores.md
│   └── relatorio-de-teste.md   ← o que o agente devolve ao fim de cada sessão
├── modelos/
│   ├── portal/                 ← raiz do portal: mkdocs.yml, pyproject.toml, gitignore, README, docs/
│   ├── metodologia/            ← dataops.md e versionamento-git.md, já genéricos e corrigidos
│   ├── projeto/                ← páginas de um projeto, com o menu (.nav.yml)
│   └── itens/                  ← modelo de guia, de pasta de medidas e de medida
└── scripts/
    ├── levantamento.py         ← contagens, dependências entre medidas e --preflight
    ├── gerar_paginas.py        ← gera modelo-de-dados.md e medidas-dax/ direto do modelo
    ├── extrair_etl.py          ← gera etl-python.md das docstrings dos scripts Python
    ├── comparar_portal.py      ← mostra o que mudou nos modelos desde que o portal foi criado
    └── tests/                  ← testes dos scripts + PBIP de exemplo (fixture)
```

## Como instalar

**Opção recomendada: plugin** (versionado, com atualização). Esta pasta é, ao mesmo tempo, o plugin (`.claude-plugin/plugin.json`) e o marketplace (`.claude-plugin/marketplace.json`). Publique-a como repositório Git próprio e, em cada máquina ou repositório de portal:

```bash
claude plugin marketplace add <dono>/<repositorio>
claude plugin install documentacao-bi@bi-documentacao --scope project
```

A skill passa a existir como `/documentacao-bi:documentacao-bi`. Para atualizar, veja `documentacao-bi/referencias/distribuicao.md` (a atualização só chega quando o campo `version` do `plugin.json` muda). Para testar antes de publicar: `claude --plugin-dir <esta pasta>`.

**Alternativa: copiar a pasta.** Copie `documentacao-bi/` para `<portal>/.claude/skills/documentacao-bi/`. Funciona, mas cada cópia envelhece sozinha.

Depois, em qualquer das opções:

1. **Repositório num caminho curto, fora do OneDrive** (por exemplo `C:\repos\<portal>`).
2. Crie a pasta `<portal>/.agents/relatorios-skill/` para os relatórios de teste.
3. Abra o Claude Code na raiz do portal e peça, por exemplo: *"Use a skill documentacao-bi para documentar este projeto. É um projeto existente."*
4. O agente faz primeiro o **diagnóstico** (só leitura) e o **plano de migração**, e espera a sua aprovação antes de alterar qualquer coisa.

Não é preciso levar o restante deste `.agents/` (linha de base e notas do laboratório): o necessário já está dentro da skill.

## Como trazer o resultado de volta

Ao fim de cada sessão, o agente do projeto novo escreve um relatório em `.agents/relatorios-skill/AAAA-MM-DD-sessao-N.md`. Traga esse arquivo para o laboratório. Com ele, a skill é corrigida e ganha uma versão nova (0.4.0, …). Com o plugin, quem usa atualiza com um comando; se você copiou a pasta, copie de novo.

## O que ainda depende de você

- **Nome do projeto (slug):** o agente vai perguntar. O mesmo nome vale para `src/<slug>/` e `docs/projetos/<slug>/`.
- **Mudar as pastas do Power BI para `src/<slug>/`:** se precisar, é você quem faz, num commit só para isso. O agente orienta e confere.
- **Commits e pull request:** o agente não faz commit. Você revisa e abre o PR.
