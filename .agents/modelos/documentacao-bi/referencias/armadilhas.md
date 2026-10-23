# Armadilhas conhecidas

Catálogo de situações que não estavam previstas e a decisão tomada em cada uma. **Consulte antes de improvisar** e, ao fim de cada sessão, acrescente aqui o que apareceu de novo (em vez de criar uma regra solta em outro arquivo). Quando uma armadilha virar regra permanente, mova-a para o `padrao-*.md` e deixe aqui só o link.

## Como registrar uma armadilha

Uma linha na tabela, no formato **Sintoma | Causa | Decisão | Origem**. Origem é o projeto e a data (ou o relatório de teste) em que apareceu.

## Ambiente e repositório

| Sintoma | Causa | Decisão | Origem |
|---|---|---|---|
| Arquivos do Power BI não abrem, erro de caminho longo ou git falha em checkout. | Repositório no OneDrive ou em caminho profundo; limite de 260 caracteres do Windows (no projeto piloto, centenas de arquivos passaram do limite). | Mover o repositório para um caminho curto fora do OneDrive (ex.: `C:\repos\<portal>`) **antes** de documentar. O `levantamento.py --preflight` detecta. | Projeto piloto, 2026-10 |
| Histórico do Git corrompido ou conflitos estranhos em `.git`. | OneDrive sincronizando a pasta `.git`. | Mesma decisão: repositório fora do OneDrive. | Projeto piloto, 2026-10 |
| O script falha com erro de codificação no Windows. | Console em codificação diferente de UTF-8. | Rodar com `PYTHONUTF8=1`. | Projeto piloto, 2026-10 |
| O projeto só tem `.pbix`. | Não está em formato PBIP. | Parar e avisar o usuário. A skill não converte. | `SKILL.md` §1 |

## Git e linha de base

| Sintoma | Causa | Decisão | Origem |
|---|---|---|---|
| `git status` mostra mudanças pendentes antes da linha de base. | Há trabalho não commitado além da skill e de `.agents/`. | Parar e perguntar o que são. A linha de base precisa ser um estado commitado. | `modo-projeto-novo.md` |
| Já existe uma tag de linha de base de outra rodada. | Documentação anterior. | Registrar qual é e não criar outra sem perguntar. | `modo-projeto-existente.md` |
| Os arquivos do Power BI não estão em `src/<slug>/`. | Projeto anterior ao padrão. | A mudança de lugar é um passo à parte, num commit só do usuário. O agente orienta e confere que os arquivos ficaram idênticos. | `padrao-git.md` |
| Duas tags com o mesmo nome em projetos diferentes do mesmo repositório. | Tag sem prefixo. | Sempre prefixar com o slug (`<slug>/baseline-pre-documentacao`). | `padrao-git.md` |

## MkDocs e build

| Sintoma | Causa | Decisão | Origem |
|---|---|---|---|
| `mkdocs build --strict` falha com página "not in nav". | Página criada fora do `.nav.yml` do projeto. | É o comportamento desejado: incluir a página no `.nav.yml`. | `padrao-mkdocs.md` |
| Plugins deixam de funcionar após atualizar o MkDocs. | MkDocs 2.0 remove o sistema de plugins. | Manter `mkdocs>=1.6,<2`. Não atualizar sem decisão registrada. | `padrao-mkdocs.md` |
| O projeto já tem um `mkdocs.yml`. | Documentação anterior. | Mostrar a diferença para o modelo e propor a fusão. Nunca sobrescrever. | `modo-projeto-existente.md` |
| Documentação antiga ainda aparece no menu raiz. | `nav` antigo no `mkdocs.yml`. | Tirar as páginas do projeto do `nav` antigo e usar o `.nav.yml` do projeto. | `modo-projeto-existente.md` |

## Modelo e relatório

| Sintoma | Causa | Decisão | Origem |
|---|---|---|---|
| Muitas medidas sem pasta de exibição. | Modelo sem organização. | Não corrigir o modelo. Documentar em `medidas-dax/sem-pasta.md` e abrir pendência. | `padrao-escrita.md` §2, itens 7 e 11 |
| Tabelas `LocalDateTable_*` e `DateTableTemplate_*` inflam as contagens. | Hierarquia automática de datas do Power BI. | O script as separa como "auto-data". Não entram no dicionário nem no diagrama. | `levantamento.py` |
| Renomear uma guia ou pasta de exibição quebra links. | O nome do arquivo seguia o nome da guia. | Nome de arquivo segue o assunto, não o nome atual. Se precisar reorganizar, criar a pasta nova, mover as medidas e registrar no changelog. | `padrao-escrita.md` §2, item 4 |
| Uma regra de negócio não aparece em lugar nenhum dos arquivos. | Conhecimento só na cabeça de quem usa. | Não inventar. Escrever `!!! pendente` e levar à sessão de validação de negócio. | `padrao-escrita.md` §2, item 6 |
| O gerador avisa "página existente sem marcadores". | A página foi escrita à mão ou é de outra versão. | Não é alterada. O usuário decide: mover o conteúdo para `arquivo/` e apagar a página, ou manter à mão. | `gerar_paginas.py` |
| A seção de uma medida ficou com "Removido do modelo". | A medida foi apagada ou renomeada no modelo. | O texto manual fica. Mover para `arquivo/` ou apagar, e registrar no changelog. Se foi renomeação, levar a descrição para a seção nova. | `gerar_paginas.py` |
| A URL de uma página de medidas mudou. | O marcador `<!-- pasta: NOME -->` da primeira linha foi apagado. | Recolocar o marcador com o nome atual da pasta de exibição; o gerador reaproveita o arquivo. | `gerar_paginas.py` |
| `gerar_paginas.py --check` falha no PR. | O modelo mudou e as páginas não foram regeneradas. | Rodar o gerador sem `--check` e incluir as páginas no PR. | `gerar_paginas.py` |
| Papel de segurança (RLS) não aparece na documentação. | O parser lê só `definition/roles/*.tmdl`. | Conferir onde o papel está definido e registrar o caso aqui. Os membros do papel nunca estão nos arquivos. | `levantamento.py` |
| Link para âncora de medida quebrado no build. | Nome de medida mudou sem regenerar a página. | Regenerar. O template `mkdocs.yml` valida âncoras (`validation.links.anchors: warn`). | `padrao-mkdocs.md` |
| O plugin foi atualizado no repositório mas ninguém recebe a versão nova. | O campo `version` do `plugin.json` não mudou; o Claude Code só atualiza quando ele muda. | Subir a versão (e a do CHANGELOG, `SKILL.md`, `README`) a cada release. O teste de empacotamento confere. | `distribuicao.md` |
| Comando da skill aponta para um caminho que não existe. | Caminho fixo `.claude/skills/...`; com o plugin a skill fica num cache. | Usar `${CLAUDE_SKILL_DIR}` no `SKILL.md` e `<pasta-da-skill>` nas referências. O teste de empacotamento proíbe o caminho fixo. | `distribuicao.md` |
| O extrator de ETL mostra ALERTA de credencial. | Senha, token ou chave literal no código, ou URL com usuário e senha. | O valor nunca é copiado para a página. Avisar o usuário: tirar do código (variável de ambiente), trocar a credencial e verificar o histórico do Git. | `extrair_etl.py` |
| O extrator de ETL não mostra os argumentos de um script. | O script usa `click`, `typer` ou outra biblioteca, e só o `argparse` é lido. | A página avisa. Descrever os argumentos à mão acima do bloco `gerado`. | `extrair_etl.py` |
| Dependência entre medidas parece incompleta. | O script só reconhece referência `[Medida]` sem tabela antes. | Conferir à mão as medidas com referência qualificada e registrar o caso aqui, se for recorrente. | `levantamento.py` |
