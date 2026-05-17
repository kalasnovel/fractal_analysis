"""
Coleta de séries de preços de commodities.

Fontes:
    - FRED (Federal Reserve Economic Data): dados reais via API.
    - Sintético: aproximação de fBm para execução sem chave FRED.
"""

import numpy as np
import pandas as pd

from config import COMMODITIES, COMMODITIES_FALLBACK, COMMODITIES_YFINANCE, DATA_INICIO, DATA_FIM


def coletar_dados(api_key: str) -> pd.DataFrame:
    """
    Baixa as séries mensais do FRED e retorna um DataFrame com
    índice DatetimeIndex de frequência mensal (MS).

    Séries diárias (WTI, Brent) são resampladas para a média mensal.
    Se o ticker principal falhar, tenta os fallbacks definidos em
    COMMODITIES_FALLBACK antes de encerrar com erro.

    Parameters
    ----------
    api_key : str
        Chave de acesso à API do FRED.
        Obtenha gratuitamente em https://fred.stlouisfed.org/docs/api/api_key.html

    Returns
    -------
    pd.DataFrame
        Colunas = nomes das commodities, índice = datas mensais.
    """
    try:
        from fredapi import Fred
    except ImportError:
        raise ImportError(
            "Pacote fredapi não encontrado. Execute: pip install fredapi"
        )

    fred   = Fred(api_key=api_key)
    frames = {}

    for nome, ticker_principal in COMMODITIES.items():
        candidatos = [ticker_principal] + COMMODITIES_FALLBACK.get(nome, [])
        serie      = None

        for ticker in candidatos:
            try:
                raw   = fred.get_series(
                    ticker,
                    observation_start=DATA_INICIO,
                    observation_end=DATA_FIM,
                )
                serie = raw.resample("MS").mean()
                print(f"  [{ticker}] {nome} — OK")
                break
            except Exception as exc:
                print(f"  [{ticker}] {nome} — falhou ({exc}), tentando próximo...")


        if serie is None:
            tentados = ", ".join(candidatos)
            raise RuntimeError(
                f"Não foi possível baixar '{nome}'. "
                f"Tickers FRED tentados: {tentados}. "
                f"Verifique os IDs em config.py ou use dados sintéticos."
            )

        frames[nome] = serie

    df       = pd.DataFrame(frames)
    df.index = pd.to_datetime(df.index)
    return df.dropna(how="all")


def dados_simulados() -> pd.DataFrame:
    """
    Gera séries sintéticas com propriedades de memória longa controladas,
    utilizando aproximação de Movimento Browniano Fracionário (fBm).

    Valores de H usados (e D teórico correspondente):
        WTI   H = 0.65 → D ≈ 1.35
        Brent H = 0.63 → D ≈ 1.37
        Soja  H = 0.51 → D ≈ 1.49
        Milho H = 0.50 → D ≈ 1.50

    Returns
    -------
    pd.DataFrame
        Mesmo formato que `coletar_dados`.
    """
    np.random.seed(7)
    datas = pd.date_range(DATA_INICIO, DATA_FIM, freq="MS")
    n     = len(datas)

    def _fbm_approx(n: int, H: float, base: float = 100.0) -> np.ndarray:
        ruido = np.random.randn(n)
        pesos = np.array([k ** (H - 0.5) for k in range(1, n + 1)])
        serie = np.convolve(ruido, pesos / pesos.sum(), mode="full")[:n]
        return base * np.exp(np.cumsum(serie * 0.03))

    parametros = {
        "WTI"   : (0.65,  30.0),
        "Brent" : (0.63,  32.0),
        "Soja"  : (0.51, 250.0),
        "Milho" : (0.50, 150.0),
    }

    df = pd.DataFrame(
        {nome: _fbm_approx(n, H, base) for nome, (H, base) in parametros.items()},
        index=datas,
    )

    # Choque de demanda simulado
    idx = df.index.get_loc("2020-03-01")
    df.iloc[idx : idx + 3, [0, 1]] *= 0.55

    return df


def dados_simulados() -> pd.DataFrame:
    """
    Gera séries sintéticas com propriedades de memória longa controladas,
    utilizando aproximação de Movimento Browniano Fracionário (fBm).

    Valores de H usados (e D teórico correspondente):
        WTI   H = 0.65 → D ≈ 1.35
        Brent H = 0.63 → D ≈ 1.37
        Soja  H = 0.51 → D ≈ 1.49
        Milho H = 0.50 → D ≈ 1.50

    Returns
    -------
    pd.DataFrame
        Mesmo formato que `coletar_dados`.
    """
    np.random.seed(7)
    datas = pd.date_range(DATA_INICIO, DATA_FIM, freq="MS")
    n     = len(datas)

    def _fbm_approx(n: int, H: float, base: float = 100.0) -> np.ndarray:
        ruido = np.random.randn(n)
        pesos = np.array([k ** (H - 0.5) for k in range(1, n + 1)])
        serie = np.convolve(ruido, pesos / pesos.sum(), mode="full")[:n]
        return base * np.exp(np.cumsum(serie * 0.03))

    parametros = {
        "WTI"   : (0.65,  30.0),
        "Brent" : (0.63,  32.0),
        "Soja"  : (0.51, 250.0),
        "Milho" : (0.50, 150.0),
    }

    df = pd.DataFrame(
        {nome: _fbm_approx(n, H, base) for nome, (H, base) in parametros.items()},
        index=datas,
    )

    # Choque de demanda simulado (Covid)
    idx = df.index.get_loc("2020-03-01")
    df.iloc[idx : idx + 3, [0, 1]] *= 0.55

    return df
