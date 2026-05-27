# ── Governorate Data ─────────────────────────────────────────────────────────
GOVS = [
    {"rank":1,  "name":"El Beheira",       "m":[4.5,4.5,4.0,4.5,5.0,4.0], "system":"New Land Corporate Reclamation",        "status":"selected",  "water":"Mixed/Canal"},
    {"rank":2,  "name":"El Qalyoubeya",    "m":[3.5,5.0,2.0,5.0,5.0,5.0], "system":"Old Delta Fragmented Smallholder",      "status":"selected",  "water":"Surface Canal"},
    {"rank":3,  "name":"Alexandria",       "m":[4.5,3.5,3.5,4.0,5.0,3.0], "system":"Mediterranean Coastal New Land",        "status":"selected",  "water":"Mixed/Canal"},
    {"rank":4,  "name":"El Dakahlia",      "m":[4.5,3.0,2.5,4.5,4.0,4.5], "system":"Mid-Delta Tail-End Salinity Zone",      "status":"selected",  "water":"Mixed/Canal"},
    {"rank":5,  "name":"Sohag",            "m":[3.5,2.5,4.5,3.5,4.5,4.5], "system":"Upper Egypt Narrow Valley (High-ET)",   "status":"selected",  "water":"Surface Nile"},
    {"rank":6,  "name":"El Wadi El Gedid", "m":[3.0,4.0,5.0,2.5,4.0,1.0], "system":"Hyper-Arid Fossil Aquifer Reclamation", "status":"boundary",  "water":"Groundwater"},
    {"rank":7,  "name":"Matrouh",          "m":[3.5,3.5,4.5,2.5,2.5,1.5], "system":"NW Coastal Desert / Bedouin Rainfed",   "status":"other",     "water":"Rainfed"},
    {"rank":8,  "name":"El Sharqia",       "m":[3.0,2.5,2.5,4.0,2.0,4.5], "system":"Eastern Delta Smallholder",             "status":"other",     "water":"Mixed/Canal"},
    {"rank":9,  "name":"South Sinai",      "m":[3.0,3.5,5.0,2.0,2.5,1.0], "system":"Sinai Mountain / Coastal",              "status":"other",     "water":"Groundwater"},
    {"rank":10, "name":"North Sinai",      "m":[3.5,3.0,4.0,2.5,2.0,2.0], "system":"Sinai Canal Zone",                      "status":"other",     "water":"Mixed/Canal"},
    {"rank":11, "name":"El Minia",         "m":[2.5,1.5,4.0,3.5,2.5,4.0], "system":"Middle Upper Egypt",                    "status":"other",     "water":"Surface Nile"},
    {"rank":12, "name":"El Fayoum",        "m":[3.0,1.5,3.0,3.5,2.5,3.5], "system":"Fayoum Depression",                     "status":"other",     "water":"Surface Canal"},
    {"rank":12, "name":"Asyut",            "m":[2.5,1.5,4.0,3.5,2.0,4.0], "system":"Central Upper Egypt",                   "status":"other",     "water":"Surface Nile"},
    {"rank":14, "name":"Kafr El Sheikh",   "m":[3.0,2.0,2.5,3.5,2.0,4.0], "system":"Northern Coastal Delta",                "status":"other",     "water":"Mixed/Canal"},
    {"rank":15, "name":"Qena",             "m":[2.5,1.5,4.5,3.0,2.0,3.5], "system":"Upper Egypt — Luxor Region",            "status":"other",     "water":"Surface Nile"},
    {"rank":16, "name":"Aswan",            "m":[2.5,2.0,5.0,3.0,1.5,2.0], "system":"Extreme Upper Egypt",                   "status":"other",     "water":"Surface Nile"},
    {"rank":17, "name":"El Gharbia",       "m":[2.5,2.0,2.0,4.0,1.5,4.5], "system":"Core Delta Smallholder",                "status":"other",     "water":"Surface Canal"},
    {"rank":18, "name":"Ismailia",         "m":[2.5,2.5,3.0,3.5,2.0,2.0], "system":"Canal Zone Reclamation",                "status":"other",     "water":"Mixed/Canal"},
    {"rank":19, "name":"Beni Suef",        "m":[2.5,1.5,3.5,3.0,2.0,3.5], "system":"Upper Egypt Transition Zone",           "status":"other",     "water":"Surface Nile"},
    {"rank":20, "name":"El Menoufia",      "m":[2.5,1.5,2.0,4.0,1.5,4.5], "system":"Central Delta",                         "status":"other",     "water":"Surface Canal"},
    {"rank":21, "name":"Luxor",            "m":[2.0,1.5,4.5,3.0,1.5,2.5], "system":"Tourism / Upper Egypt",                 "status":"other",     "water":"Surface Nile"},
    {"rank":22, "name":"Giza",             "m":[2.0,1.5,2.5,4.0,1.5,3.5], "system":"Peri-Urban / Old Land",                 "status":"other",     "water":"Surface Canal"},
    {"rank":23, "name":"Red Sea",          "m":[2.0,3.0,4.5,2.0,1.5,1.0], "system":"Sparse Coastal Desert",                 "status":"other",     "water":"Groundwater"},
    {"rank":24, "name":"Damietta",         "m":[2.5,2.0,2.0,3.0,1.5,3.0], "system":"Northern Delta Coastal",                "status":"other",     "water":"Mixed/Canal"},
    {"rank":25, "name":"Suez",             "m":[1.5,2.0,3.5,2.5,1.0,1.5], "system":"Industrial / Coastal",                  "status":"other",     "water":"Mixed"},
    {"rank":26, "name":"Cairo",            "m":[1.5,1.0,2.0,4.0,1.0,2.0], "system":"Urban Peri-Agriculture",                "status":"other",     "water":"Surface Canal"},
    {"rank":27, "name":"Port Said",        "m":[1.5,1.5,2.0,2.5,1.0,1.5], "system":"Canal Zone Urban",                      "status":"other",     "water":"Mixed"},
]

WEIGHTS = [0.22, 0.18, 0.15, 0.17, 0.18, 0.10]

M_SHORT = ["M₁ Hydrology", "M₂ Land Tenure", "M₃ Climate", "M₄ Institutional", "M₅ Representativeness", "M₆ Farm Density"]
M_FULL  = [
    "M₁ — Hydrological Source Diversity",
    "M₂ — Land Tenure & Farm Structure",
    "M₃ — Climatic & Arid Stress",
    "M₄ — Logistical & Institutional Readiness",
    "M₅ — Agricultural System Representativeness",
    "M₆ — Farmer Population Density & Generalizability",
]
M_ICONS = ["💧","🏡","☀️","🏛️","🌾","👥"]

STATUS_LABEL = {"selected": "✓ Selected", "boundary": "◎ Boundary Case", "other": "Other"}
STATUS_COLOR = {"selected": "#c8a96e", "boundary": "#ff7043", "other": "#546e7a"}

def calc_wlc(m, w=None):
    w = w or WEIGHTS
    return round(sum(wi * mi for wi, mi in zip(w, m)), 3)

def build_df(custom=None, weights=None):
    import pandas as pd
    w = weights or WEIGHTS
    rows = []
    for g in GOVS:
        m = custom.get(g["name"], g["m"]) if custom else g["m"]
        rows.append({
            "Governorate": g["name"],
            "M₁": m[0], "M₂": m[1], "M₃": m[2],
            "M₄": m[3], "M₅": m[4], "M₆": m[5],
            "WLC Score": calc_wlc(m, w),
            "Farming System": g["system"],
            "Water Source": g["water"],
            "Status": STATUS_LABEL[g["status"]],
            "_status": g["status"],
        })
    df = pd.DataFrame(rows).sort_values("WLC Score", ascending=False).reset_index(drop=True)
    df.index += 1
    return df
