"""Gera a página `etl-python.md` a partir dos scripts Python de um projeto de BI.

Faz análise ESTÁTICA (módulo `ast`): nenhum script é importado nem executado. Para cada
`.py` em --etl extrai a docstring do módulo, funções e classes com suas docstrings,
argumentos de linha de comando (argparse), bibliotecas de terceiros, variáveis de
ambiente e as operações de leitura e escrita (arquivos, banco, HTTP).

Segurança: credenciais e valores de configuração nunca são copiados do código. A página
mostra nomes de arquivo (sem diretório), nomes de variável de ambiente, nomes de parâmetro
e valores padrão simples de argumentos (números, booleanos, nomes de arquivo). Atribuição literal a
nomes como senha, token ou chave, e URL com usuário e senha, viram um ALERTA (nome e
linha, nunca o valor). Caminho absoluto no código também é sinalizado.

O conteúdo gerado fica entre marcadores `gerado`, como em gerar_paginas.py: o texto
escrito à mão acima de cada bloco é preservado.

Uso (na raiz do portal):
    python <pasta-da-skill>/scripts/extrair_etl.py \\
        --etl <pasta dos scripts> --docs docs/projetos/<slug>
    ... --excluir testes --excluir legado    (nomes de pasta a ignorar; repetível)
    ... --check      não escreve; sai com código 1 se a página estiver desatualizada
    ... --dry-run    mostra o que seria criado ou alterado

Nunca escreve dentro de --etl. No Windows, rode com PYTHONUTF8=1.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gerar_paginas import (  # noqa: E402
    MARCA_MODELO, Regiao, bloco, codigo, esc, pendente, rid, sincronizar, validar_destino,
)

PAGINA = "etl-python.md"
IGNORAR = {".git", ".venv", "venv", "env", "__pycache__", "node_modules", "build", "dist",
           "site-packages", ".mypy_cache", ".pytest_cache"}
ARQ_DEPENDENCIAS = ["requirements.txt", "pyproject.toml", "uv.lock", "poetry.lock", "Pipfile",
                    "environment.yml", ".python-version"]

SECRETO = re.compile(r"(passw|senha|secret|token|api[_-]?key|apikey|credential|pwd|chave_?acesso)",
                     re.I)
URL_COM_SENHA = re.compile(r"://[^/\s:@]+:[^/\s@]+@")
EXT_ARQ = re.compile(r"\.(csv|xlsx?|xlsm|parquet|json|txt|feather|xml|pkl|zip|sql|pbix)$", re.I)
ABSOLUTO = re.compile(r"^([A-Za-z]:[\\/]|/|\\\\)")

LEITURA = {"read_csv", "read_excel", "read_parquet", "read_json", "read_sql", "read_sql_query",
           "read_sql_table", "read_feather", "read_table", "read_pickle", "read_xml", "read_fwf",
           "load_workbook"}
ESCRITA = {"to_csv", "to_excel", "to_parquet", "to_json", "to_sql", "to_feather", "to_pickle",
           "to_xml"}
SQL_LEITURA = {"read_sql", "read_sql_query"}
BASE_BANCO = {"pyodbc", "sqlalchemy", "psycopg2", "pymysql", "sqlite3", "oracledb", "cx_Oracle",
              "mysql", "snowflake", "pymssql"}
BASE_HTTP = {"requests", "httpx"}
CLI_ALTERNATIVAS = {"click", "typer", "fire"}


# --------------------------------------------------------------------------- análise

def nome_arquivo(valor: str) -> str:
    return re.split(r"[\\/]", valor.rstrip("\\/"))[-1]


def base_nome(no: ast.AST) -> str | None:
    """Nome mais à esquerda de uma cadeia de atributos (`a.b.c` -> `a`)."""
    while isinstance(no, ast.Attribute):
        no = no.value
    return no.id if isinstance(no, ast.Name) else None


def const_str(no: ast.AST | None) -> str | None:
    return no.value if isinstance(no, ast.Constant) and isinstance(no.value, str) else None


def assinatura(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Assinatura sem valores padrão (podem conter segredos): `f(a, b: int = …)`."""
    a = fn.args
    pos = a.posonlyargs + a.args
    n_def = len(a.defaults)
    partes: list[str] = []
    for i, arg in enumerate(pos):
        txt = arg.arg + (f": {ast.unparse(arg.annotation)}" if arg.annotation else "")
        if i >= len(pos) - n_def:
            txt += " = …"
        partes.append(txt)
    if a.vararg:
        partes.append("*" + a.vararg.arg)
    elif a.kwonlyargs:
        partes.append("*")
    for arg, padrao in zip(a.kwonlyargs, a.kw_defaults):
        txt = arg.arg + (f": {ast.unparse(arg.annotation)}" if arg.annotation else "")
        partes.append(txt + (" = …" if padrao is not None else ""))
    if a.kwarg:
        partes.append("**" + a.kwarg.arg)
    ret = f" -> {ast.unparse(fn.returns)}" if fn.returns else ""
    return f"{fn.name}({', '.join(partes)}){ret}"


def primeira_linha(doc: str | None) -> str:
    if not doc:
        return ""
    for ln in doc.strip().splitlines():
        if ln.strip():
            return ln.strip()
    return ""


def analisar_arquivo(path: Path, rel: str, locais: set[str]) -> dict:
    info = {"rel": rel, "erro": None, "doc": None, "funcoes": [], "classes": [], "terceiros": set(),
            "locais": set(), "env": set(), "operacoes": [], "args": [], "executavel": False,
            "cli_outra": set(), "alertas": []}
    try:
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=rel)
    except SyntaxError as e:
        info["erro"] = f"erro de sintaxe na linha {e.lineno}: {e.msg}"
        return info
    except (UnicodeDecodeError, ValueError) as e:
        info["erro"] = f"arquivo não é texto UTF-8 válido ({type(e).__name__})"
        return info

    info["doc"] = ast.get_docstring(tree)
    for no in tree.body:
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):
            info["funcoes"].append({"sig": assinatura(no), "nome": no.name,
                                    "doc": ast.get_docstring(no), "linha": no.lineno})
        elif isinstance(no, ast.ClassDef):
            metodos = [{"sig": assinatura(m), "nome": f"{no.name}.{m.name}", "doc": ast.get_docstring(m),
                        "linha": m.lineno}
                       for m in no.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
            info["classes"].append({"nome": no.name, "doc": ast.get_docstring(no),
                                    "linha": no.lineno, "metodos": metodos})
        elif isinstance(no, ast.If) and isinstance(no.test, ast.Compare) \
                and isinstance(no.test.left, ast.Name) and no.test.left.id == "__name__":
            info["executavel"] = True

    for no in ast.walk(tree):
        if isinstance(no, ast.Import):
            for alias in no.names:
                registrar_import(info, alias.name.split(".")[0], locais, 0)
        elif isinstance(no, ast.ImportFrom):
            registrar_import(info, (no.module or "").split(".")[0], locais, no.level)
        elif isinstance(no, ast.Call):
            analisar_chamada(info, no)
        elif isinstance(no, (ast.Assign, ast.AnnAssign)):
            alvos = no.targets if isinstance(no, ast.Assign) else [no.target]
            valor = const_str(no.value)
            for alvo in alvos:
                nome = alvo.id if isinstance(alvo, ast.Name) else \
                    (alvo.attr if isinstance(alvo, ast.Attribute) else None)
                if nome and valor and SECRETO.search(nome):
                    info["alertas"].append(("credencial", no.lineno, nome))
        elif isinstance(no, ast.Constant) and isinstance(no.value, str) and URL_COM_SENHA.search(no.value):
            info["alertas"].append(("url_com_senha", no.lineno, ""))
        elif isinstance(no, ast.Subscript):  # os.environ["X"]
            if base_nome(no.value) == "os" and isinstance(no.value, ast.Attribute) \
                    and no.value.attr == "environ":
                chave = const_str(no.slice)
                if chave:
                    info["env"].add(chave)
    info["alertas"] = sorted(set(info["alertas"]))
    return info


def registrar_import(info: dict, topo: str, locais: set[str], nivel: int) -> None:
    if not topo and nivel == 0:
        return
    if nivel > 0 or topo in locais:
        if topo:
            info["locais"].add(topo)
        return
    if topo in sys.stdlib_module_names:
        return
    info["terceiros"].add(topo)
    if topo in CLI_ALTERNATIVAS:
        info["cli_outra"].add(topo)


def analisar_chamada(info: dict, c: ast.Call) -> None:
    f = c.func
    linha = c.lineno
    nome = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
    base = base_nome(f)
    primeiro = c.args[0] if c.args else None

    # parâmetros sensíveis passados como literal: connect(password="...")
    for kw in c.keywords:
        if kw.arg and SECRETO.search(kw.arg) and const_str(kw.value):
            info["alertas"].append(("credencial", kw.value.lineno, kw.arg))

    if nome == "add_argument" and isinstance(f, ast.Attribute):
        nomes = [s for s in (const_str(a) for a in c.args) if s]
        if nomes:
            kw = {k.arg: k.value for k in c.keywords if k.arg}
            padrao = None
            if "default" in kw and isinstance(kw["default"], ast.Constant):
                v = kw["default"].value
                secreto = any(SECRETO.search(n) for n in nomes)
                if isinstance(v, (bool, int, float)) or v is None:
                    padrao = repr(v)
                elif isinstance(v, str) and not secreto:
                    padrao = repr(nome_arquivo(v) if EXT_ARQ.search(v) else v)
                else:
                    padrao = "(oculto)"
            info["args"].append({
                "nomes": nomes, "ajuda": const_str(kw.get("help")),
                "obrigatorio": isinstance(kw.get("required"), ast.Constant) and kw["required"].value is True
                or not nomes[0].startswith("-"),
                "padrao": padrao, "linha": linha})
        return

    if nome in ("getenv", "get") and base == "os" or (nome == "get" and isinstance(f, ast.Attribute)
                                                      and isinstance(f.value, ast.Attribute)
                                                      and f.value.attr == "environ" and base == "os"):
        chave = const_str(primeiro)
        if chave:
            info["env"].add(chave)
        return

    def alvo(no: ast.AST | None, ignorar_sql: bool = False) -> str:
        s = const_str(no)
        if s is None:
            return "(dinâmico)"
        if ignorar_sql:
            return "(consulta SQL)"
        if URL_COM_SENHA.search(s):
            return "(oculto)"
        if EXT_ARQ.search(s):
            if ABSOLUTO.match(s):
                info["alertas"].append(("caminho_absoluto", linha, ""))
            return f"`{nome_arquivo(s)}`"
        return "(texto)"

    if isinstance(f, ast.Name) and f.id == "open":
        modo = const_str(c.args[1]) if len(c.args) > 1 else const_str(
            next((k.value for k in c.keywords if k.arg == "mode"), None))
        tipo = "escrita" if modo and any(m in modo for m in "wax") else "leitura"
        info["operacoes"].append((tipo, "arquivo", alvo(primeiro), linha))
    elif nome in LEITURA:
        info["operacoes"].append(("leitura", nome, alvo(primeiro, nome in SQL_LEITURA), linha))
    elif nome in ESCRITA:
        if nome == "to_sql":
            tabela = const_str(primeiro)
            info["operacoes"].append(("escrita", nome, f"tabela `{tabela}`" if tabela else "(dinâmico)", linha))
        else:
            info["operacoes"].append(("escrita", nome, alvo(primeiro), linha))
    elif (nome in ("connect", "create_engine") and base in BASE_BANCO) or \
            (isinstance(f, ast.Name) and f.id == "create_engine"):
        info["operacoes"].append(("conexão", "banco de dados", f"{base or 'sqlalchemy'}.{nome}", linha))
    elif (base in BASE_HTTP and nome in {"get", "post", "put", "delete", "patch", "request"}) \
            or nome == "urlopen":
        info["operacoes"].append(("conexão", "HTTP", f"{base or 'urllib'}.{nome}", linha))


def coletar(etl: Path, excluir: set[str]) -> list[Path]:
    achados = []
    for p in sorted(etl.rglob("*.py")):
        partes = set(p.relative_to(etl).parts[:-1])
        if partes & (IGNORAR | excluir):
            continue
        achados.append(p)
    return achados


def analisar(etl: Path, excluir: set[str]) -> list[dict]:
    arquivos = coletar(etl, excluir)
    locais = {p.stem for p in arquivos} | {d.name for d in etl.rglob("__init__.py") for d in [d.parent]}
    infos = [analisar_arquivo(p, p.relative_to(etl).as_posix(), locais) for p in arquivos]
    usados_por: dict[str, set[str]] = {i["rel"]: set() for i in infos}
    por_stem = {Path(i["rel"]).stem: i["rel"] for i in infos}
    for i in infos:
        for mod in i["locais"]:
            alvo = por_stem.get(mod)
            if alvo and alvo != i["rel"]:
                usados_por[alvo].add(i["rel"])
    for i in infos:
        i["usado_por"] = sorted(usados_por[i["rel"]])
    return infos


# --------------------------------------------------------------------------- páginas

ROTULO_ALERTA = {
    "credencial": "Possível credencial literal no código (parâmetro `{n}`, linha {l}). O valor não foi copiado.",
    "url_com_senha": "URL com usuário e senha no código (linha {l}). O valor não foi copiado.",
    "caminho_absoluto": "Caminho absoluto de arquivo no código (linha {l}). Prefira caminho relativo ou parâmetro.",
}


def texto_docstring(doc: str) -> str:
    return codigo(doc.strip(), "text")


def indentar(texto: str, n: int = 4) -> str:
    pad = " " * n
    return "\n".join((pad + ln) if ln else ln for ln in texto.splitlines())


def conteudo_script(i: dict) -> str:
    if i["erro"]:
        return pendente("Não foi possível ler este script", i["erro"] + ". Corrija o arquivo e rode de novo.")
    l: list[str] = []
    if i["executavel"]:
        usos = []
        for a in i["args"]:
            n = a["nomes"][-1] if a["nomes"][0].startswith("-") else a["nomes"][0].upper()
            usos.append(n.upper() if not a["nomes"][0].startswith("-") else
                        (f"{a['nomes'][-1]} VALOR" if a["obrigatorio"] else f"[{a['nomes'][-1]} VALOR]"))
        l.append(f"- **Execução:** `python {i['rel']}{' ' + ' '.join(usos) if usos else ''}`")
    else:
        l.append("- **Execução:** módulo, sem ponto de entrada (`if __name__ == \"__main__\"`).")
    if i["usado_por"]:
        l.append("- **Importado por:** " + ", ".join(f"`{r}`" for r in i["usado_por"]))
    if i["locais"]:
        l.append("- **Importa (local):** " + ", ".join(f"`{m}`" for m in sorted(i["locais"])))
    l.append("- **Bibliotecas de terceiros:** " + (", ".join(f"`{m}`" for m in sorted(i["terceiros"])) or "nenhuma"))
    l.append("- **Variáveis de ambiente:** " + (", ".join(f"`{m}`" for m in sorted(i["env"])) or "nenhuma"))
    if i["cli_outra"]:
        l.append("- **Linha de comando:** biblioteca " + ", ".join(f"`{m}`" for m in sorted(i["cli_outra"]))
                 + " detectada; os argumentos não são extraídos. Descreva-os à mão acima do bloco.")
    if i["operacoes"]:
        l += ["", "| Operação | Tipo | Alvo | Linha |", "|---|---|---|---|"]
        for tipo, kind, alvo, linha in sorted(i["operacoes"], key=lambda x: x[3]):
            l.append(f"| {tipo} | {esc(kind)} | {esc(alvo)} | {linha} |")
    if i["args"]:
        l += ["", "| Argumento | Obrigatório | Padrão | Descrição |", "|---|---|---|---|"]
        for a in i["args"]:
            l.append(f"| `{esc(' / '.join(a['nomes']))}` | {'sim' if a['obrigatorio'] else 'não'} | "
                     f"{esc(a['padrao']) if a['padrao'] else '—'} | {esc(a['ajuda'] or '—')} |")
    itens = [(f["nome"], f["sig"], f["doc"]) for f in i["funcoes"]]
    for c in i["classes"]:
        itens.append((c["nome"], f"class {c['nome']}", c["doc"]))
        itens += [(m["nome"], m["sig"], m["doc"]) for m in c["metodos"] if not m["nome"].split(".")[1].startswith("_")
                  or m["nome"].endswith(".__init__")]
    publicos = [x for x in itens if not x[0].split(".")[-1].startswith("_") or x[0].endswith(".__init__")]
    if publicos:
        l += ["", "| Função ou classe | Resumo |", "|---|---|"]
        for nome, sig, doc in publicos:
            l.append(f"| `{esc(sig)}` | {esc(primeira_linha(doc)) or '—'} |")
        sem_doc = [n for n, _, d in publicos if not d]
        if sem_doc:
            l += ["", pendente("Sem docstring",
                               "Sem docstring: " + ", ".join(f"`{n}`" for n in sem_doc)
                               + ". Peça a quem mantém o script para descrever; não suponha.")]
    docs = [(n, d) for n, _, d in publicos if d]
    if i["doc"] or docs:
        l += ["", '??? abstract "Docstrings completas"', ""]
        if i["doc"]:
            l += ["    **Módulo**", "", indentar(texto_docstring(i["doc"])), ""]
        for n, d in docs:
            l += [f"    **`{n}`**", "", indentar(texto_docstring(d)), ""]
    for tipo, linha, nome in i["alertas"]:
        l += ["", pendente("Revisar segurança", ROTULO_ALERTA[tipo].format(n=nome, l=linha))]
    return "\n".join(l)


def descricao_padrao(i: dict) -> str:
    return pendente("A confirmar", f"Qual etapa do pipeline o script `{i['rel']}` cobre, de onde lê, "
                                    "para onde escreve, quando roda e quem responde por ele?")


def montar(etl: Path, infos: list[dict], docs: Path) -> tuple[str, list[Regiao]]:
    # caminho relativo à raiz do portal (onde fica o mkdocs.yml), para o texto não depender de
    # como o comando foi chamado; sem portal por perto, só o nome da pasta
    raiz = next((p for p in [docs.resolve(), *docs.resolve().parents] if (p / "mkdocs.yml").exists()), None)
    try:
        nome_pasta = etl.resolve().relative_to(raiz).as_posix() if raiz else etl.resolve().name
    except ValueError:
        nome_pasta = etl.resolve().name
    terceiros = sorted(set().union(*[i["terceiros"] for i in infos])) if infos else []
    env = sorted(set().union(*[i["env"] for i in infos])) if infos else []
    declarados = [a for a in ARQ_DEPENDENCIAS if (etl / a).exists()]
    n_alertas = sum(len(i["alertas"]) for i in infos)
    n_erro = sum(1 for i in infos if i["erro"])
    visao = [
        f"- **{len(infos)} scripts** em `{nome_pasta}` (executáveis: {sum(1 for i in infos if i['executavel'])}).",
        "- **Bibliotecas de terceiros:** " + (", ".join(f"`{m}`" for m in terceiros) or "nenhuma") + ".",
        "- **Variáveis de ambiente:** " + (", ".join(f"`{m}`" for m in env) or "nenhuma") + ".",
        "- **Dependências declaradas:** "
        + (", ".join(f"`{a}`" for a in declarados) if declarados else "nenhum arquivo encontrado na pasta") + ".",
        f"- **Alertas de segurança:** {n_alertas}. **Scripts ilegíveis:** {n_erro}.",
    ]
    if not declarados:
        visao += ["", pendente("A confirmar", "Onde ficam as dependências Python deste ETL e qual a versão do "
                                             "Python? Não há `requirements.txt`, `pyproject.toml` ou similar na pasta.")]
    head = (
        "# ETL em Python\n\n"
        f"Scripts Python do projeto (pasta `{nome_pasta}`), lidos por **análise estática**: nenhum script foi "
        "executado. Credenciais e valores de configuração nunca são copiados para esta página: só nomes "
        "de arquivo, de variável de ambiente e de parâmetro, e valores padrão simples de argumentos.\n\n"
        '!!! info "Como esta página é mantida"\n'
        "    Os blocos entre marcadores `gerado` são reescritos por `extrair_etl.py`. Escreva acima do "
        "bloco, nunca dentro dele. Docstring é a fonte: para melhorar a página, melhore a docstring do script."
    )
    regioes = [Regiao("visao-geral", "\n".join(visao), "## Visão geral\n\n" + bloco("visao-geral", "\n".join(visao)))]
    for n, i in enumerate(infos):
        rotulo = f"script:{rid(i['rel'])}"
        c = conteudo_script(i)
        padrao = descricao_padrao(i)
        resumo = primeira_linha(i["doc"])
        manual = resumo or padrao
        titulo = "## Scripts\n\n" if n == 0 else ""
        regioes.append(Regiao(
            rotulo, c, f"{titulo}### `{i['rel']}`\n\n{manual}\n\n" + bloco(rotulo, c),
            trocar=(padrao, resumo) if resumo else None))
    return head, regioes


def gerar(etl: Path, docs: Path, excluir: set[str]) -> tuple[str, list[str], list[dict]]:
    infos = analisar(etl, excluir)
    if not infos:
        raise SystemExit(f"Nenhum arquivo .py em {etl} (ignorados: {', '.join(sorted(IGNORAR | excluir))}).")
    head, regioes = montar(etl, infos, docs)
    arq = docs / PAGINA
    atual = arq.read_text(encoding="utf-8") if arq.exists() else None
    avisos: list[str] = []
    if atual is not None and MARCA_MODELO in atual:
        atual = None
    elif atual is not None and "<!-- gerado:inicio" not in atual:
        avisos.append(f"{PAGINA}: página existente sem marcadores `gerado`; não foi alterada. "
                      "Para o gerador assumir a página, mova o conteúdo e apague-a.")
        return atual, avisos, infos
    texto, av = sincronizar(atual, head, regioes)
    return texto, avisos + [f"{PAGINA}: {a}" for a in av], infos


def main() -> None:
    ap = argparse.ArgumentParser(description="Gera etl-python.md a partir dos scripts Python (análise estática).")
    ap.add_argument("--etl", required=True, help="pasta com os scripts Python do projeto")
    ap.add_argument("--docs", required=True, help="pasta da documentação, por exemplo docs/projetos/<slug>")
    ap.add_argument("--excluir", action="append", default=[], help="nome de pasta a ignorar (repetível)")
    ap.add_argument("--check", action="store_true", help="não escreve; sai com 1 se a página estiver desatualizada")
    ap.add_argument("--dry-run", action="store_true", help="mostra o que mudaria, sem escrever")
    a = ap.parse_args()
    etl, docs = Path(a.etl), Path(a.docs)
    if not etl.is_dir():
        raise SystemExit(f"--etl não é uma pasta: {etl}")
    validar_destino(etl, docs)
    texto, avisos, infos = gerar(etl, docs, set(a.excluir))
    arq = docs / PAGINA
    existe = arq.exists()
    estado = "criada" if not existe else ("alterada" if arq.read_text(encoding="utf-8") != texto else "sem mudança")
    if estado != "sem mudança" and not (a.check or a.dry_run):
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_text(texto, encoding="utf-8", newline="\n")
    print(f"{PAGINA}: {estado}")
    for av in avisos:
        print(f"AVISO: {av}")
    for i in infos:
        for tipo, linha, nome in i["alertas"]:
            print(f"ALERTA: {i['rel']}: {ROTULO_ALERTA[tipo].format(n=nome, l=linha)}")
        if i["erro"]:
            print(f"ALERTA: {i['rel']}: {i['erro']}")
    sem_doc = sum(1 for i in infos if not i["doc"] and not i["erro"])
    print(f"scripts: {len(infos)} | sem docstring de módulo: {sem_doc} (ficam como pendência)")
    if a.check and estado != "sem mudança":
        print("check: página desatualizada. Rode sem --check para regenerar.")
        raise SystemExit(1)
    if a.check:
        print("check: ok")


if __name__ == "__main__":
    main()
