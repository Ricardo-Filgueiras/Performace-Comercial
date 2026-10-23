"""Testes do extrator de ETL Python (análise estática).

Rodar (na pasta da skill):
    PYTHONUTF8=1 python -m unittest discover -s scripts/tests -v

Usam os scripts de exemplo em tests/fixture/etl/exemplo. Os "segredos" da fixture são falsos
e existem só para provar que o extrator nunca os copia para a página.
"""

from __future__ import annotations

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))

import extrair_etl as e  # noqa: E402

FIXTURE = AQUI / "fixture" / "etl" / "exemplo"
SEGREDOS = ["abc123SEGREDO", "XYZ_SEGREDO", "p4ssWORD", "valor-secreto-no-default", "Fulano"]


def rodar(*args: str) -> tuple[int, str]:
    saida = io.StringIO()
    codigo = 0
    sys.argv = ["extrair_etl.py", *args]
    with contextlib.redirect_stdout(saida):
        try:
            e.main()
        except SystemExit as ex:
            codigo = ex.code if isinstance(ex.code, int) else 1
    return codigo, saida.getvalue()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="bi-etl-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.etl = self.tmp / "etl" / "exemplo"
        shutil.copytree(FIXTURE, self.etl)
        self.docs = self.tmp / "docs" / "projetos" / "exemplo"

    def gerar(self, *extra):
        return rodar("--etl", str(self.etl), "--docs", str(self.docs), *extra)

    def pagina(self) -> str:
        return (self.docs / "etl-python.md").read_text(encoding="utf-8")

    def escrever(self, texto: str):
        (self.docs / "etl-python.md").write_text(texto, encoding="utf-8", newline="\n")


class TestAnalise(Base):
    def setUp(self):
        super().setUp()
        self.infos = {i["rel"]: i for i in e.analisar(self.etl, set())}

    def test_ignora_venv(self):
        self.assertEqual(set(self.infos), {"carregar_vendas.py", "quebrado.py", "segredo.py", "utils.py"})

    def test_excluir_pasta(self):
        (self.etl / "legado").mkdir()
        (self.etl / "legado" / "velho.py").write_text("x = 1\n", encoding="utf-8")
        self.assertIn("legado/velho.py", {i["rel"] for i in e.analisar(self.etl, set())})
        self.assertNotIn("legado/velho.py", {i["rel"] for i in e.analisar(self.etl, {"legado"})})

    def test_carregar_vendas(self):
        i = self.infos["carregar_vendas.py"]
        self.assertTrue(i["executavel"])
        self.assertEqual(i["terceiros"], {"pandas"})
        self.assertEqual(i["locais"], {"utils"})
        self.assertEqual(i["env"], {"PASTA_ENTRADA", "BANCO_DESTINO"})
        self.assertTrue(i["doc"].startswith("Carrega as vendas do dia"))
        ops = {(t, k) for t, k, _, _ in i["operacoes"]}
        self.assertEqual(ops, {("leitura", "read_csv"), ("leitura", "read_excel"),
                               ("escrita", "to_parquet"), ("escrita", "arquivo")})
        nomes = [a["nomes"][0] for a in i["args"]]
        self.assertEqual(nomes, ["--entrada", "--saida", "--dias", "--token"])
        self.assertTrue(i["args"][0]["obrigatorio"])
        self.assertEqual(i["args"][3]["padrao"], "(oculto)")

    def test_assinatura_sem_valores_padrao(self):
        sig = next(f["sig"] for f in self.infos["carregar_vendas.py"]["funcoes"] if f["nome"] == "transformar")
        self.assertEqual(sig, "transformar(df: pd.DataFrame, moeda: str = …) -> pd.DataFrame")

    def test_dependencias_locais(self):
        self.assertEqual(self.infos["utils.py"]["usado_por"], ["carregar_vendas.py"])
        self.assertFalse(self.infos["utils.py"]["executavel"])

    def test_classe_e_metodos(self):
        c = self.infos["utils.py"]["classes"][0]
        self.assertEqual(c["nome"], "Auditor")
        self.assertEqual([m["nome"] for m in c["metodos"]], ["Auditor.__init__", "Auditor.registrar"])

    def test_alertas_de_seguranca(self):
        tipos = {(t, n) for t, _, n in self.infos["segredo.py"]["alertas"]}
        self.assertEqual(tipos, {("credencial", "senha"), ("credencial", "password"), ("url_com_senha", "")})
        self.assertEqual([t for t, _, _ in self.infos["carregar_vendas.py"]["alertas"]], ["caminho_absoluto"])

    def test_erro_de_sintaxe_nao_derruba(self):
        self.assertIn("erro de sintaxe na linha 1", self.infos["quebrado.py"]["erro"])


class TestPagina(Base):
    def test_gera_a_pagina(self):
        codigo, saida = self.gerar()
        self.assertEqual(codigo, 0, saida)
        t = self.pagina()
        self.assertIn("# ETL em Python", t)
        self.assertIn("### `carregar_vendas.py`", t)
        self.assertIn("Carrega as vendas do dia e grava o arquivo consumido pelo modelo.", t)
        self.assertIn("`python carregar_vendas.py --entrada VALOR", t)
        self.assertIn("`pandas`, `psycopg2`, `requests`", t)
        self.assertIn("`requirements.txt`", t)
        self.assertIn("`metas.xlsx`", t)                       # só o nome do arquivo
        self.assertIn("Padroniza os nomes e converte o valor", t)
        self.assertIn("Revisar segurança", t)
        self.assertIn("Não foi possível ler este script", t)
        self.assertIn("Sem docstring", t)

    def test_nunca_copia_segredos_nem_caminhos(self):
        _, saida = self.gerar()
        t = self.pagina()
        for s in SEGREDOS:
            self.assertNotIn(s, t)
            self.assertNotIn(s, saida)
        self.assertNotIn("C:\\", t)

    def test_nao_escreve_na_pasta_dos_scripts(self):
        antes = {p: p.read_bytes() for p in self.etl.rglob("*") if p.is_file()}
        self.gerar()
        depois = {p: p.read_bytes() for p in self.etl.rglob("*") if p.is_file()}
        self.assertEqual(antes, depois)

    def test_recusa_docs_dentro_da_pasta_dos_scripts(self):
        codigo, _ = rodar("--etl", str(self.etl), "--docs", str(self.etl / "docs"))
        self.assertNotEqual(codigo, 0)

    def test_idempotente_e_check(self):
        self.gerar()
        codigo, saida = self.gerar("--check")
        self.assertEqual(codigo, 0, saida)
        self.assertIn("check: ok", saida)

    def test_check_detecta_script_alterado(self):
        self.gerar()
        (self.etl / "utils.py").write_text(
            (self.etl / "utils.py").read_text(encoding="utf-8").replace("Remove espaços", "Apara espaços"),
            encoding="utf-8")
        codigo, _ = self.gerar("--check")
        self.assertEqual(codigo, 1)
        self.assertIn("Remove espaços", self.pagina())          # --check não escreve

    def test_preserva_texto_manual_e_atualiza_o_gerado(self):
        self.gerar()
        t = self.pagina()
        pend = e.descricao_padrao({"rel": "segredo.py"})
        self.assertIn(pend, t)
        self.escrever(t.replace(pend, "Carga do banco legado, roda toda madrugada.\n\nResponsável: time de dados."))
        (self.etl / "segredo.py").write_text(
            (self.etl / "segredo.py").read_text(encoding="utf-8") + "\n\ndef nova():\n    \"\"\"Função nova.\"\"\"\n",
            encoding="utf-8")
        self.gerar()
        novo = self.pagina()
        self.assertIn("Responsável: time de dados.", novo)
        self.assertIn("Função nova.", novo)

    def test_pendente_vira_resumo_quando_o_script_ganha_docstring(self):
        self.gerar()
        (self.etl / "segredo.py").write_text(
            '"""Acessos ao banco e à API de dados."""\n' + (self.etl / "segredo.py").read_text(encoding="utf-8"),
            encoding="utf-8")
        self.gerar()
        self.assertIn("Acessos ao banco e à API de dados.", self.pagina())

    def test_script_removido_nao_apaga_a_secao(self):
        self.gerar()
        (self.etl / "utils.py").unlink()
        codigo, saida = self.gerar()
        t = self.pagina()
        self.assertIn("### `utils.py`", t)
        self.assertIn("Removido do modelo", t)
        self.assertIn("saiu do modelo: script:utils.py", saida)

    def test_copia_intacta_do_modelo_e_substituida(self):
        self.docs.mkdir(parents=True)
        shutil.copy(AQUI.parent.parent / "modelos" / "projeto" / "etl-python.md", self.docs / "etl-python.md")
        self.gerar()
        t = self.pagina()
        self.assertNotIn("modelo-nao-preenchido", t)
        self.assertIn("<!-- gerado:inicio", t)

    def test_pagina_antiga_sem_marcadores_nao_e_tocada(self):
        self.docs.mkdir(parents=True)
        original = "# ETL\n\nEscrito à mão.\n"
        self.escrever(original)
        codigo, saida = self.gerar()
        self.assertEqual(codigo, 0)
        self.assertEqual(self.pagina(), original)
        self.assertIn("sem marcadores `gerado`", saida)

    def test_texto_nao_depende_de_como_o_caminho_foi_passado(self):
        import os
        (self.tmp / "mkdocs.yml").write_text("site_name: x\n", encoding="utf-8")
        self.gerar()
        self.assertIn("`etl/exemplo`", self.pagina())
        antigo = os.getcwd()
        os.chdir(self.tmp)
        try:
            codigo, saida = rodar("--etl", "etl/exemplo", "--docs", "docs/projetos/exemplo", "--check")
        finally:
            os.chdir(antigo)
        self.assertEqual(codigo, 0, saida)

    def test_pasta_sem_python_falha_com_mensagem(self):
        vazio = self.tmp / "vazio"
        vazio.mkdir()
        codigo, _ = rodar("--etl", str(vazio), "--docs", str(self.docs))
        self.assertNotEqual(codigo, 0)


if __name__ == "__main__":
    unittest.main()
