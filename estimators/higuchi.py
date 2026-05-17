"""
Dimensão fractal pelo método de Higuchi (1988).

Referência:
    Higuchi, T. (1988). Approach to an irregular time series on the basis
    of the fractal theory. Physica D: Nonlinear Phenomena, 31(2), 277–283.
"""

import numpy as np

from config import HIGUCHI_K_MAX


def dim_higuchi(
    serie: np.ndarray,
    k_max: int = HIGUCHI_K_MAX,
) -> float:
    """
    Estima a dimensão fractal pelo comprimento médio da série em múltiplas
    escalas temporais.

    Para cada escala k e ponto de início m, constrói a sub-série
    x_m^k = {x(m), x(m+k), x(m+2k), ...} e calcula seu comprimento
    normalizado L_m(k). O comprimento médio L(k) segue L(k) ~ k^{-D},
    e D é estimado pela inclinação de log L(k) vs log k.

    Parâmetros
    ----------
    serie : np.ndarray
        Série temporal (retornos ou preços).
    k_max : int
        Máximo intervalo de sub-série. Para dados mensais, recomenda-se
        k_max entre 8 e 12.

    Retornos
    -------
    float
        Dimensão fractal estimada. Retorna np.nan se dados insuficientes.

    """
    n = len(serie)
    if n < 2 * k_max:
        return np.nan

    x      = np.asarray(serie, dtype=float)
    L_vals = []

    for k in range(1, k_max + 1):
        Lk = []
        for m in range(1, k + 1):
            idx   = np.arange(m - 1, n, k)
            x_sub = x[idx]
            if len(x_sub) < 2:
                continue
            norm = (n - 1) / (k * (len(x_sub) - 1) * k)
            Lmk  = np.sum(np.abs(np.diff(x_sub))) * norm
            Lk.append(Lmk)

        L_vals.append(np.mean(Lk) if Lk else np.nan)

    ks   = np.arange(1, k_max + 1, dtype=float)
    Ls   = np.array(L_vals)
    mask = np.isfinite(Ls) & (Ls > 0)

    if mask.sum() < 3:
        return np.nan

    slope, *_ = np.polyfit(np.log(ks[mask]), np.log(Ls[mask]), 1)
    return float(-slope)
