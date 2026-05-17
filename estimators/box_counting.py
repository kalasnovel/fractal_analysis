"""
Box-counting dimension para séries temporais 1-D.

Referência:
    Falconer, K. (1990). Fractal Geometry: Mathematical Foundations
    and Applications. Chichester: Wiley.
"""

import numpy as np

from config import BOX_N_ESCALAS


def dim_box_counting(
    serie: np.ndarray,
    n_escalas: int = BOX_N_ESCALAS,
) -> float:
    """
    Estima a dimensão fractal pelo método de box-counting.

    Normaliza a série para [0, 1] em ambas as dimensões, cria uma grade
    de células ε × ε e conta N(ε) caixas que contêm ao menos um ponto.
    A dimensão é a inclinação de log N(ε) vs log(1/ε).

    Parâmetros
    ----------
    serie : np.ndarray
        Série temporal (retornos ou preços).
    n_escalas : int
        Número de escalas ε em progressão logarítmica.

    Retornos
    -------
    float
        Dimensão fractal estimada. Retorna np.nan se a série for
        curta ou degenerada.

    Notas
    -----
    Intervalo teórico: 1 ≤ D ≤ 2.
    D → 1 : série suave (persistente).
    D → 2 : série preenche o plano (anti-persistente / rugosa).
    """
    n = len(serie)
    if n < 32:
        return np.nan

    x        = np.linspace(0, 1, n)
    y_range  = serie.max() - serie.min()
    y        = (serie - serie.min()) / (y_range + 1e-10)

    epsilons = np.logspace(-3, -0.5, n_escalas)
    counts   = []

    for eps in epsilons:
        xi    = (x / eps).astype(int)
        yi    = (y / eps).astype(int)
        boxes = set(zip(xi, yi))
        counts.append(len(boxes))

    log_eps = np.log(epsilons)
    log_cnt = np.log(counts)
    mask    = np.isfinite(log_cnt) & (np.array(counts) > 1)

    if mask.sum() < 4:
        return np.nan

    slope, *_ = np.polyfit(log_eps[mask], log_cnt[mask], 1)
    return float(-slope)
