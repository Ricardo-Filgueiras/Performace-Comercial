# Metodologia DataOps

## O que é DataOps

DataOps é uma abordagem colaborativa que aplica às equipes de dados os princípios do DevOps e do Agile Manufacturing: automação, entrega contínua, testes, monitoramento e cultura de melhoria permanente.

O termo *DataOps* apareceu em 2014, num artigo de Lenny Liebmann na InformationWeek. Os princípios foram reunidos no *DataOps Manifesto*, publicado e mantido pela **DataKitchen**, empresa de Christopher Bergh, coautor do Manifesto. Ele foi inspirado no *Manifesto Ágil* e tem a mesma estrutura: cinco valores e 18 princípios.

Os cinco valores comparam duas coisas e dão preferência à primeira, sem descartar a segunda:

| Valorizamos mais… | …do que |
|---|---|
| Pessoas e interações | processos e ferramentas |
| Análises que funcionam | documentação extensa |
| Colaboração com o cliente | negociação de contratos |
| Experimentação, iteração e feedback | projeto extenso feito antes |
| Responsabilidade compartilhada pela operação | responsabilidades isoladas |

Não se trata de uma ferramenta ou plataforma. É uma mudança de mentalidade sobre como dados são produzidos, documentados e entregues.

---

## Os três pilares

### People — Colaboração e cultura

Equipes de dados tendem a trabalhar em silos: o engenheiro cuida do pipeline, o analista cuida do modelo, o usuário de negócio consome o relatório — sem comunicação sistemática entre os três. DataOps combate esse isolamento com **responsabilidade compartilhada**: quem produz os dados também é responsável por documentá-los e garantir sua qualidade.

### Process — Automação e entrega contínua

Os processos de dados precisam ser **reproduzíveis e auditáveis**. Isso inclui versionamento de pipelines, testes de qualidade dos dados, integração contínua e, em particular, o princípio que guia este portal:

**Documentation-as-code** — a documentação vive dentro do repositório, versionada junto com o código. Uma alteração em uma medida DAX e a atualização da sua documentação fazem parte do mesmo commit.

### Technology — Ferramentas que suportam o processo

A escolha das ferramentas deve servir ao processo, não o contrário. No portal de documentação de BI:

| Ferramenta | Função no fluxo DataOps |
|---|---|
| **PBIP (Power BI Project)** | Modelo semântico em TMDL e relatório em PBIR, ambos em texto versionável. Elimina o binário `.pbix` do Git. |
| **Git** | Controle de versão com histórico completo de cada alteração. A tag `<slug>/baseline-pre-documentacao` marca cada projeto antes da documentação. |
| **MkDocs Material** | Geração do site a partir dos arquivos Markdown de `docs/`, com a data de cada página tirada do Git. |
| **uv** | Instalação reproduzível do Python e das dependências do site (`pyproject.toml` + `uv.lock`). |
| **Agente de IA com a skill `documentacao-bi`** | Escreve as páginas seguindo o padrão; o autor revisa linha a linha e abre o pull request. |

As fontes de dados de cada painel (bancos, fluxos de dados, planilhas) são descritas na página **Fontes de dados** do projeto, e o motivo de usar DataOps em cada painel fica no **Sobre** do projeto.

---

## Documentation-as-code na prática

O princípio por trás do investimento em documentação é o da **Literate Programming** (Knuth, 1984): o código e a explicação do código devem coexistir. Uma medida DAX sem documentação é um ativo frágil: funciona hoje, mas ninguém sabe *por que* funciona, quais são seus limites ou como alterá-la com segurança.

O segundo valor do Manifesto (análises que funcionam acima de documentação extensa) vale aqui: a documentação se justifica quando ajuda o painel a funcionar e a ser mantido, não como fim em si.

```
Alteração no modelo
       │
       ▼
  git commit  ←────────────────────────────────────────┐
  feat: ajusta cálculo de taxa de retorno               │
  docs: documenta nova lógica em medidas-dax.md   ──────┘
       │
       ▼
  mkdocs build
       │
       ▼
  Site atualizado com data do commit (git-revision-date)
```

O plugin `git-revision-date-localized` mostra em cada página a data do último commit que a alterou. Essa data diz **quando** a página mudou, não **se** ela está correta. A correção depende de duas validações:

- **Técnica:** a revisão do pull request por outra pessoa do time de BI confirma que a página descreve o que o modelo faz.
- **De negócio:** o selo de validação na página registra que a área responsável confirmou a regra.

---

## Referências

As referências abaixo formam a base conceitual desta abordagem. São leituras recomendadas para quem quiser aprofundar:

**DataOps Manifesto**
> DataKitchen. *The DataOps Manifesto*. Disponível em: [dataopsmanifesto.org](https://dataopsmanifesto.org). Acesso em: 13 out. 2026.
> O documento de referência do movimento: cinco valores e 18 princípios (mais um 19º, "Comece testando os dados"). Christopher Bergh, fundador da DataKitchen, é coautor. O site não informa a data de publicação.

**Fundamentals of Data Engineering**
> Reis, J. & Housley, M. (2022). *Fundamentals of Data Engineering*. O'Reilly Media.
> O livro mais completo sobre o ciclo de vida da engenharia de dados moderno. Os capítulos sobre orquestração, armazenamento e gerenciamento de dados formam o pano de fundo técnico desta abordagem.

**Literate Programming**
> Knuth, D. E. (1984). *Literate Programming*. The Computer Journal, 27(2), 97–111.
> O artigo que introduziu a ideia de que programas devem ser escritos primeiramente para humanos lerem — e apenas secundariamente para máquinas executarem. Fundamento filosófico do documentation-as-code.

**DAMA-DMBOK**
> DAMA International (2017). *DAMA-DMBOK: Data Management Body of Knowledge* (2ª ed.). Technics Publications.
> O guia de referência para gestão de dados, cobrindo governança, qualidade, metadados e arquitetura. Fornece o vocabulário formal para as práticas de documentação adotadas aqui.
