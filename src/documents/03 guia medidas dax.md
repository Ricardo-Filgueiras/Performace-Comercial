# 📐 Guia de Medidas DAX - Performance Comercial

**Versão:** 2.0  
**Última Atualização:** 30 de Janeiro de 2026

---

## 📋 Índice

1. [Medidas Principais (01-13)](#medidas-principais-01-13)
2. [Medidas Temporais (20-35)](#medidas-temporais-20-35)
3. [Medidas de Meta (40-42)](#medidas-de-meta-40-42)
4. [Medidas Auxiliares (50-66)](#medidas-auxiliares-50-66)
5. [Padrões e Boas Práticas](#padrões-e-boas-práticas)
6. [Troubleshooting Comum](#troubleshooting-comum)

---

## 💰 Medidas Principais (01-13)

### 01 Faturamento

**Objetivo**: Calcular a receita bruta de vendas efetivadas.

**Fórmula**:
```dax
01 Faturamento = 
    CALCULATE(
        SUMX(
            fVendas,
            fVendas[Qtde] * fVendas[Valor Unit]
        ),
        dStatus[Id Status] = 1
    )
```

**Explicação**:
- `SUMX()`: Itera linha por linha multiplicando Quantidade × Valor Unitário
- `CALCULATE()`: Aplica filtro de contexto
- `dStatus[Id Status] = 1`: Filtra apenas vendas efetivadas

**Formato**: `"R$" #,0.00`

**Pasta**: 01.Principais

---

### 02 Custo

**Objetivo**: Calcular o custo total dos produtos vendidos (CPV).

**Fórmula**:
```dax
02 Custo = 
    CALCULATE(
        SUMX(
            fVendas,
            fVendas[Qtde] * fVendas[Custo Unit]
        ),
        dStatus[Id Status] = 1
    )
```

**Explicação**:
- Mesmo padrão do Faturamento
- Usa coluna `Custo Unit` em vez de `Valor Unit`
- Essencial para cálculo de margem bruta

**Formato**: `"R$" #,0.00`

**Pasta**: 01.Principais

---

### 03 Lucro Bruto ⭐ NOVA

**Objetivo**: Calcular o lucro antes de despesas operacionais.

**Fórmula**:
```dax
03 Lucro Bruto = 
    [01 Faturamento] - [02 Custo]
```

**Explicação**:
- Simples subtração entre Faturamento e Custo
- Base para cálculo da Margem Bruta
- Indicador crucial de rentabilidade operacional

**Formato**: `"R$" #,0.00`

**Pasta**: 01.Principais

**Relacionamento com outras medidas**:
- Usado em: `04 Margem Bruta`
- Depende de: `01 Faturamento`, `02 Custo`

---

### 04 Margem Bruta ⭐ NOVA

**Objetivo**: Calcular o percentual de lucro bruto sobre faturamento.

**Fórmula**:
```dax
04 Margem Bruta = 
// Margem Bruta = (Faturamento - Custo) / Faturamento
VAR _Faturamento = [01 Faturamento]
VAR _Custo = [02 Custo]
VAR _MargemBruta = _Faturamento - _Custo

RETURN
    DIVIDE(
        _MargemBruta,
        _Faturamento,
        BLANK()
    )
```

**Explicação**:
- Uso de variáveis (`VAR`) evita recálculos
- `DIVIDE()` com `BLANK()` evita erros de divisão por zero
- Retorna percentual de lucratividade antes de despesas

**Formato**: `0.00%`

**Pasta**: 01.Principais

**Interpretação**:
- 30% = Para cada R$ 100 vendidos, R$ 30 é lucro bruto
- Benchmark: Varia por indústria, geralmente 20-50%

---

### 05 Despesa

**Objetivo**: Calcular despesas operacionais (frete, logística).

**Fórmula**:
```dax
05 Despesa = 
    CALCULATE(
        SUMX(
            fVendas,
            fVendas[Qtde] * fVendas[Despesa Unit]
        ),
        dStatus[Id Status] = 1
    )
```

**Formato**: `"R$" #,0`

**Pasta**: 01.Principais

---

### 06 Impostos

**Objetivo**: Calcular impostos sobre vendas.

**Fórmula**:
```dax
06 Impostos = 
    CALCULATE(
        SUMX(
            fVendas,
            fVendas[Qtde] * fVendas[Impostos Unit]
        ),
        dStatus[Id Status] = 1
    )
```

**Formato**: `"R$" #,0`

**Pasta**: 01.Principais

---

### 07 Comissao

**Objetivo**: Calcular comissões pagas aos vendedores.

**Fórmula**:
```dax
07 Comissao = 
    CALCULATE(
        SUMX(
            fVendas,
            fVendas[Qtde] * fVendas[Comissão Unit]
        ),
        dStatus[Id Status] = 1
    )
```

**Formato**: `"R$" #,0`

**Pasta**: 01.Principais

---

### 08 Abatimento

**Objetivo**: Somar todos os custos e despesas.

**Fórmula**:
```dax
08 Abatimento = 
    [02 Custo] + [05 Despesa] + [06 Impostos] + [07 Comissao]
```

**Explicação**:
- Agregação de todos os "custos" para calcular resultado líquido
- Componentes:
  - Custo de produtos
  - Despesas operacionais
  - Impostos
  - Comissões

**Formato**: `"R$" #,0`

**Pasta**: 01.Principais

---

### 09 Resultado

**Objetivo**: Calcular o lucro líquido.

**Fórmula**:
```dax
09 Resultado = 
    [01 Faturamento] - [08 Abatimento]
```

**Explicação**:
- Resultado líquido após todas as deduções
- Indicador final de rentabilidade
- Base para cálculo de margem líquida

**Formato**: `"R$" #,0`

**Pasta**: 01.Principais

---

### 10 Margem

**Objetivo**: Calcular margem líquida (%).

**Fórmula**:
```dax
10 Margem = 
// Margem Líquida = Resultado / Faturamento
DIVIDE(
    [09 Resultado],
    [01 Faturamento],
    BLANK()
)
```

**Explicação**:
- Percentual de lucro líquido sobre faturamento
- Indicador principal de rentabilidade
- Tratamento de erro com `BLANK()`

**Formato**: `0.00%`

**Pasta**: 01.Principais

**Diferença de 04 Margem Bruta**:
- Margem Bruta: Antes de despesas
- Margem Líquida: Depois de todas as deduções

---

### 11 Qtde Vendas

**Objetivo**: Contar número de transações.

**Fórmula**:
```dax
11 Qtde Vendas = 
    CALCULATE(
        COUNTROWS(fVendas),
        dStatus[Id Status] = 1
    )
```

**Explicação**:
- Conta linhas na tabela fVendas
- Filtra apenas vendas efetivadas
- Útil para análise de volume

**Formato**: `0`

**Pasta**: 01.Principais

---

### 12 Positivação Clientes

**Objetivo**: Contar clientes únicos com compras.

**Fórmula**:
```dax
12 Positivação Clientes = 
// Refere-se a Qtde de clientes que efetuaram compras efetivadas
CALCULATE(
    DISTINCTCOUNT(fVendas[Id Cliente]),
    dStatus[Id Status] = 1
)
```

**Explicação**:
- `DISTINCTCOUNT()`: Conta valores únicos
- Mede cobertura de clientes
- Filtro de status é CRÍTICO ⚠️

**Formato**: `0`

**Pasta**: 01.Principais

**KPI Relacionado**: Taxa de Conversão = Positivação / Total de Clientes

---

### 13 Positivação Produtos

**Objetivo**: Contar produtos únicos vendidos.

**Fórmula**:
```dax
13 Positivação Produtos = 
// Refere-se a Qtde de produtos vendidos efetivamente
CALCULATE(
    DISTINCTCOUNT(fVendas[Id Produto]),
    dStatus[Id Status] = 1
)
```

**Explicação**:
- Mede mix de produtos
- Indica diversificação de vendas
- Base para análise ABC

**Formato**: `0`

**Pasta**: 01.Principais

---

## ⏰ Medidas Temporais (20-35)

### Padrão de Medidas Temporais

Todas as medidas temporais seguem estrutura similar:
1. Calcular valor atual
2. Calcular valor comparação (LY, LM)
3. Calcular variação com `DIVIDE()` e `BLANK()`

---

### 20 Faturamento Acumulado

**Objetivo**: Calcular acumulado no ano (YTD).

**Fórmula**:
```dax
20 Faturamento Acumulado = 
    CALCULATE(
        [01 Faturamento],
        DATESYTD(dCalendario[Id Data])
    )
```

**Explicação**:
- `DATESYTD()`: Função time intelligence
- Acumula desde 01/01 até data atual
- Respeita filtros de ano

**Formato**: `"R$" #,0.00`

**Pasta**: 02. Temporais

---

### 21 Faturamento Acumulado LY

**Objetivo**: Acumulado do ano anterior.

**Fórmula**:
```dax
21 Faturamento Acumulado LY = 
    CALCULATE(
        [20 Faturamento Acumulado],
        SAMEPERIODLASTYEAR(dCalendario[Id Data])
    )
```

**Formato**: `"R$" #,0.00`

**Pasta**: 02. Temporais

---

### 22 Faturamento LY

**Objetivo**: Faturamento do ano anterior (mesmo período).

**Fórmula**:
```dax
22 Faturamento LY = 
    CALCULATE(
        [01 Faturamento],
        SAMEPERIODLASTYEAR(dCalendario[Id Data])
    )
```

**Explicação**:
- `SAMEPERIODLASTYEAR()`: Desloca contexto para ano anterior
- Permite comparação YoY

**Formato**: `"R$" #,0.00`

**Pasta**: 02. Temporais

---

### 23 Faturamento YoY %

**Objetivo**: Variação percentual ano a ano.

**Fórmula**:
```dax
23 Faturamento YoY % = 
// Variação Year over Year do Faturamento
VAR FaturamentoAtual = [01 Faturamento]
VAR FaturamentoLY = [22 Faturamento LY]

RETURN 
    DIVIDE(
        FaturamentoAtual - FaturamentoLY,
        FaturamentoLY,
        BLANK()
    )
```

**Explicação**:
- Fórmula: (Atual - Anterior) / Anterior
- Uso de variáveis otimiza performance
- `BLANK()` evita erro quando LY não existe

**Formato**: `0.00%`

**Pasta**: 02. Temporais

**Interpretação**:
- 15% = Crescimento de 15% vs ano anterior
- -10% = Queda de 10% vs ano anterior

---

### 24 Faturamento MoM %

**Objetivo**: Variação percentual mês a mês.

**Fórmula**:
```dax
24 Faturamento MoM % = 
// Variação Month over Month do Faturamento
VAR FaturamentoAtual = [01 Faturamento]
VAR FaturamentoLM = 
    CALCULATE(
        [01 Faturamento],
        CALCULATETABLE(
            DATEADD(dCalendario[Id Data], -1, MONTH),
            dCalendario[Datas com Venda] = TRUE()
        )
    )

RETURN 
    DIVIDE(
        FaturamentoAtual - FaturamentoLM,
        FaturamentoLM,
        BLANK()
    )
```

**Explicação**:
- `DATEADD(..., -1, MONTH)`: Volta 1 mês
- Filtro `Datas com Venda = TRUE()` otimiza cálculo
- Compara com mês imediatamente anterior

**Formato**: `0.00%`

**Pasta**: 02. Temporais

---

### 25-28: Margem LM / LY / YoY % / MoM %

**Padrão Similar**: Mesmo padrão temporal aplicado à medida `10 Margem`

**Exemplo - 27 Margem YoY %**:
```dax
27 Margem YoY % = 
VAR MargemAtual = [10 Margem]
VAR MargemLY = [26 Margem LY]

RETURN 
    DIVIDE(
        MargemAtual - MargemLY,
        MargemLY,
        BLANK()
    )
```

**Formato**: `0.00%`

**Pasta**: 02. Temporais

---

### 29-32: Resultado LM / LY / YoY % / MoM %

**Padrão Similar**: Mesmo padrão temporal aplicado à medida `09 Resultado`

**Formato**: `"R$" #,0` para valores absolutos, `0.00%` para percentuais

**Pasta**: 02. Temporais

---

### 33-35: Comissao LY / YoY % / MoM %

**Padrão Similar**: Mesmo padrão temporal aplicado à medida `07 Comissao`

**Formato**: Valores em `"R$" #,0`, variações em `0.00%`

**Pasta**: 02. Temporais

---

## 🎯 Medidas de Meta (40-42)

### 40 Meta

**Objetivo**: Obter meta do período.

**Fórmula**:
```dax
40 Meta = 
    SUM(fMetas[Meta])
```

**Explicação**:
- Soma simples da tabela fMetas
- Respeita contexto de filtro (vendedor, data)
- Base para cálculos de atingimento

**Formato**: `"R$" #,0.00`

**Pasta**: 01.Principais

---

### 41 Porcentagem Meta

**Objetivo**: Calcular % de atingimento da meta.

**Fórmula**:
```dax
41 Porcentagem Meta = 
// Percentual de atingimento: Faturamento / Meta
VAR _Faturamento = [01 Faturamento]
VAR _Meta = [40 Meta]

RETURN
    DIVIDE(
        _Faturamento,
        _Meta,
        BLANK()
    )
```

**Explicação**:
- Fórmula: Realizado / Meta
- 100% = Meta atingida exatamente
- >100% = Meta superada
- <100% = Meta não atingida

**Formato**: `0.00%`

**Pasta**: 01.Principais

**Visualização Comum**: Velocímetro/Gauge

---

### 42 Diferença Meta

**Objetivo**: Calcular gap entre realizado e meta.

**Fórmula**:
```dax
42 Diferença Meta = 
    [01 Faturamento] - [40 Meta]
```

**Explicação**:
- Valor positivo: Acima da meta
- Valor negativo: Abaixo da meta
- Zero: Meta exata

**Formato**: `"R$" #,0`

**Pasta**: 01.Principais

---

## 🛠️ Medidas Auxiliares (50-66)

### 50 Eixo Y max Grafico Comercial

**Objetivo**: Definir escala máxima de gráfico dinamicamente.

**Uso**: Formatação de eixo Y

**Pasta**: 03. Formatações

---

### 51 Faturamento formatação de texto

**Objetivo**: Formatar faturamento como texto customizado.

**Uso**: Exibição em visuais personalizados

**Pasta**: 03. Formatações

---

### 52 Rank Cidade

**Objetivo**: Ranquear cidades por faturamento.

**Padrão**:
```dax
52 Rank Cidade = 
RANKX(
    ALL(dClientes[Cidade]),
    [01 Faturamento],
    ,
    DESC,
    DENSE
)
```

**Pasta**: Não categorizado

---

### 60-66: Medidas SVG

**Descrição**: Medidas que geram código SVG/HTML para visuais customizados.

**Exemplos**:
- 60: Cartão Faturamento SVG
- 61: Cartão Margem SVG
- 62: Cartão Resultado SVG
- 65: Velocímetro de Meta SVG

**Pasta**: .Visuais SVG

**Nota**: Requerem visual HTML Content ou similar

---

## 📚 Padrões e Boas Práticas

### 1. Uso de Variáveis (VAR)

✅ **BOM**:
```dax
VAR Atual = [Medida]
VAR Anterior = [Medida LY]
RETURN DIVIDE(Atual - Anterior, Anterior, BLANK())
```

❌ **EVITAR**:
```dax
DIVIDE([Medida] - [Medida LY], [Medida LY])
```

**Motivo**: Variáveis evitam recálculos e melhoram legibilidade.

---

### 2. Tratamento de Erros em Divisões

✅ **BOM**:
```dax
DIVIDE([Numerador], [Denominador], BLANK())
```

❌ **EVITAR**:
```dax
[Numerador] / [Denominador]
```

**Motivo**: `BLANK()` retorna valor vazio em vez de erro.

---

### 3. Filtros de Contexto

✅ **BOM**:
```dax
CALCULATE([Medida], dStatus[Id Status] = 1)
```

❌ **EVITAR**:
```dax
CALCULATE([Medida], FILTER(dStatus, dStatus[Id Status] = 1))
```

**Motivo**: Filtro direto é mais performático.

---

### 4. Time Intelligence

✅ **BOM**:
```dax
CALCULATE([Medida], SAMEPERIODLASTYEAR(dCalendario[Id Data]))
```

**Requisitos**:
- Tabela de calendário contínua
- Coluna de data marcada como Date Table
- Relacionamento ativo com tabela fato

---

### 5. Comentários em DAX

✅ **BOM**:
```dax
// Margem Líquida = Resultado / Faturamento
VAR _Resultado = [09 Resultado]
VAR _Faturamento = [01 Faturamento]

RETURN
    DIVIDE(_Resultado, _Faturamento, BLANK())
```

**Motivo**: Facilita manutenção e documentação.

---

## 🔧 Troubleshooting Comum

### Problema 1: Divisão por Zero

**Sintoma**: Erro "Infinity" ou valores inválidos

**Solução**:
```dax
// ✅ Usar DIVIDE com terceiro parâmetro
DIVIDE([Numerador], [Denominador], BLANK())
```

---

### Problema 2: Time Intelligence não funciona

**Sintomas**:
- SAMEPERIODLASTYEAR retorna BLANK
- DATESYTD não acumula

**Causas Comuns**:
1. Tabela de calendário não marcada como Date Table
2. Gaps na tabela de calendário
3. Relacionamento inativo

**Solução**:
```dax
// Verificar se há gaps
VAR MinDate = MIN(fVendas[Data Pedido])
VAR MaxDate = MAX(fVendas[Data Pedido])
RETURN
    COUNTROWS(
        FILTER(
            dCalendario,
            dCalendario[Id Data] >= MinDate &&
            dCalendario[Id Data] <= MaxDate
        )
    )
```

---

### Problema 3: Performance Lenta

**Sintomas**: Medidas demoram para calcular

**Soluções**:
1. Usar variáveis para evitar recálculos
2. Evitar funções iterativas desnecessárias
3. Simplificar filtros complexos
4. Usar agregações nativas (SUM) em vez de SUMX quando possível

**Exemplo de Otimização**:
```dax
// ❌ LENTO
SUMX(fVendas, [01 Faturamento])

// ✅ RÁPIDO
[01 Faturamento]
```

---

### Problema 4: Valores Duplicados

**Sintoma**: Valores muito altos ou duplicados

**Causa**: Relacionamentos incorretos (N:N) ou falta de DISTINCTCOUNT

**Solução**:
```dax
// Para contagens únicas
DISTINCTCOUNT(Tabela[Coluna])

// Para verificar relacionamentos
// Use Diagrama de Relacionamentos no Power BI
```

---

## 📊 Hierarquia de Dependências

```
01 Faturamento
├── 03 Lucro Bruto
│   └── 04 Margem Bruta
├── 08 Abatimento
│   └── 09 Resultado
│       └── 10 Margem
└── 23-24 Variações Temporais

02 Custo ────┐
05 Despesa ──┤
06 Impostos ─┼─→ 08 Abatimento
07 Comissao ─┘

40 Meta
├── 41 Porcentagem Meta
└── 42 Diferença Meta
```

---

**Documento criado em:** 30/01/2026  
**Autor:** Assistente de Modelagem Power BI  
**Versão do Documento:** 1.0
