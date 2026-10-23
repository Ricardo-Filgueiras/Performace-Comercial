"""Gera as páginas mecânicas da documentação de um projeto PBIP.

Lê as pastas .SemanticModel (TMDL) e .Report (PBIR) em --root (somente leitura) e escreve,
em --docs, as páginas cujo conteúdo vem 100% do modelo:

    modelo-de-dados.md      visão geral, diagrama ER (Mermaid), tabelas e colunas,
                            hierarquias, grupos de cálculo e papéis de segurança (RLS)
    medidas-dax/index.md    catálogo (pastas de exibição e lista A-Z)
    medidas-dax/<pasta>.md  uma página por pasta de exibição, uma seção por medida
    medidas-dax/sem-pasta.md

O que o modelo não diz (descrição de negócio, regras, escopo) continua sendo escrito pelo
agente e revisado pelo autor. Para isso, o conteúdo gerado fica entre marcadores:

    <!-- gerado:inicio medida:Faturamento -->
    ...
    <!-- gerado:fim medida:Faturamento -->

A cada execução só o que está entre marcadores é reescrito. Tudo o que está fora
(descrições, observações, regras) é preservado. Escreva sempre ACIMA do bloco gerado.
Seção cujo item saiu do modelo não é apagada: o bloco vira um aviso de pendência.

Uso (na raiz do portal):
    python <pasta-da-skill>/scripts/gerar_paginas.py \\
        --root src/<slug> --docs docs/projetos/<slug>
    ... --check      não escreve; sai com código 1 se alguma página estiver desatualizada
    ... --dry-run    mostra o que seria criado ou alterado, sem escrever

Nunca escreve dentro de --root. No Windows, rode com PYTHONUTF8=1.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from levantamento import carregar_projeto, unquote  # noqa: E402

LIMITE_ER = 15  # acima disso, o diagrama é dividido em visões por tabela fato
MARCA_MODELO = "<!-- modelo-nao-preenchido"  # primeira linha dos modelos que o gerador assume


# --------------------------------------------------------------------------- utilidades

def slugify(texto: str) -> str:
    """Mesmo critério do MkDocs (toc): sem acento, minúsculas, hífen entre palavras."""
    v = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    v = re.sub(r"[^\w\s-]", "", v).strip().lower()
    return re.sub(r"[-\s]+", "-", v)


def slug_arquivo(texto: str) -> str:
    """Nome de arquivo a partir de uma pasta de exibição: '01.Principais' -> '01-principais'."""
    v = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-")


def rid(nome: str) -> str:
    """Identificador seguro para usar dentro de um comentário HTML."""
    return re.sub(r"--|[<>]", lambda m: "".join(f"%{ord(c):02X}" for c in m.group()), nome)


def esc(texto: str) -> str:
    """Escapa o texto para uma célula de tabela Markdown."""
    return str(texto).replace("|", "\\|").replace("\n", " ")


def codigo(texto: str, linguagem: str = "dax") -> str:
    cerca = "```"
    while cerca in texto:
        cerca += "`"
    return f"{cerca}{linguagem}\n{texto}\n{cerca}"


def ini(i: str) -> str:
    return f"<!-- gerado:inicio {i} -->"


def fim(i: str) -> str:
    return f"<!-- gerado:fim {i} -->"


def bloco(i: str, conteudo: str) -> str:
    return f"{ini(i)}\n{conteudo.strip()}\n{fim(i)}"


def pendente(titulo: str, texto: str) -> str:
    return f'!!! pendente "{titulo}"\n    {texto}'


# --------------------------------------------------------------------------- sincronização

@dataclass
class Regiao:
    id: str
    conteudo: str          # o que vai entre os marcadores
    novo: str              # texto completo ao criar a seção (título + espaço manual + bloco)
    trocar: tuple[str, str] | None = None  # (texto padrão antigo, texto novo) logo acima do bloco


REMOVIDO = pendente(
    "Removido do modelo",
    "Este item não existe mais no modelo. Mova a seção para `arquivo/` ou apague-a, "
    "e registre no changelog.",
)


def _achar(texto: str, i: str) -> tuple[int, int] | None:
    a = texto.find(ini(i))
    if a < 0:
        return None
    f = texto.find(fim(i), a)
    if f < 0:
        raise SystemExit(f"Marcador sem fim: {ini(i)}. Corrija a página à mão.")
    return a, f + len(fim(i))


def _inicio_da_secao(texto: str, pos_ini: int, limite_inferior: int) -> int:
    """Posição do título (## ou ###) mais próximo acima do bloco, sem passar do limite."""
    trecho = texto[limite_inferior:pos_ini]
    ultimo = None
    for m in re.finditer(r"(?m)^#{2,4} .*$", trecho):
        ultimo = m
    return limite_inferior + ultimo.start() if ultimo else pos_ini


def sincronizar(texto: str | None, head: str, regioes: list[Regiao]) -> tuple[str, list[str]]:
    """Devolve (texto novo, avisos). `texto` é o conteúdo atual da página ou None."""
    avisos: list[str] = []
    if texto is None:
        corpo = "\n\n".join(r.novo for r in regioes)
        return head.rstrip() + "\n\n" + corpo + "\n", avisos

    ids = [r.id for r in regioes]
    # 1. regiões que saíram do modelo
    for m in list(re.finditer(r"<!-- gerado:inicio (.+?) -->", texto)):
        i = m.group(1)
        if i not in ids:
            pos = _achar(texto, i)
            if pos and texto[pos[0]:pos[1]] != bloco(i, REMOVIDO):
                texto = texto[:pos[0]] + bloco(i, REMOVIDO) + texto[pos[1]:]
                avisos.append(f"saiu do modelo: {i}")
    # 2. regiões existentes e novas
    for n, r in enumerate(regioes):
        pos = _achar(texto, r.id)
        if pos:
            texto = texto[:pos[0]] + bloco(r.id, r.conteudo) + texto[pos[1]:]
            if r.trocar:
                antigo = r.trocar[0] + "\n\n" + ini(r.id)
                if antigo in texto:
                    texto = texto.replace(antigo, r.trocar[1] + "\n\n" + ini(r.id), 1)
            continue
        # nova: entra antes da seção da próxima região que já existe; senão, no fim
        destino = None
        anterior_fim = 0
        for outra in reversed(regioes[:n]):
            p = _achar(texto, outra.id)
            if p:
                anterior_fim = p[1]
                break
        for outra in regioes[n + 1:]:
            p = _achar(texto, outra.id)
            if p:
                destino = _inicio_da_secao(texto, p[0], anterior_fim)
                break
        novo = r.novo
        if novo.startswith("## Tabelas\n\n") and "\n## Tabelas\n" in texto:
            novo = novo.split("\n\n", 1)[1]
        if destino is None:
            texto = texto.rstrip() + "\n\n" + novo + "\n"
        else:
            texto = texto[:destino] + novo + "\n\n" + texto[destino:]
    return texto, avisos


# --------------------------------------------------------------------------- modelo de dados

RE_REF_COL = re.compile(r"^('(?:[^']|'')*'|[^.]+)\.(.+)$")


def separar_ref(ref: str | None) -> tuple[str | None, str | None]:
    if not ref:
        return None, None
    m = RE_REF_COL.match(ref)
    if not m:
        return None, ref
    return unquote(m.group(1)), unquote(m.group(2))


def mer(nome: str) -> str:
    return re.sub(r"\W", "_", nome)


def diagrama_er(rels: list[dict], negocio: set[str]) -> str:
    """Mermaid erDiagram. Só relacionamentos entre tabelas de negócio."""
    itens = []
    for r in rels:
        t1, c1 = separar_ref(r["de"])
        t2, c2 = separar_ref(r["para"])
        if t1 in negocio and t2 in negocio:
            itens.append((t1, c1, t2, c2, r))

    def linha(t1, c1, t2, c2, r) -> str:
        esq = "}o" if r["de_card"] == "many" else "||"
        dir_ = "||" if r["para_card"] == "one" else "o{"
        traco = "--" if r["ativo"] else ".."
        rotulo = c1 if c1 == c2 else f"{c1} = {c2}"
        if r["filtro"] == "bothDirections":
            rotulo += " (bidirecional)"
        rotulo = rotulo.replace('"', "'")
        return f'    {mer(t1)} {esq}{traco}{dir_} {mer(t2)} : "{rotulo}"'

    def mermaid(partes) -> str:
        return "```mermaid\nerDiagram\n" + "\n".join(linha(*p) for p in partes) + "\n```"

    if not itens:
        return "Nenhum relacionamento entre tabelas de negócio."
    if len(itens) <= LIMITE_ER:
        return mermaid(itens)
    grupos: dict[str, list] = defaultdict(list)
    for p in itens:
        grupos[p[0]].append(p)
    saida = []
    for t in sorted(grupos):
        saida.append(f"### Visão: `{t}`\n\n{mermaid(grupos[t])}")
    saida.append(f"### Visão completa\n\n{mermaid(itens)}")
    return "\n\n".join(saida)


def tipo_tabela(t: dict, lado_de: set[str], lado_para: set[str]) -> str:
    if t["nome"] in lado_de:
        return "fato"
    if t["nome"] in lado_para:
        return "dimensão"
    if t["medidas"] and not t["colunas"]:
        return "auxiliar (só medidas)"
    return "auxiliar"


def origem_tabela(t: dict) -> str:
    if not t["particoes"]:
        return "—"
    partes = []
    for p in t["particoes"]:
        if p["tipo"] == "calculated":
            partes.append("tabela calculada (DAX)")
        else:
            con = ", ".join(p["conectores"]) or ("consulta M" if p["tipo"] == "m" else p["tipo"])
            partes.append(f"{con} ({p['modo'] or 'import'})")
    return "; ".join(dict.fromkeys(partes))


def secao_tabela(t: dict, lado_de, lado_para, link_fontes: str, link_medidas: str) -> str:
    linhas = [
        f"- **Tipo (inferido):** {tipo_tabela(t, lado_de, lado_para)}",
        f"- **Origem:** {origem_tabela(t)} (ver {link_fontes})",
    ]
    if t["oculta"]:
        linhas.append("- **Oculta:** sim")
    if t["medidas"]:
        linhas.append(f"- **Medidas:** {len(t['medidas'])} (ver {link_medidas})")
    if t["colunas"]:
        linhas += ["", "| Coluna | Tipo | Calculada | Observação |", "|---|---|---|---|"]
        for c in t["colunas"]:
            obs = ", ".join(x for x in ["oculta" if c["oculta"] else "",
                                        "ver expressão abaixo" if c["calculada"] else ""] if x)
            linhas.append(f"| `{esc(c['nome'])}` | {esc(c['tipo'])} | "
                          f"{'sim' if c['calculada'] else 'não'} | {obs} |")
    else:
        linhas += ["", "Tabela sem colunas (contém apenas medidas)."]
    for p in t["particoes"]:
        if p["tipo"] == "calculated" and p["fonte"]:
            linhas += ["", '??? abstract "Expressão DAX da tabela"', "",
                       indent_bloco(codigo(p["fonte"]))]
    calc = [c for c in t["colunas"] if c["calculada"] and c["expressao"]]
    if calc:
        linhas += ["", '??? abstract "Expressões das colunas calculadas"', ""]
        for c in calc:
            linhas += [f"    **`{c['nome']}`**", "", indent_bloco(codigo(c["expressao"])), ""]
    return "\n".join(linhas)


def indent_bloco(texto: str, n: int = 4) -> str:
    pad = " " * n
    return "\n".join((pad + ln) if ln else ln for ln in texto.splitlines())


def conteudo_hierarquias(tabelas: list[dict]) -> str:
    linhas = ["| Tabela | Hierarquia | Níveis (coluna) |", "|---|---|---|"]
    for t in tabelas:
        for h in t["hierarquias"]:
            niveis = " → ".join(
                f"{n['nome']}" + (f" (`{n['coluna']}`)" if n["coluna"] and n["coluna"] != n["nome"] else "")
                for n in h["niveis"])
            linhas.append(f"| `{esc(t['nome'])}` | {esc(h['nome'])} | {esc(niveis)} |")
    return "\n".join(linhas)


def conteudo_grupos(tabelas: list[dict]) -> str:
    saida = []
    for t in tabelas:
        g = t["grupo_calculo"]
        if not g:
            continue
        cab = f"**`{t['nome']}`**" + (f" (precedência {g['precedencia']})" if g["precedencia"] else "")
        saida.append(cab)
        for it in g["itens"]:
            saida.append(f"\n- **{it['nome']}**\n\n{indent_bloco(codigo(it['expressao']), 4)}")
        saida.append("")
    return "\n".join(saida)


def conteudo_rls(papeis: list[dict]) -> str:
    saida = ["Os membros de cada papel são atribuídos no serviço do Power BI e não constam nos "
             "arquivos do projeto.", ""]
    for p in papeis:
        saida.append(f"**Papel `{p['nome']}`** (permissão: {p['permissao'] or 'não informada'})")
        if not p["filtros"]:
            saida += ["", "Sem filtro de tabela: o papel não restringe linhas.", ""]
            continue
        saida.append("")
        for f in p["filtros"]:
            if "\n" in f["filtro"]:
                saida += [f"- Tabela `{f['tabela']}`:", "", indent_bloco(codigo(f["filtro"]), 4)]
            else:
                saida.append(f"- Tabela `{f['tabela']}`: `{f['filtro']}`")
        saida.append("")
    return "\n".join(saida)


def paginas_modelo(d: dict, docs: Path) -> tuple[str, str, list[Regiao]]:
    tabelas = [t for t in d["tabelas"] if not t["auto_data"]]
    auto = len(d["tabelas"]) - len(tabelas)
    nomes = {t["nome"] for t in tabelas}
    lado_de, lado_para = set(), set()
    ativos = inativos = 0
    for r in d["rels"]:
        t1, _ = separar_ref(r["de"])
        t2, _ = separar_ref(r["para"])
        if t1 in nomes and t2 in nomes:
            lado_de.add(t1)
            lado_para.add(t2)
            if r["ativo"]:
                ativos += 1
            else:
                inativos += 1
    modos = sorted({(p["modo"] or "import") for t in tabelas for p in t["particoes"]
                    if p["tipo"] != "calculated"})
    med = d["medidas"]
    n_pastas = len({m["pasta"] for m in med if m["pasta"]})
    link_fontes = link_se_existe(docs, "modelo-de-dados.md", "fontes-de-dados.md", "Fontes de dados")
    link_medidas = "[Medidas DAX](medidas-dax/index.md)"

    visao = [
        f"- **{len(d['tabelas'])} tabelas**: {len(tabelas)} de negócio e {auto} de data automática.",
        f"- **{ativos + inativos} relacionamentos** entre tabelas de negócio "
        f"(ativos: {ativos}; inativos: {inativos}).",
        f"- **Modo de armazenamento:** {', '.join(modos) if modos else 'não informado'}.",
        f"- **{len(med)} medidas** em {n_pastas} pastas de exibição ({link_medidas}).",
        f"- **Hierarquias:** {sum(len(t['hierarquias']) for t in tabelas)}. "
        f"**Grupos de cálculo:** {sum(bool(t['grupo_calculo']) for t in tabelas)}.",
        f"- **Papéis de segurança (RLS):** "
        + (f"{len(d['papeis'])}." if d["papeis"] else "nenhum papel definido no modelo."),
    ]
    head = (
        f"# Modelo de dados\n\n"
        f"Dicionário de dados do modelo semântico `{d['projeto']}.SemanticModel`: tabelas, colunas, "
        f"tipos e relacionamentos, lidos dos arquivos `.tmdl`.\n\n"
        '!!! info "Classificação inferida"\n'
        "    A classificação fato / dimensão / auxiliar foi **inferida** pelos relacionamentos de cada "
        "tabela. O modelo não registra essa classificação.\n\n"
        '!!! info "Como esta página é mantida"\n'
        "    Os blocos entre marcadores `gerado` são reescritos por `gerar_paginas.py`. "
        "Escreva observações acima do bloco, nunca dentro dele."
    )
    regioes = [
        Regiao("visao-geral", "\n".join(visao),
               "## Visão geral\n\n" + bloco("visao-geral", "\n".join(visao))),
        Regiao("er", diagrama_er(d["rels"], nomes),
               "## Diagrama ER\n\nSó os relacionamentos entre tabelas de negócio. Linha tracejada = "
               "relacionamento **inativo**. Nos nomes de tabela, caracteres especiais viram `_`.\n\n"
               + bloco("er", diagrama_er(d["rels"], nomes))),
    ]
    primeira = True
    for t in tabelas:
        c = secao_tabela(t, lado_de, lado_para, link_fontes, link_medidas)
        titulo = "## Tabelas\n\n" if primeira else ""
        primeira = False
        regioes.append(Regiao(f"tabela:{rid(t['nome'])}", c,
                              f"{titulo}### `{t['nome']}`\n\n" + bloco(f"tabela:{rid(t['nome'])}", c)))
    if any(t["hierarquias"] for t in tabelas):
        c = conteudo_hierarquias(tabelas)
        regioes.append(Regiao("hierarquias", c, "## Hierarquias\n\n" + bloco("hierarquias", c)))
    if any(t["grupo_calculo"] for t in tabelas):
        c = conteudo_grupos(tabelas)
        regioes.append(Regiao("grupos-calculo", c, "## Grupos de cálculo\n\n" + bloco("grupos-calculo", c)))
    if d["papeis"]:
        c = conteudo_rls(d["papeis"])
        regioes.append(Regiao("rls", c, "## Segurança em nível de linha (RLS)\n\n" + bloco("rls", c)))
    return "modelo-de-dados.md", head, regioes


def link_se_existe(docs: Path, de: str, para: str, texto: str) -> str:
    """Link só se a página existir; senão texto simples (links quebrados falham o build --strict)."""
    if (docs / para).exists():
        rel = Path(para).relative_to(Path(de).parent) if Path(para).is_relative_to(Path(de).parent) \
            else Path("..") / para
        return f"[{texto}]({rel.as_posix()})"
    return texto


# --------------------------------------------------------------------------- medidas

def mapear_paginas_pasta(d: dict, docs: Path) -> dict[str, str]:
    """pasta de exibição -> nome do arquivo. Reaproveita o arquivo se a página já existe
    (marcador `<!-- pasta: NOME -->` na primeira linha), para a URL não mudar."""
    existentes: dict[str, str] = {}
    pasta_docs = docs / "medidas-dax"
    if pasta_docs.exists():
        for arq in pasta_docs.glob("*.md"):
            primeira = arq.read_text(encoding="utf-8").split("\n", 1)[0]
            m = re.match(r"<!-- pasta: (.+) -->$", primeira)
            if m:
                existentes[m.group(1)] = arq.name
    usados = set(existentes.values()) | {"index.md", "sem-pasta.md"}
    mapa: dict[str, str] = {}
    for m in d["medidas"]:
        pasta = m["pasta"]
        if not pasta or pasta in mapa:
            continue
        chave = rid(pasta)
        if chave in existentes:
            mapa[pasta] = existentes[chave]
            continue
        base = slug_arquivo(pasta) or "pasta"
        nome, n = f"{base}.md", 2
        while nome in usados:
            nome, n = f"{base}-{n}.md", n + 1
        usados.add(nome)
        mapa[pasta] = nome
    mapa[""] = "sem-pasta.md"
    return mapa


def conteudo_medida(m: dict, mapa_med: dict, pagina_atual: str, docs: Path) -> str:
    def ref(nome: str) -> str:
        pag, anc = mapa_med[nome]
        alvo = f"#{anc}" if pag == pagina_atual else f"{pag}#{anc}"
        return f"[`{nome}`]({alvo})"

    guias = []
    for g in m["guias"]:
        alvo = f"guias-do-relatorio/{slugify(g)}.md"
        guias.append(f"[{g}](../{alvo})" if (docs / alvo).exists() else f"*{g}*")
    linhas = [
        f"- **Tabela:** `{m['tabela']}`",
        f"- **Formato:** `{m['formato']}`" if m["formato"] else "- **Formato:** padrão",
    ]
    if m["oculta"]:
        linhas.append("- **Oculta:** sim")
    linhas += [
        f"- **Usada nas guias:** {', '.join(guias) if guias else 'nenhum visual'}",
        f"- **Depende de:** {', '.join(ref(n) for n in m['depende_de']) or 'nenhuma medida'}",
        f"- **É usada por:** {', '.join(ref(n) for n in m['usada_por']) or 'nenhuma medida'}",
        "",
        codigo(m["expressao"]),
    ]
    return "\n".join(linhas)


def descricao_padrao(m: dict) -> str:
    return pendente("A confirmar", f"O que a medida `{m['nome']}` mede? O modelo não tem `///` para ela.")


def paginas_medidas(d: dict, docs: Path) -> list[tuple[str, str, list[Regiao]]]:
    mapa = mapear_paginas_pasta(d, docs)
    mapa_med = {m["nome"]: (mapa[m["pasta"] or ""], slugify(m["nome"])) for m in d["medidas"]}
    por_pasta: dict[str, list[dict]] = defaultdict(list)
    for m in d["medidas"]:
        por_pasta[m["pasta"] or ""].append(m)
    paginas = []
    for pasta, itens in por_pasta.items():
        arq = mapa[pasta]
        if pasta:
            head = f"<!-- pasta: {rid(pasta)} -->\n# {pasta}"
        else:
            guia = link_se_existe(docs, "medidas-dax/sem-pasta.md", "guia-do-desenvolvedor.md",
                                  "guia do desenvolvedor")
            head = ("# Sem pasta de exibição\n\n"
                    "Medidas sem `displayFolder` no modelo, agrupadas pela tabela onde estão. Pela regra do "
                    f"{guia}, nenhuma medida deveria ficar sem pasta ao final de uma tarefa no modelo; "
                    "esta página registra o que existe.")
            itens = sorted(itens, key=lambda x: (x["tabela"], x["nome"].lower()))
        resumo = (f"Medidas da pasta de exibição `{pasta}`: **{len(itens)}**." if pasta
                  else f"Medidas sem pasta de exibição: **{len(itens)}**.") \
            + " Veja o [catálogo](index.md) para as outras pastas."
        regioes = [Regiao("resumo", resumo, bloco("resumo", resumo))]
        for m in sorted(itens, key=lambda x: (x["tabela"], x["nome"].lower()) if not pasta
                        else x["nome"].lower()):
            i = f"medida:{rid(m['nome'])}"
            c = conteudo_medida(m, mapa_med, arq, docs)
            padrao = descricao_padrao(m)
            manual = m["descricao"] or padrao
            regioes.append(Regiao(
                i, c, f"## {m['nome']}\n\n{manual}\n\n" + bloco(i, c),
                trocar=(padrao, m["descricao"]) if m["descricao"] else None))
        paginas.append((f"medidas-dax/{arq}", head, regioes))

    linhas = ["| Pasta de exibição | Medidas | Página |", "|---|---:|---|"]
    contagem = Counter(m["pasta"] or "" for m in d["medidas"])
    for pasta in sorted(p for p in contagem if p):
        linhas.append(f"| {esc(pasta)} | {contagem[pasta]} | [{esc(pasta)}]({mapa[pasta]}) |")
    if contagem.get(""):
        linhas.append(f"| *Sem pasta de exibição* | {contagem['']} | [Sem pasta de exibição](sem-pasta.md) |")
    linhas.append(f"| **Total** | {len(d['medidas'])} | |")
    linhas += ["", "### Todas as medidas (A–Z)", "", "| Medida | Pasta | Tabela |", "|---|---|---|"]
    for m in sorted(d["medidas"], key=lambda x: x["nome"].lower()):
        pag, anc = mapa_med[m["nome"]]
        linhas.append(f"| [{esc(m['nome'])}]({pag}#{anc}) | {esc(m['pasta'] or '—')} | `{esc(m['tabela'])}` |")
    cat = "\n".join(linhas)
    arquivo_arq = link_se_existe(docs, "medidas-dax/index.md", "arquivo/index.md", "Arquivo")
    head_idx = ("# Medidas DAX\n\n"
                "Catálogo das medidas do modelo, com uma página para cada **pasta de exibição**. "
                "As medidas sem pasta ficam em [Sem pasta de exibição](sem-pasta.md). "
                f"Medidas de teste e sem uso em visuais estão listadas no {arquivo_arq}.\n\n"
                "Para cada medida: tabela onde está, formato, guias em que aparece, de quais medidas "
                "depende, quais medidas a usam e o código DAX copiado do modelo.")
    paginas.insert(0, ("medidas-dax/index.md", head_idx, [Regiao("catalogo", cat, bloco("catalogo", cat))]))
    return paginas


# --------------------------------------------------------------------------- execução

def gerar(root: Path, docs: Path, projeto: str | None = None) -> tuple[dict[str, str], list[str], dict]:
    """Devolve ({caminho relativo: texto final}, avisos, resumo). Não escreve nada."""
    d = carregar_projeto(root, projeto)
    paginas = [paginas_modelo(d, docs)] + paginas_medidas(d, docs)
    # páginas de medidas que já existem mas não têm mais nenhuma medida no modelo (ex.: pasta
    # esvaziada): os blocos viram aviso de pendência, o texto manual fica
    geradas = {rel for rel, _, _ in paginas}
    pasta_medidas = docs / "medidas-dax"
    if pasta_medidas.exists():
        for arq in sorted(pasta_medidas.glob("*.md")):
            rel = f"medidas-dax/{arq.name}"
            if rel not in geradas and "<!-- gerado:inicio" in arq.read_text(encoding="utf-8"):
                paginas.append((rel, "", []))
    saida, avisos = {}, []
    for rel, head, regioes in paginas:
        arq = docs / rel
        atual = arq.read_text(encoding="utf-8") if arq.exists() else None
        if atual is not None and MARCA_MODELO in atual:
            atual = None  # cópia intacta do modelo: o gerador assume a página
        elif atual is not None and regioes and "<!-- gerado:inicio" not in atual:
            avisos.append(f"{rel}: página existente sem marcadores `gerado`; não foi alterada. "
                          "Para o gerador assumir a página, mova o conteúdo (ex.: para `arquivo/`) "
                          "e apague-a.")
            saida[rel] = atual
            continue
        novo, av = sincronizar(atual, head, regioes)
        saida[rel] = novo
        avisos += [f"{rel}: {a}" for a in av]
    resumo = {
        "medidas": len(d["medidas"]),
        "medidas_sem_descricao": sum(1 for m in d["medidas"] if not m["descricao"]),
        "medidas_sem_pasta": sum(1 for m in d["medidas"] if not m["pasta"]),
    }
    return saida, avisos, resumo


def validar_destino(root: Path, docs: Path) -> None:
    r, dd = root.resolve(), docs.resolve()
    if dd == r or r in dd.parents or dd in r.parents:
        raise SystemExit(f"--docs ({dd}) não pode ser, conter ou ficar dentro de --root ({r}): "
                         "o gerador nunca escreve nas pastas do Power BI.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Gera as páginas mecânicas da documentação de um projeto PBIP.")
    ap.add_argument("--root", required=True, help="pasta com o .pbip, por exemplo src/<slug>")
    ap.add_argument("--docs", required=True, help="pasta da documentação, por exemplo docs/projetos/<slug>")
    ap.add_argument("--projeto", help="nome das pastas .SemanticModel/.Report (detectado se omitido)")
    ap.add_argument("--check", action="store_true", help="não escreve; sai com 1 se houver página desatualizada")
    ap.add_argument("--dry-run", action="store_true", help="mostra o que mudaria, sem escrever")
    a = ap.parse_args()
    root, docs = Path(a.root), Path(a.docs)
    validar_destino(root, docs)
    saida, avisos, resumo = gerar(root, docs, a.projeto)

    criadas, alteradas, iguais = [], [], []
    for rel, texto in saida.items():
        arq = docs / rel
        if not arq.exists():
            criadas.append(rel)
        elif arq.read_text(encoding="utf-8") != texto:
            alteradas.append(rel)
        else:
            iguais.append(rel)
        if not (a.check or a.dry_run) and rel not in iguais:
            arq.parent.mkdir(parents=True, exist_ok=True)
            arq.write_text(texto, encoding="utf-8", newline="\n")

    print(f"criadas: {len(criadas)} | alteradas: {len(alteradas)} | sem mudança: {len(iguais)}")
    for rel in criadas:
        print(f"  + {rel}")
    for rel in alteradas:
        print(f"  ~ {rel}")
    for av in avisos:
        print(f"AVISO: {av}")
    print(f"medidas: {resumo['medidas']} | sem `///` no modelo: {resumo['medidas_sem_descricao']} "
          f"(ficam como pendência de descrição) | sem pasta: {resumo['medidas_sem_pasta']}")
    if a.check and (criadas or alteradas):
        print("check: páginas desatualizadas. Rode sem --check para regenerar.")
        raise SystemExit(1)
    if a.check:
        print("check: ok")


if __name__ == "__main__":
    main()
