# Educação dos mantenedores

Quem vai manter a documentação precisa aprender o processo, tanto num projeto novo quanto num existente. Você, o agente, ensina **enquanto trabalha**: ao fim de cada etapa, explique em poucas linhas o que o usuário precisa saber para repetir aquilo sem você.

## Como ensinar

- **Explique o porquê, não só o como.** Cada regra do `padrao.md` tem um motivo; use-o.
- **Uma coisa por vez.** Ao fim de uma etapa, ensine só o que ela exigiu.
- **Mostre o comando e o resultado esperado.** Por exemplo: "rode `uv run mkdocs build --strict`; se terminar sem aviso, está pronto".
- **Confirme o entendimento** com uma pergunta curta quando o assunto for novo para o usuário.
- **Registre** no relatório de teste o que foi ensinado e o que gerou dúvida.

## O que um mantenedor precisa saber

| Tema | O que saber | Quando ensinar |
|---|---|---|
| Estrutura do portal | Onde fica cada coisa: `docs/projetos/<slug>/`, `src/<slug>/`, metodologia, `.nav.yml`. | Primeira sessão. |
| Rodar o site | `uv sync`, `uv run mkdocs serve` (ver no navegador), `uv run mkdocs build --strict` (conferir antes de entregar). | Primeira sessão. |
| Tipos de página | Para quem usa × para quem mantém × arquivo; o que vai em cada página. | Ao criar as páginas. |
| Pendências | Como escrever um `!!! pendente`, por que ele vai também para `pendencias.md`, como fechar uma pendência. | Ao criar a primeira pendência. |
| Revisar o que o agente escreveu | Conferir linha a linha contra o modelo; desconfiar de números e de regras sem fonte; o script confere contagens e dependências. | Antes do primeiro pull request. |
| Changelog | Registrar atividade, citar as medidas pelo nome, usar `[Não publicado]` até a versão sair. | Ao fim da primeira etapa com mudanças. |
| Git e pull request | Branch, commit no formato `tipo: descrição`, abrir o PR, usar o checklist. Mudança de lugar sempre num commit separado. | Antes do primeiro pull request. |
| Validação de negócio | O negócio valida a regra e um exemplo, nunca o DAX; onde registrar a validação. | No nível 2. |
| Alterar o modelo | Regra das pastas de exibição; `///` e `/* */`; atualizar a página da medida e o changelog no mesmo PR. | Quando o usuário for alterar o modelo. |

## Sinal de mantenedor pronto

O mantenedor consegue, sem ajuda:

- [ ] Rodar o site localmente e entender um erro do `--strict`.
- [ ] Criar uma página nova e colocá-la no menu certo.
- [ ] Escrever e fechar uma pendência.
- [ ] Revisar uma página escrita pelo agente e apontar o que está errado.
- [ ] Abrir um pull request com o checklist preenchido.
