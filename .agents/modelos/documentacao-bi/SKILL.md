---
name: documentacao-bi
description: Conduz a criação e a manutenção da documentação de projetos Power BI (PBIP) num portal único em MkDocs Material, para o agente e para o usuário. Use quando o usuário quiser iniciar, migrar, continuar ou revisar a documentação de um painel Power BI, montar o portal de documentação de BI, documentar medidas DAX, modelo de dados, fontes, guias do relatório ou regras de negócio, ou quando disser "documentar o projeto", "iniciar a documentação", "migrar a documentação para o padrão", "próximo passo da documentação". Não use para alterar o modelo semântico ou o relatório.
---

# Documentação de projetos de BI

Versão da skill: **0.3.0** (ver `CHANGELOG.md`). Esta é uma versão de teste: ao fim de cada sessão você escreve um relatório de teste (seção 7).

**Pasta desta skill:** `${CLAUDE_SKILL_DIR}`. Nos comandos abaixo e nos arquivos de `referencias/`, `<pasta-da-skill>` é essa pasta (o plugin instala a skill num cache, então não conte com um caminho fixo).

Esta skill ensina você, o agente, a construir a documentação de um projeto Power BI no **portal único de documentação de BI**, junto com o usuário. Ela foi desenhada num laboratório (um projeto piloto) e revisada por um conselho de especialistas. O porquê de cada regra está nos arquivos `referencias/padrao-*.md`.

## 1. Antes de qualquer coisa

1. Leia `referencias/padrao.md` (o índice), `padrao-estrutura.md` e `padrao-escrita.md`. São a regra do jogo. Leia os demais arquivos do padrão só quando a tarefa pedir (ver o índice), e consulte `referencias/armadilhas.md` antes de improvisar.
2. Descubra em que situação o repositório está e escolha o modo:
   - **Projeto novo:** o projeto Power BI não tem documentação. Siga `referencias/modo-projeto-novo.md`.
   - **Projeto existente:** já existe documentação (em qualquer formato) ou o repositório não segue a estrutura do portal. Siga `referencias/modo-projeto-existente.md`.
   - Na dúvida, pergunte ao usuário. Não escolha sozinho.
3. Descubra em que **nível** o projeto está (`referencias/niveis.md`). Nunca tente implementar tudo de uma vez: entregue o nível atual inteiro antes de passar ao seguinte.
4. Se o projeto não estiver em formato PBIP (só existir um `.pbix`), pare e avise o usuário.

## 2. Regras que valem sempre

- **Não altere o projeto Power BI.** Nada dentro de `*.SemanticModel/` e `*.Report/` pode ser criado, editado, renomeado ou removido, inclusive `///`, `/* */` e `displayFolder`. Problemas encontrados viram pendência.
- **Não edite dentro dos marcadores `gerado`.** As páginas `modelo-de-dados.md` e `medidas-dax/` são geradas por `scripts/gerar_paginas.py`; o que fica entre `<!-- gerado:inicio ... -->` e `<!-- gerado:fim ... -->` é reescrito a cada execução. Escreva sempre **acima** do bloco.
- **Não execute código do projeto para documentá-lo.** O extrator de ETL lê os `.py` por análise estática (`ast`). Nunca rode scripts do projeto, nem copie credenciais, caminhos de usuário ou valores de configuração para a documentação.
- **Não invente.** O que não estiver nos arquivos vira um aviso de pendência (`!!! pendente`), nunca uma suposição escrita como fato.
- **Não faça commit, push nem crie branch.** Deixe tudo no working tree. O usuário revisa e abre o pull request. A única exceção é a tag e o commit da linha de base, e só com autorização explícita do usuário na sessão.
- **Mudar arquivos de lugar é um passo separado.** Mover as pastas do Power BI para `src/<slug>/` só com autorização, num commit próprio que o usuário faz, sem misturar com outras mudanças.
- **Pergunte antes de decidir o que é do usuário:** o nome do projeto (slug), o que é rascunho, o que é oficial, o que entra no nível atual.

## 3. Estrutura do portal (resumo)

```
<portal>/
├── mkdocs.yml                ← único, na raiz
├── pyproject.toml / uv.lock
├── .gitignore
├── .claude/skills/documentacao-bi/   ← cópia local da skill (opcional; com o plugin não existe)
├── docs/
│   ├── .nav.yml              ← menu de topo do portal
│   ├── index.md              ← entradas "Quero usar" / "Quero manter"
│   ├── metodologia/          ← uma cópia só, para todos os projetos
│   ├── changelog.md          ← mudanças que afetam o portal inteiro
│   ├── stylesheets/extra.css
│   └── projetos/<slug>/      ← documentação de cada projeto
│       ├── .nav.yml          ← menu do projeto
│       └── ...
└── src/<slug>/               ← só os arquivos do Power BI
    ├── <Projeto>.pbip
    ├── <Projeto>.SemanticModel/
    └── <Projeto>.Report/
```

O `<slug>` é **o mesmo** em `src/` e em `docs/projetos/`. Os modelos de cada arquivo estão em `modelos/`.

## 4. Onde está cada coisa nesta skill

| Arquivo | Quando ler |
|---|---|
| `referencias/padrao.md` | Sempre, no início. Índice do padrão. |
| `referencias/padrao-estrutura.md`, `padrao-escrita.md` | Sempre, no início. Estrutura do portal e princípios de escrita. |
| `referencias/padrao-paginas.md` | Ao criar ou revisar páginas de um projeto. |
| `referencias/padrao-git.md` | Ao tocar em linha de base, tags, commits ou PR. |
| `referencias/padrao-mkdocs.md` | Ao montar o portal ou quando o build falhar. |
| `referencias/armadilhas.md` | Antes de improvisar diante de algo imprevisto; ao fim da sessão, para registrar o que apareceu de novo. |
| `referencias/modo-projeto-novo.md` | Projeto sem documentação. |
| `referencias/modo-projeto-existente.md` | Projeto com documentação fora do padrão. |
| `referencias/niveis.md` | Para saber o que entra agora e o que fica para depois. |
| `referencias/educacao-mantenedores.md` | Ao fim de cada etapa: o que ensinar ao usuário. |
| `referencias/relatorio-de-teste.md` | Ao fim de cada sessão. |
| `modelos/portal/` | Arquivos da raiz do portal (copiar uma vez, se ainda não existirem). |
| `modelos/metodologia/` | Páginas de metodologia (copiar uma vez para `docs/metodologia/`). |
| `modelos/projeto/` | Modelos das páginas de um projeto (copiar a pasta inteira para `docs/projetos/<slug>/` e preencher). |
| `modelos/itens/` | Modelos de itens repetidos: uma página por guia (`guia.md`), uma página por pasta de medidas (`pasta-de-medidas.md`) e uma seção por medida (`medida.md`). Não copie esta pasta para `docs/`. |
| `scripts/levantamento.py` | Contagens e dependências entre medidas, para conferir o que você escreve. Também tem `--preflight`. |
| `scripts/gerar_paginas.py` | Gera `modelo-de-dados.md` (com ER, RLS, grupos de cálculo e hierarquias) e `medidas-dax/` direto do modelo. Preserva o texto manual. `--check` serve para o PR e a CI. |
| `scripts/extrair_etl.py` | Gera `etl-python.md` das docstrings dos scripts Python do projeto, por análise estática. Só se o projeto tiver Python. Alerta sobre credencial literal no código sem copiar o valor. |
| `scripts/comparar_portal.py` | Compara um portal já criado com os modelos desta versão da skill (só leitura), para levar mudanças de `mkdocs.yml`, CSS e metodologia. |
| `referencias/distribuicao.md` | Ao instalar, atualizar ou publicar uma versão nova da skill como plugin. |
| `referencias/decisao-mkdocs.md` | Antes de qualquer decisão sobre manter ou trocar o MkDocs. |
| `scripts/tests/` | Testes dos dois scripts, com um PBIP de exemplo. Rode ao alterar os scripts: `PYTHONUTF8=1 python -m unittest discover -s scripts/tests`. |

## 5. Como trabalhar numa sessão

1. **Situação:** diga ao usuário em que modo e nível o projeto está, e qual é o próximo passo.
2. **Levantamento:** primeiro rode `python ${CLAUDE_SKILL_DIR}/scripts/levantamento.py --root src/<slug> --preflight` e trate os avisos (caminho longo, OneDrive, `.pbix`, pasta fora de `src/`). Depois rode `python ${CLAUDE_SKILL_DIR}/scripts/levantamento.py --root src/<slug>` (use `PYTHONUTF8=1` no Windows). Use os números e as dependências do script para conferir o que você escreve, em vez de contar à mão.
3. **Geração:** rode `python ${CLAUDE_SKILL_DIR}/scripts/gerar_paginas.py --root src/<slug> --docs docs/projetos/<slug>`. Ele cria `modelo-de-dados.md` e `medidas-dax/` só com o que está no modelo, e avisa quando uma página existente não tem marcadores (nesse caso não a altera). Ao mudar o modelo, rode de novo: o texto escrito à mão é preservado. Se o projeto tiver scripts Python, pergunte em que pasta ficam e rode `python ${CLAUDE_SKILL_DIR}/scripts/extrair_etl.py --etl <pasta> --docs docs/projetos/<slug>`; se não tiver, apague `etl-python.md` e a linha dele no `.nav.yml`. Trate cada ALERTA de credencial como pendência de segurança para o usuário, sem repetir o valor.
4. **Escrita:** o que o modelo não diz (descrição de negócio das medidas, regras, escopo, guias, fontes) é com você. Copie o modelo da página, preencha só com o que está nos arquivos e marque o resto como `!!! pendente`. Descrição de medida escreva acima do bloco `gerado`, no lugar do aviso.
5. **Validação:** rode `uv run mkdocs build --strict` e `python ${CLAUDE_SKILL_DIR}/scripts/gerar_paginas.py --root src/<slug> --docs docs/projetos/<slug> --check`. Os dois precisam passar. Confirme que as pastas do Power BI não mudaram (`git status --porcelain -- src/<slug>`).
6. **Ensino:** ao fim de cada etapa, explique ao usuário o que ele precisa saber para manter aquilo sozinho (`referencias/educacao-mantenedores.md`).
7. **Entrega:** resumo do que foi feito, pendências por página, o checklist do pull request e o relatório de teste.

## 6. Checklist do pull request (entregar ao usuário)

- [ ] `uv run mkdocs build --strict` passou sem avisos.
- [ ] `gerar_paginas.py --check` passou: as páginas geradas estão em dia com o modelo.
- [ ] As pastas do Power BI não mudaram, ou a mudança é só de lugar, num commit separado.
- [ ] O changelog do projeto foi atualizado, citando pelo nome as medidas afetadas.
- [ ] As páginas das medidas alteradas têm "depende de" e "é usada por" atualizados.
- [ ] Toda página nova está no `.nav.yml` do projeto.
- [ ] As regras de negócio que mudaram têm validação de negócio pedida.
- [ ] O autor revisou linha a linha o que o agente escreveu.

## 7. Relatório de teste (obrigatório nesta versão)

Ao fim de cada sessão, escreva `.agents/relatorios-skill/AAAA-MM-DD-sessao-N.md` seguindo `referencias/relatorio-de-teste.md`. Seja honesto sobre onde esta skill foi ambígua, incompleta ou errada: o relatório é usado para corrigir a próxima versão. Situações novas e a decisão tomada também entram em `referencias/armadilhas.md`.
