"""Funções de apoio compartilhadas pelos scripts de carga."""


def limpar_colunas(df):
    """Remove espaços e coloca os nomes das colunas em minúsculas."""
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def sem_docstring(x, y=1, *, z=None):
    return x


def _interna():
    """Não aparece na tabela."""


class Auditor:
    """Registra quantas linhas cada carga processou."""

    def __init__(self, nivel="info"):
        self.nivel = nivel

    def registrar(self, n: int) -> None:
        """Escreve o total de linhas no log."""
        print(n)
