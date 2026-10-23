# Modo: projeto existente

Use quando o projeto Power BI já tem documentação (em qualquer formato ou lugar) ou quando o repositório não segue a estrutura do portal. O objetivo é trazer o projeto para o padrão **por etapas**, sem perder o que já existe e sem parar o trabalho de quem usa o painel.

Diferença para o projeto novo: aqui existe um "antes" com valor. Nada do que já está escrito é apagado sem o usuário decidir.

## Etapa 1: Diagnóstico (só leitura)

Não altere nenhum arquivo nesta etapa. Levante e mostre ao usuário:

1. **Estado do Git:** `git status`, branch atual, se está sincronizado com o remoto, tags existentes. Se houver mudanças pendentes, pergunte o que são antes de seguir.
2. **Onde estão os arquivos do Power BI:** na raiz, em `src/<slug>/` ou em outro lugar. Nome do `.pbip` e das pastas `.SemanticModel` e `.Report`.
3. **Caminho do repositório:** comprimento do maior caminho de arquivo. Se passar de ~240 caracteres ou o repositório estiver no OneDrive, avise (ver `padrao-estrutura.md`, seção 1).
4. **Documentação existente:** todo `.md`, README, pasta `docs/`, `mkdocs.yml`, wiki ou arquivo citado pelo usuário. Para cada um: o que cobre, de quando é, se segue o padrão.
5. **Inventário do projeto:** rode o script de levantamento sobre a pasta do Power BI e mostre os indicadores (tabelas, medidas, medidas sem pasta, medidas com `///`, guias, guias ocultas).
6. **Comparação com o padrão:** uma tabela com cada página do padrão (`padrao-paginas.md`, seção 3) e a situação no projeto:

    | Página do padrão | Existe hoje? | Onde | Situação |
    |---|---|---|---|
    | `escopo.md` | sim | `docs/escopo.md` | aproveitável, mover |
    | `pendencias.md` | não | — | criar |

    Situações possíveis: *aproveitável* (só mover), *adaptar* (conteúdo bom, formato fora do padrão), *refazer* (desatualizado ou incorreto), *criar* (não existe).

**Entrega da etapa:** o diagnóstico como mensagem e salvo em `.agents/diagnostico-<slug>.md`. Pergunte ao usuário o slug do projeto, se ainda não estiver definido.

## Etapa 2: Plano de migração (decisão do usuário)

Monte um plano com os passos abaixo, na ordem, e marque o **nível** de cada um (`niveis.md`). Mostre o plano e **espere a aprovação** antes de alterar qualquer coisa.

1. **Linha de base:** commit do estado atual (feito pelo usuário) e tag `<slug>/baseline-pre-documentacao` (criada pelo agente só com autorização). Se já existir uma linha de base de outra rodada, registre qual é e não crie outra sem perguntar.
2. **Estrutura do portal:** se a raiz ainda não tem `mkdocs.yml`, `docs/.nav.yml`, `docs/index.md`, `docs/metodologia/` e `docs/stylesheets/extra.css`, copiar de `modelos/portal/` e `modelos/metodologia/`. Se já existe um `mkdocs.yml`, mostrar a diferença para o modelo e propor a fusão; não sobrescrever.
3. **Mudança de lugar do Power BI** (se os arquivos não estiverem em `src/<slug>/`): passo separado, feito pelo usuário num commit próprio, sem nenhuma outra mudança. O agente só orienta e confere depois que os arquivos estão idênticos.
4. **Páginas:** para cada linha *aproveitável*, *adaptar*, *refazer* ou *criar* do diagnóstico, o que será feito. Conteúdo existente que não cabe no padrão vai para `arquivo/` ou fica como está, por decisão do usuário.
5. **Menu:** criar `docs/projetos/<slug>/.nav.yml` e tirar as páginas do projeto de qualquer `nav` antigo no `mkdocs.yml`.
6. **Pendências:** converter "A confirmar", TODOs e perguntas soltas para o aviso `!!! pendente` e reunir em `pendencias.md`.

Salve o plano aprovado em `.agents/plano-migracao-<slug>.md`, com a data e o que o usuário decidiu em cada passo.

## Etapa 3: Aplicação (um passo por vez)

- Execute um passo do plano de cada vez. Ao terminar cada um, rode `uv run mkdocs build --strict` e mostre o resultado.
- Ao **mover** uma página existente, preserve o conteúdo e ajuste só o que o padrão exige (aviso de pendência, links, caminhos). Ao **adaptar**, mostre o que mudou.
- Confira com o script: contagens e dependências das medidas devem bater com o que está escrito.
- **ETL Python:** se o projeto tem scripts Python, pergunte a pasta e use `extrair_etl.py`; página `etl-python.md` antiga sem marcadores não é alterada (mesma regra das outras páginas geradas). Mostre ao usuário todo ALERTA de segurança do extrator (credencial literal, caminho absoluto) antes de seguir; nunca repita o valor.
- **Páginas geradas:** se `modelo-de-dados.md` ou `medidas-dax/` já existem sem marcadores `gerado`, o gerador não as altera e avisa. Decisão do usuário: mover o conteúdo antigo para `arquivo/` e apagar a página para o gerador criá-la, ou continuar à mão. Descrições de medidas que já existem no texto antigo devem ser levadas para acima do bloco `gerado` da medida correspondente.
- Depois de cada passo, confirme que `src/<slug>/` não mudou: `git status --porcelain -- src/<slug>`.
- Se algo do plano se mostrar errado no meio do caminho, pare e pergunte. Não improvise outro plano.

## Etapa 4: Validação e entrega

1. `uv run mkdocs build --strict` sem avisos e `gerar_paginas.py --check` com código 0.
2. As pastas do Power BI idênticas à linha de base (`git diff -M --stat <slug>/baseline-pre-documentacao -- src/<slug>` vazio, ou só renomeações).
3. Changelog do projeto com a entrada da migração; uma linha no `docs/changelog.md` do portal dizendo que o projeto entrou no portal.
4. Resumo para o usuário: o que foi feito em cada passo, as pendências por página, o que ficou para o próximo nível, o checklist do pull request (`SKILL.md`, seção 6) e a pauta da sessão de validação de negócio (as regras que precisam ser confirmadas pela área).
5. Relatório de teste (`relatorio-de-teste.md`).
