"""Levantamento somente leitura de um projeto PBIP.

Lê as pastas .SemanticModel (TMDL) e .Report (PBIR) de um projeto e imprime os
indicadores usados na linha de base e na conferência da documentação. Também
calcula, para cada medida, de quais medidas ela depende, quais medidas a usam e
em quais guias do relatório ela aparece. Não escreve nada nas pastas do Power BI.

Uso (na raiz do portal):
    python .claude/skills/documentacao-bi/scripts/levantamento.py --root src/<slug>
    python ... --root src/<slug> --json .agente/levantamento-<slug>.json
    python ... --root src/<slug> --docs docs/projetos/<slug>

Sem --projeto, o script usa a única pasta *.SemanticModel que encontrar em --root.
No Windows, rode com PYTHONUTF8=1.

Para medir a linha de base exata, rode sobre uma cópia extraída da tag:
    T=$(mktemp -d)
    git archive <slug>/baseline-pre-documentacao | tar -x -C "$T"
    PYTHONUTF8=1 python ... --root "$T/src/<slug>"
    rm -rf "$T"
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


RE_TABLE = re.compile(r"^table ('(?:[^']|'')*'|\S+)")
RE_MEASURE = re.compile(r"^\tmeasure ('(?:[^']|'')*'|[^\s=]+)\s*=\s*(.*)$")
RE_COLUMN = re.compile(r"^\tcolumn ('(?:[^']|'')*'|[^\s=]+)(\s*=\s*(.*))?$")
RE_PARTITION = re.compile(r"^\tpartition (.+?) = (\w+)\s*$")
RE_PROP = re.compile(r"^\t\t(\w+)(?::\s*(.*))?$")

FONTES_M = [
    "SharePoint.Files", "SharePoint.Contents", "Excel.Workbook", "Csv.Document",
    "Sql.Database", "Oracle.Database", "Odbc.Query", "Odbc.DataSource",
    "PowerPlatform.Dataflows", "PowerBI.Dataflows", "Web.Contents",
    "Value.NativeQuery", "Table.Combine", "#table",
]


def unquote(name: str) -> str:
    if name.startswith("'") and name.endswith("'"):
        return name[1:-1].replace("''", "'")
    return name


def indent(line: str) -> int:
    return len(line) - len(line.lstrip("\t"))


def coletar_bloco(lines: list[str], i: int, primeira: str) -> tuple[list[str], int]:
    """Lê a expressão que começa na linha i (já consumida). Retorna (linhas, próximo índice)."""
    corpo: list[str] = []
    if primeira == "```":
        j = i + 1
        while j < len(lines) and lines[j].strip() != "```":
            corpo.append(lines[j])
            j += 1
        return corpo, j + 1
    if primeira:
        corpo.append(primeira)
    j = i + 1
    while j < len(lines):
        ln = lines[j]
        if ln.strip() and indent(ln) <= 2:
            break
        corpo.append(ln)
        j += 1
    return corpo, j


def limpar(corpo: list[str]) -> str:
    texto = [ln[3:] if ln.startswith("\t\t\t") else ln.strip() for ln in corpo]
    while texto and not texto[0].strip():
        texto.pop(0)
    while texto and not texto[-1].strip():
        texto.pop()
    return "\n".join(texto)


def ler_tabela(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    tab = {"arquivo": path.name, "nome": None, "oculta": False, "medidas": [],
           "colunas": [], "particoes": []}
    doc_pendente: list[str] = []
    i = 0
    filho = False
    while i < len(lines):
        ln = lines[i]
        m = RE_TABLE.match(ln)
        if m:
            tab["nome"] = unquote(m.group(1))
            i += 1
            continue
        if ln.startswith("\t///"):
            doc_pendente.append(ln.strip()[3:].strip())
            i += 1
            continue
        if ln == "\tisHidden" and not filho:
            tab["oculta"] = True
        m = RE_MEASURE.match(ln)
        if m:
            filho = True
            corpo, j = coletar_bloco(lines, i, m.group(2).strip())
            props = {}
            while j < len(lines) and (not lines[j].strip() or indent(lines[j]) >= 2):
                pm = RE_PROP.match(lines[j])
                if pm:
                    props[pm.group(1)] = (pm.group(2) or "").strip()
                j += 1
            expr = limpar(corpo)
            tab["medidas"].append({
                "nome": unquote(m.group(1)),
                "expressao": expr,
                "pasta": props.get("displayFolder") or None,
                "formato": props.get("formatString"),
                "oculta": "isHidden" in props,
                "descricao": " ".join(doc_pendente) or None,
                "comentario_inicial": expr.lstrip().startswith("/*"),
            })
            doc_pendente = []
            i = j
            continue
        m = RE_COLUMN.match(ln)
        if m:
            filho = True
            calculada = bool(m.group(2))
            j = i + 1
            if calculada:
                _, j = coletar_bloco(lines, i, (m.group(3) or "").strip())
            props = {}
            while j < len(lines) and (not lines[j].strip() or indent(lines[j]) >= 2):
                pm = RE_PROP.match(lines[j])
                if pm and indent(lines[j]) == 2:
                    props[pm.group(1)] = (pm.group(2) or "").strip()
                j += 1
            tab["colunas"].append({
                "nome": unquote(m.group(1)),
                "calculada": calculada,
                "tipo": props.get("dataType", "(inferido)"),
                "oculta": "isHidden" in props,
                "pasta": props.get("displayFolder") or None,
            })
            doc_pendente = []
            i = j
            continue
        m = RE_PARTITION.match(ln)
        if m:
            filho = True
            j = i + 1
            modo, fonte = None, []
            while j < len(lines) and (not lines[j].strip() or indent(lines[j]) >= 2):
                s = lines[j].strip()
                if s.startswith("mode:"):
                    modo = s.split(":", 1)[1].strip()
                elif s.startswith("source"):
                    resto = s.split("=", 1)[1].strip() if "=" in s else ""
                    if resto:
                        fonte.append(resto)
                elif indent(lines[j]) >= 3:
                    fonte.append(lines[j])
                j += 1
            texto = limpar(fonte)
            tab["particoes"].append({
                "nome": m.group(1), "tipo": m.group(2), "modo": modo,
                "fonte": texto,
                "conectores": [f for f in FONTES_M if f in texto],
            })
            i = j
            continue
        if indent(ln) == 1 and ln.strip() and not ln.startswith("\t///"):
            if not ln.strip().startswith(("lineageTag", "isHidden", "showAsVariationsOnly")):
                filho = True
            doc_pendente = []
        i += 1
    tab["calculada"] = any(p["tipo"] == "calculated" for p in tab["particoes"])
    tab["auto_data"] = tab["nome"].startswith(("LocalDateTable_", "DateTableTemplate_"))
    return tab


def ler_relacionamentos(path: Path) -> list[dict]:
    rels, atual = [], None
    for ln in path.read_text(encoding="utf-8-sig").splitlines():
        if ln.startswith("relationship "):
            atual = {"id": ln.split()[1], "ativo": True, "de": None, "para": None,
                     "de_card": "many", "para_card": "one", "filtro": "oneDirection"}
            rels.append(atual)
        elif atual and ln.startswith("\t"):
            s = ln.strip()
            if s == "isActive: false":
                atual["ativo"] = False
            elif s.startswith("fromColumn:"):
                atual["de"] = s.split(":", 1)[1].strip()
            elif s.startswith("toColumn:"):
                atual["para"] = s.split(":", 1)[1].strip()
            elif s.startswith("fromCardinality:"):
                atual["de_card"] = s.split(":", 1)[1].strip()
            elif s.startswith("toCardinality:"):
                atual["para_card"] = s.split(":", 1)[1].strip()
            elif s.startswith("crossFilteringBehavior:"):
                atual["filtro"] = s.split(":", 1)[1].strip()
    return rels


def ler_expressoes(path: Path) -> list[dict]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    out = []
    re_expr = re.compile(r"^expression ('(?:[^']|'')*'|\S+)\s*=\s*(.*)$")
    for i, ln in enumerate(lines):
        m = re_expr.match(ln)
        if not m:
            continue
        corpo = [m.group(2)] if m.group(2) else []
        grupo = None
        j = i + 1
        while j < len(lines) and not lines[j].startswith("expression "):
            s = lines[j].strip()
            if indent(lines[j]) >= 2:
                corpo.append(lines[j])
            elif s.startswith("queryGroup:"):
                grupo = unquote(s.split(":", 1)[1].strip())
            j += 1
        texto = limpar(corpo)
        out.append({
            "nome": unquote(m.group(1)),
            "parametro": "IsParameterQuery=true" in texto,
            "grupo": grupo,
            "conectores": [f for f in FONTES_M if f in texto],
            "fonte": texto,
        })
    return out


def campos_visual(obj, parent=None, acc=None):
    if acc is None:
        acc = set()
    if isinstance(obj, dict):
        if "Property" in obj and isinstance(obj.get("Expression"), dict):
            ent = obj["Expression"].get("SourceRef", {}).get("Entity")
            if ent:
                acc.add((parent or "?", ent, obj["Property"]))
        for k, v in obj.items():
            campos_visual(v, k, acc)
    elif isinstance(obj, list):
        for v in obj:
            campos_visual(v, parent, acc)
    return acc


def ler_relatorio(rep: Path) -> dict:
    base = rep / "definition" / "pages"
    ordem = json.loads((base / "pages.json").read_text(encoding="utf-8-sig"))
    paginas = []
    for pos, pid in enumerate(ordem.get("pageOrder", []), start=1):
        pj = json.loads((base / pid / "page.json").read_text(encoding="utf-8-sig"))
        visuais, tipos, campos = 0, Counter(), set()
        for vf in sorted((base / pid / "visuals").glob("*/visual.json")):
            v = json.loads(vf.read_text(encoding="utf-8-sig"))
            visuais += 1
            tipos[v.get("visual", {}).get("visualType", v.get("visualGroup") and "group" or "?")] += 1
            campos |= campos_visual(v)
        paginas.append({
            "ordem": pos, "id": pid, "nome": pj.get("displayName"),
            "oculta": pj.get("visibility") == "HiddenInViewMode",
            "visuais": visuais, "tipos": dict(tipos),
            "campos": sorted({(e, p) for _, e, p in campos}),
            "medidas_ou_colunas": sorted(campos),
        })
    bm = rep / "definition" / "bookmarks"
    return {"ativa": ordem.get("activePageName"), "paginas": paginas,
            "bookmarks": len(list(bm.glob("*.bookmark.json"))) if bm.exists() else 0}


RE_REF = re.compile(r"(?<![\w'\]])\[([^\[\]]+)\]")


def detectar_projeto(root: Path, nome: str | None) -> str:
    if nome:
        return nome
    achados = sorted(p.name[: -len(".SemanticModel")] for p in root.glob("*.SemanticModel"))
    if len(achados) != 1:
        raise SystemExit(f"Esperava 1 pasta *.SemanticModel em {root}, achei {len(achados)}: {achados}. Use --projeto.")
    return achados[0]


def dependencias(medidas: list[dict]) -> dict[str, dict[str, list[str]]]:
    """Para cada medida: medidas que ela referencia ([Nome] sem tabela antes) e medidas que a usam."""
    nomes = {m["nome"] for m in medidas}
    dep = {m["nome"]: sorted({r for r in RE_REF.findall(m["expressao"]) if r in nomes and r != m["nome"]})
           for m in medidas}
    usada = {n: [] for n in nomes}
    for n, refs in dep.items():
        for r in refs:
            usada[r].append(n)
    return {n: {"depende_de": dep[n], "usada_por": sorted(usada[n])} for n in nomes}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="pasta com o .pbip, por exemplo src/<slug>")
    ap.add_argument("--projeto", help="nome das pastas .SemanticModel/.Report (detectado se omitido)")
    ap.add_argument("--docs", help="pasta da documentação do projeto, para contar páginas")
    ap.add_argument("--json")
    a = ap.parse_args()
    root = Path(a.root)
    projeto = detectar_projeto(root, a.projeto)
    sm = root / f"{projeto}.SemanticModel" / "definition"
    tabelas = [ler_tabela(p) for p in sorted((sm / "tables").glob("*.tmdl"))]
    rels = ler_relacionamentos(sm / "relationships.tmdl")
    exprs = ler_expressoes(sm / "expressions.tmdl")
    rel = ler_relatorio(root / f"{projeto}.Report")

    medidas = [m | {"tabela": t["nome"]} for t in tabelas for m in t["medidas"]]
    nomes_medidas = {m["nome"] for m in medidas}
    pastas = Counter(m["pasta"] or "(sem pasta de exibição)" for m in medidas)
    negocio = [t for t in tabelas if not t["auto_data"]]
    deps = dependencias(medidas)
    uso_guias: dict[str, list[str]] = defaultdict(list)
    for pg in rel["paginas"]:
        for _, prop in pg["campos"]:
            if prop in nomes_medidas and pg["nome"] not in uso_guias[prop]:
                uso_guias[prop].append(pg["nome"])
    for m in medidas:
        m["depende_de"] = deps[m["nome"]]["depende_de"]
        m["usada_por"] = deps[m["nome"]]["usada_por"]
        m["guias"] = uso_guias.get(m["nome"], [])
    sem_uso = [m["nome"] for m in medidas if not m["guias"] and not m["usada_por"]]
    docs = sorted(p.as_posix() for p in Path(a.docs).rglob("*.md")) if a.docs and Path(a.docs).exists() else []

    ind = {
        "projeto": projeto,
        "tabelas (total, incl. auto-data)": len(tabelas),
        "tabelas de negócio (sem auto-data)": len(negocio),
        "tabelas auto-data (LocalDateTable/DateTableTemplate)": len(tabelas) - len(negocio),
        "colunas (total)": sum(len(t["colunas"]) for t in tabelas),
        "colunas em tabelas de negócio": sum(len(t["colunas"]) for t in negocio),
        "colunas calculadas": sum(c["calculada"] for t in negocio for c in t["colunas"]),
        "relacionamentos (total)": len(rels),
        "relacionamentos inativos": sum(not r["ativo"] for r in rels),
        "relacionamentos com auto-data": sum("LocalDateTable_" in (r["para"] or "") for r in rels),
        "medidas": len(medidas),
        "medidas sem pasta de exibição": pastas.get("(sem pasta de exibição)", 0),
        "medidas com ///": sum(bool(m["descricao"]) for m in medidas),
        "medidas com /* */ na 1ª linha": sum(m["comentario_inicial"] for m in medidas),
        "medidas sem uso (nem em visual nem em outra medida)": len(sem_uso),
        "expressões M compartilhadas": len(exprs),
        "parâmetros": sum(e["parametro"] for e in exprs),
        "guias do relatório": len(rel["paginas"]),
        "guias ocultas": sum(p["oculta"] for p in rel["paginas"]),
        "visuais": sum(p["visuais"] for p in rel["paginas"]),
        "indicadores (bookmarks)": rel["bookmarks"],
    }
    if a.docs:
        ind["páginas de documentação"] = len(docs)
    for k, v in ind.items():
        print(f"{k}: {v}")
    print()
    print("medidas por pasta de exibição:")
    for k, v in sorted(pastas.items()):
        print(f"  {k}: {v}")

    if a.json:
        Path(a.json).write_text(json.dumps({
            "indicadores": ind, "pastas": pastas, "tabelas": tabelas,
            "medidas": medidas, "medidas_sem_uso": sem_uso,
            "relacionamentos": rels, "expressoes": exprs, "relatorio": rel,
            "docs": docs,
        }, ensure_ascii=False, indent=1, default=list), encoding="utf-8")


if __name__ == "__main__":
    main()
