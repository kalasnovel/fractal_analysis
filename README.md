# Dimensão Fractal de Séries de Preços de Commodities

Estimação da dimensão fractal de séries de preços de commodities pelo método de
Higuchi (1988), com comparação ao benchmark teórico D = 2 − H derivado via DFA.

## Estrutura

```
fractal_dimension/
├── config.py               # Constantes e parâmetros globais
├── run.py                  # Ponto de entrada principal
├── requirements.txt
├── data/
│   ├── collector.py        # Coleta via FRED API
│   └── preprocessor.py     # Retornos logarítmicos e limpeza
├── estimators/
│   ├── higuchi.py          # Dimensão fractal pelo método de Higuchi
│   └── dfa.py              # Expoente de Hurst via DFA → benchmark 2 − H
├── analysis/
│   ├── global_stats.py     # Tabelas comparativas entre métodos
│   └── rolling.py          # Dimensão fractal em janela deslizante
├── visualization/
│   ├── style.py            # Estilo global de figuras
│   ├── fig1_paths.py       # Caminhos de preços coloridos por D
│   ├── fig2_bars.py        # Barras comparativas por método
│   ├── fig3_scatter.py     # Scatter D_Higuchi vs 2 − H
│   ├── fig4_rolling.py     # D rolling ao longo do tempo
│   └── fig5_heatmap.py     # Heatmap D por período trienal
└── outputs/                # Figuras e tabelas geradas
```

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

Edite `config.py` e insira sua chave FRED:

```python
FRED_API_KEY = "sua_chave_aqui"
```

Chave gratuita: https://fred.stlouisfed.org/docs/api/api_key.html

## Execução

```bash
python run.py
```

Sem chave FRED, o pipeline roda com dados sintéticos automaticamente.

## Saídas

| Arquivo | Descrição |
|---|---|
| `outputs/tabela1_d_global.csv` | D_Higuchi, H_DFA, 2−H e discrepância por commodity |
| `outputs/tabela2_concordancia.csv` | Correlação e RMSE entre Higuchi e 2 − H |
| `outputs/fig1_paths.png` | Caminhos de preços coloridos por D global |
| `outputs/fig2_bars.png` | Barras agrupadas D_Higuchi × 2 − H por commodity |
| `outputs/fig3_scatter.png` | Concordância numérica entre estimadores |
| `outputs/fig4_rolling.png` | D rolling em janela deslizante de 60 meses |
| `outputs/fig5_heatmap.png` | Heatmap D por commodity e período trienal |

## Notas metodológicas

O estimador de box-counting está presente em `estimators/box_counting.py` mas não
é utilizado na análise principal. Avaliações preliminares revelaram instabilidade
numérica com valores abaixo do limite teórico inferior de 1, inviabilizando seu uso.

A dimensão fractal é estimada sobre o logaritmo dos preços e não sobre os retornos
logarítmicos. Retornos formam uma série aproximadamente estacionária cuja geometria
tende a D próximo de 2 por construção, sem carregar informação sobre o caminho
percorrido pelos preços. O DFA, por sua construção, integra os retornos antes de
estimar H, tornando-o conceitualmente comparável ao Higuchi aplicado ao log dos preços.