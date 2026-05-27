import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="أداة MCDA للري الذكي — مصر",
    page_icon="🌊",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    * { font-family: 'Cairo', sans-serif; }
    .main { direction: rtl; }
</style>
""", unsafe_allow_html=True)

GOVS = [
    {"rank":1,  "name":"البحيرة",       "nameEn":"El Beheira",      "m":[4.5,4.5,4.0,4.5,5.0,4.0], "system":"أراضي مستصلحة حديثة — شركات كبرى",         "status":"selected"},
    {"rank":2,  "name":"القليوبية",     "nameEn":"El Qalyoubeya",   "m":[3.5,5.0,2.0,5.0,5.0,5.0], "system":"دلتا قديمة — حيازات صغيرة مجزأة",           "status":"selected"},
    {"rank":3,  "name":"الإسكندرية",   "nameEn":"Alexandria",      "m":[4.5,3.5,3.5,4.0,5.0,3.0], "system":"أراضي ساحلية متوسطية مستصلحة",              "status":"selected"},
    {"rank":4,  "name":"الدقهلية",     "nameEn":"El Dakahlia",     "m":[4.5,3.0,2.5,4.5,4.0,4.5], "system":"منطقة ملوحة ذيل قناة دلتا وسطى",            "status":"selected"},
    {"rank":5,  "name":"سوهاج",        "nameEn":"Sohag",           "m":[3.5,2.5,4.5,3.5,4.5,4.5], "system":"وادي صعيد ضيق — إجهاد حراري عالٍ",           "status":"selected"},
    {"rank":6,  "name":"الوادي الجديد","nameEn":"El Wadi El Gedid","m":[3.0,4.0,5.0,2.5,4.0,1.0], "system":"استصلاح خزان جوفي أحفوري — شبه جاف",        "status":"boundary"},
    {"rank":7,  "name":"مطروح",        "nameEn":"Matrouh",         "m":[3.5,3.5,4.5,2.5,2.5,1.5], "system":"ساحل شمال غرب — بدو / أمطار",               "status":"other"},
    {"rank":8,  "name":"الشرقية",      "nameEn":"El Sharqia",      "m":[3.0,2.5,2.5,4.0,2.0,4.5], "system":"دلتا شرقية — صغار مزارعين",                 "status":"other"},
    {"rank":9,  "name":"جنوب سيناء",   "nameEn":"South Sinai",     "m":[3.0,3.5,5.0,2.0,2.5,1.0], "system":"سيناء جبلية / ساحلية",                      "status":"other"},
    {"rank":10, "name":"شمال سيناء",   "nameEn":"North Sinai",     "m":[3.5,3.0,4.0,2.5,2.0,2.0], "system":"سيناء — منطقة القناة",                      "status":"other"},
    {"rank":11, "name":"المنيا",       "nameEn":"El Minia",        "m":[2.5,1.5,4.0,3.5,2.5,4.0], "system":"صعيد أوسط",                                 "status":"other"},
    {"rank":12, "name":"الفيوم",       "nameEn":"El Fayoum",       "m":[3.0,1.5,3.0,3.5,2.5,3.5], "system":"منخفض الفيوم",                              "status":"other"},
    {"rank":12, "name":"أسيوط",        "nameEn":"Asyut",           "m":[2.5,1.5,4.0,3.5,2.0,4.0], "system":"صعيد أوسط — أسيوط",                        "status":"other"},
    {"rank":14, "name":"كفر الشيخ",    "nameEn":"Kafr El Sheikh",  "m":[3.0,2.0,2.5,3.5,2.0,4.0], "system":"دلتا شمالية ساحلية",                        "status":"other"},
    {"rank":15, "name":"قنا",          "nameEn":"Qena",            "m":[2.5,1.5,4.5,3.0,2.0,3.5], "system":"صعيد — منطقة الأقصر",                       "status":"other"},
    {"rank":16, "name":"أسوان",        "nameEn":"Aswan",           "m":[2.5,2.0,5.0,3.0,1.5,2.0], "system":"أقصى صعيد",                                 "status":"other"},
    {"rank":17, "name":"الغربية",      "nameEn":"El Gharbia",      "m":[2.5,2.0,2.0,4.0,1.5,4.5], "system":"دلتا وسطى — صغار مزارعين",                  "status":"other"},
    {"rank":18, "name":"الإسماعيلية",  "nameEn":"Ismailia",        "m":[2.5,2.5,3.0,3.5,2.0,2.0], "system":"استصلاح منطقة القناة",                      "status":"other"},
    {"rank":19, "name":"بني سويف",     "nameEn":"Beni Suef",       "m":[2.5,1.5,3.5,3.0,2.0,3.5], "system":"صعيد — منطقة انتقالية",                     "status":"other"},
    {"rank":20, "name":"المنوفية",     "nameEn":"El Menoufia",     "m":[2.5,1.5,2.0,4.0,1.5,4.5], "system":"دلتا وسطى",                                 "status":"other"},
    {"rank":21, "name":"الأقصر",       "nameEn":"Luxor",           "m":[2.0,1.5,4.5,3.0,1.5,2.5], "system":"سياحة / صعيد علوي",                         "status":"other"},
    {"rank":22, "name":"الجيزة",       "nameEn":"Giza",            "m":[2.0,1.5,2.5,4.0,1.5,3.5], "system":"حضري — أراضي قديمة",                        "status":"other"},
    {"rank":23, "name":"البحر الأحمر", "nameEn":"Red Sea",         "m":[2.0,3.0,4.5,2.0,1.5,1.0], "system":"صحراء ساحلية متفرقة",                       "status":"other"},
    {"rank":24, "name":"دمياط",        "nameEn":"Damietta",        "m":[2.5,2.0,2.0,3.0,1.5,3.0], "system":"دلتا شمالية ساحلية",                        "status":"other"},
    {"rank":25, "name":"السويس",       "nameEn":"Suez",            "m":[1.5,2.0,3.5,2.5,1.0,1.5], "system":"صناعي / ساحلي",                             "status":"other"},
    {"rank":26, "name":"القاهرة",      "nameEn":"Cairo",           "m":[1.5,1.0,2.0,4.0,1.0,2.0], "system":"حضري — زراعة محيطية",                       "status":"other"},
    {"rank":27, "name":"بورسعيد",      "nameEn":"Port Said",       "m":[1.5,1.5,2.0,2.5,1.0,1.5], "system":"حضري — منطقة القناة",                       "status":"other"},
]

WEIGHTS_BASE = [0.22, 0.18, 0.15, 0.17, 0.18, 0.10]
M_NAMES = ["M₁ تنوع هيدرولوجي", "M₂ هيكل حيازات", "M₃ إجهاد مناخي", "M₄ جاهزية مؤسسية", "M₅ تمثيل النظام", "M₆ كثافة مزارعين"]
M_FULL  = ["M₁ — تنوع المصدر المائي", "M₂ — هيكل حيازة الأراضي", "M₃ — الإجهاد المناخي",
           "M₄ — الجاهزية المؤسسية", "M₅ — تمثيلية النظام الزراعي", "M₆ — كثافة المزارعين"]

def calc_wlc(m, w):
    return round(sum(wi * mi for wi, mi in zip(w, m)), 3)

def build_df(custom_scores=None, weights=None):
    w = weights if weights else WEIGHTS_BASE
    rows = []
    for g in GOVS:
        m = custom_scores.get(g["name"], g["m"]) if custom_scores else g["m"]
        score = calc_wlc(m, w)
        rows.append({
            "المحافظة": g["name"],
            "Governorate": g["nameEn"],
            "M₁": m[0], "M₂": m[1], "M₃": m[2],
            "M₄": m[3], "M₅": m[4], "M₆": m[5],
            "WLC Score": score,
            "النظام الزراعي": g["system"],
            "الحالة": "مختارة ✓" if g["status"]=="selected" else "حالة حدودية" if g["status"]=="boundary" else "أخرى",
        })
    df = pd.DataFrame(rows).sort_values("WLC Score", ascending=False).reset_index(drop=True)
    df.index += 1
    return df

# ── Header ──
st.markdown("# 🌊 أداة MCDA للري الذكي — مصر")
st.markdown("نموذج **Weighted Linear Combination** مطبق على 27 محافظة مصرية | Stage 1 Six-Criterion WLC")
st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 نتائج WLC",
    "🧮 حساب تفاعلي",
    "🔬 Sensitivity Analysis",
    "✏️ تعديل الدرجات",
    "📥 تحميل البيانات"
])

# ══════════════════════════════════════════════════════
# TAB 1 — WLC Results
# ══════════════════════════════════════════════════════
with tab1:
    df = build_df()
    st.markdown("### 🏆 المحافظات الخمس المختارة")
    top5 = df[df["الحالة"] == "مختارة ✓"].head(5)
    cols = st.columns(5)
    for i, (_, row) in enumerate(top5.iterrows()):
        with cols[i]:
            st.metric(label=row["المحافظة"], value=row["WLC Score"])
            st.caption(row["النظام الزراعي"])

    st.markdown("---")
    st.markdown("### 📋 جدول كل المحافظات")
    display_df = df[["المحافظة","M₁","M₂","M₃","M₄","M₅","M₆","WLC Score","الحالة","النظام الزراعي"]].copy()
    def highlight_status(val):
        if val == "مختارة ✓": return "background-color: #fff8e1; font-weight: bold"
        elif val == "حالة حدودية": return "background-color: #fff3e0"
        return ""
    st.dataframe(display_df.style.map(highlight_status, subset=["الحالة"]), use_container_width=True, height=600)

    st.markdown("### 📊 مقارنة بصرية — أعلى 10 محافظات")
    fig = px.bar(df.head(10), x="WLC Score", y="المحافظة", orientation="h",
                 color="الحالة",
                 color_discrete_map={"مختارة ✓":"#c8a96e","حالة حدودية":"#e65100","أخرى":"#90a4ae"},
                 text="WLC Score")
    fig.update_layout(yaxis={"categoryorder":"total ascending"}, height=420)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════
# TAB 2 — حساب تفاعلي (الجديد)
# ══════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🧮 أدخلي درجات أي محافظة وشوفي النتيجة فوراً")
    st.info("عدّلي درجات أي محافظة من الـ 27 — الترتيب الكامل بيتحدث لحظة بلحظة ومقارن بالمحافظات اللي فوقها وتحتها.")

    # تهيئة session state لحفظ الدرجات المعدلة
    if "custom_scores" not in st.session_state:
        st.session_state.custom_scores = {g["name"]: list(g["m"]) for g in GOVS}

    # اختيار المحافظة
    gov_names = [g["name"] for g in GOVS]
    col_sel, col_reset = st.columns([3, 1])
    with col_sel:
        selected = st.selectbox("اختاري المحافظة اللي عايزة تعدليها", gov_names, key="interactive_gov")
    with col_reset:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↺ إعادة تعيين كل الدرجات"):
            st.session_state.custom_scores = {g["name"]: list(g["m"]) for g in GOVS}
            st.rerun()

    gov_obj = next(g for g in GOVS if g["name"] == selected)
    current_m = st.session_state.custom_scores[selected]

    st.markdown(f"**النظام الزراعي:** {gov_obj['system']}")
    st.markdown("---")

    # sliders للمحافظة المختارة
    st.markdown("#### أدخلي الدرجات (من 1 إلى 5):")
    new_m = []
    cols_s = st.columns(3)
    for i, name in enumerate(M_FULL):
        with cols_s[i % 3]:
            val = st.slider(name, min_value=1.0, max_value=5.0,
                            value=float(current_m[i]), step=0.5, key=f"int_s{i}")
            new_m.append(val)

    # حفظ الدرجات الجديدة
    st.session_state.custom_scores[selected] = new_m

    # حساب الترتيب الكامل بالدرجات المعدلة
    df_custom = build_df(custom_scores=st.session_state.custom_scores)
    df_base   = build_df()

    # نتيجة المحافظة المختارة
    st.markdown("---")
    st.markdown("### 📍 نتيجة المحافظة المختارة")

    new_score    = calc_wlc(new_m, WEIGHTS_BASE)
    orig_score   = calc_wlc(gov_obj["m"], WEIGHTS_BASE)
    new_rank     = int(df_custom[df_custom["المحافظة"] == selected].index[0])
    orig_rank    = int(df_base[df_base["المحافظة"] == selected].index[0])
    rank_delta   = orig_rank - new_rank  # موجب = تحسّن
    score_delta  = round(new_score - orig_score, 3)

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("WLC Score الجديد",   new_score,  delta=score_delta)
    r2.metric("WLC Score الأصلي",   orig_score)
    r3.metric("الترتيب الجديد",     f"#{new_rank}",  delta=f"{rank_delta:+d} مركز" if rank_delta != 0 else "نفس الترتيب")
    r4.metric("الترتيب الأصلي",     f"#{orig_rank}")

    # مقارنة بالمحافظات فوقها وتحتها
    st.markdown("---")
    st.markdown("### 🔼🔽 مقارنة بالجيران في الترتيب")

    total = len(df_custom)
    above = df_custom[df_custom.index == new_rank - 1] if new_rank > 1 else None
    below = df_custom[df_custom.index == new_rank + 1] if new_rank < total else None

    nb_cols = st.columns(3)

    with nb_cols[0]:
        if above is not None and not above.empty:
            ab = above.iloc[0]
            st.markdown("**🔼 المحافظة اللي فوقها**")
            st.markdown(f"### {ab['المحافظة']}")
            st.markdown(f"Score: **{ab['WLC Score']}**")
            diff_above = round(ab['WLC Score'] - new_score, 3)
            st.markdown(f"الفرق: `+{diff_above}` عنك")
            st.caption(ab['النظام الزراعي'])
        else:
            st.markdown("**🥇 أعلى محافظة في الترتيب!**")

    with nb_cols[1]:
        st.markdown("**📍 المحافظة المختارة**")
        st.markdown(f"### {selected}")
        st.markdown(f"Score: **{new_score}**")
        st.markdown(f"الترتيب: **#{new_rank}** من {total}")
        pct = round((total - new_rank) / total * 100)
        st.markdown(f"أعلى من **{pct}%** من المحافظات")

    with nb_cols[2]:
        if below is not None and not below.empty:
            bl = below.iloc[0]
            st.markdown("**🔽 المحافظة اللي تحتها**")
            st.markdown(f"### {bl['المحافظة']}")
            st.markdown(f"Score: **{bl['WLC Score']}**")
            diff_below = round(new_score - bl['WLC Score'], 3)
            st.markdown(f"الفرق: `+{diff_below}` عنها")
            st.caption(bl['النظام الزراعي'])
        else:
            st.markdown("**آخر محافظة في الترتيب**")

    # جدول الترتيب الكامل مع تمييز المحافظة المختارة
    st.markdown("---")
    st.markdown("### 📋 الترتيب الكامل بعد التعديل")

    changed = []
    for g in GOVS:
        orig = calc_wlc(g["m"], WEIGHTS_BASE)
        new  = calc_wlc(st.session_state.custom_scores[g["name"]], WEIGHTS_BASE)
        if abs(new - orig) > 0.001:
            changed.append(g["name"])

    if changed:
        st.info(f"✏️ تم تعديل درجات: {' | '.join(changed)}")

    show_df = df_custom[["المحافظة","M₁","M₂","M₃","M₄","M₅","M₆","WLC Score","الحالة"]].copy()

    def highlight_interactive(row):
        if row["المحافظة"] == selected:
            return ["background-color: #e3f2fd; font-weight: bold"] * len(row)
        if row["الحالة"] == "مختارة ✓":
            return ["background-color: #fff8e1"] * len(row)
        if row["الحالة"] == "حالة حدودية":
            return ["background-color: #fff3e0"] * len(row)
        return [""] * len(row)

    st.dataframe(
        show_df.style.apply(highlight_interactive, axis=1),
        use_container_width=True,
        height=700
    )

    # رسم بياني للترتيب الكامل
    st.markdown("### 📊 الترتيب البصري الكامل")
    colors = []
    for _, row in df_custom.iterrows():
        if row["المحافظة"] == selected:
            colors.append("#2196F3")
        elif row["الحالة"] == "مختارة ✓":
            colors.append("#c8a96e")
        elif row["الحالة"] == "حالة حدودية":
            colors.append("#e65100")
        else:
            colors.append("#90a4ae")

    fig3 = go.Figure(go.Bar(
        x=df_custom["WLC Score"],
        y=df_custom["المحافظة"],
        orientation="h",
        marker_color=colors,
        text=df_custom["WLC Score"],
        textposition="outside"
    ))
    fig3.update_layout(
        yaxis={"categoryorder": "total ascending"},
        height=800,
        title=f"الترتيب الكامل — المحافظة المختارة ({selected}) باللون الأزرق"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════
# TAB 3 — Sensitivity Analysis
# ══════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🔬 اختبار الحساسية — غيّر الأوزان وشوف التأثير")
    st.info("غيّر أوزان المعايير — مجموعها لازم يساوي 1.00 بالظبط")

    cols2 = st.columns(3)
    new_weights = []
    for i, name in enumerate(M_NAMES):
        with cols2[i % 3]:
            w = st.slider(name, min_value=0.01, max_value=0.50,
                          value=WEIGHTS_BASE[i], step=0.01, key=f"w{i}")
            new_weights.append(w)

    total_w = round(sum(new_weights), 3)
    if abs(total_w - 1.0) > 0.005:
        st.error(f"⚠️ مجموع الأوزان = {total_w} — لازم يبقى 1.00 بالظبط")
    else:
        st.success(f"✓ مجموع الأوزان = {total_w}")
        df_new  = build_df(weights=new_weights)
        df_base2 = build_df()
        merged = df_new[["المحافظة","WLC Score","الحالة"]].copy()
        merged.columns = ["المحافظة","Score الجديد","الحالة"]
        base_scores = df_base2.set_index("المحافظة")["WLC Score"]
        merged["Score الأصلي"] = merged["المحافظة"].map(base_scores)
        merged["Δ التغيير"] = (merged["Score الجديد"] - merged["Score الأصلي"]).round(3)
        merged = merged.sort_values("Score الجديد", ascending=False).reset_index(drop=True)
        merged.index += 1
        st.dataframe(merged[["المحافظة","Score الأصلي","Score الجديد","Δ التغيير","الحالة"]], use_container_width=True, height=500)

        fig2 = go.Figure()
        top10 = merged.head(10)
        fig2.add_trace(go.Bar(name="Score أصلي", x=top10["المحافظة"], y=top10["Score الأصلي"], marker_color="#90a4ae"))
        fig2.add_trace(go.Bar(name="Score جديد", x=top10["المحافظة"], y=top10["Score الجديد"], marker_color="#c8a96e"))
        fig2.update_layout(barmode="group", title="مقارنة: Score الأصلي vs الجديد", height=380)
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════
# TAB 4 — Edit Scores
# ══════════════════════════════════════════════════════
with tab4:
    st.markdown("### ✏️ تعديل درجات أي محافظة")
    gov_names2 = [g["name"] for g in GOVS]
    selected2  = st.selectbox("اختاري المحافظة", gov_names2, key="edit_gov")
    gov_idx2   = next(i for i,g in enumerate(GOVS) if g["name"]==selected2)
    gov_data2  = GOVS[gov_idx2]
    st.markdown(f"**{gov_data2['name']}** — {gov_data2['system']}")
    st.markdown("---")
    new_scores2 = []
    cols3 = st.columns(3)
    for i, full_name in enumerate(M_FULL):
        with cols3[i % 3]:
            s = st.slider(full_name, min_value=1.0, max_value=5.0,
                          value=float(gov_data2["m"][i]), step=0.5, key=f"s2_{i}")
            new_scores2.append(s)
    new_wlc2  = calc_wlc(new_scores2, WEIGHTS_BASE)
    orig_wlc2 = calc_wlc(gov_data2["m"], WEIGHTS_BASE)
    delta2    = round(new_wlc2 - orig_wlc2, 3)
    c1,c2,c3  = st.columns(3)
    c1.metric("WLC Score الأصلي", orig_wlc2)
    c2.metric("WLC Score الجديد", new_wlc2, delta=delta2)
    c3.metric("التغيير", f"{'+' if delta2>=0 else ''}{delta2}")

# ══════════════════════════════════════════════════════
# TAB 5 — Download
# ══════════════════════════════════════════════════════
with tab5:
    st.markdown("### 📥 تحميل النتائج")
    df_dl = build_df()
    st.dataframe(df_dl[["المحافظة","Governorate","M₁","M₂","M₃","M₄","M₅","M₆","WLC Score","الحالة","النظام الزراعي"]], use_container_width=True)
    csv = df_dl.to_csv(index=True, encoding="utf-8-sig")
    st.download_button(label="⬇️ تحميل CSV", data=csv, file_name="egypt_irrigation_mcda.csv", mime="text/csv")
    st.markdown("---")
    st.markdown("### 📐 صيغة الـ WLC")
    st.latex(r"S = (0.22 \times M_1) + (0.18 \times M_2) + (0.15 \times M_3) + (0.17 \times M_4) + (0.18 \times M_5) + (0.10 \times M_6)")
    weights_df = pd.DataFrame({"المعيار": M_FULL, "الوزن": WEIGHTS_BASE, "النسبة": [f"{w*100:.0f}%" for w in WEIGHTS_BASE]})
    st.dataframe(weights_df, use_container_width=True, hide_index=True)

st.divider()
st.caption("أداة MCDA للري الذكي في مصر · Stage 1 WLC Model · البيانات من MALR 2017 و WMRI 2018")
