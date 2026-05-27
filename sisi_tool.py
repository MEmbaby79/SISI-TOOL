import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="SISI — Smart Irrigation Suitability Index | Egypt",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── PALETTE ──────────────────────────────────────────────────────────────────
BG       = "#f0f7f4"
BG2      = "#e4f0eb"
CARD     = "#ffffff"
BORDER   = "#c8ddd4"
TEXT     = "#1a3328"
TEXT_MID = "#2d5a47"
TEXT_LT  = "#5a8a72"

# Level colors — meaningful gradient
L_COLORS = {
    1: "#d32f2f",   # Red — basic/critical
    2: "#f57c00",   # Orange — low
    3: "#fbc02d",   # Amber — moderate
    "3S": "#7b1fa2",# Purple — solar adapted
    4: "#388e3c",   # Green — advanced
    5: "#1565c0",   # Blue — precision
}
L_NAMES = {
    1: "L1 — Basic Smart Awareness",
    2: "L2 — Semi-Automated Drip",
    3: "L3 — Automated Soil-Based",
    "3S": "L3S — Solar Adapted",
    4: "L4 — Climate-Integrated",
    5: "L5 — Precision + UAV",
}

# ── SISI CRITERIA & WEIGHTS ───────────────────────────────────────────────────
WEIGHTS = {"C1": 0.30, "C2": 0.20, "C3": 0.15, "C4": 0.15, "C5": 0.20}
C_NAMES = {
    "C1": "C₁ — Irrigation Type & Infrastructure",
    "C2": "C₂ — Infrastructure & Energy Supply",
    "C3": "C₃ — Soil & Environmental Conditions",
    "C4": "C₄ — Crop Type & Economic Sensitivity",
    "C5": "C₅ — Socioeconomic Readiness",
}
C_ICONS = {"C1":"🚿","C2":"⚡","C3":"🌱","C4":"🌾","C5":"👥"}

# ── SCORING RUBRICS ───────────────────────────────────────────────────────────
RUBRICS = {
    "C1": {
        1: "Surface/flood only; no pressurized system; DU <50%; manual gates",
        1.5: "Surface dominant; minor drip (<15%); aged pump; DU ~55%",
        2: "< 30% drip; outdated system; low uniformity; no automation",
        2.5: "Partial HDPE mainline; gated pipe; some pressurized zones; DU ~65%",
        3: "30–70% drip; partial automation; UC ~75–80%; basic manifold",
        3.5: "Drip on 70%+ but old laterals (T-Tape); DU ~71%; expansion infrastructure ready",
        4: "> 70% drip; multi-zone manifold; UC > 85%; VFD pump; some SCADA legacy",
        4.5: "Full drip (>95%); 220-zone manifold; UC > 90%; GIS-mapped; legacy SCADA present",
        5: "Full drip + SCADA; UC > 92%; subsurface drip; sensor-integrated; DU > 95%",
    },
    "C2": {
        1: "No grid; diesel only; no backup; no connectivity; GSM 1 bar",
        1.4: "Single-phase; 4–6 hr daily outage; no backup; weak GSM (2 bars)",
        1.5: "Single-phase; frequent outages; no solar; limited GSM",
        2: "Unreliable grid (>4 hr outage/day); no solar; weak GSM signal",
        2.5: "Reliable 3-phase; <2 hr planned outage/week; diesel backup; 4G (4 bars)",
        3: "Grid or solar; moderate outages; good GSM; basic data logger possible",
        3.5: "3-phase grid; <1 hr outage; generator backup; 4G; internet-connected field office",
        4: "Stable grid + 5kVA generator; strong 4G; internet-connected; existing automation HW",
        4.5: "Dedicated HV substation; 500 kW diesel standby; fiber LAN; full 4G LTE",
        5: "Dual reliable supply + solar + UPS; fiber/4G LTE; IoT gateway; cloud-connected",
    },
    "C3": {
        1: "Heavy clay / saline (EC > 4 dS/m); poor drainage; waterlogging risk",
        1.5: "Clay loam; EC 2–4 dS/m; limited drainage; slow infiltration",
        2: "Clay loam; EC 1.5–2.5 dS/m; moderate drainage; high water retention",
        2.5: "Clay loam; EC 0.8–1.1 dS/m; adequate drainage; AWC ~84 mm/m",
        3: "Sandy loam; EC 0.8–1.6 dS/m; good drainage; moderate AWC",
        3.5: "Sandy to sandy loam; EC 1.4–2.2 dS/m (rising); salinity manageable with EC sensors",
        4: "Sandy soils; EC < 0.8 dS/m; excellent drainage; low AWC — ideal for high-frequency drip",
        4.5: "Loam; EC 0.5–0.7 dS/m; excellent drainage; 3 GW monitoring wells; sensor-compatible",
        5: "Optimal sandy loam; EC < 0.5 dS/m; fully instrumented; no constraints",
    },
    "C4": {
        1: "Subsistence staple crops; income < EGP 15K/feddan; no market linkage",
        1.5: "Staple crops; low margins; local market; income ~EGP 15–20K/feddan",
        2: "Mixed staple/vegetable; moderate margins; government procurement",
        2.5: "Wheat/maize rotation; strategic crops; medium margins; EGP ~30K/feddan",
        3: "Onion/garlic — medium-high value; cooperative market; EGP ~45K/feddan",
        3.5: "Vegetables/field crops; good market access; EGP ~45–55K/feddan",
        4: "High-value crops (watermelon, tomato); export potential; EGP ~58K/feddan",
        4.5: "Premium citrus/grapes/olives; EU certified export; EGP > 120K/feddan; GlobalG.A.P.",
        5: "Premium/export crops; contract farming; highest Kc sensitivity; digital traceability",
    },
    "C5": {
        1: "Illiterate/primary education; no smartphone; no bank account; no cooperative; extension > 3 yrs",
        1.4: "Primary education (6 yrs); no smartphone; no bank; no cooperative; TAM PU = 2.3/5",
        1.5: "Primary education; basic phone only; no credit; rented land; minimal extension",
        2: "Primary education; basic smartphone; limited credit; some cooperative contact",
        2.5: "Low-moderate education; smartphone; 0% credit access; high willingness to invest",
        3: "Secondary education; cooperative member; some credit; regular extension contact",
        3.5: "Secondary education (9.8 yrs); smartphone; cooperative member; some credit; TAM PU = 3.6",
        4: "Secondary+ education; smartphone + tablet; formal credit; workshop attendance; TAM PU = 4.1",
        4.5: "Corporate management; PhD agronomist; IT team; prior IoT; capital access; ISO 9001",
        5: "Higher education; strong capital; tech-experienced; cooperative leadership; export networks",
    },
}

# ── LEVEL REQUIREMENTS ────────────────────────────────────────────────────────
LEVEL_REQUIREMENTS = {
    1: {
        "range": "1.00 – 2.00",
        "water_saving": "10–20%",
        "investment_egp": "25K–45K",
        "description": "Basic environmental monitoring. No infrastructure change. Soil moisture sensors + visual indicators + SMS alerts.",
        "components": [
            {"item": "Soil moisture sensor nodes (Sentek Drill & Drop)", "spec": "Dual-depth 20 & 40 cm; ±1% VWC; analog 4–20 mA", "qty": "2 nodes", "ref": "FAO-56; Sentek 2020"},
            {"item": "Solar-powered GSM data logger", "spec": "Campbell CR300; IP67; local storage; GSM-enabled", "qty": "1 unit", "ref": "Campbell 2021"},
            {"item": "Solar panel + sealed battery", "spec": "20W monocrystalline + 40Ah VRLA per node", "qty": "2 sets", "ref": "IEC 61215"},
            {"item": "Compact automatic weather station", "spec": "Air T, RH, rainfall, wind — basic ET₀ support", "qty": "1 unit", "ref": "FAO Paper 56"},
            {"item": "Arabic SMS alert system", "spec": "Automated irrigation advisory via GSM", "qty": "1 service", "ref": "FAO e-Agriculture 2020"},
            {"item": "Visual soil moisture indicators (LED traffic light)", "spec": "Color-coded: Red/Yellow/Green; literacy-independent", "qty": "2 units", "ref": "WMRI 2026"},
        ],
        "color": L_COLORS[1],
        "key_discriminator": "Sensors only — no automation; farmer-decision support",
        "literature": "FAO-MASSCOTE Level 1; World Bank SARI L1; Rogers (2003) — awareness stage"
    },
    2: {
        "range": "2.01 – 2.80",
        "water_saving": "20–35%",
        "investment_egp": "60K–120K",
        "description": "Semi-automated drip irrigation. Timer-based controller + GSM + mobile app + basic fertigation.",
        "components": [
            {"item": "Drip laterals — Netafim UniRam 16mm", "spec": "33 cm spacing; 1.6 L/hr; pressure-compensated; clog-resistant", "qty": "Per feddan coverage", "ref": "ISO 11545:2009; Netafim"},
            {"item": "HDPE mainline 63mm + sub-main 40mm", "spec": "SDR 11; PN16; buried 60 cm depth", "qty": "Per farm layout", "ref": "ISO 4427"},
            {"item": "8-zone irrigation controller + GSM/4G", "spec": "Rain Bird ESP-LXD; GSM/4G communication module", "qty": "1 unit", "ref": "IEC 30141:2018"},
            {"item": "Soil moisture sensors — Decagon 5TM", "spec": "Volumetric WC + temperature; 20 & 40 cm depth", "qty": "3 nodes", "ref": "FAO Paper 56; Decagon"},
            {"item": "Booster pump + VFD", "spec": "Grundfos CM5-6 1.1 kW + Schneider ATV312 0.75 kW VFD", "qty": "1 unit", "ref": "ISO 9261:2004"},
            {"item": "Filter station — Arkal 120-mesh", "spec": "2-inch disc filter + Y-strainer sand separator", "qty": "1 unit", "ref": "FAO Paper 63"},
            {"item": "Venturi fertigation unit", "spec": "Mazaer 2-inch + 200L HDPE mixing tank + 4 injectors", "qty": "1 unit", "ref": "Phocaides 2007 FAO"},
            {"item": "AgriSense cloud platform", "spec": "Arabic dashboard + mobile app + weekly advisory", "qty": "1-yr licence", "ref": "FAO e-Agriculture 2020"},
        ],
        "color": L_COLORS[2],
        "key_discriminator": "Drip network + timer controller + soil sensing; manual smartphone overrides",
        "literature": "Al-Ghobari & Dewidar 2018; Lamm et al. 2012; FAO Paper 63; ISO 11545"
    },
    3: {
        "range": "2.81 – 3.60",
        "water_saving": "30–45%",
        "investment_egp": "150K–350K",
        "description": "Closed-loop soil-threshold automation. 100% drip + LoRaWAN sensors + solenoid valves. Irrigation auto-triggered at 50–60% AWC depletion.",
        "components": [
            {"item": "Drip expansion — Netafim UniRam 16mm", "spec": "20 cm spacing; 1.0 L/hr; PC emitters; 100% coverage", "qty": "Full farm", "ref": "ISO 11545:2009"},
            {"item": "Soil sensor nodes — Decagon GS3", "spec": "VWC + EC + Temperature; 20 & 40 cm; LoRaWAN compatible", "qty": "5–8 nodes", "ref": "Doorenbos & Pruitt 1977"},
            {"item": "Automated controller — soil-threshold + ET₀ dual mode", "spec": "Baseline 3200; 8-zone; soil-trigger + ET₀ mode", "qty": "1 unit", "ref": "IEC 30141:2018"},
            {"item": "4-zone solenoid valves — Hunter PGV", "spec": "1-inch; normally-closed; 24VAC; replaces manual ball valves", "qty": "4–8 valves", "ref": "ISO 9261:2004"},
            {"item": "IoT data gateway + cloud connection", "spec": "FarmHack IoT Egyptian platform; Arabic dashboard; 1-yr licence", "qty": "1 unit", "ref": "FAO e-Agriculture 2020"},
            {"item": "Pressure regulators + gauges at zones", "spec": "Netafim 1.5 Bar at zone inlets; 4 pressure gauges", "qty": "4 sets", "ref": "Phocaides 2007"},
            {"item": "Mobile app — iOS + Android", "spec": "Farmer + agronomist + WMRI access; real-time dashboard", "qty": "1 licence", "ref": "World Bank SARI 2016"},
        ],
        "color": L_COLORS[3],
        "key_discriminator": "Soil-threshold closed-loop control; SCADA-ready; mobile app",
        "literature": "FAO Paper 56 Allen et al. 1998; Doorenbos & Pruitt 1977; ISO 16075; IEC 30141"
    },
    "3S": {
        "range": "2.81 – 3.60 (off-grid)",
        "water_saving": "30–45%",
        "investment_egp": "100K–200K",
        "description": "L3 for remote/off-grid zones (Upper Egypt, western desert). Solar PV + DC pump + EC salinity monitoring + leaching algorithm.",
        "components": [
            {"item": "Solar PV array — Longi Hi-MO6", "spec": "375W monocrystalline; 21.3% efficiency; 25-yr guarantee", "qty": "4 panels (1.5 kWp)", "ref": "IEC 61215; Chandel et al. 2015"},
            {"item": "VRLA battery bank", "spec": "Hoppecke 12V 100Ah sealed; 2 units in series (24V)", "qty": "2 units", "ref": "Aliyu et al. 2018"},
            {"item": "MPPT solar charge controller", "spec": "Victron SmartSolar 100/30; Bluetooth monitoring", "qty": "1 unit", "ref": "IEC 62509"},
            {"item": "DC submersible pump", "spec": "Grundfos SQFlex 11SQF-2; 11 m³/hr at 25 m head", "qty": "1 unit", "ref": "Wolfert et al. 2017"},
            {"item": "EC + pH inline sensors", "spec": "Hanna HI9813-6N; pre-mix monitoring; 4–20 mA output", "qty": "2 sensors", "ref": "ISO 16075 Parts 1–4"},
            {"item": "Soil sensor nodes — Decagon 5TM VWC + EC", "spec": "Combined VWC + EC; 15 & 35 cm depth", "qty": "4 nodes", "ref": "FAO Paper 29 Ayers & Westcott"},
            {"item": "Solar-powered 6-zone controller", "spec": "Rain Bird ESP-LX solar variant; battery-backed; no grid", "qty": "1 unit", "ref": "IEC 30141:2018"},
            {"item": "Leaching algorithm module", "spec": "AgriSense Salinity Manager; automated LF scheduling", "qty": "1 module", "ref": "FAO Paper 29; ISO 16075"},
            {"item": "Drip expansion — Netafim Dripnet PC 16mm", "spec": "30 cm spacing; 1.0 L/hr; PC emitters", "qty": "Per feddan", "ref": "ISO 11545:2009"},
        ],
        "color": L_COLORS["3S"],
        "key_discriminator": "Solar-powered closed-loop; EC salinity monitoring; leaching algorithm",
        "literature": "Chandel et al. 2015; Aliyu et al. 2018; ISO 16075; FAO Paper 29 Ayers & Westcott 1985"
    },
    4: {
        "range": "3.61 – 4.40",
        "water_saving": "35–50%",
        "investment_egp": "500K–1.5M",
        "description": "Multi-zone SCADA + automated weather station + ET₀/Penman-Monteith + NWP API. 20–250 zones. Predictive scheduling.",
        "components": [
            {"item": "SCADA system — Jain Unity PRO", "spec": "220-zone; cloud + on-premise dual architecture; Arabic/English UI", "qty": "Full farm", "ref": "World Bank SARI 2016; EU PAMM 2019"},
            {"item": "Soil sensor network — Sentek Drill & Drop", "spec": "30 + 60 + 90 cm tri-depth; KRIGING spatial interpolation", "qty": "80 nodes per 6,000 fed.", "ref": "FAO Paper 56; Sentek 2020"},
            {"item": "Automatic weather stations — Davis Vantage Pro2", "spec": "Full-spec: T, RH, wind, rain, solar radiation, barometric P", "qty": "4 per large farm", "ref": "Allen et al. 1998 FAO-56"},
            {"item": "NWP/API integration — ECMWF ERA5", "spec": "7-day forecast; rain event suspension; ET₀ auto-calculation", "qty": "1 API licence", "ref": "IPCC AR6 2021; Allen et al. 1998"},
            {"item": "AI irrigation scheduling engine", "spec": "ET₀ + Kc + soil + NWP multi-model; AgriAI Egypt cloud platform", "qty": "1 platform", "ref": "Wolfert et al. 2017; Smith & Taylor 2024"},
            {"item": "Electromagnetic flow meters — Elster V100", "spec": "Mag-flow 4-inch; all wells + canal inlets", "qty": "12 meters", "ref": "FAO-MASSCOTE 2007; ICID 2021"},
            {"item": "Fertilizer injection — Dosatron D25RE", "spec": "Zone-specific precision fertigation; × 12 units", "qty": "12 units", "ref": "Phocaides 2007 FAO"},
            {"item": "Farm Management Software FMS-360", "spec": "Integrates SCADA + sensors + accounts + export records; Arabic", "qty": "1 licence", "ref": "World Bank OP 4.07"},
            {"item": "Fiber optic backbone extension", "spec": "300 m additional fiber to remaining farm zones", "qty": "300 m", "ref": "IEC 30141:2018"},
        ],
        "color": L_COLORS[4],
        "key_discriminator": "ET₀-based predictive scheduling; NWP API; multi-zone SCADA; flow monitoring",
        "literature": "Allen et al. 1998; Wolfert et al. 2017; World Bank SARI 2016; EU PAMM Horizon 2020; ECMWF"
    },
    5: {
        "range": "4.41 – 5.00",
        "water_saving": "40–60%",
        "investment_egp": "> 2M",
        "description": "Fully autonomous precision agriculture. UAV multispectral + variable-rate irrigation + AI/ML model + digital twin.",
        "components": [
            {"item": "UAV platform — DJI Matrice 300 RTK", "spec": "55-min flight; omnidirectional obstacle avoidance; 2-unit redundancy", "qty": "2 UAVs", "ref": "Frontiers Agronomy 2025; WMRI 2026"},
            {"item": "Multispectral camera — MicaSense RedEdge-MX", "spec": "5-band NDVI/NDWI/NDRE/Chlorophyll; 8 cm resolution at 120m", "qty": "2 cameras", "ref": "Zwart & Bastiaanssen 2024"},
            {"item": "Ground Control Points — permanent", "spec": "Trimble R10 RTK survey; 24 concrete GCP monuments", "qty": "24 GCPs", "ref": "ISO IEC 30141"},
            {"item": "Image processing — Pix4Dfields", "spec": "Automated ortho mosaic + stress zone maps; annual licence", "qty": "1 licence", "ref": "Frontiers Sustainable Food 2026"},
            {"item": "AI/ML irrigation model — custom", "spec": "PyTorch crop water stress model; WMRI + Cairo University", "qty": "1 model", "ref": "Wolfert et al. 2017; Smith & Taylor 2024"},
            {"item": "Digital twin platform — iTwin Agriculture", "spec": "Farm-scale 3D model + IoT sensor integration", "qty": "1 licence", "ref": "MWRI 2026; Zwart & Bastiaanssen 2024"},
            {"item": "All Level 4 components", "spec": "Full SCADA + sensors + NWP + FMS (see L4)", "qty": "Full system", "ref": "See Level 4 references"},
            {"item": "Variable Rate Irrigation (VRI) integration", "spec": "Prescription map → SCADA zone management; GIS layer", "qty": "1 system", "ref": "Australia Murray-Darling 2019; CSIRO 2021"},
        ],
        "color": L_COLORS[5],
        "key_discriminator": "UAV multispectral + VRI + AI/ML + digital twin; fully autonomous",
        "literature": "CSIRO 2021; Wolfert et al. 2017; Zwart & Bastiaanssen 2024; Frontiers Agronomy 2025; MWRI 2026"
    },
}

# ── GOVERNORATE DATA ──────────────────────────────────────────────────────────
# 5 studied + 22 estimated
GOVS_DATA = {
    # Studied governorates (from document)
    "El Qalyoubeya": {
        "lat": 30.33, "lon": 31.22,
        "C1": 1.5, "C2": 1.4, "C3": 2.5, "C4": 2.5, "C5": 1.5,
        "studied": True, "water": "Surface Canal",
        "system": "Old Delta Fragmented Smallholder",
        "notes": "SISI = 1.78. Surface basin only; bamboo channels; 4–6 hr daily outage; primary education; no smartphone.",
        "farm": "El Hassan Mohamed Zaher Farm",
    },
    "El Dakahlia": {
        "lat": 31.17, "lon": 31.49,
        "C1": 2.5, "C2": 2.5, "C3": 3.0, "C4": 2.5, "C5": 3.5,
        "studied": True, "water": "Mixed/Canal",
        "system": "Mid-Delta Tail-End Salinity",
        "notes": "SISI = 2.78. Partial HDPE; gated pipe; 3-phase reliable; cooperative member; secondary education.",
        "farm": "Ezz Eldeen Farm",
    },
    "Alexandria": {
        "lat": 31.20, "lon": 29.92,
        "C1": 3.5, "C2": 4.0, "C3": 3.5, "C4": 3.5, "C5": 4.0,
        "studied": True, "water": "Mixed/Canal",
        "system": "Mediterranean Coastal New Land",
        "notes": "SISI = 3.71. 73% drip; reliable grid + generator; watermelon; formal credit; TAM PU=4.1.",
        "farm": "Ahmed Farag Khalil Farm",
    },
    "Sohag": {
        "lat": 26.56, "lon": 31.70,
        "C1": 3.0, "C2": 4.0, "C3": 3.5, "C4": 3.0, "C5": 3.8,
        "studied": True, "water": "Surface Nile + GW",
        "system": "Upper Egypt Narrow Valley",
        "notes": "SISI = 3.44. Partial drip; excellent solar potential; EC rising; onion/garlic; cooperative member.",
        "farm": "Abu Bakr A.H. Mohamed Farm",
    },
    "El Beheira": {
        "lat": 30.85, "lon": 30.34,
        "C1": 4.5, "C2": 4.5, "C3": 4.0, "C4": 4.5, "C5": 3.8,
        "studied": True, "water": "Mixed/Canal + GW",
        "system": "New Land Corporate Reclamation",
        "notes": "SISI = 4.29. 70% drip; dedicated HV substation; premium export citrus; corporate management.",
        "farm": "El Maghraby Commercial Agricultural Company",
    },
    # Estimated governorates (based on farming system analogy)
    "El Gharbia":    {"lat": 30.87,"lon": 31.03,"C1":1.5,"C2":2.0,"C3":2.5,"C4":2.0,"C5":2.0,"studied":False,"water":"Surface Canal","system":"Core Delta Smallholder","notes":"Estimated — core Delta smallholder; limited modernization.","farm":"—"},
    "El Menoufia":   {"lat": 30.60,"lon": 30.99,"C1":1.5,"C2":2.0,"C3":2.5,"C4":1.5,"C5":2.0,"studied":False,"water":"Surface Canal","system":"Central Delta","notes":"Estimated — central Delta; dense smallholder; flood dominant.","farm":"—"},
    "El Sharqia":    {"lat": 30.74,"lon": 31.72,"C1":2.0,"C2":2.5,"C3":2.5,"C4":2.0,"C5":2.5,"studied":False,"water":"Mixed/Canal","system":"Eastern Delta Smallholder","notes":"Estimated — Eastern Delta; partial drip transition.","farm":"—"},
    "Kafr El Sheikh":{"lat": 31.11,"lon": 30.94,"C1":2.0,"C2":2.0,"C3":2.5,"C4":2.0,"C5":2.0,"studied":False,"water":"Mixed/Canal","system":"Northern Coastal Delta","notes":"Estimated — northern coastal Delta; moderate modernization.","farm":"—"},
    "Damietta":      {"lat": 31.42,"lon": 31.81,"C1":2.0,"C2":2.0,"C3":2.5,"C4":2.0,"C5":2.0,"studied":False,"water":"Mixed/Canal","system":"Northern Delta Coastal","notes":"Estimated — coastal Delta; flood dominant.","farm":"—"},
    "El Ismailia":   {"lat": 30.60,"lon": 32.27,"C1":2.5,"C2":3.0,"C3":3.0,"C4":2.5,"C5":2.5,"studied":False,"water":"Mixed/Canal","system":"Canal Zone Reclamation","notes":"Estimated — Canal Zone; partial modernization.","farm":"—"},
    "El Fayoum":     {"lat": 29.31,"lon": 30.84,"C1":2.0,"C2":2.0,"C3":2.5,"C4":2.0,"C5":2.0,"studied":False,"water":"Surface Canal","system":"Fayoum Depression","notes":"Estimated — unique gravity Bahr Yusuf; mostly flood.","farm":"—"},
    "Beni Suef":     {"lat": 28.92,"lon": 30.87,"C1":1.5,"C2":1.5,"C3":2.5,"C4":1.5,"C5":1.5,"studied":False,"water":"Surface Nile","system":"Upper Egypt Transition","notes":"Estimated — transitional Upper Egypt; basic infrastructure.","farm":"—"},
    "El Minia":      {"lat": 28.12,"lon": 30.74,"C1":1.5,"C2":1.5,"C3":3.0,"C4":1.5,"C5":1.5,"studied":False,"water":"Surface Nile","system":"Middle Upper Egypt","notes":"Estimated — Nile pump system; limited modernization.","farm":"—"},
    "Asyut":         {"lat": 27.18,"lon": 31.18,"C1":1.5,"C2":1.5,"C3":3.0,"C4":2.0,"C5":1.5,"studied":False,"water":"Surface Nile","system":"Central Upper Egypt","notes":"Estimated — central Upper Egypt; surface dominant.","farm":"—"},
    "Qena":          {"lat": 26.16,"lon": 32.72,"C1":1.5,"C2":1.5,"C3":3.5,"C4":2.0,"C5":1.5,"studied":False,"water":"Surface Nile","system":"Upper Egypt Luxor Region","notes":"Estimated — high ET₀; limited infrastructure.","farm":"—"},
    "Luxor":         {"lat": 25.69,"lon": 32.64,"C1":1.5,"C2":1.5,"C3":3.5,"C4":2.0,"C5":1.5,"studied":False,"water":"Surface Nile","system":"Tourism/Upper Egypt","notes":"Estimated — tourism dominated; limited ag modernization.","farm":"—"},
    "Aswan":         {"lat": 24.09,"lon": 32.90,"C1":1.5,"C2":2.0,"C3":4.0,"C4":2.0,"C5":1.5,"studied":False,"water":"Surface Nile","system":"Extreme Upper Egypt","notes":"Estimated — High Dam regulation; extreme ET₀.","farm":"—"},
    "El Wadi El Gedid":{"lat": 25.52,"lon": 28.88,"C1":2.5,"C2":1.5,"C3":4.5,"C4":2.5,"C5":2.0,"studied":False,"water":"Groundwater","system":"Hyper-Arid Fossil Aquifer","notes":"Estimated — deep fossil aquifer; remote; extreme heat.","farm":"—"},
    "Matrouh":       {"lat": 31.35,"lon": 27.24,"C1":2.0,"C2":1.5,"C3":3.5,"C4":2.0,"C5":1.5,"studied":False,"water":"Rainfed/GW","system":"NW Coastal Desert","notes":"Estimated — Bedouin rainfed; limited irrigation.","farm":"—"},
    "North Sinai":   {"lat": 30.93,"lon": 33.08,"C1":2.0,"C2":2.0,"C3":3.0,"C4":2.0,"C5":2.0,"studied":False,"water":"Mixed/Canal","system":"Sinai Canal Zone","notes":"Estimated — Canal Zone extension; moderate readiness.","farm":"—"},
    "South Sinai":   {"lat": 28.24,"lon": 33.77,"C1":1.5,"C2":1.5,"C3":4.0,"C4":2.0,"C5":1.5,"studied":False,"water":"Groundwater","system":"Sinai Mountain/Coastal","notes":"Estimated — mountain/coastal; minimal agriculture.","farm":"—"},
    "Red Sea":       {"lat": 25.04,"lon": 34.88,"C1":1.0,"C2":1.5,"C3":4.0,"C4":1.5,"C5":1.0,"studied":False,"water":"Groundwater","system":"Sparse Coastal Desert","notes":"Estimated — extremely sparse ag; minimal readiness.","farm":"—"},
    "Giza":          {"lat": 29.99,"lon": 31.15,"C1":1.5,"C2":2.5,"C3":2.5,"C4":2.0,"C5":2.5,"studied":False,"water":"Surface Canal","system":"Peri-Urban Old Land","notes":"Estimated — peri-urban encroachment; declining ag.","farm":"—"},
    "Cairo":         {"lat": 30.06,"lon": 31.25,"C1":1.0,"C2":2.5,"C3":2.0,"C4":1.0,"C5":2.0,"studied":False,"water":"Surface Canal","system":"Urban Peri-Agriculture","notes":"Estimated — minimal ag; urban encroachment.","farm":"—"},
    "Suez":          {"lat": 29.97,"lon": 32.55,"C1":1.0,"C2":2.0,"C3":2.5,"C4":1.0,"C5":1.5,"studied":False,"water":"Mixed","system":"Industrial/Coastal","notes":"Estimated — industrial; minimal ag.","farm":"—"},
    "Port Said":     {"lat": 31.26,"lon": 32.28,"C1":1.0,"C2":2.0,"C3":2.0,"C4":1.0,"C5":1.5,"studied":False,"water":"Mixed","system":"Canal Zone Urban","notes":"Estimated — urban Canal Zone; minimal ag.","farm":"—"},
}

def calc_sisi(c1, c2, c3, c4, c5):
    return round(0.30*c1 + 0.20*c2 + 0.15*c3 + 0.15*c4 + 0.20*c5, 3)

def get_level(score, solar_adapted=False):
    if score <= 2.00: return 1
    if score <= 2.80: return 2
    if score <= 3.60: return "3S" if solar_adapted else 3
    if score <= 4.40: return 4
    return 5

def level_color(lvl):
    return L_COLORS.get(lvl, "#888")

def build_map_df(custom=None):
    rows = []
    for gov, d in GOVS_DATA.items():
        c = custom.get(gov, d) if custom else d
        s = calc_sisi(c["C1"], c["C2"], c["C3"], c["C4"], c["C5"])
        # Determine if solar adapted (remote + unreliable grid)
        solar = (c["C2"] <= 2.0 and c["C3"] >= 3.5)
        lvl = get_level(s, solar)
        rows.append({
            "Governorate": gov, "lat": d["lat"], "lon": d["lon"],
            "SISI": s, "Level": lvl, "Level_Num": lvl if lvl != "3S" else 3,
            "Level_Name": L_NAMES.get(lvl, ""),
            "Color": level_color(lvl),
            "Studied": d["studied"],
            "System": d["system"],
            "Water": d["water"],
            "Notes": d["notes"],
            "Farm": d["farm"],
            "C1": c["C1"], "C2": c["C2"], "C3": c["C3"], "C4": c["C4"], "C5": c["C5"],
        })
    return pd.DataFrame(rows).sort_values("SISI", ascending=False).reset_index(drop=True)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{{font-family:'Inter',sans-serif;color:{TEXT};}}
.stApp{{background:{BG};}}
#MainMenu{{visibility:hidden;}}footer{{visibility:hidden;}}header{{visibility:hidden;}}
.stTabs [data-baseweb="tab-list"]{{gap:4px;background:{BG2};border-radius:12px;padding:5px;border:1px solid {BORDER};}}
.stTabs [data-baseweb="tab"]{{border-radius:8px;color:{TEXT_MID};font-weight:500;font-size:13px;padding:8px 14px;}}
.stTabs [aria-selected="true"]{{background:#1a5c40!important;color:white!important;}}
[data-testid="metric-container"]{{background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:16px;border-top:3px solid #1a5c40;box-shadow:0 2px 6px rgba(0,0,0,0.05);}}
[data-testid="stMetricLabel"]{{color:{TEXT_LT}!important;font-size:11px!important;font-weight:600!important;text-transform:uppercase;}}
[data-testid="stMetricValue"]{{color:#1a5c40!important;font-weight:700!important;font-size:24px!important;}}
.stButton>button{{background:#1a5c40;color:white;border:none;border-radius:8px;font-weight:600;}}
.stButton>button:hover{{background:#2d7a58;}}
.stDownloadButton>button{{background:#8b6914!important;color:white!important;border:none!important;}}
.stInfo{{background:#e8f5f3!important;border:1px solid rgba(26,92,64,0.25)!important;border-radius:10px!important;}}
.stSuccess{{background:#f0fdf4!important;border:1px solid #86efac!important;border-radius:10px!important;}}
.stError{{background:#fef2f2!important;border:1px solid #fca5a5!important;border-radius:10px!important;}}
hr{{border-color:{BORDER}!important;}}
[data-testid="stDataFrame"]{{border:1px solid {BORDER};border-radius:12px;overflow:hidden;}}
.stExpander{{background:{CARD}!important;border:1px solid {BORDER}!important;border-radius:12px!important;}}
</style>""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#1a5c40 0%,#0f3d2a 60%,#1a5c40 100%);
    border-radius:18px;padding:26px 36px;margin-bottom:22px;box-shadow:0 6px 24px rgba(26,92,64,0.3);">
  <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;">
    <div style="background:rgba(255,255,255,0.15);width:54px;height:54px;border-radius:14px;
        display:flex;align-items:center;justify-content:center;font-size:28px;">💧</div>
    <div>
      <h1 style="margin:0;font-family:'Lora',serif;font-size:24px;font-weight:700;color:white;">
          SISI — Smart Irrigation Suitability Index | Egypt</h1>
      <p style="margin:5px 0 0;color:rgba(255,255,255,0.65);font-size:12px;">
          5 Criteria · AHP-WSM · WMRI 2026 · FAO-56 · ISO 11545 · IEC 30141 · 27 Governorates</p>
    </div>
    <div style="margin-left:auto;display:flex;gap:8px;flex-wrap:wrap;">
      <span style="background:rgba(255,255,255,0.15);color:white;padding:3px 12px;border-radius:20px;font-size:11px;font-weight:600;border:1px solid rgba(255,255,255,0.25);">27 Governorates</span>
      <span style="background:#8b6914;color:white;padding:3px 12px;border-radius:20px;font-size:11px;font-weight:600;">5 Studied ✦</span>
      <span style="background:rgba(255,255,255,0.1);color:rgba(255,255,255,0.8);padding:3px 12px;border-radius:20px;font-size:11px;">L1–L5 Classification</span>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
df_map = build_map_df()
k1,k2,k3,k4,k5,k6 = st.columns(6)
k1.metric("🗺️ Governorates", "27")
k2.metric("🔬 Studied", "5")
k3.metric("📊 Avg SISI", round(df_map["SISI"].mean(),2))
k4.metric("L1 Sites", len(df_map[df_map["Level"]==1]))
k5.metric("L3–L4 Sites", len(df_map[df_map["Level_Num"].isin([3,4])]))
k6.metric("L5 Ready", len(df_map[df_map["Level"]==5]))
st.markdown("---")

tab1,tab2,tab3,tab4,tab5 = st.tabs([
    "🗺️  Egypt SISI Map",
    "🧮  Farm Assessment",
    "📋  Level Requirements",
    "📊  All Governorates",
    "📥  Download",
])

# ═══ TAB 1 — MAP ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 🗺️ Smart Irrigation Suitability Map — Egypt")
    st.info("Map shows current/estimated SISI level per governorate. Studied farms (●) have field-verified data. Others are estimated from farming system analogies. Update scores in **Farm Assessment** tab to reflect new field data.")

    # Legend
    leg_cols = st.columns(6)
    for i, (lv, lc) in enumerate(L_COLORS.items()):
        with leg_cols[i]:
            st.markdown(f'<div style="background:{lc};border-radius:8px;padding:8px;text-align:center;color:white;font-size:11px;font-weight:600;">{L_NAMES[lv]}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Map
    df_map2 = df_map.copy()
    df_map2["Size"] = df_map2["Studied"].apply(lambda x: 20 if x else 12)
    df_map2["Symbol"] = df_map2["Studied"].apply(lambda x: "circle" if x else "circle-open")
    df_map2["Label"] = df_map2["Level"].astype(str)
    df_map2["Hover"] = df_map2.apply(lambda r:
        f"<b>{r['Governorate']}</b><br>"
        f"SISI Score: <b>{r['SISI']}</b><br>"
        f"Level: <b>{r['Level_Name']}</b><br>"
        f"System: {r['System']}<br>"
        f"Water: {r['Water']}<br>"
        f"{'🔬 Field Verified' if r['Studied'] else '📐 Estimated'}<br>"
        f"{r['Notes'][:80]}...",
        axis=1
    )

    fig_map = go.Figure()

    for lvl, lc in L_COLORS.items():
        subset = df_map2[df_map2["Level"] == lvl]
        if subset.empty: continue
        studied_s = subset[subset["Studied"]]
        other_s   = subset[~subset["Studied"]]

        if not studied_s.empty:
            fig_map.add_trace(go.Scattermapbox(
                lat=studied_s["lat"], lon=studied_s["lon"],
                mode="markers+text",
                marker=dict(size=18, color=lc, opacity=0.95),
                text=studied_s["Governorate"],
                textposition="top center",
                textfont=dict(size=10, color="#1a3328"),
                hovertext=studied_s["Hover"],
                hoverinfo="text",
                name=f"L{lvl} — Studied",
                legendgroup=str(lvl),
            ))
        if not other_s.empty:
            fig_map.add_trace(go.Scattermapbox(
                lat=other_s["lat"], lon=other_s["lon"],
                mode="markers+text",
                marker=dict(size=12, color=lc, opacity=0.6),
                text=other_s["Governorate"],
                textposition="top center",
                textfont=dict(size=9, color="#4a6741"),
                hovertext=other_s["Hover"],
                hoverinfo="text",
                name=f"L{lvl} — Estimated",
                legendgroup=str(lvl),
                legendgrouptitle={"text": L_NAMES[lvl]},
            ))

    fig_map.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={"lat": 26.8, "lon": 30.8},
        mapbox_zoom=5.2,
        paper_bgcolor=BG,
        height=620,
        margin={"r":0,"t":10,"l":0,"b":0},
        legend=dict(bgcolor=CARD, bordercolor=BORDER, borderwidth=1, font=dict(size=10)),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # SISI bar chart
    st.markdown("### 📊 SISI Scores — All Governorates")
    df_bar = df_map.sort_values("SISI", ascending=True)
    fig_bar = go.Figure(go.Bar(
        x=df_bar["SISI"], y=df_bar["Governorate"],
        orientation="h",
        marker_color=df_bar["Color"],
        text=df_bar.apply(lambda r: f"{r['SISI']} | L{r['Level']}", axis=1),
        textposition="outside",
        textfont={"size":9, "color":TEXT},
    ))
    fig_bar.update_layout(
        height=780, paper_bgcolor=BG, plot_bgcolor="#eef5f1",
        font={"family":"Inter","color":TEXT},
        margin={"r":100,"t":20,"l":10,"b":10},
        xaxis=dict(range=[0,5.4], gridcolor=BORDER),
        yaxis=dict(gridcolor=BORDER),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ═══ TAB 2 — FARM ASSESSMENT ══════════════════════════════════════════════════
with tab2:
    st.markdown("### 🧮 Farm-Level SISI Assessment Tool")
    st.info("Enter field survey data for any governorate or new farm. The tool calculates the SISI score, assigns the maturity level, and lists all required equipment with academic references.")

    col_gov, col_new = st.columns([3,1])
    with col_gov:
        gov_list = list(GOVS_DATA.keys()) + ["➕ New Farm (Custom)"]
        selected_gov = st.selectbox("Select Governorate or enter new farm", gov_list)
    with col_new:
        st.markdown("<br>", unsafe_allow_html=True)
        solar_check = st.checkbox("☀️ Off-grid / Solar Candidate")

    if selected_gov == "➕ New Farm (Custom)":
        farm_name = st.text_input("Farm name / location", "New Farm")
        d_base = {"C1":2.0,"C2":2.0,"C3":2.5,"C4":2.0,"C5":2.0}
    else:
        farm_name = GOVS_DATA[selected_gov]["farm"]
        d_base = GOVS_DATA[selected_gov]

    st.markdown(f"**Farm:** {farm_name}")
    st.markdown("#### Enter Criterion Scores (1.0 – 5.0):")

    sc1,sc2,sc3 = st.columns(3)
    sc_cols = [sc1,sc2,sc3,sc1,sc2]
    scores = {}
    for i, (ck, cn) in enumerate(C_NAMES.items()):
        with sc_cols[i]:
            v = st.slider(f"{C_ICONS[ck]} {cn}", 1.0, 5.0,
                          float(d_base.get(ck, 2.0)), 0.1, key=f"fa_{ck}")
            scores[ck] = v
            # Show rubric hint
            # Find closest rubric
            closest = min(RUBRICS[ck].keys(), key=lambda x: abs(x-v))
            st.caption(f"📌 {RUBRICS[ck][closest][:80]}...")

    sisi = calc_sisi(scores["C1"],scores["C2"],scores["C3"],scores["C4"],scores["C5"])
    level = get_level(sisi, solar_check)
    lc = level_color(level)
    ln = L_NAMES.get(level,"")

    st.markdown("---")
    st.markdown("### 📍 Assessment Result")
    r1,r2,r3,r4 = st.columns(4)
    r1.metric("SISI Score", sisi)
    r2.metric("Maturity Level", str(level))
    r3.metric("Water Saving", LEVEL_REQUIREMENTS[level]["water_saving"])
    r4.metric("Investment (EGP)", LEVEL_REQUIREMENTS[level]["investment_egp"])

    st.markdown(f"""
    <div style="background:{lc};border-radius:14px;padding:18px 24px;margin:16px 0;color:white;">
      <p style="font-size:11px;font-weight:700;text-transform:uppercase;margin:0 0 6px;opacity:0.8;">Classification</p>
      <h3 style="margin:0;font-family:'Lora',serif;font-size:22px;">{ln}</h3>
      <p style="margin:8px 0 0;font-size:13px;opacity:0.9;">SISI Range: {LEVEL_REQUIREMENTS[level]["range"]}</p>
      <p style="margin:4px 0 0;font-size:13px;opacity:0.85;">{LEVEL_REQUIREMENTS[level]["description"]}</p>
    </div>""", unsafe_allow_html=True)

    # Score breakdown
    st.markdown("#### Score Breakdown")
    breakdown_rows = []
    for ck, cn in C_NAMES.items():
        breakdown_rows.append({
            "Criterion": cn,
            "Weight": f"{WEIGHTS[ck]*100:.0f}%",
            "Score": scores[ck],
            "Weighted": round(WEIGHTS[ck]*scores[ck], 3),
        })
    df_bk = pd.DataFrame(breakdown_rows)
    st.dataframe(df_bk, use_container_width=True, hide_index=True, height=220)

    st.markdown("---")
    st.markdown("### 🔧 Required Equipment & Components")
    st.markdown(f"*Based on: {LEVEL_REQUIREMENTS[level]['literature']}*")
    comp_rows = []
    for c in LEVEL_REQUIREMENTS[level]["components"]:
        comp_rows.append(c)
    df_comp = pd.DataFrame(comp_rows)
    st.dataframe(df_comp, use_container_width=True, hide_index=True, height=320)

    # Upgrade pathway
    if level != 5 and level != "3S":
        next_level = level + 1 if isinstance(level, int) else 4
        st.markdown(f"---")
        st.markdown(f"### ⬆️ Upgrade Pathway to Level {next_level}")
        upgrade_info = {
            1: {"infra":"Install pressurized drip ≥50% farm area; central filtration; stable grid/solar","capacity":"3-day WMRI drip maintenance course; join cooperative","sisi":"+0.80 to +1.20","scale":"≥5 feddans"},
            2: {"infra":"Expand drip to 100%; GSM modules; soil-threshold automated controller + solenoids","capacity":"Smartphone irrigation dashboard proficiency; SCADA operational training","sisi":"+0.50 to +0.90","scale":"≥7 feddans"},
            3: {"infra":"On-farm automated weather station; flow meters all zones; SCADA multi-zone upgrade","capacity":"Farm manager; Penman-Monteith ET₀ training; data interpretation","sisi":"+0.70 to +1.00","scale":"≥50 feddans"},
            4: {"infra":"Full SCADA integration; RTK GPS-enabled multispectral UAV; cloud AI analytics","capacity":"Certified UAV pilot; data specialist; digital twin configuration","sisi":"+0.40 to +0.80","scale":"≥300 feddans"},
        }
        if level in upgrade_info:
            ui = upgrade_info[level]
            uc1,uc2 = st.columns(2)
            with uc1:
                st.markdown(f"""<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:16px;">
                <p style="color:{TEXT_LT};font-size:11px;font-weight:700;text-transform:uppercase;margin-bottom:8px;">Infrastructure Upgrades</p>
                <p style="color:{TEXT};font-size:13px;">{ui['infra']}</p>
                </div>""", unsafe_allow_html=True)
            with uc2:
                st.markdown(f"""<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:16px;">
                <p style="color:{TEXT_LT};font-size:11px;font-weight:700;text-transform:uppercase;margin-bottom:8px;">Capacity & Scale</p>
                <p style="color:{TEXT};font-size:13px;"><b>Capacity:</b> {ui['capacity']}<br><b>SISI improvement:</b> {ui['sisi']}<br><b>Min scale:</b> {ui['scale']}</p>
                </div>""", unsafe_allow_html=True)

# ═══ TAB 3 — LEVEL REQUIREMENTS ══════════════════════════════════════════════
with tab3:
    st.markdown("### 📋 Smart Irrigation Level Requirements — Full Reference")
    st.markdown(f"""<div style="background:#e8f5f3;border-left:4px solid #1a5c40;border-radius:0 12px 12px 0;padding:14px 18px;margin-bottom:20px;">
    <p style="color:#1a5c40;font-weight:700;margin:0 0 4px;font-family:'Lora',serif;">SISI Formula (AHP-WSM)</p>
    <p style="color:{TEXT_MID};font-size:13px;margin:0;font-family:monospace;">
    SISI = (0.30×C₁) + (0.20×C₂) + (0.15×C₃) + (0.15×C₄) + (0.20×C₅)
    </p><p style="color:{TEXT_LT};font-size:11px;margin:6px 0 0;">CR = -0.000446 &lt; 0.10 ✓ | λmax = 4.998 | Expert panel n=7 | WMRI/NWRC/ARC/Banha University</p>
    </div>""", unsafe_allow_html=True)

    for lvl, req in LEVEL_REQUIREMENTS.items():
        lc2 = level_color(lvl)
        with st.expander(f"  {L_NAMES[lvl]}   |   SISI: {req['range']}   |   Water saving: {req['water_saving']}   |   Investment: {req['investment_egp']} EGP"):
            st.markdown(f"""<div style="background:rgba(0,0,0,0.03);border-radius:10px;padding:12px 16px;margin-bottom:12px;border-left:4px solid {lc2};">
            <p style="color:{TEXT_MID};font-size:14px;line-height:1.8;">{req['description']}</p>
            <p style="color:{TEXT_LT};font-size:11px;font-style:italic;margin-top:6px;">📚 {req['literature']}</p>
            </div>""", unsafe_allow_html=True)
            st.markdown("**Required Components & Specifications:**")
            df_c = pd.DataFrame(req["components"])
            st.dataframe(df_c, use_container_width=True, hide_index=True, height=min(320, 60+len(req["components"])*42))
            st.caption(f"🎯 Key discriminator: {req['key_discriminator']}")

# ═══ TAB 4 — ALL GOVERNORATES ════════════════════════════════════════════════
with tab4:
    st.markdown("### 📊 SISI Results — All 27 Governorates")
    df_show = df_map[["Governorate","SISI","Level","Level_Name","C1","C2","C3","C4","C5","System","Water","Studied","Farm"]].copy()
    df_show["Studied"] = df_show["Studied"].apply(lambda x: "🔬 Field" if x else "📐 Est.")

    def hl_level(val):
        c_map = {1:"background-color:#fdecea;color:#c62828;font-weight:700",
                 2:"background-color:#fff3e0;color:#e65100;font-weight:700",
                 3:"background-color:#fffde7;color:#f57f17;font-weight:700",
                 "3S":"background-color:#f3e5f5;color:#6a1b9a;font-weight:700",
                 4:"background-color:#e8f5e9;color:#2e7d32;font-weight:700",
                 5:"background-color:#e3f2fd;color:#1565c0;font-weight:700"}
        return c_map.get(val, "")

    st.dataframe(df_show.style.map(hl_level, subset=["Level"]), use_container_width=True, height=700)

    # Distribution chart
    st.markdown("### 📈 Level Distribution")
    dist = df_map.groupby("Level").size().reset_index(name="Count")
    dist["Level_Name"] = dist["Level"].map(L_NAMES)
    dist["Color"] = dist["Level"].map(L_COLORS)
    fig_dist = go.Figure(go.Bar(
        x=dist["Level_Name"], y=dist["Count"],
        marker_color=dist["Color"],
        text=dist["Count"], textposition="outside",
        textfont={"size":12, "color":TEXT}
    ))
    fig_dist.update_layout(
        height=340, paper_bgcolor=BG, plot_bgcolor="#eef5f1",
        font={"family":"Inter","color":TEXT},
        xaxis=dict(gridcolor=BORDER), yaxis=dict(gridcolor=BORDER),
        margin={"t":20}
    )
    st.plotly_chart(fig_dist, use_container_width=True)

# ═══ TAB 5 — DOWNLOAD ════════════════════════════════════════════════════════
with tab5:
    st.markdown("### 📥 Download SISI Results")
    df_dl = df_map[["Governorate","SISI","Level","Level_Name","C1","C2","C3","C4","C5","System","Water","Farm","Notes"]].copy()
    st.dataframe(df_dl, use_container_width=True)
    csv = df_dl.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("⬇️ Download CSV", csv, "egypt_sisi_results.csv", "text/csv")

    st.markdown("---")
    st.markdown("### 📐 AHP Weights Reference")
    wdf = pd.DataFrame({
        "Criterion": list(C_NAMES.values()),
        "Code": list(C_NAMES.keys()),
        "Weight": [0.30,0.20,0.15,0.15,0.20],
        "Percentage": ["30%","20%","15%","15%","20%"],
        "Literature Basis": [
            "FAO Paper 63; Al-Ghobari 2018; Phocaides 2007",
            "Wolfert et al. 2017; Chandel et al. 2015; IEC 30141",
            "FAO Paper 56; Doorenbos & Pruitt 1977; ISO 16075",
            "Hedley 2015; FAO Paper 56 Kc; IFAD 2015",
            "Rogers 2003; Feder et al. 1985; Metcalfe et al. 2019",
        ]
    })
    st.dataframe(wdf, use_container_width=True, hide_index=True)

st.markdown(f"""<div style="text-align:center;padding:14px;border-top:1px solid {BORDER};margin-top:8px;">
<span style="color:{TEXT_LT};font-size:11px;">SISI Tool · WMRI 2026 · FAO-56 · ISO 11545 · IEC 30141 · World Bank SARI · AHP-WSM (CR=-0.000446) · Built with Streamlit 💧</span>
</div>""", unsafe_allow_html=True)
