# 📖 Dicionário de Dados - Performance Comercial

**Versão:** 2.0  
**Última Atualização:** 30 de Janeiro de 2026

---

## 📋 Índice

1. [Tabelas Fato](#tabelas-fato)
2. [Tabelas Dimensão](#tabelas-dimensão)
3. [Tabelas de Medidas](#tabelas-de-medidas)
4. [Relacionamentos](#relacionamentos)
5. [Glossário de Termos](#glossário-de-termos)

---

## 📊 Tabelas Fato

### fVendas

**Descrição**: Tabela central do modelo contendo todas as transações de vendas.

**Granularidade**: Uma linha por item vendido em cada pedido.

**Total de Colunas**: 15

#### Colunas

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| **Data Pedido** | DateTime | Data em que o pedido foi realizado | 2025-01-15 |
| **Data Envio** | DateTime | Data de envio do pedido | 2025-01-17 |
| **Num Venda** | String | Número único do pedido | VND-2025-00123 |
| **Id Produto** | Int64 | Chave estrangeira para dProdutos | 1001 |
| **Id Vendedor** | Int64 | Chave estrangeira para dVendedores | 5 |
| **Id Cliente** | Int64 | Chave estrangeira para dClientes | 2034 |
| **Id Unidade** | Int64 | Chave estrangeira para dUnidades | 3 |
| **Id Status** | Int64 | Chave estrangeira para dStatus (1=Efetivado) | 1 |
| **Id Pgto** | Int64 | Chave estrangeira para dPagamento | 2 |
| **Qtde** | Int64 | Quantidade vendida | 10 |
| **Valor Unit** | Double | Valor unitário de venda | 150.00 |
| **Custo Unit** | Double | Custo unitário do produto | 90.00 |
| **Despesa Unit** | Int64 | Despesa unitária (frete, logística) | 5 |
| **Impostos Unit** | Double | Impostos por unidade | 22.50 |
| **Comissão Unit** | Double | Comissão por unidade | 7.50 |

#### Relacionamentos
- → dCalendario (Data Pedido → Id Data) - ATIVO
- → dCalendario (Data Envio → Id Data) - INATIVO
- → dProdutos (Id Produto → Id Produto) - ATIVO
- → dVendedores (Id Vendedor → Id Vendedor) - ATIVO
- → dClientes (Id Cliente → Id Cliente) - ATIVO
- → dUnidades (Id Unidade → Id Unidade) - ATIVO
- → dStatus (Id Status → Id Status) - ATIVO
- → dPagamento (Id Pgto → Id Pagamento) - ATIVO

#### Observações
- O campo **Data Pedido** é a data principal usada nos relacionamentos ativos
- **Data Envio** tem relacionamento inativo para análises alternativas
- **Status = 1** indica vendas efetivadas (usado em filtros de medidas)
- Valores unitários permitem cálculos flexíveis de totais

---

### fMetas

**Descrição**: Armazena as metas de vendas por vendedor e período.

**Granularidade**: Uma linha por vendedor por data.

**Total de Colunas**: 3

#### Colunas

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| **data** | DateTime | Data de referência da meta | 2025-01-01 |
| **Id Vendedor** | Int64 | Chave estrangeira para dVendedores | 5 |
| **Meta** | Double | Valor da meta para o período | 50000.00 |

#### Relacionamentos
- → dCalendario (data → Id Data) - ATIVO
- → dVendedores (Id Vendedor → Id Vendedor) - ATIVO

#### Observações
- Geralmente configurado mensalmente
- Pode ser agregado para análises trimestrais/anuais
- Usado nas medidas 40-42 (Meta, Porcentagem Meta, Diferença Meta)

---

## 🗂️ Tabelas Dimensão

### dCalendario

**Descrição**: Dimensão temporal completa com atributos de data.

**Tipo**: Dimensão Role-Playing (usada por múltiplas colunas de data)

**Total de Colunas**: 13 + 3 calculadas

#### Colunas Físicas

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| **Id Data** | DateTime | Chave primária - data única | 2025-01-15 |
| **Ano** | Int64 | Ano | 2025 |
| **Nome do Mês** | String | Nome completo do mês | Janeiro |
| **Mês** | Int64 | Número do mês (1-12) | 1 |
| **Dia** | Int64 | Dia do mês (1-31) | 15 |
| **Semestre** | String | Semestre (S1, S2) | S1 |
| **Trimestre** | String | Trimestre (T1-T4) | T1 |
| **Mes Abreviado** | String | Mês abreviado | Jan |
| **Mes-Ano** | String | Formato mês-ano | Jan-2025 |
| **Mes Ano Classificação** | Int64 | Ordenação numérica | 202501 |

#### Colunas Calculadas

| Coluna | Tipo | Fórmula | Descrição |
|--------|------|---------|-----------|
| **Datas com Venda** | Boolean | EXISTS(fVendas) | TRUE se houve vendas nesta data |
| **Semana dia Num** | Int64 | WEEKDAY() | Número do dia da semana (1-7) |
| **Semana dia Nome** | String | FORMAT(WEEKDAY()) | Nome do dia da semana |

#### Hierarquia
- **Ano → Semestre → Trimestre → Mês → Dia**

#### Observações
- Cobre período completo de dados históricos + futuro
- Coluna **Datas com Venda** otimiza cálculos MoM
- Usada em análises temporais (YoY, MoM, YTD)

---

### dClientes

**Descrição**: Cadastro de clientes com informações geográficas.

**Total de Colunas**: 5

#### Colunas

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| **Id Cliente** | Int64 | Chave primária única | 2034 |
| **Nome** | String | Razão social/nome do cliente | Distribuidora ABC Ltda |
| **Cidade** | String | Cidade do cliente | São Paulo |
| **Estado** | String | UF do estado | SP |
| **Região** | String | Região geográfica | Sudeste |

#### Relacionamentos
- fVendas (Id Cliente) ← N:1 → dClientes (Id Cliente)

#### Observações
- Permite análise geográfica (cidade, estado, região)
- Usado em medida **12 Positivação Clientes**
- Base para análises de cobertura e penetração

---

### dProdutos

**Descrição**: Catálogo de produtos com hierarquia de categorização.

**Total de Colunas**: 5

#### Colunas

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| **Id Produto** | Int64 | Chave primária única | 1001 |
| **Nome** | String | Nome do produto | Óleo Motor 5W30 |
| **Categoria** | String | Categoria principal | Lubrificantes |
| **Subcategoria** | String | Subcategoria do produto | Óleos Automotivos |
| **Marca** | String | Marca do produto | Castrol |

#### Relacionamentos
- fVendas (Id Produto) ← N:1 → dProdutos (Id Produto)

#### Observações
- Hierarquia natural: Marca → Categoria → Subcategoria → Produto
- Usado em medida **13 Positivação Produtos**
- Base para análises de mix de produtos

---

### dVendedores

**Descrição**: Cadastro de vendedores com estrutura hierárquica.

**Total de Colunas**: 4

#### Colunas

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| **Id Vendedor** | Int64 | Chave primária única | 5 |
| **Nome** | String | Nome completo do vendedor | João Silva |
| **Região** | String | Região de atuação | Sul |
| **Gerente** | String | Nome do gerente responsável | Maria Santos |

#### Relacionamentos
- fVendas (Id Vendedor) ← N:1 → dVendedores (Id Vendedor)
- fMetas (Id Vendedor) ← N:1 → dVendedores (Id Vendedor)

#### Observações
- Permite análise por vendedor individual
- Hierarquia: Gerente → Região → Vendedor
- Base para análises de performance e comissionamento

---

### dUnidades

**Descrição**: Unidades de negócio/filiais da empresa.

**Total de Colunas**: 2

#### Colunas

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| **Id Unidade** | Int64 | Chave primária única | 3 |
| **Nome Unidade** | String | Nome da unidade/filial | Unidade SP Centro |

#### Relacionamentos
- fVendas (Id Unidade) ← N:1 → dUnidades (Id Unidade)

#### Observações
- Permite análise por centro de distribuição
- Útil para logística e análise regional

---

### dStatus

**Descrição**: Status das transações de venda.

**Total de Colunas**: 2

#### Colunas

| Coluna | Tipo | Descrição | Valores Possíveis |
|--------|------|-----------|-------------------|
| **Id Status** | Int64 | Chave primária | 1, 2, 3, ... |
| **Descrição** | String | Descrição do status | Efetivado, Cancelado, Pendente |

#### Relacionamentos
- fVendas (Id Status) ← N:1 → dStatus (Id Status)

#### Observações Críticas
⚠️ **IMPORTANTE**: Status = 1 significa "Efetivado"
- Todas as medidas de negócio filtram por `dStatus[Id Status] = 1`
- Status diferente de 1 são vendas não efetivadas (canceladas, pendentes, etc.)

---

### dPagamento

**Descrição**: Formas de pagamento aceitas.

**Total de Colunas**: 2

#### Colunas

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| **Id Pagamento** | Int64 | Chave primária | 2 |
| **Descrição** | String | Forma de pagamento | Cartão de Crédito, Boleto, PIX |

#### Relacionamentos
- fVendas (Id Pgto) ← N:1 → dPagamento (Id Pagamento)

#### Observações
- Permite análise de preferências de pagamento
- Útil para análises de fluxo de caixa

---

## 📏 Tabelas de Medidas

### _Medidas

**Descrição**: Tabela virtual contendo todas as medidas DAX principais.

**Total de Medidas**: 44

#### Organização por Pastas

##### 📁 01.Principais (13 medidas)
Medidas fundamentais de negócio:
- 01 Faturamento
- 02 Custo
- 03 Lucro Bruto ⭐ NOVA
- 04 Margem Bruta ⭐ NOVA
- 05 Despesa
- 06 Impostos
- 07 Comissao
- 08 Abatimento
- 09 Resultado
- 10 Margem
- 11 Qtde Vendas
- 12 Positivação Clientes
- 13 Positivação Produtos

##### 📁 02. Temporais (16 medidas)
Comparações temporais:
- 20-24: Faturamento (Acumulado, LY, YoY%, MoM%)
- 25-28: Margem (LM, LY, YoY%, MoM%)
- 29-32: Resultado (LM, LY, YoY%, MoM%)
- 33-35: Comissão (LY, YoY%, MoM%)

##### 📁 01.Principais - Metas (3 medidas)
Análise de metas:
- 40 Meta
- 41 Porcentagem Meta
- 42 Diferença Meta

##### 📁 03. Formatações (5 medidas)
Medidas auxiliares:
- 50 Eixo Y max Grafico Comercial
- 51 Faturamento formatação de texto
- 52 Rank Cidade
- 53 Max Y Visual 01 pg Vendedores
- 54 Nome Vendedor

##### 📁 .Visuais SVG (7 medidas)
Medidas para visuais customizados:
- 60-63: SVG Cartões (Faturamento, Margem, Resultado, Comissão)
- 64: SVG Tabela HTML
- 65: SVG Percentual Meta Velocímetro
- 66: Meta Cor

---

### zMetricas

**Descrição**: Tabela auxiliar com métricas de suporte.

**Total de Medidas**: 6

**Observações**: Usado para cálculos intermediários e métricas técnicas.

---

## 🔗 Relacionamentos

### Resumo de Relacionamentos

| # | De | Para | Cardinalidade | Filtro | Status |
|---|----|----|---------------|--------|--------|
| 1 | fVendas.Data Pedido | dCalendario.Id Data | N:1 | Unidirecional | ✅ Ativo |
| 2 | fVendas.Data Envio | dCalendario.Id Data | N:1 | Unidirecional | ⭕ Inativo |
| 3 | fVendas.Id Cliente | dClientes.Id Cliente | N:1 | Unidirecional | ✅ Ativo |
| 4 | fVendas.Id Produto | dProdutos.Id Produto | N:1 | Unidirecional | ✅ Ativo |
| 5 | fVendas.Id Vendedor | dVendedores.Id Vendedor | N:1 | Unidirecional | ✅ Ativo |
| 6 | fVendas.Id Unidade | dUnidades.Id Unidade | N:1 | Unidirecional | ✅ Ativo |
| 7 | fVendas.Id Status | dStatus.Id Status | N:1 | Unidirecional | ✅ Ativo |
| 8 | fVendas.Id Pgto | dPagamento.Id Pagamento | N:1 | Unidirecional | ✅ Ativo |
| 9 | fMetas.data | dCalendario.Id Data | N:1 | Unidirecional | ✅ Ativo |
| 10 | fMetas.Id Vendedor | dVendedores.Id Vendedor | N:1 | Unidirecional | ✅ Ativo |

### Observações sobre Relacionamentos

#### Role-Playing Dimension
- **dCalendario** é usado duas vezes por fVendas:
  - Data Pedido (ATIVO) - usado por padrão
  - Data Envio (INATIVO) - ativado via `USERELATIONSHIP()` quando necessário

#### Filtros Unidirecionais
- Todos os filtros são **One Direction** (Unidirecional)
- Dimensões filtram Fatos, mas Fatos não filtram Dimensões
- Garante performance e evita ambiguidades

---

## 📚 Glossário de Termos

### Termos de Negócio

**Faturamento**: Receita bruta de vendas efetivadas (Status = 1), calculada como Qtde × Valor Unit.

**Custo**: Custo dos produtos vendidos (CPV), calculado como Qtde × Custo Unit.

**Lucro Bruto**: Diferença entre Faturamento e Custo (Faturamento - Custo).

**Margem Bruta**: Percentual de lucro bruto sobre faturamento ((Lucro Bruto / Faturamento) × 100).

**Despesa**: Despesas operacionais (frete, logística, embalagem).

**Impostos**: Impostos sobre vendas (ICMS, PIS, COFINS, etc.).

**Comissão**: Comissões pagas aos vendedores.

**Abatimento**: Soma de todos os custos e despesas (Custo + Despesa + Impostos + Comissão).

**Resultado**: Lucro líquido após todos os abatimentos (Faturamento - Abatimento).

**Margem Líquida**: Percentual de resultado sobre faturamento ((Resultado / Faturamento) × 100).

**Positivação**: Quantidade de clientes ou produtos únicos com vendas no período.

**Meta**: Objetivo de faturamento estabelecido para vendedores/períodos.

### Termos Temporais

**LY (Last Year)**: Ano anterior - mesmo período do ano passado.

**LM (Last Month)**: Mês anterior - mês imediatamente anterior.

**YoY (Year over Year)**: Comparação com o mesmo período do ano anterior.

**MoM (Month over Month)**: Comparação com o mês anterior.

**YTD (Year to Date)**: Acumulado desde o início do ano até a data atual.

### Termos Técnicos

**Granularidade**: Nível de detalhe dos dados (linha a linha).

**Cardinalidade**: Tipo de relacionamento (1:N, N:1, N:N).

**Filtro de Contexto**: Filtros aplicados que determinam quais dados são calculados.

**Role-Playing Dimension**: Dimensão usada múltiplas vezes com significados diferentes.

**Calculated Column**: Coluna calculada armazenada na tabela.

**Measure (Medida)**: Cálculo DAX executado no contexto de consulta.

---

**Documento criado em:** 30/01/2026  
**Autor:** Assistente de Modelagem Power BI  
**Versão do Documento:** 1.0
