# Padrão de documentação dos projetos de BI

Este padrão define como a documentação de cada projeto Power BI (PBIP) é organizada e escrita no portal único de documentação de BI. Ele nasceu de um laboratório com um projeto piloto (2026-10) e da revisão de um conselho de especialistas. Cada regra traz o motivo, para que quem mantém saiba quando ela se aplica.

> Este padrão é **provisório**. Ele será revisado depois do segundo projeto documentado, com o que os dois projetos ensinarem.

O padrão está dividido por tema. **Não leia tudo de uma vez:** leia os dois primeiros no começo da sessão e os demais só quando a tarefa pedir.

| Arquivo | Conteúdo | Quando ler |
|---|---|---|
| `padrao-estrutura.md` (§1) | Estrutura do portal, pastas `docs/` e `src/`, slug, caminho do repositório | Início de toda sessão |
| `padrao-escrita.md` (§2) | 12 princípios de escrita: pendências, dois públicos, não inventar, dupla validação, fronteira de escopo | Início de toda sessão |
| `padrao-paginas.md` (§3) | Cada página de um projeto: o que contém e observações | Ao criar ou revisar páginas |
| `padrao-git.md` (§4) | Linha de base, tags, commits, mudança de lugar, `.gitignore` | Ao tocar em Git, tags ou PR |
| `padrao-mkdocs.md` (§5 e §6) | Setup do MkDocs, plugins, risco do MkDocs 2.0 e o que ficou para depois | Ao montar ou corrigir o portal, ou quando o build falhar |

Armadilhas já encontradas em projetos reais, com a decisão tomada em cada uma, estão em `armadilhas.md`. Consulte antes de improvisar.
