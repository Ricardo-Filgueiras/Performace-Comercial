# Kit de documentação de BI

Tudo o que é preciso para criar a documentação de um projeto Power BI no portal único, na forma de uma **skill** do Claude Code: `documentacao-bi/` (versão 0.1.0, em teste).

Origem: laboratório do Gestão de compras e revisão do conselho de arquitetura da documentação. O registro das decisões está em `../notas/`.

## O que tem aqui

```
documentacao-bi/
├── SKILL.md                    ← instruções para o agente
├── CHANGELOG.md                ← versões da skill
├── referencias/
│   ├── padrao.md               ← o padrão, com o porquê de cada regra
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
    └── levantamento.py         ← contagens e dependências entre medidas
```

## Como levar para o projeto novo

1. **Repositório num caminho curto, fora do OneDrive** (por exemplo `C:\repos\<portal>`).
2. Copie a pasta `documentacao-bi/` para `<portal>/.claude/skills/documentacao-bi/`. É nessa pasta que o Claude Code reconhece a skill.
3. Crie a pasta `<portal>/.agente/relatorios-skill/` para os relatórios de teste.
4. Abra o Claude Code na raiz do portal e peça, por exemplo: *"Use a skill documentacao-bi para documentar este projeto. É um projeto existente."* Também dá para chamar a skill direto com `/documentacao-bi`.
5. O agente faz primeiro o **diagnóstico** (só leitura) e o **plano de migração**, e espera a sua aprovação antes de alterar qualquer coisa.

Não é preciso copiar o restante deste `.agente/` (notas, linha de base do laboratório): o necessário já está dentro da skill.

## Como trazer o resultado de volta

Ao fim de cada sessão, o agente do projeto novo escreve um relatório em `.agente/relatorios-skill/AAAA-MM-DD-sessao-N.md`. Traga esse arquivo para o laboratório. Com ele, a skill é corrigida e ganha uma versão nova (0.2.0, …), que você copia de novo para o projeto.

## O que ainda depende de você

- **Nome do projeto (slug):** o agente vai perguntar. O mesmo nome vale para `src/<slug>/` e `docs/projetos/<slug>/`.
- **Mudar as pastas do Power BI para `src/<slug>/`:** se precisar, é você quem faz, num commit só para isso. O agente orienta e confere.
- **Commits e pull request:** o agente não faz commit. Você revisa e abre o PR.
