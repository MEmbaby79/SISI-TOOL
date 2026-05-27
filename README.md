# 🌊 Smart Irrigation MCDA Tool — Egypt

An interactive Multi-Criteria Decision Analysis (MCDA) dashboard for smart irrigation site selection across all 27 Egyptian governorates.

## 🔗 Live Demo
> Deploy link appears here after publishing on Streamlit Cloud

## 📊 Features
- **WLC Results** — Full ranking of all 27 governorates with visual charts
- **Interactive Calculator** — Adjust any governorate's scores and see real-time ranking updates
- **Sensitivity Analysis** — Test model stability by changing criterion weights
- **Edit Scores** — Modify individual scores per criterion
- **Download Data** — Export results as CSV

## 🧮 Methodology
The tool applies a **Weighted Linear Combination (WLC)** model:

```
S = (0.22×M₁) + (0.18×M₂) + (0.15×M₃) + (0.17×M₄) + (0.18×M₅) + (0.10×M₆)
```

| Criterion | Weight | Description |
|-----------|--------|-------------|
| M₁ | 22% | Hydrological Source Diversity |
| M₂ | 18% | Land Tenure & Farm Structure |
| M₃ | 15% | Climatic & Arid Stress |
| M₄ | 17% | Logistical & Institutional Readiness |
| M₅ | 18% | Agricultural System Representativeness |
| M₆ | 10% | Farmer Population Density & Generalizability |

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure
```
irrigation_dashboard/
├── app.py              # Main dashboard
├── pages/
│   ├── 1_WLC_Results.py
│   ├── 2_Calculator.py
│   ├── 3_Sensitivity.py
│   └── 4_Download.py
├── data/
│   └── governorates.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 📚 Data Sources
- MALR (2017) — Ministry of Agriculture & Land Reclamation
- WMRI (2018) — Water Management Research Institute
- Nour El-Din (2013), Allen et al. (1998)

## 👩‍💻 Built With
- [Streamlit](https://streamlit.io)
- [Plotly](https://plotly.com)
- [Pandas](https://pandas.pydata.org)
