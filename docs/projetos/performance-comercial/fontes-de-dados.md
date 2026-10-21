# Fontes de dados

De onde vêm os dados do modelo, lido das partições (`tables/*.tmdl`) e das expressões compartilhadas (`expressions.tmdl`).

Os dados deste projeto são **fictícios**, criados para o portfólio. Não existe sistema de origem nem pipeline por trás das planilhas.

## Resumo por conector

| Conector | Destino | Tabelas | Atualização | Responsável |
|---|---|---|---|---|
| Excel (`Excel.Workbook`), arquivo `Vendas.xlsx` | `Caminho_Extracao` | `fVendas` | Manual, no Power BI Desktop. Dados fixos, de 2018 a 2021 | Desenvolvedor do projeto |
| Excel (`Excel.Workbook`), arquivo `Dimensões.xlsx` | `Caminho_Dimensoes` | `dClientes`, `dProdutos`, `dVendedores`, `dUnidades`, `dStatus`, `dPagamento` e a consulta `dCidades` | Manual. Dados fixos | Desenvolvedor do projeto |
| Pasta com planilhas Excel (`Folder.Files`), uma por ano | `Caminho_Meta` | `fMetas` | Manual. Dados fixos, de 2018 a 2021 | Desenvolvedor do projeto |
| Gerada no Power Query (sem arquivo) | — | `dCalendario` | Fixa: 1.461 dias a partir de 01/01/2018 | Desenvolvedor do projeto |
| Tabela digitada no Power Query (sem arquivo) | — | `zMetricas` | Fixa | Desenvolvedor do projeto |

Todas as tabelas usam o modo **Import**: os dados são copiados para o modelo quando alguém usa **Atualizar** no Power BI Desktop. O repositório não tem agendamento de atualização. Como os dados não recebem valores depois de 31/12/2021, não há necessidade de atualização periódica.

O responsável é o autor do projeto, Ricardo Filgueiras, segundo o `README.md` do repositório.

## Fronteira com o pipeline

A documentação deste projeto começa na fonte que o modelo lê. O que acontece antes (por exemplo, dentro de um fluxo de dados) é de outro projeto e fica documentado lá.

Neste projeto **não existe etapa anterior**: as planilhas ficam no próprio repositório, na pasta `data/`, e são lidas diretamente pelo modelo.

| Fonte consumida | Equipe responsável | Documentação do pipeline | Horário de atualização | Colunas que o painel usa |
|---|---|---|---|---|
| `data/Extrações/Vendas.xlsx`, aba `fVendas` | Desenvolvedor do projeto | Não há | Sem atualização | 15 das 20 colunas da planilha (ver [`fVendas`](modelo-de-dados.md#fvendas)) |
| `data/Dimensões/Dimensões.xlsx`, tabelas `Clientes`, `Cidades`, `Produtos`, `Vendedores`, `Unidades`, `Status` e `Pagamento` | Desenvolvedor do projeto | Não há | Sem atualização | Todas as colunas de cada tabela |
| `data/Metas/Meta AAAA.xlsx` (2018 a 2021) | Desenvolvedor do projeto | Não há | Sem atualização | Id do vendedor e os 12 meses |

O cabeçalho da planilha de vendas traz o título "Microsiga Protheus", o nome de um ERP. Isso sugere que o layout da planilha imita a extração desse sistema, mas, como os dados são fictícios, não há ERP real por trás.

Os arquivos `data/Metas/Catalogo.pdf` e a pasta `data/imagens/` ficam no repositório, mas nenhuma consulta do modelo os lê.

## Transformações no Power Query

| Tabela | Transformações antes da carga |
|---|---|
| `fVendas` | Lê a aba `fVendas` de `Vendas.xlsx`. A aba começa com linhas de título: a consulta promove a primeira linha a cabeçalho, remove as linhas em que a terceira coluna está vazia e promove a linha seguinte a cabeçalho definitivo. Define os tipos, renomeia `Data` para `Data Pedido` e **mantém só 15 das 20 colunas**. Ficam de fora `Nome Vendedor`, `Nome Cliente`, `Nome Unidade`, `Faturamento Total` e `Custo Total` |
| `fMetas` | Lê todos os `.xlsx` da pasta de metas e ignora arquivos temporários do Excel (nome iniciado por `~`). Junta as planilhas, promove o cabeçalho, remove linhas de título, **transforma as colunas dos 12 meses em linhas** (`Mes` e `Valor Meta`), monta a data com o mês e o ano tirado do nome do arquivo e define os tipos |
| `dCalendario` | Gera 1.461 datas a partir de 01/01/2018 e calcula ano, nome do mês, mês, dia, semestre, trimestre, mês abreviado, mês-ano e a chave de ordenação. Renomeia `Data` para `Id Data` |
| `dClientes` | Lê a tabela `Clientes`, junta com a consulta `dCidades` pelo `Id Cidade` (junção à esquerda) para trazer cidade, UF e estado, e mantém 5 colunas |
| `dProdutos`, `dVendedores`, `dUnidades`, `dStatus`, `dPagamento` | Leem a tabela correspondente de `Dimensões.xlsx` e só definem os tipos das colunas |
| `dCidades` (consulta, não vira tabela) | Lê a tabela `Cidades` de `Dimensões.xlsx`, define os tipos e remove espaços das pontas de `Estado` |
| `zMetricas` | Tabela digitada no próprio Power Query, com as colunas `Metrica` e `Ordem` |
| `_Medidas` | Tabela vazia (sem colunas), usada só para guardar medidas |

!!! warning "Dependência do nome do primeiro arquivo de metas"
    A consulta `fMetas` usa o texto `Meta 2018.xlsx` como **nome de coluna** em duas etapas (tipo e extração do ano). Essa coluna recebe esse nome porque o arquivo `Meta 2018.xlsx` é o primeiro da pasta. Se ele for renomeado ou removido, a consulta falha. A coluna também só funciona para arquivos com nome no formato `Meta AAAA.xlsx`.

!!! pendente "A confirmar"
    A consulta `fMetas` lê 15 colunas de cada planilha de meta (`Column1` a `Column15`). Confirmar se todas as planilhas têm esse mesmo formato (Id do vendedor, nome do vendedor e os 12 meses).

## Parâmetros

| Parâmetro | Valor | Uso |
|---|---|---|
| `Caminho_Extracao` | `C:\Github\Performace-Comercial\data\Extrações` | Pasta de `Vendas.xlsx`. Lido por `fVendas` |
| `Caminho_Dimensoes` | `C:\Github\Performace-Comercial\data\Dimensões` | Pasta de `Dimensões.xlsx`. Lido por `dClientes`, `dProdutos`, `dVendedores`, `dUnidades`, `dStatus`, `dPagamento` e `dCidades` |
| `Caminho_Meta` | `C:\Github\Performace-Comercial\data\Metas` | Pasta das planilhas de meta. Lido por `fMetas` |

Os três ficam no grupo de consultas **Parâmetros de dados**. Os valores são caminhos absolutos para a pasta `data/` da cópia local do repositório. Quem clonar o projeto em outro lugar precisa **atualizar os três parâmetros** antes de atualizar os dados. O passo a passo está em [Como atualizar o valor dos parâmetros](#como-atualizar-o-valor-dos-parametros).

## Como atualizar o valor dos parâmetros

Os arquivos de dados são planilhas Excel guardadas na pasta `data/` do repositório, junto com o projeto. Os parâmetros guardam o caminho dessa pasta no seu computador. Depois de clonar o repositório, faça uma vez:

1. Clone o repositório e anote o caminho da pasta `data/`, por exemplo `C:\Users\voce\repos\Performace-Comercial\data`.
2. Abra o arquivo `src/projeto/performance-comercial/Performance Comercial.pbip` no Power BI Desktop.
3. Na guia **Página Inicial**, clique em **Transformar dados** e escolha **Editar parâmetros**.
4. Preencha os três parâmetros com o caminho de cada subpasta:

    | Parâmetro | Valor |
    |---|---|
    | `Caminho_Extracao` | `<caminho do repositório>\data\Extrações` |
    | `Caminho_Dimensoes` | `<caminho do repositório>\data\Dimensões` |
    | `Caminho_Meta` | `<caminho do repositório>\data\Metas` |

5. Clique em **OK** e, na faixa amarela, em **Aplicar alterações**. O Power BI recarrega os dados.
6. Confira se os cartões do relatório mostram valores e se nenhuma consulta apresenta erro.

!!! warning "Cuidados"
    - Não renomeie as subpastas `Extrações`, `Dimensões` e `Metas`, nem os arquivos `Vendas.xlsx` e `Dimensões.xlsx`: as consultas procuram esses nomes.
    - Não renomeie `Meta 2018.xlsx` (ver o aviso em *Transformações no Power Query*).
    - Se o Power BI avisar que o caminho não existe, confira acentos e barras no valor do parâmetro.

!!! pendente "A confirmar"
    Os passos acima descrevem a interface do Power BI Desktop em português e não foram executados na escrita desta documentação. O desenvolvedor deve conferir os nomes dos botões na versão que usa.

## Consultas sem uso aparente

Todas as consultas e parâmetros do modelo são lidos por alguma tabela. A consulta `dCidades` é usada por `dClientes` e os três parâmetros são usados pelas tabelas listadas acima.

Do lado dos arquivos, `Catalogo.pdf` e `data/imagens/` não são lidos por nenhuma consulta. Colunas da planilha de vendas que a consulta descarta: `Nome Vendedor`, `Nome Cliente`, `Nome Unidade`, `Faturamento Total` e `Custo Total`.
