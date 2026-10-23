# Decisão: manter o MkDocs ou migrar

**Estado: adiada.** A decisão será tomada ao fim do segundo projeto documentado, com o que os dois ensinarem, **mas com prazo**: o portal depende de uma ferramenta em fim de ciclo (ver abaixo), então a reavaliação acontece no que vier primeiro entre o fim do segundo projeto e **dezembro de 2026**.

## O que se sabe (pesquisado em 2026-10-23)

| Fato | Fonte | Confiança |
|---|---|---|
| O Material for MkDocs está em modo de manutenção: a 9.7.0 foi a última versão com recursos novos; a equipe passou a focar no **Zensical**. Correções críticas e de segurança foram prometidas por pelo menos 12 meses a partir de nov. 2025, **ou seja, até cerca de novembro de 2026**. | Notas de versão do Material (via buscas) | média: confira a data atual no site do projeto |
| O MkDocs 2.0 remove o sistema de plugins e não traz caminho de migração, segundo o aviso que o próprio Material exibe no build. O Material 9.7.5 limitou o MkDocs a `<2`. | Aviso do Material; este portal já fixa `mkdocs>=1.6,<2` | média: o aviso é da equipe do Material, não do projeto MkDocs |
| O Zensical foi feito para ler `mkdocs.yml` existente, mas a cobertura de plugins é parcial e os relatos variam no tempo. | zensical.org/compatibility | baixa: verificar cada plugin deste portal na página oficial |
| Há forks da comunidade (por exemplo ProperDocs e MaterialX) como alternativa com compatibilidade de plugins. | Buscas | baixa: não avaliados |

Dependências do portal que precisam funcionar em qualquer alternativa: `mkdocs-material` (tema), `mkdocs-awesome-nav` (menu por pasta, regra do padrão), `mkdocs-git-revision-date-localized-plugin` (data de cada página), `mkdocs-panzoom-plugin` (zoom nos diagramas), admonitions, `pymdownx.details`, Mermaid, e a validação `--strict` com âncoras.

## Opções

| Opção | Custo | Risco |
|---|---|---|
| **A. Ficar no MkDocs 1.x + Material atual** (como hoje) | nenhum agora | sem correções após o fim do suporte do Material (nov. 2026); o `<2` evita a quebra, mas a ferramenta fica parada |
| **B. Migrar para o Zensical** | médio: testar o portal de exemplo, cada plugin e o `--strict` | cobertura de plugins; ferramenta jovem |
| **C. Fork da comunidade** (ProperDocs, MaterialX) | baixo a médio | dependência de um mantenedor pequeno |
| **D. Outro gerador** (por exemplo Docusaurus) | alto: reescrever menu, avisos e validações; os geradores `gerar_paginas.py` e `extrair_etl.py` geram Markdown e Mermaid, que continuam valendo | abandona a regra do menu por pasta e o `--strict` atual |

Os geradores e as páginas são Markdown puro com admonitions e Mermaid. **O conteúdo não é o que prende a decisão; o prende é o tema e os plugins.**

## Critérios de decisão

1. O portal de exemplo compila com `--strict`, com validação de âncoras, na ferramenta nova?
2. Menu por pasta (`.nav.yml`), data de revisão, zoom em diagramas e aviso `pendente` funcionam sem remendo?
3. A ferramenta tem versão estável e mantenedores ativos nos últimos 6 meses?
4. Quanto custa migrar *e* quanto custa ficar parado (sem correção de segurança)?
5. O aviso de nov. 2026 já passou? Se sim, a opção A deixou de ser neutra.

## Roteiro de teste (meio dia)

1. Copie o portal de teste (modelos da skill + PBIP de exemplo + páginas geradas) para uma pasta temporária.
2. Instale a ferramenta candidata num ambiente isolado (`uv`), sem alterar o portal original.
3. Rode o build equivalente ao `mkdocs build --strict` e liste o que quebrou, plugin por plugin.
4. Preencha a tabela de critérios acima e registre a decisão em `docs/metodologia` do portal com data e commit.

Até lá: **manter `mkdocs>=1.6,<2`** (ver `padrao-mkdocs.md`) e não adotar recurso novo que dependa de plugin sem alternativa.
