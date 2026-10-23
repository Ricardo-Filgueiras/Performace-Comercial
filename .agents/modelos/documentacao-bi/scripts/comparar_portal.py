"""Compara os arquivos de um portal já criado com os modelos desta versão da skill.

Os arquivos de `modelos/portal/` e `modelos/metodologia/` são copiados uma vez para o
repositório do portal. Quando a skill ganha uma versão nova (por exemplo, o `mkdocs.yml`
passa a validar âncoras), os portais antigos não mudam sozinhos. Este script mostra, só
para leitura, o que difere, para você decidir o que levar para o portal:

    ausente      o portal não tem o arquivo (provavelmente algo novo no modelo)
    igual        sem diferença
    diferente    mostra o diff (modelo -> portal); diferenças de nome do site e do menu são normais

Compara apenas arquivos que costumam evoluir com a skill: mkdocs.yml, pyproject.toml,
.gitignore, docs/stylesheets/extra.css e as páginas de metodologia. Não olha README, menus,
índice nem changelog, que são do portal.

Uso (na raiz do portal ou apontando para ele):
    python <pasta-da-skill>/scripts/comparar_portal.py --portal .
    ... --check    sai com código 1 se algum arquivo estiver ausente ou diferente

Nunca escreve nada. No Windows, rode com PYTHONUTF8=1.
"""

from __future__ import annotations

import argparse
import difflib
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
MODELOS = SKILL / "modelos"

# (arquivo no modelo, caminho no portal)
FIXOS = [
    (MODELOS / "portal" / "mkdocs.yml", "mkdocs.yml"),
    (MODELOS / "portal" / "pyproject.toml", "pyproject.toml"),
    (MODELOS / "portal" / "gitignore", ".gitignore"),
    (MODELOS / "portal" / "docs" / "stylesheets" / "extra.css", "docs/stylesheets/extra.css"),
]


def pares() -> list[tuple[Path, str]]:
    achados = list(FIXOS)
    for md in sorted((MODELOS / "metodologia").glob("*.md")):
        achados.append((md, f"docs/metodologia/{md.name}"))
    return achados


def ler(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").splitlines(keepends=True)


def comparar(portal: Path) -> list[tuple[str, str, str]]:
    """Devolve [(caminho no portal, situação, diff)]."""
    saida = []
    for modelo, destino in pares():
        alvo = portal / destino
        if not alvo.exists():
            saida.append((destino, "ausente", ""))
            continue
        a, b = ler(modelo), ler(alvo)
        if a == b:
            saida.append((destino, "igual", ""))
            continue
        diff = "".join(difflib.unified_diff(a, b, f"modelo/{destino}", f"portal/{destino}", n=1))
        saida.append((destino, "diferente", diff))
    return saida


def main() -> None:
    ap = argparse.ArgumentParser(description="Compara um portal com os modelos desta versão da skill (só leitura).")
    ap.add_argument("--portal", default=".", help="raiz do portal (onde fica o mkdocs.yml)")
    ap.add_argument("--check", action="store_true", help="sai com 1 se houver arquivo ausente ou diferente")
    ap.add_argument("--sem-diff", action="store_true", help="mostra só a lista, sem os diffs")
    a = ap.parse_args()
    portal = Path(a.portal)
    if not (portal / "mkdocs.yml").exists():
        raise SystemExit(f"{portal.resolve()} não parece a raiz de um portal (sem mkdocs.yml).")
    resultado = comparar(portal)
    for destino, situacao, diff in resultado:
        print(f"{situacao:10} {destino}")
        if diff and not a.sem_diff:
            print(diff.rstrip("\n"))
            print()
    pendentes = [r for r in resultado if r[1] != "igual"]
    print(f"\n{len(resultado)} arquivos comparados: {len(pendentes)} para revisar.")
    if a.check and pendentes:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
