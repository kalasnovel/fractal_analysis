"""
Figura 4 — Rugosidade geométrica D em janela deslizante ao longo do tempo.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from config import CORES, EVENTOS, JANELA_ROLLING
from analysis.rolling import d_rolling


def fig4_d_rolling(
    log_precos: pd.DataFrame,
    savepath: str | None = None,
) -> plt.Figure:
    """
    Calcula e plota D (Higuchi) em janela deslizante para cada commodity.

    Parâmetros
    ----------
    log_precos : pd.DataFrame
        Log dos preços mensais por commodity.
    savepath : str | None

    Returns
    -------
    plt.Figure
    """
    print("  Calculando D rolling — aguarde...")

    fig, ax = plt.subplots(figsize=(14, 6))

    for col in log_precos.columns:
        serie  = log_precos[col].dropna()
        d_roll = d_rolling(serie, janela=JANELA_ROLLING, metodo="higuchi")
        ax.plot(d_roll.index, d_roll, label=col,
                color=CORES.get(col, "gray"), linewidth=1.4, alpha=0.85)

    ax.axhline(1.5, color="black", linewidth=1.0, linestyle="--", alpha=0.7,
               label="D = 1.5  (random walk)")
    ax.axhspan(1.5, 2.0, alpha=0.04, color="#E24B4A")
    ax.axhspan(1.0, 1.5, alpha=0.04, color="#1D9E75")

    # Definir ylim antes de posicionar os textos de eventos
    ax.set_ylim(1.10, 1.90)
    y_label = 1.87   # posição fixa abaixo do topo

    for label, data_ev in EVENTOS.items():
        x = pd.Timestamp(data_ev)
        ax.axvline(x, color="gray", linewidth=0.9, linestyle=":", alpha=0.8)
        ax.text(x, y_label, label,
                fontsize=7, rotation=90, va="top", ha="right", color="gray",
                clip_on=True)

    ax.text(pd.Timestamp("2000-06-01"), 1.62, "Rugoso (D > 1.5)",
            fontsize=9, color="#A32D2D", alpha=0.7)
    ax.text(pd.Timestamp("2000-06-01"), 1.32, "Suave (D < 1.5)",
            fontsize=9, color="#0F6E56", alpha=0.7)

    ax.set_ylabel(f"D (Higuchi) — janela {JANELA_ROLLING} meses")
    ax.set_xlabel("Data")
    ax.set_title(
        f"Figura 4 — Rugosidade geométrica rolling ({JANELA_ROLLING} meses)",
        fontweight="bold",
    )
    ax.legend(loc="lower right", ncol=2)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.xaxis.set_major_locator(mdates.YearLocator(4))
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()

    if savepath:
        fig.savefig(savepath, bbox_inches="tight", dpi=200)

    return fig