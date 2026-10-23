"""Testes de empacotamento e de higiene do kit.

Rodar (na pasta da skill):
    PYTHONUTF8=1 python -m unittest discover -s scripts/tests -v

Conferem que a versão é a mesma em todos os lugares (o plugin só atualiza quando o campo
`version` muda), que os manifestos estão corretos, que os caminhos da skill não dependem de
onde ela está instalada e que nenhum termo de projeto anterior vazou para o kit.

A lista de termos proibidos guarda só HASHES (termos_proibidos.sha256), para a própria lista
não vazar o que ela protege. Para incluir um termo novo:
    python scripts/tests/test_plugin.py --hash "termo novo"
e acrescente a linha impressa ao arquivo termos_proibidos.sha256.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import tempfile
import unicodedata
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SKILL = AQUI.parent.parent
KIT = SKILL.parent
HASHES = AQUI / "termos_proibidos.sha256"
sys.path.insert(0, str(AQUI.parent))

EXT_TEXTO = {".md", ".py", ".yml", ".yaml", ".json", ".toml", ".css", ".txt", ".tmdl", ".pbip", ".gitignore"}


def normalizar(texto: str) -> list[str]:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return re.findall(r"[a-z0-9]+", sem_acento.lower())


def hash_termo(termo: str) -> str:
    return hashlib.sha256(" ".join(normalizar(termo)).encode("utf-8")).hexdigest()


def ngramas(texto: str, ate: int = 3):
    palavras = normalizar(texto)
    for n in range(1, ate + 1):
        for i in range(len(palavras) - n + 1):
            yield " ".join(palavras[i:i + n])


def arquivos_texto():
    for p in sorted(KIT.rglob("*")):
        if not p.is_file() or p == HASHES or "__pycache__" in p.parts:
            continue
        if p.suffix.lower() in EXT_TEXTO or p.name in {"gitignore", ".gitignore"}:
            yield p


def versao_skill() -> str:
    m = re.search(r"Versão da skill: \*\*([\d.]+)\*\*", (SKILL / "SKILL.md").read_text(encoding="utf-8"))
    assert m, "SKILL.md sem 'Versão da skill: **X.Y.Z**'"
    return m.group(1)


class TestEmpacotamento(unittest.TestCase):
    def setUp(self):
        # Copiada sozinha para .claude/skills/, a skill não tem os manifestos do plugin ao lado:
        # os testes de manifesto e de versão se aplicam só ao kit completo.
        self.no_kit = not (KIT / ".claude-plugin" / "plugin.json").exists()
        if not self.no_kit:
            self.plugin = json.loads((KIT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
            self.mercado = json.loads((KIT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))

    def exigir_kit(self):
        if self.no_kit:
            self.skipTest("fora do kit (sem .claude-plugin ao lado da skill)")

    def test_manifesto_do_plugin(self):
        self.exigir_kit()
        self.assertEqual(self.plugin["name"], "documentacao-bi")
        self.assertRegex(self.plugin["version"], r"^\d+\.\d+\.\d+$")
        self.assertTrue(self.plugin["description"])
        for caminho in self.plugin["skills"]:
            self.assertTrue(caminho.startswith("./"))
            self.assertTrue((KIT / caminho / "SKILL.md").exists(), caminho)

    def test_marketplace_aponta_para_o_plugin(self):
        self.exigir_kit()
        self.assertTrue(self.mercado["name"])
        self.assertTrue(self.mercado["owner"]["name"])
        entrada = self.mercado["plugins"][0]
        self.assertEqual(entrada["name"], self.plugin["name"])
        self.assertTrue(entrada["source"].startswith("./"))
        # a versão fica só no plugin.json: nos dois lugares, o plugin.json vence sem aviso
        self.assertNotIn("version", entrada)
        self.assertNotIn("version", self.mercado)

    def test_versao_igual_em_todos_os_lugares(self):
        self.exigir_kit()
        v = self.plugin["version"]
        self.assertEqual(versao_skill(), v)
        cab = re.search(r"(?m)^## \[(\d+\.\d+\.\d+)\]", (SKILL / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertEqual(cab.group(1), v, "primeira entrada do CHANGELOG diferente da versão do plugin")
        self.assertIn(f"versão {v}", (KIT / "README.md").read_text(encoding="utf-8"))
        self.assertIn(f"**Versão da skill:** {v}",
                      (SKILL / "referencias" / "relatorio-de-teste.md").read_text(encoding="utf-8"))

    def test_frontmatter_da_skill(self):
        texto = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        fm = texto.split("---")[1]
        self.assertRegex(fm, r"(?m)^name: documentacao-bi$")
        self.assertRegex(fm, r"(?m)^description: .{40,}")

    def test_caminhos_nao_dependem_de_onde_a_skill_esta(self):
        skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("${CLAUDE_SKILL_DIR}/scripts/", skill_md)
        for p in [SKILL / "SKILL.md", *sorted((SKILL / "scripts").glob("*.py"))]:
            texto = p.read_text(encoding="utf-8")
            self.assertNotIn(".claude/skills/documentacao-bi/scripts", texto, p.name)

    def test_todo_script_citado_existe(self):
        citados = set(re.findall(r"scripts/([a-z_]+\.py)", (SKILL / "SKILL.md").read_text(encoding="utf-8")))
        self.assertTrue(citados)
        for nome in citados:
            self.assertTrue((SKILL / "scripts" / nome).exists(), nome)


class TestHigiene(unittest.TestCase):
    def test_nenhum_termo_de_projeto_anterior(self):
        proibidos = {ln.strip() for ln in HASHES.read_text(encoding="utf-8").splitlines()
                     if ln.strip() and not ln.startswith("#")}
        self.assertTrue(proibidos, "lista de hashes vazia")
        achados = []
        for p in arquivos_texto():
            try:
                texto = p.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                continue
            for ng in set(ngramas(texto)):
                if hashlib.sha256(ng.encode("utf-8")).hexdigest() in proibidos:
                    achados.append(f"{p.relative_to(KIT).as_posix()} (termo proibido, hash {hash_termo(ng)[:10]}…)")
        self.assertEqual(achados, [], "termo de projeto anterior no kit; remova ou generalize")

    def test_o_detector_funciona(self):
        h = hash_termo("Termo  de ÉXEMPLO")
        self.assertEqual(h, hash_termo("termo de exemplo"))
        self.assertIn(h, {hashlib.sha256(ng.encode()).hexdigest() for ng in ngramas("um Termo de Exemplo qualquer")})


class TestCompararPortal(unittest.TestCase):
    def test_portal_modelo_nao_difere(self):
        import comparar_portal as c
        tmp = Path(tempfile.mkdtemp(prefix="bi-portal-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        modelos = SKILL / "modelos"
        shutil.copytree(modelos / "portal", tmp, dirs_exist_ok=True)
        shutil.move(str(tmp / "gitignore"), str(tmp / ".gitignore"))
        (tmp / "docs" / "metodologia").mkdir(parents=True, exist_ok=True)
        for md in (modelos / "metodologia").glob("*.md"):
            shutil.copy(md, tmp / "docs" / "metodologia" / md.name)
        situacoes = {s for _, s, _ in c.comparar(tmp)}
        self.assertEqual(situacoes, {"igual"})

    def test_detecta_diferente_e_ausente(self):
        import comparar_portal as c
        tmp = Path(tempfile.mkdtemp(prefix="bi-portal-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        (tmp / "mkdocs.yml").write_text("site_name: Antigo\n", encoding="utf-8")
        res = {d: (s, diff) for d, s, diff in c.comparar(tmp)}
        self.assertEqual(res["mkdocs.yml"][0], "diferente")
        self.assertIn("-site_name: Antigo".replace("-", "+", 1), res["mkdocs.yml"][1])
        self.assertEqual(res["pyproject.toml"][0], "ausente")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--hash":
        print(hash_termo(sys.argv[2]))
    else:
        unittest.main()
