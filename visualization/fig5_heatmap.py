"""
Figura 5 — Heatmap de D (Higuchi) por commodity e período trienal.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from estimators import dim_higuchi


def fig5_heatmap_d(
    log_precos: pd.DataFrame,
    savepath: str | None = None,
) -> plt.Figure:
    """
    Heatmap de D (Higuchi) calculado em janelas trienais sobre log(preços).

    Parâmetros
    ----------
    log_precos : pd.DataFrame
        Log dos preços mensais por commodity.
    savepath : str | None

    Returns
    -------
    plt.Figure
    """
    periodos = pd.date_range("1995-01-01", "2024-12-31", freq="3YS")
    labels   = [str(p.year) for p in periodos]
    matriz   = pd.DataFrame(index=log_precos.columns, columns=labels[:-1])

    for col in log_precos.columns:
        r = log_precos[col].dropna()
        for j in range(len(periodos) - 1):
            sub = r.loc[periodos[j] : periodos[j + 1]]
            if len(sub) >= 30:
                matriz.loc[col, labels[j]] = dim_higuchi(sub.values, k_max=8)

    matriz = matriz.astype(float)

    fig, ax = plt.subplots(figsize=(14, 4))
    im = ax.imshow(matriz.values, aspect="auto", cmap="RdYlGn_r",
                   vmin=1.25, vmax=1.75)

    ax.set_xticks(range(len(matriz.columns)))
    ax.set_xticklabels(matriz.columns, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(matriz.index)))
    ax.set_yticklabels(matriz.index, fontsize=10)

    for i in range(len(matriz.index)):
        for j in range(len(matriz.columns)):
            val = matriz.iloc[i, j]
            if not np.isnan(val):
                cor_txt = "black" if 1.35 < val < 1.65 else "white"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                        fontsize=8, color=cor_txt)

    cbar = fig.colorbar(im, ax=ax, orientation="vertical",
                        fraction=0.02, pad=0.02)
    cbar.set_label("D (Higuchi)")
    cbar.ax.axhline(1.5, color="black", linewidth=1.5, linestyle="--")

    ax.set_title(
        "Figura 5 — Heatmap de rugosidade geométrica D (Higuchi) por commodity e período trienal",
        fontweight="bold", fontsize=11,
    )
    fig.tight_layout()

    if savepath:
        fig.savefig(savepath, bbox_inches="tight", dpi=200)

    return fig
