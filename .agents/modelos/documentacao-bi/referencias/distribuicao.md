# Distribuição, versão e atualização da skill

A skill é distribuída como **plugin do Claude Code**. Esta página explica como instalar, como lançar uma versão nova, como os portais antigos recebem as mudanças e por que a escolha foi plugin e não `copier`. Fatos sobre o formato de plugin foram conferidos na documentação do Claude Code (code.claude.com/docs/en/plugins) em 2026-10-23 e com `claude plugin validate` na versão 2.1.247 do CLI; confira de novo se a versão do CLI for bem diferente.

## O que há no kit

```
<kit>/                              ← publique esta pasta como repositório Git
├── .claude-plugin/
│   ├── plugin.json                 ← nome, descrição e a ÚNICA fonte da versão
│   └── marketplace.json            ← lista o plugin (source "./", sem version)
└── documentacao-bi/                ← a skill (SKILL.md, referencias/, modelos/, scripts/)
```

`plugin.json` aponta a skill com `"skills": ["./documentacao-bi"]`, então não houve cópia nem mudança de pastas. A skill aparece como `/documentacao-bi:documentacao-bi`.

## Instalar

```bash
claude plugin marketplace add <dono>/<repositorio>
claude plugin install documentacao-bi@bi-documentacao --scope project
```

- `--scope project` grava a ativação em `.claude/settings.json` do portal; versionada no Git, vale para quem clonar. **Cada pessoa ainda precisa rodar o `install`** na sua máquina: o commit não baixa o plugin.
- `--scope user` vale para todos os projetos da pessoa.
- Testar sem publicar: `claude --plugin-dir <kit>`.

## Atualizar

| Quem | Como |
|---|---|
| Qualquer pessoa | `claude plugin marketplace update` e depois `claude plugin update documentacao-bi@bi-documentacao` (ou a aba *Installed* do `/plugin`). A sessão aberta só usa a versão nova depois de `/reload-plugins` ou numa sessão nova. |
| O time | A atualização automática vem **desligada** para marketplaces de terceiros ou locais; cada pessoa liga em `/plugin` > *Marketplaces* > *Enable auto-update*, ou atualiza à mão. |

**Regra mais importante: o plugin só atualiza se o campo `version` do `plugin.json` mudar.** Commits novos com a mesma versão não chegam a ninguém. Por isso a versão vive em um lugar só (`plugin.json`; a entrada do marketplace não tem `version`) e o teste `scripts/tests/test_plugin.py` confere que ela é igual no `SKILL.md`, no `CHANGELOG.md`, no `README.md` e no relatório de teste.

## Lançar uma versão nova (checklist)

1. Escolha o número: correção sem mudar o comportamento = patch; recurso novo = minor; mudança que exige ação dos usuários = major.
2. Atualize **todos** os lugares: `plugin.json`, `SKILL.md` ("Versão da skill"), primeira entrada do `CHANGELOG.md`, `README.md` ("versão X") e `referencias/relatorio-de-teste.md`.
3. Rode os testes: `PYTHONUTF8=1 python -m unittest discover -s documentacao-bi/scripts/tests`.
4. Valide o empacotamento: `claude plugin validate <kit>` (e `--strict`).
5. Teste a skill de verdade: `claude --plugin-dir <kit>` num portal de teste.
6. Faça o commit e a tag `v<versão>` no repositório do kit.
7. Avise o time: `claude plugin marketplace update` e `claude plugin update documentacao-bi@bi-documentacao`.

## Atualizar os portais que já existem

Atualizar o plugin muda a skill (instruções, scripts e modelos), mas **não muda os arquivos que já foram copiados para o portal** (`mkdocs.yml`, `pyproject.toml`, CSS, metodologia). Para ver o que mudou:

```bash
python <pasta-da-skill>/scripts/comparar_portal.py --portal .
```

Ele só lê: lista cada arquivo como *igual*, *diferente* (com o diff) ou *ausente*. Diferenças de nome do site e de menu são normais. Leve para o portal só o que fizer sentido, num commit próprio. Depois, nas páginas geradas, rode os geradores sem `--check`: o texto escrito à mão é preservado.

## Por que plugin e não `copier`

| | Plugin | `copier` |
|---|---|---|
| Distribui instruções do agente, scripts e modelos | sim | não é o foco |
| Versão e atualização | nativas (`version`) | `copier update` com histórico |
| Atualiza arquivos já copiados para o portal | não (usa `comparar_portal.py`) | sim, com mesclagem de conflitos |
| Dependência extra | nenhuma além do Claude Code | instalar e aprender o `copier` |

O ponto fraco do plugin (arquivos já copiados) é pequeno hoje: poucos arquivos, e o `comparar_portal.py` mostra o que mudou. **Reavalie o `copier`** quando houver mais de uns 3 portais ou quando a mesclagem manual dos arquivos copiados começar a dar trabalho. Nesse caso, o `copier` entraria só para a raiz do portal (`modelos/portal/` e `modelos/metodologia/`); a skill continuaria sendo o plugin.

## Cuidados

- Nunca grave caminho fixo da skill (`.claude/skills/...`) nos comandos: com o plugin ela fica num cache e o caminho muda a cada versão. O `SKILL.md` usa `${CLAUDE_SKILL_DIR}`, que o Claude Code resolve ao carregar a skill; os arquivos de `referencias/` usam `<pasta-da-skill>`, e o agente usa a pasta que o `SKILL.md` mostra. O teste de empacotamento proíbe o caminho fixo.
- O plugin carrega o conteúdo do kit inteiro. Não ponha no kit nome de projeto, dado de negócio, credencial nem caminho de usuário. O teste de higiene confere termos proibidos por hash; para incluir um termo novo: `python documentacao-bi/scripts/tests/test_plugin.py --hash "termo"` e acrescente a linha a `termos_proibidos.sha256`.
