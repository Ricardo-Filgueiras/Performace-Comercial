# 🔗 Relacionamentos - Performance Comercial

**Versão:** 2.0  
**Última Atualização:** 30 de Janeiro de 2026

---

## 📋 Índice

1. [Visão Geral](#visao-geral)
2. [Diagrama de Relacionamentos](#diagrama-de-relacionamentos)
3. [Relacionamentos Detalhados](#relacionamentos-detalhados)
4. [Role-Playing Dimensions](#role-playing-dimensions)
5. [Boas Práticas](#boas-praticas)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

### Estatísticas do Modelo

- **Total de Relacionamentos**: 10
- **Relacionamentos Ativos**: 9
- **Relacionamentos Inativos**: 1
- **Tipo de Relacionamentos**: Todos N:1 (Many-to-One)
- **Filtro de Propagação**: Todos unidirecionais (One Direction)

### Princípios do Modelo

✅ **Star Schema Puro**
- Fatos no centro
- Dimensões ao redor
- Sem relacionamentos dimensão-dimensão

✅ **Filtros Unidirecionais**
- Dimensões filtram Fatos
- Fatos não filtram Dimensões
- Melhor performance

✅ **Chaves Surrogadas**
- IDs numéricos inteiros (Int64)
- Otimizadas para compressão

---

## 📊 Diagrama de Relacionamentos

### Diagrama Completo

```
                    ┌─────────────────┐
                    │   dCalendario   │
                    │  (Date Table)   │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            │                │                │
    ┌───────▼──────┐  ┌──────▼──────┐        │
    │   fVendas    │  │   fMetas    │        │
    │  (Fact 1)    │  │  (Fact 2)   │        │
    └┬─┬─┬─┬─┬─┬─┬┘  └──────┬──────┘        │
     │ │ │ │ │ │ │           │               │
     │ │ │ │ │ │ │     ┌─────▼──────────────▼──┐
     │ │ │ │ │ │ │     │    dVendedores        │
     │ │ │ │ │ │ │     │   (Dimension)         │
     │ │ │ │ │ │ │     └───────────────────────┘
     │ │ │ │ │ │ │
     │ │ │ │ │ │ └────► dPagamento
     │ │ │ │ │ └──────► dStatus (FILTRO CRÍTICO!)
     │ │ │ │ └────────► dUnidades
     │ │ │ └──────────► dClientes
     │ │ └────────────► dProdutos
     │ └──────────────► (dCalendario - INATIVO)
     └────────────────► (dCalendario - ATIVO)
```

### Legenda
- **─►**: Relacionamento Ativo
- **─⊗►**: Relacionamento Inativo
- **▼**: Direção do Filtro (1 → N)

---

## 🔍 Relacionamentos Detalhados

### 1️⃣ fVendas → dCalendario (Data Pedido) ✅ ATIVO

| Propriedade | Valor |
|-------------|-------|
| **Coluna Origem** | fVendas[Data Pedido] |
| **Coluna Destino** | dCalendario[Id Data] |
| **Cardinalidade** | N:1 (Many-to-One) |
| **Direção Filtro** | Unidirecional (Única) |
| **Status** | ✅ Ativo |
| **Integridade Referencial** | Não |

**Descrição**: Relacionamento principal para análises temporais baseadas na data do pedido.

**Uso**:
- Todas as análises temporais padrão
- Funções Time Intelligence (YoY, MoM, YTD)
- Filtros de período em slicers

**Exemplo de Uso**:
```dax
// Automaticamente usa Data Pedido
[01 Faturamento]
```

---

### 2️⃣ fVendas → dCalendario (Data Envio) ⭕ INATIVO

| Propriedade | Valor |
|-------------|-------|
| **Coluna Origem** | fVendas[Data Envio] |
| **Coluna Destino** | dCalendario[Id Data] |
| **Cardinalidade** | N:1 (Many-to-One) |
| **Direção Filtro** | Unidirecional (Única) |
| **Status** | ⭕ Inativo |
| **Integridade Referencial** | Não |

**Descrição**: Relacionamento alternativo para análises baseadas na data de envio.

**Uso**:
- Deve ser ativado explicitamente via `USERELATIONSHIP()`
- Útil para análises logísticas
- Análise de lead time (pedido → envio)

**Exemplo de Uso**:
```dax
// Ativar relacionamento alternativo
Faturamento por Data Envio = 
CALCULATE(
    [01 Faturamento],
    USERELATIONSHIP(fVendas[Data Envio], dCalendario[Id Data])
)
```

**⚠️ Nota Importante**: Este é um exemplo de **Role-Playing Dimension** - dCalendario é usado duas vezes com significados diferentes.

---

### 3️⃣ fVendas → dClientes ✅ ATIVO

| Propriedade | Valor |
|-------------|-------|
| **Coluna Origem** | fVendas[Id Cliente] |
| **Coluna Destino** | dClientes[Id Cliente] |
| **Cardinalidade** | N:1 (Many-to-One) |
| **Direção Filtro** | Unidirecional (Única) |
| **Status** | ✅ Ativo |

**Descrição**: Relaciona vendas aos clientes.

**Uso**:
- Análise por cliente
- Segmentação geográfica (via cidade/estado/região)
- Análise de positivação
- Análise RFM (Recência, Frequência, Valor Monetário)

**Medidas que Dependem**:
- `12 Positivação Clientes`
- Análises de cobertura

---

### 4️⃣ fVendas → dProdutos ✅ ATIVO

| Propriedade | Valor |
|-------------|-------|
| **Coluna Origem** | fVendas[Id Produto] |
| **Coluna Destino** | dProdutos[Id Produto] |
| **Cardinalidade** | N:1 (Many-to-One) |
| **Direção Filtro** | Unidirecional (Única) |
| **Status** | ✅ Ativo |

**Descrição**: Relaciona vendas aos produtos.

**Uso**:
- Análise por produto
- Hierarquia Marca → Categoria → Subcategoria → Produto
- Mix de produtos
- Análise ABC

**Medidas que Dependem**:
- `13 Positivação Produtos`
- Análises de sortimento

---

### 5️⃣ fVendas → dVendedores ✅ ATIVO

| Propriedade | Valor |
|-------------|-------|
| **Coluna Origem** | fVendas[Id Vendedor] |
| **Coluna Destino** | dVendedores[Id Vendedor] |
| **Cardinalidade** | N:1 (Many-to-One) |
| **Direção Filtro** | Unidirecional (Única) |
| **Status** | ✅ Ativo |

**Descrição**: Relaciona vendas aos vendedores.

**Uso**:
- Análise de performance individual
- Hierarquia Gerente → Região → Vendedor
- Cálculo de comissões
- Ranking de vendedores

**Medidas Relacionadas**:
- `07 Comissao`
- Todas as análises de performance de vendedores

---

### 6️⃣ fVendas → dUnidades ✅ ATIVO

| Propriedade | Valor |
|-------------|-------|
| **Coluna Origem** | fVendas[Id Unidade] |
| **Coluna Destino** | dUnidades[Id Unidade] |
| **Cardinalidade** | N:1 (Many-to-One) |
| **Direção Filtro** | Unidirecional (Única) |
| **Status** | ✅ Ativo |

**Descrição**: Relaciona vendas às unidades de negócio.

**Uso**:
- Análise por filial/centro de distribuição
- Análise regional operacional
- Otimização logística

---

### 7️⃣ fVendas → dStatus ✅ ATIVO ⚠️ CRÍTICO

| Propriedade | Valor |
|-------------|-------|
| **Coluna Origem** | fVendas[Id Status] |
| **Coluna Destino** | dStatus[Id Status] |
| **Cardinalidade** | N:1 (Many-to-One) |
| **Direção Filtro** | Unidirecional (Única) |
| **Status** | ✅ Ativo |

**Descrição**: Relaciona vendas ao status da transação.

**⚠️ IMPORTÂNCIA CRÍTICA**:
Este relacionamento é FUNDAMENTAL para o modelo. Todas as medidas de negócio DEVEM filtrar por `dStatus[Id Status] = 1` (Efetivado).

**Valores de Status**:
- **1 = Efetivado**: Venda confirmada (USAR EM MEDIDAS)
- **2 = Cancelado**: Venda cancelada (EXCLUIR DE MEDIDAS)
- **3 = Pendente**: Aguardando confirmação (EXCLUIR DE MEDIDAS)

**Exemplo de Uso Correto**:
```dax
// ✅ CORRETO - Com filtro de status
01 Faturamento = 
CALCULATE(
    SUMX(fVendas, fVendas[Qtde] * fVendas[Valor Unit]),
    dStatus[Id Status] = 1  // <-- ESSENCIAL!
)

// ❌ INCORRETO - Sem filtro
Faturamento ERRADO = 
SUMX(fVendas, fVendas[Qtde] * fVendas[Valor Unit])
// Inclui vendas canceladas e pendentes!
```

**Impacto**: Sem este filtro, métricas incluirão vendas canceladas e pendentes, distorcendo completamente os resultados!

---

### 8️⃣ fVendas → dPagamento ✅ ATIVO

| Propriedade | Valor |
|-------------|-------|
| **Coluna Origem** | fVendas[Id Pgto] |
| **Coluna Destino** | dPagamento[Id Pagamento] |
| **Cardinalidade** | N:1 (Many-to-One) |
| **Direção Filtro** | Unidirecional (Única) |
| **Status** | ✅ Ativo |

**Descrição**: Relaciona vendas às formas de pagamento.

**Uso**:
- Análise de preferências de pagamento
- Análise de fluxo de caixa
- Condições de pagamento

---

### 9️⃣ fMetas → dCalendario ✅ ATIVO

| Propriedade | Valor |
|-------------|-------|
| **Coluna Origem** | fMetas[data] |
| **Coluna Destino** | dCalendario[Id Data] |
| **Cardinalidade** | N:1 (Many-to-One) |
| **Direção Filtro** | Unidirecional (Única) |
| **Status** | ✅ Ativo |

**Descrição**: Relaciona metas às datas.

**Uso**:
- Sincronização temporal entre vendas e metas
- Permite comparação realizado vs meta no tempo

**Medidas que Dependem**:
- `40 Meta`
- `41 Porcentagem Meta`
- `42 Diferença Meta`

---

### 🔟 fMetas → dVendedores ✅ ATIVO

| Propriedade | Valor |
|-------------|-------|
| **Coluna Origem** | fMetas[Id Vendedor] |
| **Coluna Destino** | dVendedores[Id Vendedor] |
| **Cardinalidade** | N:1 (Many-to-One) |
| **Direção Filtro** | Unidirecional (Única) |
| **Status** | ✅ Ativo |

**Descrição**: Relaciona metas aos vendedores.

**Uso**:
- Metas individuais por vendedor
- Análise de atingimento por vendedor
- Cascateamento para gerente/região

---

## 🎭 Role-Playing Dimensions

### O que é Role-Playing Dimension?

Uma dimensão usada múltiplas vezes na tabela fato com significados diferentes.

### Exemplo no Modelo: dCalendario

A dimensão **dCalendario** é usada DUAS VEZES por fVendas:

1. **Data Pedido** (ATIVO): Data em que o pedido foi realizado
2. **Data Envio** (INATIVO): Data em que o pedido foi enviado

#### Por que um relacionamento é inativo?

O Power BI não permite dois relacionamentos ativos entre as mesmas tabelas. Isso evitaria ambiguidade: qual data usar?

#### Como usar o relacionamento inativo?

Use a função `USERELATIONSHIP()`:

```dax
// Faturamento por Data de Pedido (padrão)
[01 Faturamento]

// Faturamento por Data de Envio (ativa relacionamento alternativo)
Faturamento por Envio = 
CALCULATE(
    [01 Faturamento],
    USERELATIONSHIP(fVendas[Data Envio], dCalendario[Id Data])
)
```

#### Caso de Uso Prático: Lead Time

```dax
// Análise de tempo entre pedido e envio
Lead Time Médio = 
VAR Pedidos = 
    SUMMARIZE(
        fVendas,
        fVendas[Num Venda],
        "DataPedido", MIN(fVendas[Data Pedido]),
        "DataEnvio", MIN(fVendas[Data Envio])
    )
RETURN
    AVERAGEX(
        Pedidos,
        [DataEnvio] - [DataPedido]
    )
```

---

## ✅ Boas Práticas

### 1. Sempre Use Relacionamentos Nativos

✅ **BOM**:
```dax
// Deixa o modelo fazer o trabalho
[01 Faturamento]
```

❌ **EVITAR**:
```dax
// Relacionamento manual (lento e propenso a erros)
SUMX(
    fVendas,
    CALCULATE(
        fVendas[Qtde] * fVendas[Valor Unit],
        FILTER(dProdutos, dProdutos[Id Produto] = fVendas[Id Produto])
    )
)
```

---

### 2. Evite Relacionamentos Bidirecionais

❌ **EVITAR**: Cross-filtering bidirecional

**Motivos**:
- Prejudica performance
- Cria ambiguidade
- Dificulta debugging

**Exceção**: Relacionamentos N:N podem requerer, mas devem ser raros.

---

### 3. Use Chaves Surrogadas Inteiras

✅ **BOM**: Int64 (ID numérico)
❌ **EVITAR**: String (GUID, texto)

**Motivos**:
- Inteiros comprimem melhor
- Joins são mais rápidos
- Menor uso de memória

---

### 4. Mantenha Integridade Referencial

Garanta que todas as chaves estrangeiras existam na dimensão:

```sql
-- Exemplo de validação
SELECT DISTINCT fv.Id Cliente
FROM fVendas fv
LEFT JOIN dClientes dc ON fv.Id Cliente = dc.Id Cliente
WHERE dc.Id Cliente IS NULL
```

**Resultado esperado**: Nenhuma linha (todas as chaves existem)

---

## 🔧 Troubleshooting

### Problema 1: Valores Duplicados

**Sintoma**: Totais muito altos, como se valores estivessem duplicados.

**Causa Provável**: Relacionamento N:N acidental

**Diagnóstico**:
```dax
// Verificar se há duplicatas na dimensão
Duplicatas Clientes = 
COUNTROWS(dClientes) - DISTINCTCOUNT(dClientes[Id Cliente])
// Deve retornar 0
```

**Solução**: Garantir chave primária única em dimensões.

---

### Problema 2: Blank Values

**Sintoma**: Linhas "(blank)" nos visuais

**Causa Provável**: Chaves estrangeiras nulas ou sem correspondência

**Diagnóstico**:
```dax
// Contar vendas sem cliente
Vendas Sem Cliente = 
CALCULATE(
    COUNTROWS(fVendas),
    ISBLANK(fVendas[Id Cliente])
)
```

**Solução**: 
1. Limpar dados de origem
2. Adicionar linha "Desconhecido" na dimensão (ID = -1 ou 0)

---

### Problema 3: Filtros Não Funcionam

**Sintoma**: Slicer não filtra visual

**Causas Possíveis**:
1. Relacionamento inativo
2. Direção de filtro errada
3. Relacionamento ausente

**Diagnóstico**:
- Verifique Diagrama de Relacionamentos
- Confirme setas de filtro apontam corretamente
- Teste com `CALCULATE` e filtro explícito

---

### Problema 4: Time Intelligence Não Funciona

**Sintoma**: SAMEPERIODLASTYEAR retorna blank

**Causas Possíveis**:
1. Tabela de calendário não marcada como Date Table
2. Relacionamento com calendário está inativo
3. Gaps (buracos) na tabela de calendário

**Solução**:
```
1. Modelagem → Marcar como Tabela de Data
2. Verificar relacionamento está ativo
3. Garantir calendário contínuo (sem gaps)
```

---

## 📊 Matriz de Relacionamentos

| Tabela Fato | Dimensão | Coluna FK | Coluna PK | Status |
|-------------|----------|-----------|-----------|--------|
| fVendas | dCalendario | Data Pedido | Id Data | ✅ Ativo |
| fVendas | dCalendario | Data Envio | Id Data | ⭕ Inativo |
| fVendas | dClientes | Id Cliente | Id Cliente | ✅ Ativo |
| fVendas | dProdutos | Id Produto | Id Produto | ✅ Ativo |
| fVendas | dVendedores | Id Vendedor | Id Vendedor | ✅ Ativo |
| fVendas | dUnidades | Id Unidade | Id Unidade | ✅ Ativo |
| fVendas | dStatus | Id Status | Id Status | ✅ Ativo ⚠️ |
| fVendas | dPagamento | Id Pgto | Id Pagamento | ✅ Ativo |
| fMetas | dCalendario | data | Id Data | ✅ Ativo |
| fMetas | dVendedores | Id Vendedor | Id Vendedor | ✅ Ativo |

---

**Documento criado em:** 30/01/2026  
**Autor:** Assistente de Modelagem Power BI  
**Versão do Documento:** 1.0
