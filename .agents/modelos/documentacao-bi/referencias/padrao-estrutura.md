<!-- Parte do padrão. Índice em padrao.md. -->
# 1. Estrutura do portal

```
<portal>/
├── README.md                 ← como instalar e rodar o portal (não é sobre negócio)
├── mkdocs.yml                ← único: tema, plugins, validação
├── pyproject.toml / uv.lock  ← dependências Python do site
├── .gitignore
├── .claude/skills/documentacao-bi/   ← cópia local da skill (opcional; com o plugin instalado não existe)
├── .agents/                  ← arquivos de trabalho, versionados (notas, relatórios de teste)
├── docs/
│   ├── .nav.yml              ← menu de topo do portal
│   ├── index.md              ← entrada: "Quero usar um painel" / "Quero manter um painel"
│   ├── metodologia/          ← dataops.md, versionamento-git.md (uma cópia só)
│   ├── changelog.md          ← changelog do portal
│   ├── stylesheets/extra.css ← aviso "pendente" (cor de alerta padrão do Material)
│   ├── assets/               ← imagens comuns (só se houver)
│   └── projetos/<slug>/      ← documentação de um projeto
│       ├── .nav.yml          ← menu do projeto
│       └── ...               ← páginas (seção 3)
└── src/<slug>/               ← só os arquivos do Power BI
    ├── <Projeto>.pbip
    ├── <Projeto>.SemanticModel/
    └── <Projeto>.Report/
```

| Regra | Por quê |
|---|---|
| **Um portal para todos os projetos.** | Ao pesquisar uma medida, o usuário precisa achar em quais projetos ela é usada, qual é a regra e o que mudou. Com um site por painel, um é atualizado e outro não, e os usuários veem versões divergentes. |
| **A documentação fica em `docs/projetos/<slug>/`; o Power BI fica em `src/<slug>/`.** | O site lê só `docs/`. O Power BI fica separado do conteúdo do site, e cada projeto tem uma pasta previsível nos dois lados. |
| **O mesmo `<slug>` nos dois lados.** | O nome da pasta é o que liga a documentação aos arquivos do Power BI. Nomes diferentes obrigam a manter uma tabela de correspondência. O slug é escolhido pelo usuário, em minúsculas e com hífens, e não muda se o nome do `.pbip` mudar. |
| **Uma pasta em `src/` só quando o projeto existe.** | Pastas vazias não são versionadas pelo Git e não dizem nada a quem lê. |
| **Metodologia e glossário uma vez só, na raiz.** | Copiados em cada projeto, divergem na primeira correção. |
| **Menu de cada projeto no próprio `.nav.yml`** (plugin `mkdocs-awesome-nav`). | Um menu central com todos os projetos vira centenas de entradas, gera conflito no Git e faz páginas esquecidas sumirem do site. |
| **Repositório num caminho curto, fora do OneDrive** (por exemplo `C:\repos\`). | No laboratório, com o repositório no OneDrive, 394 arquivos do Power BI passaram do limite de 260 caracteres do Windows. O OneDrive sincronizando a pasta `.git` também pode corromper o histórico. |
| **Scripts Python ficam onde o projeto já os tem** (qualquer pasta do repositório). | O gerador de ETL recebe a pasta por parâmetro; impor um lugar obriga a mover scripts que já rodam em produção. |
