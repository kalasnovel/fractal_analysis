"""
Figura 3 — Scatter D_Higuchi vs 2 − H: teste empírico da identidade D + H = 2.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

from config import CORES


def fig3_scatter_concordancia(
    tab: pd.DataFrame,
    savepath: str | None = None,
) -> plt.Figure:
    """
    Scatter plot D_Higuchi vs D_teórico = 2 − H.
    A linha de 45° representa concordância perfeita.
    Desvios indicam multifractalidade latente.

    Parâmetros
    ----------
    tab : pd.DataFrame
        Saída de `tabela_dimensao_global`.
    savepath : str | None

    Returns
    -------
    plt.Figure
    """
    d_hig = tab["D (Higuchi)"].values
    d_teo = tab["2 − H (teórico)"].values
    nomes = tab.index.tolist()

    fig, ax = plt.subplots(figsize=(7, 6))

    for i, nome in enumerate(nomes):
        cor = CORES.get(nome, "gray")
        ax.scatter(d_teo[i], d_hig[i], color=cor, s=120, zorder=5,
                   edgecolors="white", linewidth=0.8)
        ax.annotate(
            nome,
            (d_teo[i], d_hig[i]),
            textcoords="offset points",
            xytext=(7, 4),
            fontsize=8.5,
            color=cor,
        )

    lim_min = min(np.nanmin(d_hig), np.nanmin(d_teo)) - 0.05
    lim_max = max(np.nanmax(d_hig), np.nanmax(d_teo)) + 0.05
    ax.plot([lim_min, lim_max], [lim_min, lim_max],
            color="black", linewidth=1.0, linestyle="--",
            label="Concordância perfeita (D = 2 − H)")

    mask = np.isfinite(d_hig) & np.isfinite(d_teo)
    if mask.sum() >= 2:
        r = np.corrcoef(d_teo[mask], d_hig[mask])[0, 1]
        rmse = np.sqrt(np.mean((d_hig[mask] - d_teo[mask]) ** 2))
        ax.text(
            0.05, 0.94,
            f"r = {r:.3f}  ·  RMSE = {rmse:.3f}\nn = 4 · evidência apenas descritiva",
            transform=ax.transAxes,
            fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.85, ec="#888"),
            verticalalignment="top",
        )

    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)
    ax.set_xlabel("D teórico = 2 − H (DFA)")
    ax.set_ylabel("D estimado (Higuchi)")
    ax.set_title(
        "Figura 3 — Concordância numérica entre D (Higuchi) e D teórico = 2 − H",
        fontweight="bold",
    )
    ax.legend()
    fig.tight_layout()

    if savepath:
        fig.savefig(savepath, bbox_inches="tight", dpi=200)

    return fig