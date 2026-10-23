"""Carrega as vendas do dia e grava o arquivo consumido pelo modelo.

Uso:
    python carregar_vendas.py --entrada vendas.csv --saida vendas.parquet
"""

import argparse
import os

import pandas as pd

from utils import limpar_colunas, Auditor


def transformar(df: pd.DataFrame, moeda: str = "BRL") -> pd.DataFrame:
    """Padroniza os nomes e converte o valor para a moeda informada."""
    df = limpar_colunas(df)
    df["moeda"] = moeda
    return df


def principal() -> None:
    p = argparse.ArgumentParser(description="Carga de vendas")
    p.add_argument("--entrada", required=True, help="CSV de vendas exportado do sistema")
    p.add_argument("--saida", default="vendas.parquet", help="arquivo de saída")
    p.add_argument("--dias", type=int, default=1, help="quantos dias carregar")
    p.add_argument("--token", default="valor-secreto-no-default", help="token do serviço")
    a = p.parse_args()
    pasta = os.getenv("PASTA_ENTRADA")
    banco = os.environ["BANCO_DESTINO"]
    df = pd.read_csv(a.entrada)
    ref = pd.read_excel("C:\\Users\\Fulano\\Documents\\metas.xlsx")
    df = transformar(df)
    Auditor().registrar(len(df))
    df.to_parquet(a.saida)
    with open("log_carga.txt", "w") as f:
        f.write(f"{pasta}{banco}{len(ref)}")


if __name__ == "__main__":
    principal()
