"""
Pré-processamento das séries de preços.
"""

import numpy as np
import pandas as pd


def preprocessar(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Aplica forward-fill conservador e calcula retornos logarítmicos mensais.

    Parameters
    ----------
    df : pd.DataFrame
        Séries de preços brutas com possíveis valores ausentes.

    Returns
    -------
    precos : pd.DataFrame
        Preços após preenchimento (máximo 2 meses consecutivos).
    retornos : pd.DataFrame
        Retornos logarítmicos r_t = ln(P_t / P_{t-1}), sem a primeira linha.
    """
    precos   = df.ffill(limit=2)
    retornos = np.log(precos / precos.shift(1)).dropna()
    return precos, retornos
