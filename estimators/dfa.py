"""
Expoente de Hurst via Detrended Fluctuation Analysis (DFA).

Usado exclusivamente como benchmark teórico: D_teo = 2 − H.

Referência:
    Peng, C.-K. et al. (1994). Mosaic organization of DNA nucleotides.
    Physical Review E, 49(2), 1685–1689.
"""

import numpy as np

from config import DFA_ORDEM


def hurst_dfa(
    serie: np.ndarray,
    ordem: int = DFA_ORDEM,
) -> float:
    """
    Estima o Expoente de Hurst H pelo método DFA.

    Integra a série (perfil), divide em segmentos de tamanho s, remove
    tendência polinomial local de grau `ordem` em cada segmento e calcula
    a flutuação média F(s). O expoente H é a inclinação de log F(s) vs log s.

    Parameters
    ----------
    serie : np.ndarray
        Série de retornos logarítmicos.
    ordem : int
        Grau do polinômio de detrending. 1 = linear (DFA-1).

    Returns
    -------
    float
        Expoente de Hurst H. Retorna np.nan se dados insuficientes.

    Notes
    -----
    H < 0.5 : anti-persistente (reversão à média).
    H = 0.5 : random walk.
    H > 0.5 : persistente (memória longa).

    O benchmark teórico da dimensão fractal é D = 2 − H.
    """
    n = len(serie)
    if n < 32:
        return np.nan

    perfil = np.cumsum(serie - serie.mean())
    lags   = np.unique(
        np.floor(np.logspace(np.log10(4), np.log10(n // 4), 20)).astype(int)
    )

    flutuacoes, lag_vals = [], []

    for lag in lags:
        n_seg = n // lag
        if n_seg < 4:
            continue
        f2 = []
        for s in range(n_seg):
            seg  = perfil[s * lag : (s + 1) * lag]
            coef = np.polyfit(np.arange(lag), seg, ordem)
            tend = np.polyval(coef, np.arange(lag))
            f2.append(np.mean((seg - tend) ** 2))
        flutuacoes.append(np.sqrt(np.mean(f2)))
        lag_vals.append(lag)

    if len(lag_vals) < 3:
        return np.nan

    slope, *_ = np.polyfit(np.log(lag_vals), np.log(flutuacoes), 1)
    return float(slope)
