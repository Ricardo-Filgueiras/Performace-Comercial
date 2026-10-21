# Performance Comercial

Projeto de análise de performance comercial desenvolvido em Power BI (formato `.pbip`), versionado com Git e documentado com MkDocs. **[Veja a documentação publicada](https://ricardo-filgueiras.github.io/Performace-Comercial/)** e como ela foi construída.

---

## Descrição

Dashboard de Business Intelligence para acompanhamento de KPIs comerciais: faturamento, resultado, margem, metas, positivação de clientes e produtos, análises temporais (YoY, MoM, YTD) e performance por vendedor, produto, cidade e unidade.

O modelo semântico segue arquitetura **Star Schema** com medidas DAX organizadas por categoria e documentação técnica completa publicada via MkDocs Material.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Relatório e modelo semântico | Power BI (formato PBIP) |
| Documentação | MkDocs Material |
| Gerenciador de pacotes Python | uv |
| Versionamento | Git / GitHub |
| Publicação da documentação | `mkdocs gh-deploy`, manual (a automação com GitHub Actions ainda não existe) |

---

## Estrutura de pastas

```
Performace-Comercial/
├── data/                          # Dados do painel (planilhas Excel)
│   ├── Dimensões/
│   ├── Extrações/
│   ├── Metas/
│   └── imagens/
├── docs/                          # Fonte da documentação MkDocs
│   ├── index.md                   # Entrada do portal
│   ├── changelog.md               # Changelog do portal
│   ├── metodologia/               # DataOps e versionamento com Git
│   ├── stylesheets/
│   └── projetos/
│       └── performance-comercial/ # Documentação do projeto
├── src/
│   └── projeto/
│       └── performance-comercial/ # Arquivos Power BI (PBIP)
│           ├── Performance Comercial.pbip
│           ├── Performance Comercial.Report/
│           └── Performance Comercial.SemanticModel/
├── notas/                         # Diário da reescrita da documentação (fora do Git)
├── .agents/                       # Kit e skill de documentação de BI
├── mkdocs.yml                     # Configuração do MkDocs
├── pyproject.toml                 # Dependências Python (uv)
├── uv.lock
└── README.md
```

---

## Documentação

### Ver a documentação publicada

A documentação do projeto está no ar, publicada com GitHub Pages: **https://ricardo-filgueiras.github.io/Performace-Comercial/**

Ela foi escrita a partir dos arquivos do modelo e do relatório, conferida com um script de levantamento e validada com `mkdocs build --strict`. Para ver como ela é construída e mantida:

| Quero ver | Página |
|---|---|
| O que o painel resolve e para quem | [Escopo](https://ricardo-filgueiras.github.io/Performace-Comercial/projetos/performance-comercial/escopo/) |
| Cada guia do relatório | [Guias do relatório](https://ricardo-filgueiras.github.io/Performace-Comercial/projetos/performance-comercial/guias-do-relatorio/) |
| O código e as dependências das 50 medidas | [Medidas DAX](https://ricardo-filgueiras.github.io/Performace-Comercial/projetos/performance-comercial/medidas-dax/) |
| Por que o projeto é como é | [Decisões técnicas](https://ricardo-filgueiras.github.io/Performace-Comercial/projetos/performance-comercial/decisoes-tecnicas/) |
| Como trabalhar no projeto e na documentação | [Guia do desenvolvedor](https://ricardo-filgueiras.github.io/Performace-Comercial/projetos/performance-comercial/guia-do-desenvolvedor/) |
| A visão geral da documentação | [Sobre esta documentação](https://ricardo-filgueiras.github.io/Performace-Comercial/projetos/performance-comercial/readme/) |

### Rodar localmente

Requer [uv](https://docs.astral.sh/uv/) instalado.

```bash
uv run mkdocs serve
```

Acesse em `http://127.0.0.1:8000`.

### Publicar no GitHub Pages

```bash
uv run mkdocs gh-deploy
```

O comando faz o build e faz push do conteúdo estático para a branch `gh-pages` automaticamente.

---

## Como usar o projeto Power BI

1. Clone o repositório:
   ```bash
   git clone https://github.com/Ricardo-Filgueiras/Performace-Comercial.git
   ```
2. Abra o arquivo `src/projeto/performance-comercial/Performance Comercial.pbip` no **Power BI Desktop** (versão 2.146+).
3. Atualize o valor dos três parâmetros de caminho (`Caminho_Extracao`, `Caminho_Dimensoes` e `Caminho_Meta`) para a pasta `data/` da sua cópia. O passo a passo está em [Como atualizar o valor dos parâmetros](docs/projetos/performance-comercial/fontes-de-dados.md#como-atualizar-o-valor-dos-parametros).

---

## Autor

**Ricardo Filgueiras**
- LinkedIn: [ricardo-filgueiras-b4607b232](https://www.linkedin.com/in/ricardo-filgueiras-b4607b232/)
- Dashboard publicado: [Power BI Service](https://app.powerbi.com/view?r=eyJrIjoiNjRlNmRhYzktODY2Yy00MTI2LWIyYTYtMDczNTFjNTkyZDMzIiwidCI6ImVhNmIyNzRlLTE4MmYtNDc0Yy04YWMwLTQzOWM5ZTE1Yjg3ZSJ9)

---

## Licença

MIT — veja o arquivo [LICENSE](LICENSE) para detalhes.
