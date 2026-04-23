# Performance Comercial

Projeto de análise de performance comercial desenvolvido em Power BI (formato `.pbip`), versionado com Git e documentado com MkDocs.

---

## Descrição

Dashboard de Business Intelligence para acompanhamento de KPIs comerciais: faturamento, resultado, margem, metas, positivação de clientes e produtos, análises temporais (YoY, MoM, YTD) e performance por vendedor, produto e região.

O modelo semântico segue arquitetura **Star Schema** com medidas DAX organizadas por categoria e documentação técnica completa publicada via MkDocs Material.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Relatório e modelo semântico | Power BI (formato PBIP) |
| Documentação | MkDocs Material |
| Gerenciador de pacotes Python | uv |
| Versionamento | Git / GitHub |
| CI/CD docs | GitHub Actions |

---

## Estrutura de pastas

```
Performace-Comercial/
├── docs/                          # Fonte da documentação MkDocs
│   ├── index.md
│   ├── 01 visao geral.md
│   ├── 02 dicionario dados.md
│   ├── 03 guia medidas dax.md
│   ├── 04 relacionamentos.md
│   ├── 05 changelog.md
│   ├── 06 boas praticas.md
│   ├── estrutura_definition_legivel.md
│   └── requisitos.md
├── src/
│   ├── data/                      # Fontes de dados (Excel/CSV)
│   │   ├── Dimensões/
│   │   ├── Extrações/
│   │   ├── Metas/
│   │   └── imagens/
│   └── projeto/                   # Arquivos Power BI (PBIP)
│       ├── Performace Comercial.pbip
│       ├── Performace Comercial.Report/
│       └── Performace Comercial.SemanticModel/
├── .github/workflows/docs.yml     # CI/CD publicação da documentação
├── mkdocs.yml                     # Configuração do MkDocs
├── pyproject.toml                 # Dependências Python (uv)
├── uv.lock
└── README.md
```

---

## Documentação

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
   git clone https://github.com/RicardoFilgueiras/Performace-Comercial.git
   ```
2. Abra o arquivo `src/projeto/Performace Comercial.pbip` no **Power BI Desktop** (versão 2.146+).
3. Se necessário, remapeie o caminho das fontes de dados em `src/data/`.

---

## Autor

**Ricardo Filgueiras**
- LinkedIn: [ricardo-filgueiras-b4607b232](https://www.linkedin.com/in/ricardo-filgueiras-b4607b232/)
- Dashboard publicado: [Power BI Service](https://app.powerbi.com/view?r=eyJrIjoiNjRlNmRhYzktODY2Yy00MTI2LWIyYTYtMDczNTFjNTkyZDMzIiwidCI6ImVhNmIyNzRlLTE4MmYtNDc0Yy04YWMwLTQzOWM5ZTE1Yjg3ZSJ9)

---

## Licença

MIT — veja o arquivo [LICENSE](LICENSE) para detalhes.
