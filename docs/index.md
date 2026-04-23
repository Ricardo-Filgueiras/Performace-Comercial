# Performance Comercial

Documentação técnica do modelo semântico Power BI do projeto **Performance Comercial**.

O modelo analisa resultados de vendas, margens, metas e comissões — permitindo acompanhamento detalhado por vendedor, produto, cliente, unidade e período.

---

## Sobre o Projeto

O relatório é construído sobre uma arquitetura **Star Schema** com 2 tabelas fato, 7 dimensões e 50 medidas DAX organizadas por categoria. Os dados são originados de planilhas Excel e processados via Power Query diretamente no Power BI Desktop.

O projeto é versionado com **Git** no formato `.pbip`, o que permite rastreabilidade completa de mudanças no modelo semântico.

---

## Navegação Rápida

| Dúvida | Onde encontrar |
|--------|---------------|
| Como o modelo está estruturado? | [Visão Geral](01 visao geral.md) |
| O que significa cada coluna e tabela? | [Dicionário de Dados](02 dicionario dados.md) |
| Como funciona determinada medida DAX? | [Guia de Medidas DAX](03 guia medidas dax.md) |
| Como as tabelas se relacionam? | [Relacionamentos](04 relacionamentos.md) |
| O que mudou no modelo recentemente? | [Changelog](05 changelog.md) |
| Como desenvolver e manter o projeto? | [Boas Práticas](06 boas praticas.md) |

---

## Resumo do Modelo

| Item | Quantidade |
|------|-----------|
| Tabelas Fato | 2 (`fVendas`, `fMetas`) |
| Tabelas Dimensão | 7 |
| Medidas DAX | 50 |
| Relacionamentos | 10 (9 ativos, 1 inativo) |

---

!!! tip "Primeiro acesso?"
    Comece pela [Visão Geral](01 visao geral.md) para entender a arquitetura do modelo, depois consulte o [Dicionário de Dados](02 dicionario dados.md) para entender o significado de cada campo.
