"""
Figura 2 — Barras agrupadas comparando D_box, D_Higuchi e 2 − H por commodity.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from config import CORES


def fig2_barras_comparativo(
    tab: pd.DataFrame,
    savepath: str | None = None,
) -> plt.Figure:
    """
    Barras agrupadas com os três estimadores de D para cada commodity.
    Linha horizontal em D = 1.5 marca o benchmark de random walk.

    Parâmetros
    ----------
    tab : pd.DataFrame
        Saída de `tabela_dimensao_global`.
    savepath : str | None

    Returns
    -------
    plt.Figure
    """
    nomes = tab.index.tolist()
    d_hig = tab["D (Higuchi)"].values
    d_teo = tab["2 − H (teórico)"].values
    x     = np.arange(len(nomes))
    w     = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))

    b1 = ax.bar(x - w / 2, d_hig, w, label="Higuchi",      color="#1D9E75", alpha=0.85)
    b2 = ax.bar(x + w / 2, d_teo, w, label="2 − H (DFA)",  color="#D85A30", alpha=0.85)

    ax.axhline(1.5, color="black", linewidth=1.1, linestyle="--",
               label="D = 1.5  (H = 0.5)")
    ax.axhspan(1.5, 2.0, alpha=0.04, color="#E24B4A")
    ax.axhspan(1.0, 1.5, alpha=0.04, color="#1D9E75")

    for bars in (b1, b2):
        for bar in bars:
            h = bar.get_height()
            if np.isfinite(h):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    h + 0.003,
                    f"{h:.3f}",
                    ha="center", va="bottom", fontsize=8.5,
                )

    ax.set_xticks(x)
    ax.set_xticklabels(nomes, rotation=15, ha="right")
    ax.set_ylim(1.15, 1.85)
    ax.set_ylabel("Dimensão Fractal D")
    ax.set_title(
        "Figura 2 — Dimensão fractal por commodity, Higuchi e 2 − H (DFA)",
        fontweight="bold",
    )
    ax.legend()
    fig.tight_layout()

    if savepath:
        fig.savefig(savepath, bbox_inches="tight", dpi=200)

    return fig