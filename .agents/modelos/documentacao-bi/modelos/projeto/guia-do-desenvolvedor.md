# Guia do desenvolvedor

Convenções práticas para trabalhar no painel e na documentação. Para instalar e rodar o site, veja o `README.md` na raiz do repositório.

## Onde está cada coisa

| Quero mexer em… | Arquivo |
|---|---|
| Uma medida ou coluna | `src/<slug>/<Projeto>.SemanticModel/definition/tables/<Tabela>.tmdl` |
| Um relacionamento | `src/<slug>/<Projeto>.SemanticModel/definition/relationships.tmdl` |
| Uma consulta compartilhada ou parâmetro | `src/<slug>/<Projeto>.SemanticModel/definition/expressions.tmdl` |
| Uma guia do relatório | `src/<slug>/<Projeto>.Report/definition/pages/<id>/page.json` |
| A ordem das guias | `src/<slug>/<Projeto>.Report/definition/pages/pages.json` |
| Um visual | `src/<slug>/<Projeto>.Report/definition/pages/<id>/visuals/<id>/visual.json` |
| A documentação deste projeto | `docs/projetos/<slug>/` |

Prefira editar pelo Power BI Desktop e salvar. Editar o TMDL à mão funciona, mas confira no Desktop antes de commitar.

## Regras para o modelo

- **Nenhuma medida fica sem pasta de exibição ao final de uma tarefa.** Antes do commit, toda medida nova ou alterada está numa pasta.
- **Não renomeie pastas de exibição nem guias sem necessidade.** Renomear quebra o vínculo com a documentação sem avisar. Se precisar reorganizar, crie uma pasta nova, mova as medidas e registre no changelog.
- **Documente a medida no próprio modelo:**

    ```tmdl
    /// Valor líquido das vendas do período (soma de ValorLiquido).
    measure ValorLiquido =
            /* Base: fFato[ValorLiquido]. Não exclui devoluções. */
            SUM(fFato[ValorLiquido])
    ```

    `///` vira a descrição exibida no Power BI; `/* */` na primeira linha aparece na barra de fórmulas.

## Nomes

<!-- Prefixos e convenções de nome usados no modelo, com exemplos. -->

## Ao alterar o painel

1. Faça a mudança no Power BI Desktop e salve o PBIP.
2. Confira o diff só nas pastas que você esperava mudar.
3. Atualize a página afetada: medida → [Medidas DAX](medidas-dax/index.md) (incluindo "depende de" e "é usada por"); tabela ou relacionamento → [Modelo de dados](modelo-de-dados.md); guia → página da guia.
4. Decisão de arquitetura → [Decisões técnicas](decisoes-tecnicas.md), com data e commit.
5. Anote no [Changelog](changelog.md), em `[Não publicado]`, citando as medidas pelo nome.
6. Rode `uv run mkdocs build --strict`.
7. Abra o pull request com o checklist.

## Checklist do pull request

- [ ] `uv run mkdocs build --strict` passou sem avisos.
- [ ] O diff do Power BI mexe só nas pastas esperadas.
- [ ] O changelog foi atualizado, citando as medidas pelo nome.
- [ ] As páginas das medidas alteradas têm "depende de" e "é usada por" atualizados.
- [ ] Toda página nova está no `.nav.yml` do projeto.
- [ ] Se uma regra de negócio mudou, a validação de negócio foi pedida.
- [ ] O que o agente escreveu foi revisado linha a linha.
