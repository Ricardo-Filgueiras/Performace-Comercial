# 📊 Dashboard Performance Comercial - Visão Geral

**Última Atualização:** 30 de Janeiro de 2026  
**Versão:** 2.0  
**Status:** ✅ Modelo Otimizado e Documentado

---

## 📋 Índice

1. [Objetivo do Dashboard](#objetivo-do-dashboard)
2. [Arquitetura do Modelo](#arquitetura-do-modelo)
3. [Estrutura de Tabelas](#estrutura-de-tabelas)
4. [Métricas Principais](#métricas-principais)
5. [Atualizações Recentes](#atualizações-recentes)
6. [Convenções e Padrões](#convenções-e-padrões)

---

## 🎯 Objetivo do Dashboard

O Dashboard **Performance Comercial** foi desenvolvido para fornecer análises completas sobre o desempenho de vendas da empresa, permitindo:

### Análises Principais
- **Faturamento e Rentabilidade**: Acompanhamento de receitas, custos, margens e resultados
- **Gestão de Metas**: Monitoramento do atingimento de metas comerciais
- **Análises Temporais**: Comparações Year-over-Year (YoY) e Month-over-Month (MoM)
- **Performance por Dimensões**: Análise por produtos, clientes, vendedores e unidades
- **Positivação**: Cobertura de clientes e produtos

### Públicos-Alvo
- **Diretoria Comercial**: Visão estratégica de resultados
- **Gerência de Vendas**: Acompanhamento de metas e performance
- **Equipe Comercial**: Monitoramento individual e por território
- **Controladoria**: Análise de rentabilidade e custos

---

## 🏗️ Arquitetura do Modelo

### Tipo de Modelo
**Star Schema** (Esquema Estrela) com:
- **2 Tabelas Fato**: fVendas, fMetas
- **6 Tabelas Dimensão**: dCalendario, dClientes, dProdutos, dVendedores, dUnidades, dStatus, dPagamento
- **2 Tabelas de Medidas**: _Medidas (44 medidas), zMetricas (6 medidas)

### Características Técnicas
- **Compatibilidade**: Power BI Desktop (versão 2.146.1254.0)
- **Modo**: Import
- **Cultura**: pt-BR
- **Total de Medidas**: 50
- **Total de Relacionamentos**: 10

### Diagrama Simplificado
```
            ┌─────────────┐
            │ dCalendario │
            └──────┬──────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
   ┌────▼───┐ ┌───▼────┐     │
   │ fVendas│ │ fMetas │     │
   └───┬─┬─┬┘ └────┬───┘     │
       │ │ │       │         │
   ┌───▼ │ │   ┌───▼─────────▼──┐
   │dProd│ │   │  dVendedores   │
   └─────┘ │   └────────────────┘
       ┌───▼──────┐
       │dClientes │
       └──────────┘
```

---

## 📊 Estrutura de Tabelas

### Tabelas Fato

#### **fVendas** (Tabela Central)
- **Descrição**: Registra todas as transações de vendas
- **Granularidade**: Uma linha por item vendido
- **Colunas Principais**: 15 colunas
  - Datas: Data Pedido, Data Envio
  - IDs: Id Produto, Id Vendedor, Id Cliente, Id Unidade, Id Status, Id Pgto
  - Valores: Qtde, Valor Unit, Custo Unit, Despesa Unit, Impostos Unit, Comissão Unit
- **Relacionamentos**: 9 relacionamentos ativos + 1 inativo

#### **fMetas** (Metas Comerciais)
- **Descrição**: Armazena as metas de vendas por vendedor e período
- **Granularidade**: Uma linha por vendedor por data
- **Colunas Principais**: 3 colunas
  - Data, Id Vendedor, Valor Meta
- **Relacionamentos**: 2 relacionamentos

### Tabelas Dimensão

#### **dCalendario** (Dimensão Temporal)
- **Descrição**: Dimensão de datas para análises temporais
- **Colunas**: 13 colunas + 1 hierarquia
- **Atributos**: Ano, Mês, Dia, Semestre, Trimestre, Semana
- **Colunas Calculadas**: Datas com Venda, Semana dia Num, Semana dia Nome

#### **dClientes** (Dimensão Cliente)
- **Descrição**: Cadastro de clientes
- **Colunas**: 5 colunas
- **Atributos**: Id Cliente, Nome, Cidade, Estado, Região

#### **dProdutos** (Dimensão Produto)
- **Descrição**: Catálogo de produtos
- **Colunas**: 5 colunas
- **Atributos**: Id Produto, Nome, Categoria, Subcategoria, Marca

#### **dVendedores** (Dimensão Vendedor)
- **Descrição**: Cadastro de vendedores
- **Colunas**: 4 colunas
- **Atributos**: Id Vendedor, Nome, Região, Gerente

#### **dUnidades** (Dimensão Unidade)
- **Descrição**: Unidades de negócio/filiais
- **Colunas**: 2 colunas
- **Atributos**: Id Unidade, Nome Unidade

#### **dStatus** (Dimensão Status)
- **Descrição**: Status das vendas
- **Colunas**: 2 colunas
- **Valores**: 1=Efetivado, 2=Cancelado, etc.

#### **dPagamento** (Dimensão Forma de Pagamento)
- **Descrição**: Formas de pagamento
- **Colunas**: 2 colunas
- **Atributos**: Id Pagamento, Descrição

### Tabelas de Medidas

#### **_Medidas** (Medidas Principais)
- **Total**: 44 medidas DAX
- **Organização**: Por pastas de display
- **Categorias**: Principais, Temporais, Formatações, Visuais SVG

#### **zMetricas** (Métricas Auxiliares)
- **Total**: 6 medidas
- **Uso**: Métricas de suporte e cálculos intermediários

---

## 📈 Métricas Principais

### Categoria: Principais (01-13)
| # | Medida | Descrição | Formato |
|---|--------|-----------|---------|
| 01 | Faturamento | Receita bruta de vendas efetivadas | R$ |
| 02 | Custo | Custo total dos produtos vendidos | R$ |
| 03 | Lucro Bruto | Faturamento - Custo | R$ |
| 04 | Margem Bruta | (Lucro Bruto / Faturamento) × 100 | % |
| 05 | Despesa | Despesas operacionais | R$ |
| 06 | Impostos | Impostos sobre vendas | R$ |
| 07 | Comissao | Comissões pagas | R$ |
| 08 | Abatimento | Soma de Custo + Despesa + Impostos + Comissão | R$ |
| 09 | Resultado | Lucro líquido (Faturamento - Abatimento) | R$ |
| 10 | Margem | Margem líquida (Resultado / Faturamento) | % |
| 11 | Qtde Vendas | Quantidade total de transações | # |
| 12 | Positivação Clientes | Clientes únicos com compras | # |
| 13 | Positivação Produtos | Produtos únicos vendidos | # |

### Categoria: Temporais (20-35)
| # | Medida | Descrição | Tipo |
|---|--------|-----------|------|
| 20 | Faturamento Acumulado | Acumulado no ano | YTD |
| 21 | Faturamento Acumulado LY | Acumulado no ano anterior | YTD |
| 22 | Faturamento LY | Faturamento ano anterior | LY |
| 23 | Faturamento YoY % | Variação ano a ano | YoY |
| 24 | Faturamento MoM % | Variação mês a mês | MoM |
| 25-28 | Margem LM/LY/YoY/MoM | Comparações de margem | Temporal |
| 29-32 | Resultado LM/LY/YoY/MoM | Comparações de resultado | Temporal |
| 33-35 | Comissão LY/YoY/MoM | Comparações de comissão | Temporal |

### Categoria: Metas (40-42)
| # | Medida | Descrição | Uso |
|---|--------|-----------|-----|
| 40 | Meta | Meta de vendas do período | Baseline |
| 41 | Porcentagem Meta | % de atingimento da meta | KPI |
| 42 | Diferença Meta | Gap: Faturamento - Meta | Gap Analysis |

---

## 🔄 Atualizações Recentes

### Versão 2.0 - Janeiro 2026

#### ✅ Correções Implementadas
1. **Positivação Corrigida**: Adicionado filtro `Status = 1` nas medidas de positivação
2. **Margem Bruta Criada**: Nova medida conceitual correta (Faturamento - Custo) / Faturamento
3. **Lucro Bruto Criado**: Valor absoluto da margem bruta
4. **Tratamento de Erros**: Todas as divisões agora retornam `BLANK()` em caso de erro
5. **Otimização com Variáveis**: Uso de VAR para melhor performance e legibilidade
6. **Numeração de Medidas**: Sistema de numeração para melhor organização

#### 🎯 Melhorias de Performance
- Redução de recálculos através de variáveis DAX
- Otimização de medidas temporais
- Documentação inline em todas as medidas

#### 📚 Documentação Criada
- Visão Geral do Modelo
- Dicionário de Dados completo
- Guia de Medidas DAX
- Convenções e Padrões

---

## 📐 Convenções e Padrões

### Nomenclatura de Medidas

#### Prefixos Numéricos
- **01-19**: Medidas principais de negócio
- **20-39**: Comparações temporais (LY, LM, YoY, MoM)
- **40-49**: Medidas relacionadas a metas
- **50-59**: Medidas auxiliares/formatação
- **60-79**: Medidas para visuais (SVG, HTML)
- **80-89**: Medidas de ranking/ordenação
- **90-99**: Medidas de teste/desenvolvimento

#### Sufixos Temporais
- **LY**: Last Year (Ano Anterior)
- **LM**: Last Month (Mês Anterior)
- **YoY**: Year over Year (Variação Anual)
- **MoM**: Month over Month (Variação Mensal)
- **YTD**: Year to Date (Acumulado no Ano)

### Nomenclatura de Tabelas

#### Prefixos
- **f**: Tabelas Fato (fact) - Ex: fVendas, fMetas
- **d**: Tabelas Dimensão (dimension) - Ex: dClientes, dProdutos
- **_**: Tabelas de Medidas - Ex: _Medidas
- **z**: Tabelas Auxiliares - Ex: zMetricas

### Padrões DAX

#### Divisões
```dax
// ✅ CORRETO - Com tratamento de erro
DIVIDE([Numerador], [Denominador], BLANK())

// ❌ INCORRETO - Sem tratamento
[Numerador] / [Denominador]
```

#### Variáveis
```dax
// ✅ CORRETO - Uso de variáveis
VAR ValorAtual = [Medida]
VAR ValorAnterior = [Medida LY]
RETURN DIVIDE(ValorAtual - ValorAnterior, ValorAnterior, BLANK())

// ❌ MENOS EFICIENTE - Sem variáveis
DIVIDE([Medida] - [Medida LY], [Medida LY], BLANK())
```

#### Filtros
```dax
// ✅ CORRETO - Filtro explícito
CALCULATE([Medida], dStatus[Id Status] = 1)

// ❌ PERIGOSO - Sem filtro de status
[Medida]
```

---

## 📞 Suporte e Manutenção

### Contatos
- **Desenvolvedor**: Campeão Distribuição e Logística Ltda
- **Localização**: GitHub/Performace-Comercial

### Estrutura de Arquivos
```
/documents/
├── 01-VISAO-GERAL.md (este arquivo)
├── 02-DICIONARIO-DADOS.md
├── 03-GUIA-MEDIDAS-DAX.md
├── 04-RELACIONAMENTOS.md
├── 05-CHANGELOG.md
└── 06-BOAS-PRATICAS.md
```

### Versionamento
- **Major**: Mudanças estruturais significativas (ex: 1.0 → 2.0)
- **Minor**: Novas funcionalidades/medidas (ex: 2.0 → 2.1)
- **Patch**: Correções e ajustes (ex: 2.1 → 2.1.1)

---

## 🚀 Próximas Melhorias Planejadas

### Fase 2 - Métricas Essenciais (Planejado)
- [ ] Ticket Médio e variações
- [ ] Produtividade por vendedor
- [ ] Mix de produtos (ABC)
- [ ] Métricas avançadas de meta (Projeção, Run Rate)

### Fase 3 - Análises Avançadas (Futuro)
- [ ] Análise RFM de clientes
- [ ] Segmentação ABC automática
- [ ] Projeções e forecasting
- [ ] Análise de churn de clientes

---

**Documento criado em:** 30/01/2026  
**Autor:** Assistente de Modelagem Power BI  
**Versão do Documento:** 1.0
