"""
Dimensão fractal em janela deslizante (rolling).

A série passada deve ser log(preços), não retornos.
"""

import numpy as np
import pandas as pd

from config import JANELA_ROLLING
from estimators import dim_higuchi, dim_box_counting


def d_rolling(
    log_precos: pd.Series,
    janela: int = JANELA_ROLLING,
    metodo: str = "higuchi",
) -> pd.Series:
    """
    Calcula a dimensão fractal do caminho de log(preços) em janela
    deslizante mês a mês.

    Parameters
    ----------
    log_precos : pd.Series
        Log dos preços mensais com índice DatetimeIndex.
    janela : int
        Número de observações por janela.
    metodo : str
        "higuchi" (padrão) ou "box_counting".

    Returns
    -------
    pd.Series
        Série D(t) com o mesmo índice de `log_precos`.
        As primeiras `janela − 1` posições são NaN.
    """
    fn = dim_higuchi if metodo == "higuchi" else dim_box_counting

    valores = [np.nan] * len(log_precos)

    for i in range(janela, len(log_precos) + 1):
        sub            = log_precos.iloc[i - janela : i].values
        valores[i - 1] = fn(sub)

    return pd.Series(valores, index=log_precos.index, name=f"D_{metodo}")
