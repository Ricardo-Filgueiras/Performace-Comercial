<!-- Parte do padrão. Índice em padrao.md. -->
# 3. Páginas de um projeto

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
| `etl-python.md` | Scripts Python do projeto: o que cada um faz, como executar, entradas e saídas, bibliotecas, variáveis de ambiente e alertas de segurança. | **Opcional**: só se o projeto tem scripts Python (senão, apague a página e a linha do `.nav.yml`). Gerada das docstrings por `extrair_etl.py`. |
| `decisoes-tecnicas.md` | Decisões de arquitetura (ADR): data, commit, contexto, decisão, consequências. | Data e commit preenchidos no momento em que a decisão é escrita. |
| `guia-do-desenvolvedor.md` | Onde está cada coisa no PBIP, convenções, regra das pastas de exibição, checklist do PR. | Caminhos sempre a partir de `src/<slug>/`. |
| `pendencias.md` | Todas as pendências do projeto num lugar só, com página de origem, dono e prioridade. | |
| `changelog.md` | Mudanças do projeto no formato Keep a Changelog. | Registra **atividade**, não resultado. Toda entrada cita pelo nome as medidas afetadas. |

### Páginas geradas por script

`modelo-de-dados.md` e `medidas-dax/` (índice, uma página por pasta de exibição e `sem-pasta.md`) são geradas por `scripts/gerar_paginas.py` a partir do `.SemanticModel` e do `.Report`. Isso inclui tabelas, colunas, relacionamentos, diagrama ER, hierarquias, grupos de cálculo, papéis de segurança (RLS) e, por medida, tabela, formato, guias, "depende de", "é usada por" e código.

| Regra | Por quê |
|---|---|
| **O conteúdo gerado fica entre marcadores** `<!-- gerado:inicio X -->` e `<!-- gerado:fim X -->`. Escreva sempre **acima** do bloco. | O gerador reescreve só o que está entre marcadores; o texto manual (descrições, observações) sobrevive a cada execução. |
| **Item que saiu do modelo não é apagado.** O bloco vira um aviso de pendência "Removido do modelo". | A documentação não decide sozinha apagar texto escrito por uma pessoa. |
| **O arquivo de uma pasta de exibição é fixado pelo marcador `<!-- pasta: NOME -->`.** | Renomear a pasta de exibição não muda a URL (princípio 4 de escrita). |
| **`--check` no PR e na CI.** | Alterou o modelo e esqueceu de regenerar: o check falha, e a documentação não fica atrás do modelo. |
| **Página existente sem marcadores não é tocada.** | Documentação escrita à mão em outro formato é decisão do usuário (ver `modo-projeto-existente.md`). |

`etl-python.md` segue as mesmas regras de marcadores, e é gerada por `scripts/extrair_etl.py` por **análise estática**: o script nunca importa nem executa o código do projeto, mostra só nomes (arquivo, variável de ambiente, parâmetro) e transforma credencial literal em alerta, sem copiar o valor.

Fica fora do gerador, e é escrito pelo agente com revisão humana: descrição de negócio das medidas, regras de negócio, escopo, guias do relatório, fontes de dados e decisões técnicas.

### Arquivo

| Página | O que contém |
|---|---|
| `arquivo/index.md` | Guias ocultas e rascunhos, medidas de teste e medidas sem uso em visuais. |

*Por quê:* rascunhos continuam documentados, mas não disputam atenção com o que está em uso.
