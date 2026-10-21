# Padrão de documentação dos projetos de BI

Este padrão define como a documentação de cada projeto Power BI (PBIP) é organizada e escrita no portal único de documentação de BI. Ele nasceu do laboratório do Gestão de compras (2026-10) e da revisão de um conselho de especialistas. Cada regra traz o motivo, para que quem mantém saiba quando ela se aplica.

> Este padrão é **provisório**. Ele será revisado depois do segundo projeto documentado, com o que os dois projetos ensinarem.

## 1. Estrutura do portal

```
<portal>/
├── README.md                 ← como instalar e rodar o portal (não é sobre negócio)
├── mkdocs.yml                ← único: tema, plugins, validação
├── pyproject.toml / uv.lock  ← dependências Python do site
├── .gitignore
├── .claude/skills/documentacao-bi/   ← skill de documentação
├── .agente/                  ← arquivos de trabalho, versionados (notas, relatórios de teste)
├── docs/
│   ├── .nav.yml              ← menu de topo do portal
│   ├── index.md              ← entrada: "Quero usar um painel" / "Quero manter um painel"
│   ├── metodologia/          ← dataops.md, versionamento-git.md (uma cópia só)
│   ├── changelog.md          ← changelog do portal
│   ├── stylesheets/extra.css ← aviso "pendente" e cor de destaque
│   ├── assets/               ← imagens comuns (só se houver)
│   └── projetos/<slug>/      ← documentação de um projeto
│       ├── .nav.yml          ← menu do projeto
│       └── ...               ← páginas (seção 3)
└── src/<slug>/               ← só os arquivos do Power BI
    ├── <Projeto>.pbip
    ├── <Projeto>.SemanticModel/
    └── <Projeto>.Report/
```

| Regra | Por quê |
|---|---|
| **Um portal para todos os projetos.** | Ao pesquisar uma medida, o usuário precisa achar em quais projetos ela é usada, qual é a regra e o que mudou. Com um site por painel, um é atualizado e outro não, e os usuários veem versões divergentes. |
| **A documentação fica em `docs/projetos/<slug>/`; o Power BI fica em `src/<slug>/`.** | O site lê só `docs/`. O Power BI fica separado do conteúdo do site, e cada projeto tem uma pasta previsível nos dois lados. |
| **O mesmo `<slug>` nos dois lados.** | O nome da pasta é o que liga a documentação aos arquivos do Power BI. Nomes diferentes obrigam a manter uma tabela de correspondência. O slug é escolhido pelo usuário, em minúsculas e com hífens, e não muda se o nome do `.pbip` mudar. |
| **Uma pasta em `src/` só quando o projeto existe.** | Pastas vazias não são versionadas pelo Git e não dizem nada a quem lê. |
| **Metodologia e glossário uma vez só, na raiz.** | Copiados em cada projeto, divergem na primeira correção. |
| **Menu de cada projeto no próprio `.nav.yml`** (plugin `mkdocs-awesome-nav`). | Um menu central com todos os projetos vira centenas de entradas, gera conflito no Git e faz páginas esquecidas sumirem do site. |
| **Repositório num caminho curto, fora do OneDrive** (por exemplo `C:\repos\`). | No laboratório, com o repositório no OneDrive, 394 arquivos do Power BI passaram do limite de 260 caracteres do Windows. O OneDrive sincronizando a pasta `.git` também pode corromper o histórico. |

## 2. Princípios de escrita

1. **Cada página tem propósito único.** Se duas páginas parecem repetir a mesma coisa, uma delas está fora do lugar. Escreva uma vez e aponte com link nos outros lugares.
2. **Dois públicos.** O menu de cada projeto tem três blocos: *Para quem usa* (área de negócio), *Para quem mantém* (time de BI) e *Arquivo* (guias ocultas, rascunhos, medidas de teste e sem uso). *Por quê:* comprador e desenvolvedor procuram coisas diferentes; misturados, os dois se perdem.
3. **Nomenclatura: página × guia.** "Página" é uma página desta documentação; "guia" é uma aba do relatório no Power BI.
4. **Nome de arquivo estável.** O nome do arquivo segue o assunto, não o nome atual da guia ou da pasta de exibição. Renomear uma guia não pode quebrar a URL.
5. **Quebrar uma página só quando ela ficar grande demais para ler de relance**, usando uma organização que já existe (pastas de exibição, guias do relatório). Exceção: as guias do relatório já nascem uma por página.
6. **Não inventar; marcar o que falta.** O que não está nos arquivos vira um aviso de pendência:

    ```markdown
    !!! pendente "A confirmar"
        Qual é o objetivo da guia *Home* e quem a usa?
    ```

    Toda pendência também entra em `pendencias.md`. *Por quê:* uma afirmação errada escrita com confiança é pior que uma pergunta aberta.
7. **A documentação se adapta ao modelo, nunca o contrário.** A primeira rodada só lê o `.SemanticModel` e o `.Report`. Medidas sem pasta de exibição vão para uma página própria. Problemas viram pendência, não correção.
8. **Escrita com agente de IA, revisão humana.** O agente escreve as páginas; o autor revisa linha a linha contra o projeto. O agente confere contagens e dependências com o script de levantamento em vez de contar à mão.
9. **Dupla validação.** A data de uma página mostra quando ela mudou, não se está correta.
    - **Validação técnica:** pull request revisado por outra pessoa do time de BI.
    - **Validação de negócio:** a área responsável confirma a **regra** e um **resultado de exemplo** que ela conhece. O negócio nunca valida o DAX; a tradução para DAX é responsabilidade do BI.
10. **Fronteira de escopo.** A linhagem documentada começa no fluxo de dados (ou na fonte que o modelo lê). O que acontece antes é de outro projeto. A fronteira fica registrada em `fontes-de-dados.md`: equipe responsável, link da documentação do pipeline, horário de atualização e colunas que o painel usa.
11. **Nenhuma medida sem pasta de exibição ao final de uma tarefa no modelo.** É uma regra para quem altera o modelo, registrada no guia do desenvolvedor. A documentação não corrige isso: só registra.
12. **Docstring em duas camadas no modelo.** `///` antes de `measure 'Nome' =` vira a descrição exibida no Power BI; `/* */` na primeira linha da expressão aparece na barra de fórmulas. Adicioná-las é uma etapa posterior, em commits próprios, fora da documentação inicial.

## 3. Páginas de um projeto

Modelos em `modelos/projeto/`. Todas ficam em `docs/projetos/<slug>/`.

### Para quem usa

| Página | O que contém | Observação |
|---|---|---|
| `readme.md` | Por que a documentação existe, termos usados, "se você procura X, veja Y", e a seção "Por que DataOps neste projeto". | Entrada do projeto. |
| `escopo.md` | O que o painel resolve, objetivo, público, processos cobertos, dentro e fora do escopo. | Quase tudo começa como pendência. |
| `como-usar.md` | Jornadas reais do usuário de negócio ("como decido o pedido da semana"). | Nasce vazia. Só é escrita depois de conversar com a área de negócio. |
| `regras-de-negocio.md` | Glossário do projeto e regras de cálculo gerais, cada uma com onde está implementada. | Cada regra recebe depois o selo de validação de negócio. |
| `guias-do-relatorio/` | `index.md` com a tabela de guias e uma página por guia. | Cada página de guia: em cima, a parte de quem usa; embaixo, "Detalhes técnicos" num bloco recolhível. |

### Para quem mantém

| Página | O que contém | Observação |
|---|---|---|
| `modelo-de-dados.md` | Tabelas, colunas, tipos, relacionamentos e diagrama ER. | Diagrama com mais de ~15 relacionamentos: dividir em visões por assunto e manter uma visão completa no fim. Expressão DAX de tabela calculada num bloco recolhível. |
| `medidas-dax/` | `index.md` com o catálogo e uma página por pasta de exibição, mais "Sem pasta de exibição". | Cada medida: tabela, formato, guias em que aparece, **depende de**, **é usada por** e o código. |
| `fontes-de-dados.md` | Conectores, tabelas, transformações antes da carga, **frequência de atualização**, **responsável** e a **fronteira** com o pipeline. | |
| `decisoes-tecnicas.md` | Decisões de arquitetura (ADR): data, commit, contexto, decisão, consequências. | Data e commit preenchidos no momento em que a decisão é escrita. |
| `guia-do-desenvolvedor.md` | Onde está cada coisa no PBIP, convenções, regra das pastas de exibição, checklist do PR. | Caminhos sempre a partir de `src/<slug>/`. |
| `pendencias.md` | Todas as pendências do projeto num lugar só, com página de origem, dono e prioridade. | |
| `changelog.md` | Mudanças do projeto no formato Keep a Changelog. | Registra **atividade**, não resultado. Toda entrada cita pelo nome as medidas afetadas. |

### Arquivo

| Página | O que contém |
|---|---|
| `arquivo/index.md` | Guias ocultas e rascunhos, medidas de teste e medidas sem uso em visuais. |

*Por quê:* rascunhos continuam documentados, mas não disputam atenção com o que está em uso.

## 4. Versionamento com Git

| Regra | Por quê |
|---|---|
| **Linha de base antes de documentar:** tag anotada `<slug>/baseline-pre-documentacao` no estado commitado do projeto. | Permite comparar o antes e o depois. O prefixo evita conflito entre projetos no mesmo repositório. |
| **Tags de versão com prefixo:** `<slug>/v1.0.0`, `portal/v1.0.0`. | Mesmo motivo. Cada versão do changelog tem uma tag. |
| **Nada direto na `main`.** O agente deixa as mudanças no working tree; o autor revisa e abre o pull request. | A revisão das sessões de IA acontece no PR. |
| **Mudar um projeto de lugar num commit próprio**, com a remoção e a adição juntas e sem alterar conteúdo. | O Git reconhece a renomeação e mantém o histórico de cada arquivo (`git log --follow`). Comparações com a linha de base passam a usar `git diff -M`. |
| **Commits no formato `tipo: descrição`** (`feat`, `fix`, `docs`, `refactor`, `chore`). Mudança no modelo e mudança só de documentação em commits separados quando não dependem uma da outra. | Histórico legível. |
| **`.gitignore`:** `.pbi/localSettings.json`, `.pbi/cache.abf`, `*.pbix`, `.venv/`, `site/`, `__pycache__/`. | Caches locais e binários grandes nunca entram no histórico. |

## 5. Setup do MkDocs

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

## 6. O que ficou para depois

Ideias decididas mas adiadas estão em `niveis.md` (níveis 2 e 3): validação de negócio formal, glossário corporativo, changelog do portal ligado aos projetos, CI, blocos-fonte por medida, números por variável, rodapé com link do changelog, formulário "Sugerir correção", identidade visual, indicadores e publicação com login.
