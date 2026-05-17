"""
Estatísticas globais: tabelas comparativas entre estimadores de D.

Nota metodológica
-----------------
Higuchi mede a dimensão fractal do *caminho geométrico*
da série. Devem ser aplicados ao log(preços), que é o objeto geométrico
de interesse. Aplicados a retornos logarítmicos (série estacionária
oscilando em torno de zero), ambos convertem invariavelmente para D ≈ 2
porque a série se comporta como ruído branco.

O DFA, por construção, integra os retornos antes de analisar (equivalendo
a analisar o caminho de preços), por isso hurst_dfa() recebe retornos e
o benchmark teórico 2 − H estima a dimensão do caminho de preços.

Os três estimadores ficam comparáveis apenas quando Higuchi
recebe log(preços) e DFA recebe retornos.
"""

import numpy as np
import pandas as pd
from scipy import stats

from config import CLASSES
from estimators import dim_higuchi, hurst_dfa


def tabela_dimensao_global(
    precos: pd.DataFrame,
    retornos: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula D_Higuchi sobre log(preços) e H_DFA sobre retornos.
    O benchmark teórico D = 2 − H permite comparar os dois estimadores.

    Parameters
    ----------
    precos : pd.DataFrame
        Preços mensais por commodity.
    retornos : pd.DataFrame
        Retornos logarítmicos mensais por commodity.

    Returns
    -------
    pd.DataFrame
        Tabela indexada por commodity com as colunas:
        Classe, D (Higuchi), H (DFA), 2 − H (teórico),
        Discrepância, Rugosidade.
    """
    rows = []

    for col in retornos.columns:
        r   = retornos[col].dropna().values
        lnp = np.log(precos[col].dropna().values)
        print(f"  Estimando dimensões: {col}...")

        d_hig = dim_higuchi(lnp)
        h_dfa = hurst_dfa(r)
        d_teo = 2.0 - h_dfa if not np.isnan(h_dfa) else np.nan
        disc  = round(d_hig - d_teo, 4) if not np.isnan(d_hig + d_teo) else np.nan

        rows.append({
            "Commodity"       : col,
            "Classe"          : CLASSES.get(col, ""),
            "D (Higuchi)"     : round(d_hig, 4),
            "H (DFA)"         : round(h_dfa, 4),
            "2 − H (teórico)" : round(d_teo, 4),
            "Discrepância"    : disc,
            "Rugosidade"      : _classificar(d_hig),
        })

    return pd.DataFrame(rows).set_index("Commodity")



def tabela_concordancia(tab: pd.DataFrame) -> pd.DataFrame:
    """
    Avalia a concordância entre D (Higuchi) e 2 − H (DFA) pelo
    coeficiente de correlação de Pearson e pelo RMSE.

    Parameters
    ----------
    tab : pd.DataFrame
        Saída de `tabela_dimensao_global`.

    Returns
    -------
    pd.DataFrame
        Correlação e RMSE entre Higuchi e 2 − H.
    """
    d_hig = tab["D (Higuchi)"].values
    d_teo = tab["2 − H (teórico)"].values
    mask  = np.isfinite(d_hig) & np.isfinite(d_teo)

    r    = float(np.corrcoef(d_hig[mask], d_teo[mask])[0, 1])
    rmse = float(np.sqrt(np.mean((d_hig[mask] - d_teo[mask]) ** 2)))

    return pd.DataFrame([{
        "Par"           : "Higuchi × 2 − H (DFA)",
        "Correlação (r)": round(r, 4),
        "RMSE"          : round(rmse, 4),
    }])


def _classificar(d: float) -> str:
    if np.isnan(d):
        return ""
    if d > 1.6:
        return "Alta (D > 1.6)"
    if d > 1.4:
        return "Média (1.4 – 1.6)"
    return "Baixa (D < 1.4)"