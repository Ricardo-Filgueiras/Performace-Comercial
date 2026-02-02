# Requisitos do Projeto de BI: Dashboard Comercial (Power BI)

### 1. Objetivo do Projeto
Desenvolver um dashboard interativo no Power BI para análise comercial, com foco em vendas, lucro e desempenho por produto, região e período, destacando KPIs estratégicos para tomada de decisão.

---

### 2. Escopo Funcional

#### a. Indicadores Principais (KPIs)
- **Total de Vendas**
- **Lucro Bruto e Margem de Lucro**
- **Quantidade de Produtos Vendidos**
- **Ticket Médio**
- **Crescimento de Vendas (%)**
- **Meta vs Realizado**

#### b. Dimensões de Análise
- **Produto**: categoria, marca, SKU
- **Região**: estado, cidade, zona geográfica
- **Período**: dia, mês, trimestre, ano

#### c. Visualizações
- Gráficos de linha para evolução temporal
- Mapas geográficos para desempenho regional
- Tabelas dinâmicas com filtros por produto e região
- Cartões de KPIs com alertas visuais
- Segmentações por período e categoria

#### d. Interatividade
- Filtros dinâmicos (slicers) por produto, região e período
- Drill-down e drill-through para detalhamento
- Botões de navegação entre páginas do dashboard
- Tooltip com informações adicionais ao passar o mouse

---

### 3. Requisitos Técnicos

#### a. Fonte de Dados
- ERP ou sistema de vendas
- Planilhas Excel ou CSV
- Banco de dados SQL ou serviços em nuvem (Azure, Google BigQuery)

#### b. Modelagem de Dados
- Tabelas de fatos: Vendas, Lucros
- Tabelas de dimensão: Produto, Região, Tempo
- Relacionamentos bem definidos (modelo estrela ou snowflake)

#### c. Atualização
- Atualização automática diária ou sob demanda
- Controle de versão e histórico de dados

---

### 4. Requisitos de Segurança
- Controle de acesso por usuário (RLS – Row-Level Security)
- Proteção de dados sensíveis (criptografia e anonimização)

---

### 5. 📈 Métricas de Sucesso
- Tempo de resposta do dashboard < 5 segundos
- Aderência às metas de vendas e lucro
- Engajamento dos usuários (acessos e interações)
- Feedback positivo dos gestores comerciais

---

Se quiser, posso ajudar a criar o modelo de dados, os DAX para os KPIs ou até esboçar o layout visual do dashboard. Quer seguir por algum desses caminhos?
