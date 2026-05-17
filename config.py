"""
Parâmetros globais do projeto.
"""

# ── API ───────────────────────────────────────────────────────────────────────
FRED_API_KEY = ""

# ── Séries de preços (FRED tickers) ──────────────────────────────────────────
COMMODITIES: dict[str, str] = {
    "WTI"   : "DCOILWTICO",
    "Brent" : "DCOILBRENTEU",
    "Soja"  : "PSOYBUSDM",        # Global price of Soybeans, USD/metric ton (IMF)
    "Milho" : "PMAIZMTUSDM",      # Global price of Maize, USD/metric ton (IMF)
}

CLASSES: dict[str, str] = {
    "WTI"   : "Energético",
    "Brent" : "Energético",
    "Soja"  : "Agrícola",
    "Milho" : "Agrícola",
}

# Tickers alternativos tentados automaticamente se o principal falhar
COMMODITIES_FALLBACK: dict[str, list[str]] = {
    "WTI"   : ["MCOILWTICO"],
    "Brent" : ["MCOILBRENTEU"],
    "Soja"  : [],
    "Milho" : [],
}

# Reservado para extensões futuras
COMMODITIES_YFINANCE: dict[str, str] = {}

# ── Período ───────────────────────────────────────────────────────────────────
DATA_INICIO = "1990-01-01"
DATA_FIM    = "2024-12-31"

# ── Parâmetros de estimação ───────────────────────────────────────────────────
BOX_N_ESCALAS  = 20     # número de escalas ε no box-counting
HIGUCHI_K_MAX  = 10     # máximo intervalo k no método de Higuchi
DFA_ORDEM      = 1      # ordem do polinômio de detrending no DFA
JANELA_ROLLING = 60     # meses na janela deslizante

# ── Eventos históricos marcados nas figuras ───────────────────────────────────
EVENTOS: dict[str, str] = {
    "Crise 2008"    : "2008-09-01",
    "OPEP 2014"     : "2014-11-01",
    "Covid-19 2020" : "2020-03-01",
    "Ucrânia 2022"  : "2022-02-01",
}

# ── Paleta de cores por commodity ─────────────────────────────────────────────
CORES: dict[str, str] = {
    "WTI"   : "#D85A30",
    "Brent" : "#BA7517",
    "Soja"  : "#1D9E75",
    "Milho" : "#7F77DD",
}

# ── Diretório de saída ────────────────────────────────────────────────────────
OUTPUT_DIR = "outputs"
