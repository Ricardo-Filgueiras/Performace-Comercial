"""Testes do levantamento e do gerador de páginas.

Rodar (na pasta da skill):
    PYTHONUTF8=1 python -m unittest discover -s scripts/tests -v

Usam o PBIP de exemplo em tests/fixture/src/exemplo (modelo sintético, com RLS, grupo de
cálculo, hierarquia, relacionamento inativo e bidirecional). Para conferir também um
projeto real, defina BI_PROJETO_REAL com o caminho da pasta que contém o .pbip.
"""

from __future__ import annotations

import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))

import gerar_paginas as g  # noqa: E402
import levantamento as lv  # noqa: E402

FIXTURE = AQUI / "fixture" / "src" / "exemplo"


def rodar(*args: str) -> tuple[int, str]:
    """Executa gerar_paginas.main() e devolve (código de saída, saída)."""
    saida = io.StringIO()
    codigo = 0
    sys.argv = ["gerar_paginas.py", *args]
    with contextlib.redirect_stdout(saida):
        try:
            g.main()
        except SystemExit as e:
            codigo = e.code if isinstance(e.code, int) else 1
    return codigo, saida.getvalue()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="bi-doc-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.root = self.tmp / "src" / "exemplo"
        shutil.copytree(FIXTURE, self.root)
        self.docs = self.tmp / "docs" / "projetos" / "exemplo"

    def gerar(self, *extra):
        return rodar("--root", str(self.root), "--docs", str(self.docs), *extra)

    def ler(self, rel: str) -> str:
        return (self.docs / rel).read_text(encoding="utf-8")

    def escrever(self, rel: str, texto: str):
        (self.docs / rel).write_text(texto, encoding="utf-8", newline="\n")

    def tmdl(self, rel: str) -> Path:
        return self.root / "Exemplo.SemanticModel" / "definition" / rel


class TestParser(Base):
    def setUp(self):
        super().setUp()
        self.d = lv.carregar_projeto(self.root)

    def tabela(self, nome):
        return next(t for t in self.d["tabelas"] if t["nome"] == nome)

    def test_hierarquia(self):
        h = self.tabela("dCalendario")["hierarquias"]
        self.assertEqual(len(h), 1)
        self.assertEqual(h[0]["nome"], "Ano e Mês")
        self.assertEqual([n["coluna"] for n in h[0]["niveis"]], ["Ano", "Mês"])

    def test_grupo_de_calculo_sem_vazar_propriedades(self):
        grupo = self.tabela("Time Intelligence")["grupo_calculo"]
        self.assertEqual(grupo["precedencia"], "1")
        itens = {i["nome"]: i["expressao"] for i in grupo["itens"]}
        self.assertEqual(list(itens), ["Atual", "YTD", "Ano Anterior"])
        self.assertEqual(itens["Atual"], "SELECTEDMEASURE()")
        self.assertNotIn("ordinal", itens["YTD"])
        self.assertNotIn("formatStringDefinition", itens["YTD"])
        self.assertTrue(itens["Ano Anterior"].startswith("CALCULATE(\n    SELECTEDMEASURE()"))

    def test_papeis_rls(self):
        papeis = {p["nome"]: p for p in self.d["papeis"]}
        self.assertEqual(set(papeis), {"Gerente", "Vendedor"})
        self.assertEqual(papeis["Vendedor"]["filtros"][0]["tabela"], "dCliente")
        self.assertEqual(papeis["Vendedor"]["filtros"][0]["filtro"], "[Email] = USERPRINCIPALNAME()")
        self.assertEqual(papeis["Vendedor"]["membros"], 1)
        multi = papeis["Gerente"]["filtros"][0]["filtro"]
        self.assertIn("[Valor] > 0", multi)
        self.assertNotIn("```", multi)

    def test_coluna_calculada_guarda_expressao(self):
        col = next(c for c in self.tabela("fVendas")["colunas"] if c["calculada"])
        self.assertEqual(col["nome"], "Valor Líquido")
        self.assertEqual(col["expressao"], "[Valor] * 0.9")

    def test_auto_data_separada(self):
        self.assertTrue(self.tabela("LocalDateTable_1111")["auto_data"])
        self.assertFalse(self.tabela("fVendas")["auto_data"])

    def test_dependencias_e_uso(self):
        m = {x["nome"]: x for x in self.d["medidas"]}
        self.assertEqual(m["Faturamento LY"]["depende_de"], ["Faturamento"])
        self.assertEqual(m["Faturamento"]["usada_por"], ["Faturamento LY", "Variação Anual"])
        self.assertEqual(m["Faturamento"]["guias"], ["Visão Geral"])
        self.assertEqual(m["Medida Solta"]["guias"], [])
        self.assertEqual(m["Medida Solta"]["usada_por"], [])


class TestPreflight(Base):
    def test_fora_de_src_avisa(self):
        avisos = lv.preflight(self.root.parent.parent)
        self.assertTrue(any("src/<slug>" in a for a in avisos))

    def test_pbix_sem_pbip(self):
        pasta = self.tmp / "src" / "x"
        pasta.mkdir(parents=True)
        (pasta / "a.pbix").write_bytes(b"")
        self.assertTrue(any(".pbix" in a for a in lv.preflight(pasta)))

    def test_projeto_correto_sem_avisos(self):
        self.assertEqual(lv.preflight(self.root), [])


class TestGeracao(Base):
    def test_cria_as_paginas(self):
        codigo, saida = self.gerar()
        self.assertEqual(codigo, 0, saida)
        esperadas = {"modelo-de-dados.md", "medidas-dax/index.md", "medidas-dax/01-principais.md",
                     "medidas-dax/02-temporais.md", "medidas-dax/sem-pasta.md"}
        achadas = {p.relative_to(self.docs).as_posix() for p in self.docs.rglob("*.md")}
        self.assertEqual(achadas, esperadas)

    def test_nunca_escreve_no_projeto_powerbi(self):
        antes = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.gerar()
        depois = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(antes, depois)

    def test_recusa_docs_dentro_do_projeto(self):
        codigo, _ = rodar("--root", str(self.root), "--docs", str(self.root / "docs"))
        self.assertNotEqual(codigo, 0)
        self.assertFalse((self.root / "docs").exists())

    def test_modelo_de_dados(self):
        self.gerar()
        t = self.ler("modelo-de-dados.md")
        self.assertIn("**7 tabelas**: 6 de negócio e 1 de data automática", t)
        self.assertIn("fVendas }o..|| dCalendario", t)            # inativo
        self.assertIn("(bidirecional)", t)                          # filtro nos dois sentidos
        self.assertNotIn("LocalDateTable", t.split("## Tabelas")[0])  # auto-data fora do ER
        self.assertIn("### `fVendas`", t)
        self.assertIn("**Tipo (inferido):** fato", t)
        self.assertIn("**Tipo (inferido):** dimensão", t)
        self.assertIn("tabela calculada (DAX)", t)
        self.assertIn("Sql.Database (import)", t)
        self.assertIn("## Hierarquias", t)
        self.assertIn("Ano e Mês", t)
        self.assertIn("## Grupos de cálculo", t)
        self.assertIn("Ano Anterior", t)
        self.assertIn("## Segurança em nível de linha (RLS)", t)
        self.assertIn("Papel `Vendedor`", t)
        self.assertIn("[Email] = USERPRINCIPALNAME()", t)
        self.assertIn("`Valor Líquido`", t)

    def test_pagina_de_medidas(self):
        self.gerar()
        t = self.ler("medidas-dax/02-temporais.md")
        self.assertTrue(t.startswith("<!-- pasta: 02. Temporais -->"))
        self.assertIn("## Faturamento LY", t)
        self.assertIn("[`Faturamento`](01-principais.md#faturamento)", t)   # link entre páginas
        self.assertIn("[`Variação Anual`](#variacao-anual)", t)             # link na mesma página
        self.assertIn("Usada nas guias:** *Visão Geral*", self.ler("medidas-dax/01-principais.md"))
        self.assertIn("Soma do valor líquido das vendas.", self.ler("medidas-dax/01-principais.md"))
        self.assertIn("!!! pendente", t)                                   # sem /// no modelo
        sem = self.ler("medidas-dax/sem-pasta.md")
        self.assertIn("## Medida Solta", sem)
        idx = self.ler("medidas-dax/index.md")
        self.assertIn("| **Total** | 4 |", idx)

    def test_link_de_guia_so_se_a_pagina_existe(self):
        (self.docs / "guias-do-relatorio").mkdir(parents=True)
        self.escrever("guias-do-relatorio/visao-geral.md", "# Visão Geral\n")
        self.gerar()
        self.assertIn("[Visão Geral](../guias-do-relatorio/visao-geral.md)",
                      self.ler("medidas-dax/01-principais.md"))

    def test_idempotente_e_check(self):
        self.gerar()
        codigo, saida = self.gerar("--check")
        self.assertEqual(codigo, 0, saida)
        self.assertIn("sem mudança: 5", saida)

    def test_check_detecta_pagina_desatualizada(self):
        self.gerar()
        p = self.tmdl("tables/_Medidas.tmdl")
        p.write_text(p.read_text(encoding="utf-8").replace("measure 'Medida Solta' = 1",
                                                           "measure 'Medida Solta' = 2"),
                     encoding="utf-8", newline="\n")
        codigo, saida = self.gerar("--check")
        self.assertEqual(codigo, 1)
        self.assertIn("~ medidas-dax/sem-pasta.md", saida)
        self.assertNotIn("```dax\n2\n```", self.ler("medidas-dax/sem-pasta.md"))   # --check não escreve

    def test_preserva_texto_manual_e_atualiza_o_gerado(self):
        self.gerar()
        pag = "medidas-dax/02-temporais.md"
        t = self.ler(pag)
        pendente = g.descricao_padrao({"nome": "Faturamento LY"})
        self.assertIn(pendente, t)
        self.escrever(pag, t.replace(pendente, "Faturamento do mesmo período do ano anterior.\n\n"
                                     "Regra validada pela diretoria comercial."))
        p = self.tmdl("tables/_Medidas.tmdl")
        p.write_text(p.read_text(encoding="utf-8").replace("SAMEPERIODLASTYEAR", "DATEADD_ANO"),
                     encoding="utf-8", newline="\n")
        self.gerar()
        novo = self.ler(pag)
        self.assertIn("Regra validada pela diretoria comercial.", novo)
        self.assertIn("DATEADD_ANO", novo)
        self.assertNotIn("SAMEPERIODLASTYEAR", novo)

    def test_pendente_vira_descricao_quando_o_modelo_ganha_docstring(self):
        self.gerar()
        p = self.tmdl("tables/_Medidas.tmdl")
        p.write_text(p.read_text(encoding="utf-8").replace(
            "\tmeasure 'Medida Solta' = 1", "\t/// Valor fixo de teste.\n\tmeasure 'Medida Solta' = 1"),
            encoding="utf-8", newline="\n")
        self.gerar()
        sem = self.ler("medidas-dax/sem-pasta.md")
        self.assertIn("Valor fixo de teste.", sem)
        self.assertNotIn("!!! pendente", sem)

    def test_medida_removida_nao_apaga_a_secao(self):
        self.gerar()
        p = self.tmdl("tables/_Medidas.tmdl")
        texto = p.read_text(encoding="utf-8")
        ini = texto.index("\tmeasure 'Medida Solta'")
        fim = texto.index("\tpartition")
        p.write_text(texto[:ini] + texto[fim:], encoding="utf-8", newline="\n")
        _, saida = self.gerar()
        sem = self.ler("medidas-dax/sem-pasta.md")
        self.assertIn("## Medida Solta", sem)
        self.assertIn("Removido do modelo", sem)
        self.assertIn("saiu do modelo: medida:Medida Solta", saida)
        _, saida2 = self.gerar()
        self.assertEqual(self.ler("medidas-dax/sem-pasta.md"), sem)   # estável na 2ª rodada
        self.assertIn("sem mudança: 5", saida2)

    def test_medida_nova_entra_na_ordem(self):
        self.gerar()
        p = self.tmdl("tables/_Medidas.tmdl")
        p.write_text(p.read_text(encoding="utf-8").replace(
            "\tmeasure 'Variação Anual'",
            "\tmeasure 'Faturamento Zeta' = [Faturamento]\n\t\tdisplayFolder: 02. Temporais\n\n"
            "\tmeasure 'Variação Anual'"), encoding="utf-8", newline="\n")
        self.gerar()
        t = self.ler("medidas-dax/02-temporais.md")
        ordem = [t.index(f"## {n}") for n in ("Faturamento LY", "Faturamento Zeta", "Variação Anual")]
        self.assertEqual(ordem, sorted(ordem))

    def test_pasta_renomeada_mantem_o_arquivo(self):
        self.gerar()
        p = self.tmdl("tables/_Medidas.tmdl")
        p.write_text(p.read_text(encoding="utf-8").replace("02. Temporais", "02. Comparativos"),
                     encoding="utf-8", newline="\n")
        # a página existente continua sendo a mesma URL, mesmo com a pasta nova
        self.escrever("medidas-dax/02-temporais.md",
                      self.ler("medidas-dax/02-temporais.md").replace(
                          "<!-- pasta: 02. Temporais -->", "<!-- pasta: 02. Comparativos -->"))
        self.gerar()
        achadas = {p.name for p in (self.docs / "medidas-dax").glob("*.md")}
        self.assertIn("02-temporais.md", achadas)
        self.assertNotIn("02-comparativos.md", achadas)

    def test_tabela_nova_entra_antes_das_secoes_finais(self):
        self.gerar()
        (self.tmdl("tables/aTeste.tmdl")).write_text(
            "table aTeste\n\tcolumn Id\n\t\tdataType: int64\n", encoding="utf-8", newline="\n")
        self.gerar()
        t = self.ler("modelo-de-dados.md")
        self.assertIn("### `aTeste`", t)
        self.assertLess(t.index("### `aTeste`"), t.index("## Hierarquias"))
        self.assertEqual(t.count("\n## Tabelas\n"), 1)

    def test_copia_intacta_do_modelo_e_substituida(self):
        for rel in ("modelo-de-dados.md", "medidas-dax/index.md", "medidas-dax/sem-pasta.md"):
            (self.docs / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(AQUI.parent.parent / "modelos" / "projeto" / rel, self.docs / rel)
        codigo, saida = self.gerar()
        self.assertEqual(codigo, 0, saida)
        for rel in ("modelo-de-dados.md", "medidas-dax/index.md", "medidas-dax/sem-pasta.md"):
            t = self.ler(rel)
            self.assertNotIn("modelo-nao-preenchido", t)
            self.assertNotIn("<Projeto>", t)
            self.assertIn("<!-- gerado:inicio", t)

    def test_pagina_antiga_sem_marcadores_nao_e_tocada(self):
        self.docs.mkdir(parents=True)
        original = "# Modelo de dados\n\nTexto escrito à mão em outro formato.\n"
        self.escrever("modelo-de-dados.md", original)
        codigo, saida = self.gerar()
        self.assertEqual(codigo, 0, saida)
        self.assertEqual(self.ler("modelo-de-dados.md"), original)
        self.assertIn("sem marcadores `gerado`", saida)


class TestDiagrama(unittest.TestCase):
    def test_divide_em_visoes_acima_do_limite(self):
        rels = []
        for i in range(g.LIMITE_ER + 3):
            rels.append({"de": f"f{i % 3}.Id{i}", "para": f"d{i}.Id{i}", "ativo": True,
                         "de_card": "many", "para_card": "one", "filtro": "oneDirection"})
        negocio = {f"f{i}" for i in range(3)} | {f"d{i}" for i in range(g.LIMITE_ER + 3)}
        txt = g.diagrama_er(rels, negocio)
        self.assertIn("### Visão: `f0`", txt)
        self.assertIn("### Visão completa", txt)
        self.assertEqual(txt.count("```mermaid"), 4)

    def test_nome_com_espaco_vira_underscore(self):
        rels = [{"de": "'Fato Vendas'.Id", "para": "'Dim Cliente'.Id", "ativo": True,
                 "de_card": "many", "para_card": "one", "filtro": "oneDirection"}]
        txt = g.diagrama_er(rels, {"Fato Vendas", "Dim Cliente"})
        self.assertIn("Fato_Vendas }o--|| Dim_Cliente", txt)


@unittest.skipUnless(os.environ.get("BI_PROJETO_REAL"), "defina BI_PROJETO_REAL para rodar")
class TestProjetoReal(unittest.TestCase):
    def test_gera_e_e_idempotente(self):
        root = Path(os.environ["BI_PROJETO_REAL"])
        docs = Path(tempfile.mkdtemp(prefix="bi-real-"))
        self.addCleanup(shutil.rmtree, docs, ignore_errors=True)
        d = lv.carregar_projeto(root)
        c1, s1 = rodar("--root", str(root), "--docs", str(docs))
        c2, s2 = rodar("--root", str(root), "--docs", str(docs), "--check")
        self.assertEqual((c1, c2), (0, 0), s1 + s2)
        total = sum(len(t["medidas"]) for t in d["tabelas"])
        self.assertIn(f"| **Total** | {total} |", (docs / "medidas-dax" / "index.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
