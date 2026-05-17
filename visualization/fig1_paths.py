"""
Figura 1 — Caminhos de preços coloridos por rugosidade geométrica D.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from config import EVENTOS


def fig1_caminhos_coloridos(
    precos: pd.DataFrame,
    tab: pd.DataFrame,
    savepath: str | None = None,
) -> plt.Figure:
    """
    Painel com os caminhos de preços de cada commodity, com cor
    proporcional ao valor de D (Higuchi): verde para D baixo
    (persistente / suave) e vermelho para D alto (rugoso).

    Parâmetros
    ----------
    precos : pd.DataFrame
        Preços mensais por commodity.
    tab : pd.DataFrame
        Tabela com coluna "D (Higuchi)" indexada por commodity.
    savepath : str | None
        Caminho para salvar a figura. Nenhum arquivo é salvo se None.

    Returns
    -------
    plt.Figure
    """
    commodities = list(precos.columns)
    ncols = 2
    nrows = (len(commodities) + 1) // ncols

    fig, axes = plt.subplots(nrows, ncols, figsize=(13, nrows * 3.2))
    axes      = axes.flatten()

    d_min, d_max = 1.2, 1.8
    cmap         = plt.cm.RdYlGn_r

    for i, col in enumerate(commodities):
        ax    = axes[i]
        d_val = tab.loc[col, "D (Higuchi)"]
        norm  = (d_val - d_min) / (d_max - d_min)
        cor   = cmap(np.clip(norm, 0, 1))

        ax.plot(precos.index, precos[col], color=cor, linewidth=1.1)

        for _, data_ev in EVENTOS.items():
            ax.axvline(
                pd.Timestamp(data_ev),
                color="gray", linewidth=0.8, linestyle=":", alpha=0.6,
            )

        ax.set_title(f"{col}  |  D = {d_val:.3f}", fontweight="bold")
        ax.set_ylabel("Preço (USD)")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.xaxis.set_major_locator(mdates.YearLocator(5))
        ax.tick_params(axis="x", rotation=30)

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.tight_layout(rect=[0, 0, 0.87, 0.92])

    sm   = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(d_min, d_max))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axes[:i+1], orientation="vertical",
                        fraction=0.015, pad=0.02, shrink=0.8)
    cbar.set_label("D (Higuchi) — rugosidade geométrica", labelpad=8)
    cbar.ax.axhline(1.5, color="black", linewidth=1.2, linestyle="--")

    fig.suptitle(
        "Figura 1 — Caminhos de preços com cor proporcional ao D (Higuchi) global da commodity",
        fontsize=12, fontweight="bold",
    )

    if savepath:
        fig.savefig(savepath, bbox_inches="tight", dpi=200)

    return fig