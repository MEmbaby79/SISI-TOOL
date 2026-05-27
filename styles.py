DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 40%, #0a1628 100%);
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(255,255,255,0.04);
    border-radius: 14px;
    padding: 6px;
    border: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: rgba(255,255,255,0.5);
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 13px;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1e3a5f, #2d6a9f) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(45,106,159,0.4);
}

[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(30,58,95,0.6), rgba(13,27,42,0.8));
    border: 1px solid rgba(100,180,255,0.15);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(10px);
    transition: transform 0.2s;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    border-color: rgba(100,180,255,0.3);
}
[data-testid="stMetricLabel"] {
    color: rgba(180,210,255,0.7) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="stMetricValue"] {
    color: #64b4ff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 28px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #1e3a5f, #2d6a9f);
    color: white;
    border: 1px solid rgba(100,180,255,0.3);
    border-radius: 10px;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2d6a9f, #3d8fd4);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(45,106,159,0.4);
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #1a4a2e, #2d7a4a) !important;
    border-color: rgba(100,220,150,0.3) !important;
    color: #90eeb4 !important;
}

.stInfo {
    background: rgba(30,58,95,0.4) !important;
    border: 1px solid rgba(100,180,255,0.2) !important;
    border-radius: 12px !important;
}
.stSuccess {
    background: rgba(20,60,35,0.4) !important;
    border: 1px solid rgba(100,220,150,0.2) !important;
    border-radius: 12px !important;
}
.stError {
    background: rgba(80,20,20,0.4) !important;
    border: 1px solid rgba(255,100,100,0.2) !important;
    border-radius: 12px !important;
}

hr { border-color: rgba(255,255,255,0.07) !important; }
.stCaption { color: rgba(255,255,255,0.35) !important; font-size: 11px !important; }

[data-testid="stDataFrame"] {
    border: 1px solid rgba(100,180,255,0.1);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stSidebar"] {
    background: rgba(10,15,30,0.95) !important;
    border-right: 1px solid rgba(100,180,255,0.08) !important;
}
</style>
"""

HEADER_HTML = """
<div style="
    background: linear-gradient(135deg, rgba(30,58,95,0.8) 0%, rgba(13,27,42,0.9) 100%);
    border: 1px solid rgba(100,180,255,0.15);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 20px;
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
">
    <div style="position:absolute;top:-40px;right:-40px;width:200px;height:200px;
        background:radial-gradient(circle,rgba(45,106,159,0.15),transparent);border-radius:50%;"></div>
    <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
        <div style="background:linear-gradient(135deg,#1e3a5f,#2d6a9f);
            width:52px;height:52px;border-radius:14px;display:flex;align-items:center;
            justify-content:center;font-size:24px;box-shadow:0 8px 24px rgba(45,106,159,0.4);">🌊</div>
        <div>
            <h1 style="margin:0;font-family:'Space Grotesk',sans-serif;font-size:24px;
                font-weight:700;color:white;letter-spacing:-0.5px;">
                Smart Irrigation MCDA — Egypt
            </h1>
            <p style="margin:4px 0 0;color:rgba(180,210,255,0.5);font-size:12px;">
                WLC Model · 27 Governorates · Six-Criterion Framework · Stage 1
            </p>
        </div>
        <div style="margin-left:auto;display:flex;gap:8px;flex-wrap:wrap;">
            <span style="background:rgba(100,180,255,0.1);border:1px solid rgba(100,180,255,0.2);
                color:#64b4ff;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;">
                27 Governorates
            </span>
            <span style="background:rgba(200,169,110,0.1);border:1px solid rgba(200,169,110,0.2);
                color:#c8a96e;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;">
                5 Selected
            </span>
        </div>
    </div>
</div>
"""

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,32,53,0.5)",
    font={"family": "Inter", "color": "rgba(255,255,255,0.7)"},
    legend={"bgcolor": "rgba(0,0,0,0)"},
    margin={"r": 80, "t": 40},
)

COLOR_SELECTED = "#c8a96e"
COLOR_BOUNDARY = "#ff7043"
COLOR_OTHER    = "#37474f"
COLOR_ACTIVE   = "#2196F3"
COLOR_GRID     = "rgba(255,255,255,0.05)"
