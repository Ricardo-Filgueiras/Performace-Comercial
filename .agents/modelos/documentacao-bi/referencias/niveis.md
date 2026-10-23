# Níveis de implementação

Nem tudo o que foi decidido precisa existir no primeiro dia. A documentação de um projeto avança por níveis. Entregue um nível inteiro antes de começar o seguinte, e diga ao usuário em que nível o projeto está.

**Critério do nível 1:** entra se, sem ele, o projeto nasceria com a estrutura errada, se ele muda a forma de escrever uma página, ou se protege o que já existe. O que só **melhora** algo que já funciona fica para os níveis 2 e 3.

## Nível 1: Essencial

| Item | Onde está |
|---|---|
| Estrutura do portal e do projeto (`docs/projetos/<slug>/`, `src/<slug>/`, mesmo slug) | `padrao-estrutura.md` §1 |
| Menu do projeto em `.nav.yml` com os blocos *Para quem usa*, *Para quem mantém* e *Arquivo* | `padrao-escrita.md` §2, item 2 |
| Todas as páginas da seção 3 do padrão (com `como-usar.md` ainda vazia) | `padrao-paginas.md` §3 |
| Pendências como `!!! pendente` e reunidas em `pendencias.md` | `padrao-escrita.md` §2, item 6 |
| Modelo de dados e medidas geradas por `gerar_paginas.py`, com `--check` passando | `padrao-paginas.md` §3 |
| ETL Python documentado por `extrair_etl.py`, quando o projeto tem scripts | `padrao-paginas.md` §3 |
| Medidas com "depende de" e "é usada por" | `padrao-paginas.md` §3 |
| Fontes com frequência de atualização, responsável e fronteira com o pipeline | `padrao-escrita.md` §2, item 10 |
| Guias com "Detalhes técnicos" recolhível | `padrao-paginas.md` §3 |
| Changelog do projeto | `padrao-paginas.md` §3 |
| Linha de base com tag prefixada; nada direto na `main`; checklist do PR | `padrao-git.md` §4; `SKILL.md` §6 |
| `mkdocs build --strict` passando, com página fora do menu quebrando o build | `padrao-mkdocs.md` §5 |

## Nível 2: Validação e uso

Começa depois que o nível 1 do projeto foi aprovado num pull request.

| Item | O que é |
|---|---|
| Sessão de validação de negócio | A área confirma cada regra principal e um resultado de exemplo. O resultado vai para a página: validado por, data, exemplo usado. |
| `como-usar.md` | Jornadas reais escritas a partir da sessão de validação. |
| Glossário corporativo | Termos que valem para vários projetos sobem para `docs/glossario/`, a partir do segundo projeto. |
| Changelog do portal ligado aos projetos | Mudança do portal que afeta um projeto ganha uma linha curta no changelog do projeto, apontando para a entrada do portal. |
| CI | GitHub Actions com `uv sync`, `mkdocs build --strict`, `gerar_paginas.py --check`, `extrair_etl.py --check` (se houver ETL) e os testes dos scripts. |

## Nível 3: Automação e publicação

| Item | O que é |
|---|---|
| Inventário por variável | O script gera `inventario.yml`; as páginas usam `{{ inventario.medidas }}` (`mkdocs-macros-plugin`, com Jinja desligado nos blocos DAX). |
| Bloco-fonte por medida | Um arquivo por medida, incluído com `pymdownx.snippets` onde ela for citada, inclusive em outros projetos. |
| Rodapé de rastreabilidade | *Hook* que mostra a última mudança, o link para a entrada do changelog e o commit. |
| "Sugerir correção" | Link no rodapé para um Microsoft Forms com a página preenchida; respostas triadas pelo BI. |
| Identidade visual | Logo, ícone e paleta da organização, seguindo o manual de marca se existir. O modelo usa só a cor de alerta padrão do Material para o aviso "pendente". |
| Indicadores | Página de resultados: cobertura de descrições, regras validadas, pendências, perguntas repetidas ao BI. |
| Publicação com login | Depende do plano do GitHub, da segurança entre projetos e do local de publicação. |
