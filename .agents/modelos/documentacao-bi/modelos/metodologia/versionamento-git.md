# Versionamento com Git

O Git é a ferramenta de versionamento do portal. Os projetos Power BI (PBIP) e a documentação deles vivem no mesmo repositório e no mesmo histórico. É isso que torna a documentação *documentation-as-code*: uma mudança no modelo e a atualização da página que a descreve podem ir no mesmo pull request.

## Onde fica cada coisa

| Caminho | O que é |
|---|---|
| `src/<slug>/` | Arquivos do Power BI de um projeto |
| `docs/projetos/<slug>/` | Documentação desse projeto |

O `<slug>` é o mesmo nos dois lugares.

## Linha de base

Antes de documentar um projeto, o estado dele é commitado e marcado com uma tag anotada com o prefixo do projeto:

```bash
git tag -a <slug>/baseline-pre-documentacao -m "<Projeto> antes da documentação"
git log -1 --format="%h %ad" --date=short
```

A foto desse estado (tabelas, medidas, guias e indicadores) fica em `.agents/linha-de-base-<slug>.md`, fora do site.

Enquanto valer a regra de não alterar o modelo na documentação inicial, a pasta `src/<slug>/` precisa ficar igual à da tag.

## Comparar o antes com o depois

```bash
# tudo o que mudou desde a foto, reconhecendo arquivos que mudaram de lugar
git diff -M --stat <slug>/baseline-pre-documentacao

# só o Power BI do projeto: precisa voltar vazio enquanto o modelo não for alterado
git diff -M --stat <slug>/baseline-pre-documentacao -- src/<slug>

# mudanças ainda não commitadas no Power BI do projeto
git status --porcelain -- src/<slug>

# refazer as contagens do projeto
PYTHONUTF8=1 python <pasta-da-skill>/scripts/levantamento.py --root src/<slug>
```

## Fluxo de trabalho

1. Crie uma branch para a mudança.
2. Faça a mudança. Quando um agente de IA escreve a documentação, ele deixa tudo no working tree, sem commit.
3. Revise linha a linha o que mudou.
4. Faça os commits e abra o pull request com o checklist preenchido.
5. Outra pessoa do time de BI revisa e aprova. Nada entra direto na `main`.

## Mudar um projeto de lugar

Mover os arquivos do Power BI (por exemplo, da raiz para `src/<slug>/`) é **um commit só para isso**: a remoção e a adição juntas, sem nenhuma alteração de conteúdo. Assim o Git reconhece a renomeação e o histórico de cada arquivo continua acessível com `git log --follow`.

## Convenção de commits

Mensagens no formato `tipo: descrição curta`, em português:

| Tipo | Quando usar | Exemplo |
|---|---|---|
| `feat` | nova medida, tabela, guia ou visual | `feat: medida de variação anual` |
| `fix` | correção de cálculo ou de visual | `fix: filtro de data no visual de resumo` |
| `docs` | só documentação | `docs: regras de cálculo da margem` |
| `refactor` | reorganização sem mudar resultado (pastas de exibição, `///`, mudança de lugar) | `refactor: move o projeto para src/<slug>` |
| `chore` | configuração, dependências, `.gitignore` | `chore: plugin de menu por pasta` |

Separe em commits diferentes a mudança no modelo e a mudança só de documentação quando elas não dependem uma da outra.

## Tags de versão

Cada versão do changelog de um projeto recebe uma tag com o prefixo do projeto (`<slug>/v1.0.0`). Mudanças do portal inteiro usam `portal/v1.0.0`. Comparação entre versões: `git diff <slug>/v1.0.0 <slug>/v1.1.0`.

## O que depende do Git

- **Data e commit das decisões técnicas:** cada decisão registra o hash do commit (`git log -1 --format="%h %ad" --date=short`).
- **Datas das páginas:** o plugin `git-revision-date-localized` lê o `git log`. Ele precisa do clone com histórico completo (em CI, `fetch-depth: 0`). Páginas ainda não commitadas mostram a data do build.
- **Comparação entre versões:** pelas tags.

## O que não entra no repositório

`.pbi/localSettings.json` e `.pbi/cache.abf` (configurações locais e cache do Power BI Desktop), arquivos `.pbix`, `.venv/`, `site/` e `__pycache__/`. Todos estão no `.gitignore`.
