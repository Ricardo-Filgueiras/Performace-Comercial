# 📘 Boas Práticas - Performance Comercial

**Versão:** 2.0  
**Última Atualização:** 30 de Janeiro de 2026

---

## 📋 Índice

1. [Princípios Gerais](#principios-gerais)
2. [Modelagem de Dados](#modelagem-de-dados)
3. [Medidas DAX](#medidas-dax)
4. [Performance](#performance)
5. [Nomenclatura](#nomenclatura)
6. [Documentação](#documentacao)
7. [Testes](#testes)
8. [Manutenção](#manutencao)

---

## 🎯 Princípios Gerais

### Simplicidade Primeiro
> "Faça a coisa mais simples que possa funcionar" - Kent Beck

✅ **Prefira**: Soluções simples e diretas
❌ **Evite**: Complexidade desnecessária

**Exemplo**:
```dax
// ✅ SIMPLES
Total Vendas = SUM(fVendas[Valor])

// ❌ COMPLEXO (sem necessidade)
Total Vendas = 
SUMX(
    FILTER(
        ALL(fVendas),
        fVendas[Valor] <> BLANK()
    ),
    fVendas[Valor]
)
```

---

### Consistência é Chave
- Siga padrões estabelecidos
- Mantenha nomenclatura consistente
- Use mesma estrutura DAX em medidas similares

---

### Documente Decisões
- Por que escolheu esta abordagem?
- Quais alternativas foram consideradas?
- Quais foram os trade-offs?

---

## 📊 Modelagem de Dados

### 1. Use Star Schema

✅ **Estrutura Recomendada**:
```
      Dimensões
         │
    ┌────┼────┐
    ▼    ▼    ▼
    Fato Central
```

❌ **Evite**: Snowflake Schema desnecessário

**Motivo**: Star Schema é mais simples, mais rápido e mais intuitivo.

---

### 2. Chaves Surrogadas Inteiras

✅ **BOM**:
```
Id Cliente: 1, 2, 3, 4, ...
Tipo: Int64
```

❌ **EVITAR**:
```
Id Cliente: "CLI-2025-00001"
Tipo: String
```

**Motivos**:
- 🗜️ Melhor compressão (menor tamanho do modelo)
- ⚡ Joins mais rápidos
- 💾 Menor uso de memória

---

### 3. Tabelas de Dimensão Simples

**Princípios**:
- Uma linha = um registro único
- Chave primária sempre única
- Sem duplicatas

**Verificação**:
```dax
// Deve retornar 0
Duplicatas = 
COUNTROWS(dClientes) - DISTINCTCOUNT(dClientes[Id Cliente])
```

---

### 4. Tabela de Calendário Contínua

✅ **Requisitos Essenciais**:
- Sem gaps (dias faltando)
- Cobre todo período de dados + futuro
- Marcada como Date Table
- Tipo de dados: Date (não DateTime)

**Exemplo de Criação**:
```dax
dCalendario = 
CALENDAR(
    DATE(2020, 1, 1),  // Início
    DATE(2030, 12, 31) // Fim (inclui futuro)
)
```

---

### 5. Relacionamentos Unidirecionais

✅ **Padrão Recomendado**:
```
Dimensão (1) → (N) Fato
```

❌ **Evite**: Filtros bidirecionais sem necessidade real

**Exceções Válidas**:
- Relacionamentos N:N quando inevitável
- Casos específicos de bridge tables

---

### 6. Evite Colunas Calculadas Desnecessárias

**Quando Usar Colunas Calculadas**:
- Agrupamentos estáticos (ex: Faixas de Valor)
- Atributos de dimensão derivados
- Chaves de relacionamento

**Quando Usar Medidas**:
- Agregações (SUM, AVERAGE, COUNT, etc.)
- Cálculos contextuais
- Time intelligence

✅ **Coluna Calculada Apropriada**:
```dax
// Em dProdutos
Categoria Preço = 
SWITCH(
    TRUE(),
    dProdutos[Preco] < 50, "Baixo",
    dProdutos[Preco] < 200, "Médio",
    "Alto"
)
```

❌ **Coluna Calculada Inapropriada**:
```dax
// Em fVendas (NÃO FAZER!)
Total Linha = fVendas[Qtde] * fVendas[Valor Unit]
// Use medida em vez disso!
```

---

## 🧮 Medidas DAX

### 1. Sempre Trate Divisões por Zero

✅ **SEMPRE**:
```dax
Margem = DIVIDE([Resultado], [Faturamento], BLANK())
```

❌ **NUNCA**:
```dax
Margem = [Resultado] / [Faturamento]
```

**Opções para terceiro parâmetro**:
- `BLANK()`: Retorna vazio (recomendado)
- `0`: Retorna zero
- Valor customizado: Retorna valor específico

---

### 2. Use Variáveis (VAR)

✅ **Com Variáveis** (Recomendado):
```dax
Margem YoY % = 
VAR MargemAtual = [10 Margem]
VAR MargemLY = [26 Margem LY]
VAR Variacao = MargemAtual - MargemLY

RETURN
    DIVIDE(Variacao, MargemLY, BLANK())
```

❌ **Sem Variáveis** (Não recomendado):
```dax
Margem YoY % = 
DIVIDE(
    [10 Margem] - [26 Margem LY],
    [26 Margem LY],
    BLANK()
)
```

**Benefícios de VAR**:
- ⚡ Performance (evita recálculos)
- 📖 Legibilidade (código mais claro)
- 🐛 Debugging (mais fácil encontrar erros)
- ✅ Manutenibilidade (mais fácil atualizar)

---

### 3. Nomenclatura de Medidas

**Padrão Estabelecido**:
```
[Número] [Nome Descritivo]
```

**Exemplos**:
- `01 Faturamento`
- `23 Faturamento YoY %`
- `40 Meta`

**Convenção de Numeração**:
- **01-19**: Medidas principais
- **20-39**: Comparações temporais
- **40-49**: Medidas de meta
- **50-59**: Auxiliares/formatação
- **60-79**: Visuais SVG
- **80-89**: Rankings
- **90-99**: Teste/desenvolvimento

---

### 4. Sufixos Temporais Consistentes

**Padrão Estabelecido**:
- **LY**: Last Year (Ano Anterior)
- **LM**: Last Month (Mês Anterior)
- **YoY**: Year over Year (Variação Anual)
- **MoM**: Month over Month (Variação Mensal)
- **YTD**: Year to Date (Acumulado no Ano)
- **QTD**: Quarter to Date (Acumulado no Trimestre)

**Exemplos**:
- `22 Faturamento LY`
- `23 Faturamento YoY %`
- `24 Faturamento MoM %`
- `20 Faturamento Acumulado` (YTD)

---

### 5. Comentários Inline

✅ **BOM** (Comentário Útil):
```dax
04 Margem Bruta = 
// Margem Bruta = (Faturamento - Custo) / Faturamento
VAR _Faturamento = [01 Faturamento]
VAR _Custo = [02 Custo]
VAR _MargemBruta = _Faturamento - _Custo

RETURN
    DIVIDE(_MargemBruta, _Faturamento, BLANK())
```

❌ **RUIM** (Comentário Óbvio):
```dax
Soma = 
// Soma valores
SUM(Tabela[Coluna])
```

**Quando Comentar**:
- Lógica de negócio não óbvia
- Fórmulas complexas
- Decisões de design
- Workarounds temporários

---

### 6. Formatação Consistente

**Padrões de Formato**:
```dax
// Moeda
"R$" #,0.00;-"R$" #,0.00;"R$" #,0.00

// Percentual
0.00%;-0.00%;0.00%

// Inteiro
0

// Inteiro com separador
#,0
```

**Aplicar via Propriedades**:
```
1. Selecione a medida
2. Propriedades → Format
3. Escolha formato apropriado
```

---

### 7. Evite Funções Iterativas Desnecessárias

✅ **RÁPIDO**:
```dax
Total = SUM(fVendas[Valor])
```

❌ **LENTO**:
```dax
Total = SUMX(fVendas, fVendas[Valor])
```

**Quando SUMX é Necessário**:
```dax
// Cálculo linha por linha
Faturamento = 
SUMX(
    fVendas,
    fVendas[Qtde] * fVendas[Valor Unit]
)
```

**Funções Nativas vs Iterativas**:
| Nativa (Rápida) | Iterativa (Lenta) | Quando Usar Iterativa |
|-----------------|-------------------|------------------------|
| SUM() | SUMX() | Multiplicações linha a linha |
| AVERAGE() | AVERAGEX() | Cálculos complexos por linha |
| COUNT() | COUNTX() | Contagens condicionais complexas |
| MIN() / MAX() | MINX() / MAXX() | Quando MIN/MAX simples não funciona |

---

## ⚡ Performance

### 1. Use Filtros Eficientes

✅ **EFICIENTE**:
```dax
CALCULATE(
    [Medida],
    dStatus[Id Status] = 1
)
```

❌ **INEFICIENTE**:
```dax
CALCULATE(
    [Medida],
    FILTER(
        dStatus,
        dStatus[Id Status] = 1
    )
)
```

**Motivo**: Filtro direto cria uma tabela de filtro menor internamente.

---

### 2. Minimize Uso de FILTER()

**Quando FILTER() é Necessário**:
- Condições complexas
- Múltiplas colunas
- Lógica condicional avançada

**Exemplo Válido**:
```dax
Clientes Premium = 
CALCULATE(
    [01 Faturamento],
    FILTER(
        dClientes,
        dClientes[Tipo] = "Premium" &&
        dClientes[Score] > 80
    )
)
```

---

### 3. Evite ALL() Desnecessários

✅ **BOM** (Contextual):
```dax
[01 Faturamento]
```

❌ **RUIM** (Remove contexto sem necessidade):
```dax
CALCULATE([01 Faturamento], ALL(dProdutos))
```

**Quando Usar ALL()**:
- Cálculos de % do total
- Remover filtros específicos
- Contexto de tabela completa necessário

---

### 4. Monitore o Tamanho do Modelo

**Comandos Úteis**:
```dax
// Ver tamanho por tabela
// Use DAX Studio ou Tabular Editor
```

**Metas de Tamanho**:
- < 100 MB: Excelente
- 100-500 MB: Bom
- 500 MB - 1 GB: Aceitável
- \> 1 GB: Considere otimizações

**Técnicas de Otimização**:
1. Remova colunas desnecessárias
2. Use tipos de dados apropriados
3. Considere agregações
4. Remova duplicatas

---

### 5. Teste Performance Regularmente

**Ferramentas**:
- **DAX Studio**: Análise de queries
- **Performance Analyzer** (Power BI): Tempo de visuais
- **Tabular Editor**: Análise de modelo

**Métricas para Monitorar**:
- Tempo de refresh
- Tempo de renderização de visuais
- Tamanho do modelo
- Tempo de queries DAX

---

## 📝 Nomenclatura

### Tabelas

**Convenções**:
- **f**: Fato (ex: fVendas, fMetas)
- **d**: Dimensão (ex: dClientes, dProdutos)
- **_**: Medidas (ex: _Medidas)
- **z**: Auxiliar (ex: zMetricas)

**Formato**: PascalCase
- ✅ `fVendas`
- ❌ `f_vendas` ou `fvendas`

---

### Colunas

**Formato**: PascalCase ou Com Espaços

✅ **Aceitável**:
- `IdCliente` ou `Id Cliente`
- `ValorUnit` ou `Valor Unit`

**Consistência**: Escolha um padrão e mantenha

**Evite**:
- `id_cliente` (snake_case)
- `IDCLIENTE` (UPPER_CASE)

---

### Medidas

**Já Coberto**: Ver seção "Medidas DAX"

---

## 📚 Documentação

### 1. Descrições de Medidas

**Template**:
```
[Nome da Medida]: [Descrição concisa do que calcula]

Opcional:
- Fórmula em linguagem natural
- Quando usar
- Notas especiais
```

**Exemplo**:
```
04 Margem Bruta: Margem Bruta (%) = (Faturamento - Custo) / Faturamento

Diferente de 10 Margem (líquida) que considera todas as deduções.
Use para análise de precificação e rentabilidade operacional.
```

---

### 2. Documentação Externa

**Mantenha Atualizado**:
- ✅ Visão Geral (README)
- ✅ Dicionário de Dados
- ✅ Guia de Medidas
- ✅ Changelog

**Quando Atualizar**:
- Após adicionar/remover tabelas
- Após adicionar/modificar medidas importantes
- Após mudanças estruturais
- Versionamento (ex: v2.0 → v2.1)

---

### 3. Comentários em M (Power Query)

**Estrutura**:
```m
// Passo 1: Carregar dados fonte
let
    Fonte = ...
    
// Passo 2: Filtrar registros válidos
    Filtrado = ...
    
// Passo 3: Transformar tipos
    TiposAlterados = ...
in
    TiposAlterados
```

---

## 🧪 Testes

### 1. Validação de Dados

**Checklist**:
- [ ] Chaves estrangeiras têm correspondência?
- [ ] Não há duplicatas em dimensões?
- [ ] Datas estão em formato correto?
- [ ] Não há valores negativos onde não deveria?

**Medidas de Validação**:
```dax
// Vendas sem cliente
Vendas Órfãs = 
CALCULATE(
    COUNTROWS(fVendas),
    ISBLANK(RELATED(dClientes[Nome]))
)
// Deve retornar 0

// Duplicatas em dimensão
Duplicatas Cliente = 
COUNTROWS(dClientes) - DISTINCTCOUNT(dClientes[Id Cliente])
// Deve retornar 0
```

---

### 2. Teste de Medidas

**Cenários de Teste**:
1. **Caso Normal**: Dados típicos
2. **Caso Limite**: Valores extremos
3. **Caso Nulo**: Sem dados
4. **Caso Erro**: Divisão por zero

**Exemplo**:
```dax
// Testar se margem funciona com faturamento zero
// Resultado esperado: BLANK() (não erro)
Teste Margem = [10 Margem]
// Aplicar filtro onde faturamento = 0
```

---

### 3. Testes de Regressão

**Após Mudanças**:
- [ ] Medidas principais ainda funcionam?
- [ ] Valores totalizam corretamente?
- [ ] Visuais ainda renderizam?
- [ ] Performance não degradou significativamente?

---

## 🔧 Manutenção

### 1. Backup Regular

**Frequência**: Antes de mudanças significativas

**Versionamento**:
```
Performance-Comercial_v2.0.0_2026-01-30.pbix
Performance-Comercial_v2.0.1_2026-02-05.pbix
```

---

### 2. Limpeza Periódica

**Mensal**:
- [ ] Remover medidas não utilizadas
- [ ] Remover colunas não utilizadas
- [ ] Verificar queries não utilizadas
- [ ] Limpar cache

**Trimestral**:
- [ ] Revisar estrutura do modelo
- [ ] Avaliar performance
- [ ] Atualizar documentação
- [ ] Arquivar versões antigas

---

### 3. Monitoramento de Uso

**Métricas**:
- Visuais mais utilizados
- Medidas mais consultadas
- Horários de pico
- Tempo de resposta

**Ferramentas**:
- Power BI Service (Premium)
- Application Insights
- Logs personalizados

---

### 4. Atualizações de Dados

**Checklist**:
- [ ] Refresh automático configurado?
- [ ] Tratamento de erros implementado?
- [ ] Notificações de falha ativas?
- [ ] Log de refresh verificado regularmente?

---

## ✅ Checklist de Qualidade

### Antes de Publicar Mudanças

- [ ] Todos os testes passam
- [ ] Documentação atualizada
- [ ] Descrições de medidas novas preenchidas
- [ ] Changelog atualizado
- [ ] Backup criado
- [ ] Performance validada
- [ ] Revisão de código feita

---

### Revisão Mensal

- [ ] Performance do modelo aceitável
- [ ] Documentação ainda relevante
- [ ] Medidas obsoletas removidas
- [ ] Novos requisitos identificados
- [ ] Feedback de usuários coletado

---

## 📖 Recursos Recomendados

### Leitura Essencial
1. [DAX Patterns](https://www.daxpatterns.com/)
2. [SQLBI Articles](https://www.sqlbi.com/articles/)
3. [Power BI Best Practices](https://docs.microsoft.com/power-bi/guidance/)

### Ferramentas
1. **DAX Studio**: Análise e otimização de queries
2. **Tabular Editor**: Edição avançada de modelo
3. **ALM Toolkit**: Comparação de modelos
4. **Power BI Helper**: Documentação automática

### Comunidades
1. Power BI Community Forum
2. Reddit: r/PowerBI
3. Stack Overflow: power-bi tag

---

**Documento criado em:** 30/01/2026  
**Mantido por:** Equipe de BI - Campeão Distribuição e Logística Ltda  
**Versão do Documento:** 1.0  
**Próxima Revisão:** 30/04/2026
