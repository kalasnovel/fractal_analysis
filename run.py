"""
Ponto de entrada principal do pipeline de análise.

Executa as etapas em sequência:
    1. Coleta de dados (FRED ou sintético)
    2. Pré-processamento
    3. Estimação global de D por commodity
    4. Avaliação de concordância entre métodos
    5. Geração das cinco figuras
    6. Impressão do sumário de resultados

Uso:
    python run.py
"""

import os
import sys
import numpy as np
from scipy import stats

import config
from data import coletar_dados, dados_simulados, preprocessar
from analysis import tabela_dimensao_global, tabela_concordancia
from visualization import (
    aplicar_estilo,
    fig1_caminhos_coloridos,
    fig2_barras_comparativo,
    fig3_scatter_concordancia,
    fig4_d_rolling,
    fig5_heatmap_d,
)


def main() -> None:
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    aplicar_estilo()

    # ── 1. Coleta ─────────────────────────────────────────────────────────────
    print("\n[1/5] Coletando dados...")
    if config.FRED_API_KEY == "SUA_CHAVE_AQUI":
        print("  Chave FRED não configurada — usando dados sintéticos.")
        print("  Edite FRED_API_KEY em config.py para usar dados reais.")
        df = dados_simulados()
    else:
        df = coletar_dados(config.FRED_API_KEY)

    print(f"  {len(df)} observações mensais "
          f"({df.index[0].date()} → {df.index[-1].date()})")

    # ── 2. Pré-processamento ──────────────────────────────────────────────────
    print("\n[2/5] Pré-processando séries...")
    precos, retornos = preprocessar(df)
    print(f"  {len(retornos)} retornos logarítmicos calculados.")

    # ── 3. Estimação global ───────────────────────────────────────────────────
    print("\n[3/5] Estimando dimensões fractais...")
    log_precos = np.log(precos)
    tab = tabela_dimensao_global(precos, retornos)

    print("\n  Tabela 1 — Dimensão fractal por commodity:")
    print(tab.to_string())
    tab.to_csv(os.path.join(config.OUTPUT_DIR, "tabela1_d_global.csv"))

    tab_conc = tabela_concordancia(tab)
    print("\n  Tabela 2 — Concordância entre estimadores:")
    print(tab_conc.to_string(index=False))
    tab_conc.to_csv(
        os.path.join(config.OUTPUT_DIR, "tabela2_concordancia.csv"),
        index=False,
    )

    # ── 4. Figuras ────────────────────────────────────────────────────────────
    print("\n[4/5] Gerando figuras...")

    _salvar = lambda nome: os.path.join(config.OUTPUT_DIR, nome)

    fig1_caminhos_coloridos(precos, tab, _salvar("fig1_paths.png"))
    print("  fig1_paths.png")

    fig2_barras_comparativo(tab, _salvar("fig2_bars.png"))
    print("  fig2_bars.png")

    fig3_scatter_concordancia(tab, _salvar("fig3_scatter.png"))
    print("  fig3_scatter.png")

    fig4_d_rolling(log_precos, _salvar("fig4_rolling.png"))
    print("  fig4_rolling.png")

    fig5_heatmap_d(log_precos, _salvar("fig5_heatmap.png"))
    print("  fig5_heatmap.png")

    # ── 5. Sumário ────────────────────────────────────────────────────────────
    print("\n[5/5] Sumário de resultados:")
    print("─" * 68)
    for idx, row in tab.iterrows():
        d    = row["D (Higuchi)"]
        dt   = row["2 − H (teórico)"]
        disc = row["Discrepância"]
        mark = "▲" if d > 1.5 else "▼"
        print(f"  {mark} {idx:<10}  D_Hig={d:.3f}  2−H={dt:.3f}"
              f"  Δ={disc:+.4f}  {row['Rugosidade']}")
    print("─" * 68)

    d_hig = tab["D (Higuchi)"].values
    d_teo = tab["2 − H (teórico)"].values
    mask  = np.isfinite(d_hig) & np.isfinite(d_teo)
    if mask.sum() >= 2:
        r, p   = stats.pearsonr(d_hig[mask], d_teo[mask])
        rmse   = np.sqrt(np.mean((d_hig[mask] - d_teo[mask]) ** 2))
        print(f"\n  Teste D + H = 2:  r = {r:.4f}  p = {p:.4f}  RMSE = {rmse:.4f}")

    print(f"\n  Saídas em ./{config.OUTPUT_DIR}/\n")


if __name__ == "__main__":
    main()
