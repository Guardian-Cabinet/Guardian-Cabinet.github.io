import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. 페이지 설정
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="🌬️ 대기질 모니터링 대시보드",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. 커스텀 CSS (다크 테마)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── 메트릭 카드 ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0F1923 0%, #162231 100%);
    border: 1px solid rgba(94, 186, 213, 0.2);
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(94, 186, 213, 0.2);
    border-color: rgba(94, 186, 213, 0.5);
}
div[data-testid="stMetric"] label {
    color: #7AA2B3 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #E0F0F6 !important;
}

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080E14 0%, #0F1923 100%);
    border-right: 1px solid rgba(94, 186, 213, 0.15);
}

/* ── 탭 ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(15, 25, 35, 0.5);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(94, 186, 213, 0.15) !important;
    border-color: transparent !important;
}

/* ── 차트 컨테이너 ── */
div[data-testid="stPlotlyChart"] {
    background: rgba(15, 25, 35, 0.4);
    border-radius: 12px;
    padding: 8px;
    border: 1px solid rgba(94, 186, 213, 0.1);
    transition: border-color 0.3s ease;
}
div[data-testid="stPlotlyChart"]:hover {
    border-color: rgba(94, 186, 213, 0.3);
}

/* ── 데이터프레임 ── */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(94, 186, 213, 0.15);
}

hr { border-color: rgba(94, 186, 213, 0.15) !important; }
.block-container { padding-top: 2rem; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #080E14; }
::-webkit-scrollbar-thumb { background: #5EBAD5; border-radius: 3px; }

/* ── 커스텀 컴포넌트 ── */
.gradient-title {
    background: linear-gradient(120deg, #5EBAD5 0%, #A8E6CF 30%, #5EBAD5 60%, #3D7EA6 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gshift 4s ease infinite;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
@keyframes gshift {
    0% { background-position: 0% center; }
    50% { background-position: 100% center; }
    100% { background-position: 0% center; }
}
.page-subtitle { color: #7AA2B3; font-size: 1rem; margin-bottom: 2rem; }
.section-header {
    color: #A8E6CF;
    font-size: 1.15rem;
    font-weight: 600;
    margin: 1.5rem 0 1rem 0;
    padding-left: 12px;
    border-left: 3px solid #5EBAD5;
}
.kpi-card {
    background: linear-gradient(135deg, #0F1923 0%, #162231 100%);
    border: 1px solid rgba(94, 186, 213, 0.2);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(94, 186, 213, 0.15);
}
.kpi-card.good::before { background: linear-gradient(90deg, #6BCB77, #A8E6CF); }
.kpi-card.moderate::before { background: linear-gradient(90deg, #F5D5A0, #FFB347); }
.kpi-card.bad::before { background: linear-gradient(90deg, #FF6B6B, #FF4757); }
.kpi-card.info::before { background: linear-gradient(90deg, #5EBAD5, #A8E6CF); }
.kpi-icon { font-size: 2rem; margin-bottom: 8px; }
.kpi-value { font-size: 2rem; font-weight: 700; color: #E0F0F6; margin: 4px 0; }
.kpi-label { font-size: 0.85rem; color: #7AA2B3; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.kpi-sub { font-size: 0.8rem; color: #5EBAD5; margin-top: 6px; }

.grade-badge {
    display: inline-block;
    padding: 4px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    margin-top: 6px;
}
.grade-good { background: rgba(107,203,119,0.15); color: #6BCB77; }
.grade-moderate { background: rgba(255,179,71,0.15); color: #FFB347; }
.grade-bad { background: rgba(255,107,107,0.15); color: #FF6B6B; }
.grade-verybad { background: rgba(255,71,87,0.15); color: #FF4757; }
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. 차트 공통 설정
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COLORS = ["#5EBAD5", "#A8E6CF", "#FFB347", "#FF6B6B", "#C39BD3", "#F5D5A0", "#6BCB77"]
DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#C0D8E4", size=12),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11),
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(gridcolor="rgba(94,186,213,0.08)", zerolinecolor="rgba(94,186,213,0.1)"),
    yaxis=dict(gridcolor="rgba(94,186,213,0.08)", zerolinecolor="rgba(94,186,213,0.1)"),
    hoverlabel=dict(bgcolor="#0F1923", font_size=12, font_color="#E0F0F6"),
)

POLLUTANT_INFO = {
    "PM10":  {"unit": "㎍/㎥", "icon": "🫁", "name": "미세먼지(PM10)",
              "좋음": 30, "보통": 80, "나쁨": 150},
    "PM25":  {"unit": "㎍/㎥", "icon": "😷", "name": "초미세먼지(PM2.5)",
              "좋음": 15, "보통": 35, "나쁨": 75},
    "O3":    {"unit": "ppm", "icon": "☀️", "name": "오존(O₃)",
              "좋음": 0.030, "보통": 0.090, "나쁨": 0.150},
    "NO2":   {"unit": "ppm", "icon": "🏭", "name": "이산화질소(NO₂)",
              "좋음": 0.030, "보통": 0.060, "나쁨": 0.200},
    "CO":    {"unit": "ppm", "icon": "💨", "name": "일산화탄소(CO)",
              "좋음": 2.0, "보통": 9.0, "나쁨": 15.0},
    "SO2":   {"unit": "ppm", "icon": "🔥", "name": "아황산가스(SO₂)",
              "좋음": 0.020, "보통": 0.050, "나쁨": 0.150},
}

POLLUTANT_COLORS = {
    "PM10": "#FF6B6B", "PM25": "#FF4757", "O3": "#FFB347",
    "NO2": "#C39BD3", "CO": "#5EBAD5", "SO2": "#F5D5A0",
}


def apply_dark(fig, title=""):
    fig.update_layout(**DARK_LAYOUT)
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=16, color="#A8E6CF")))
    return fig


def section_header(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def get_grade(value, pollutant):
    info = POLLUTANT_INFO[pollutant]
    if value <= info["좋음"]:
        return "좋음", "good"
    elif value <= info["보통"]:
        return "보통", "moderate"
    elif value <= info["나쁨"]:
        return "나쁨", "bad"
    else:
        return "매우나쁨", "verybad"


def kpi_card(icon, label, value, sub="", grade_class="info"):
    st.markdown(f"""
    <div class="kpi-card {grade_class}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. 데이터 로드 & 전처리
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data
def load_data():
    df = pd.read_csv("202501-air.csv", encoding="utf-8")
    # 날짜·시간 파싱
    df["측정일시_str"] = df["측정일시"].astype(str)
    df["날짜"] = pd.to_datetime(df["측정일시_str"].str[:8], format="%Y%m%d")
    df["시간"] = df["측정일시_str"].str[8:10].astype(int)
    df["요일"] = df["날짜"].dt.day_name()
    df["일자"] = df["날짜"].dt.day
    # 시도·구 분리
    parts = df["지역"].str.split(n=1, expand=True)
    df["시도"] = parts[0]
    df["구군"] = parts[1]
    return df


df = load_data()
pollutants = ["PM10", "PM25", "O3", "NO2", "CO", "SO2"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. 사이드바 필터
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0 1.5rem 0;">
        <div style="font-size:2.5rem; margin-bottom:4px;">🌬️</div>
        <div style="font-size:1.1rem; font-weight:700; color:#A8E6CF; letter-spacing:1px;">
            AIR QUALITY</div>
        <div style="font-size:0.75rem; color:#7AA2B3; margin-top:2px;">
            2025년 1월 대기질 모니터링</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    st.header("🎯 필터 설정")

    # 시도 선택
    sido_list = sorted(df["시도"].unique().tolist())
    selected_sido = st.multiselect("시도 선택", sido_list, default=sido_list)

    # 날짜 범위
    min_date = df["날짜"].min().date()
    max_date = df["날짜"].max().date()
    date_range = st.date_input("분석 기간", value=(min_date, max_date),
                                min_value=min_date, max_value=max_date)

    # 측정망
    mang_list = df["망"].unique().tolist()
    selected_mang = st.multiselect("측정망", mang_list, default=mang_list)

    # 주요 오염물질 선택
    st.divider()
    st.header("📊 오염물질")
    primary_pollutant = st.selectbox(
        "주요 분석 대상",
        pollutants,
        format_func=lambda x: f"{POLLUTANT_INFO[x]['icon']} {POLLUTANT_INFO[x]['name']}"
    )

    st.divider()
    total_stations = df["측정소명"].nunique()
    st.caption(f"📍 총 측정소: **{total_stations}개**")
    st.caption(f"📅 데이터: **2025년 1월**")
    st.caption(f"📊 전체 레코드: **{len(df):,}건**")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. 필터 적용
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
filtered = df.copy()
if selected_sido:
    filtered = filtered[filtered["시도"].isin(selected_sido)]
if selected_mang:
    filtered = filtered[filtered["망"].isin(selected_mang)]
if len(date_range) == 2:
    filtered = filtered[(filtered["날짜"].dt.date >= date_range[0]) &
                         (filtered["날짜"].dt.date <= date_range[1])]

p_info = POLLUTANT_INFO[primary_pollutant]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. 메인 헤더
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown('<div class="gradient-title">🌬️ 대기질 모니터링 대시보드</div>'
            '<div class="page-subtitle">2025년 1월 · 실시간 대기오염 측정 데이터 분석</div>',
            unsafe_allow_html=True)

# ── 요약 KPI ──
avg_pm10 = filtered["PM10"].mean()
avg_pm25 = filtered["PM25"].mean()
avg_o3 = filtered["O3"].mean()
avg_no2 = filtered["NO2"].mean()

pm10_grade, pm10_cls = get_grade(avg_pm10, "PM10")
pm25_grade, pm25_cls = get_grade(avg_pm25, "PM25")

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("🫁", "PM10 평균", f"{avg_pm10:.1f} ㎍/㎥",
             f'<span class="grade-badge grade-{pm10_cls}">{pm10_grade}</span>', pm10_cls)
with k2:
    kpi_card("😷", "PM2.5 평균", f"{avg_pm25:.1f} ㎍/㎥",
             f'<span class="grade-badge grade-{pm25_cls}">{pm25_grade}</span>', pm25_cls)
with k3:
    o3_g, o3_c = get_grade(avg_o3, "O3")
    kpi_card("☀️", "O₃ 평균", f"{avg_o3:.4f} ppm",
             f'<span class="grade-badge grade-{o3_c}">{o3_g}</span>', o3_c)
with k4:
    kpi_card("📍", "측정 데이터", f"{len(filtered):,}건",
             f"측정소 {filtered['측정소명'].nunique()}개", "info")

st.markdown("")
st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. 탭 구성
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 종합 개요", "📈 시계열 분석", "🗺️ 지역 비교", "⏰ 시간대·요일", "📋 데이터 탐색"
])

# ──────────────────────────────────────────────
# 탭 1: 종합 개요
# ──────────────────────────────────────────────
with tab1:
    section_header("6대 오염물질 현황")

    cols = st.columns(3)
    for i, pol in enumerate(pollutants):
        info = POLLUTANT_INFO[pol]
        val = filtered[pol].mean()
        grade_text, grade_cls = get_grade(val, pol)
        with cols[i % 3]:
            fmt = f"{val:.4f}" if val < 1 else f"{val:.1f}"
            kpi_card(info["icon"], info["name"], f"{fmt} {info['unit']}",
                     f'<span class="grade-badge grade-{grade_cls}">{grade_text}</span>', grade_cls)

    st.markdown("")
    section_header(f"{p_info['name']} — 일별 추이")

    daily_avg = filtered.groupby("날짜")[primary_pollutant].mean().reset_index()
    daily_avg.columns = ["날짜", "평균값"]

    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(
        x=daily_avg["날짜"], y=daily_avg["평균값"], name="일 평균",
        fill="tozeroy", fillcolor=f"rgba({','.join(str(int(POLLUTANT_COLORS[primary_pollutant].lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.15)",
        line=dict(color=POLLUTANT_COLORS[primary_pollutant], width=2.5),
        mode="lines",
    ))
    # 기준선 표시
    fig_daily.add_hline(y=p_info["좋음"], line_dash="dash", line_color="#6BCB77",
                         annotation_text=f"좋음 기준: {p_info['좋음']}", annotation_font=dict(color="#6BCB77", size=10))
    fig_daily.add_hline(y=p_info["보통"], line_dash="dash", line_color="#FFB347",
                         annotation_text=f"보통 기준: {p_info['보통']}", annotation_font=dict(color="#FFB347", size=10))

    apply_dark(fig_daily, f"{p_info['name']} 일별 평균 추이")
    fig_daily.update_layout(height=380, yaxis_title=f"{p_info['unit']}")
    st.plotly_chart(fig_daily, use_container_width=True)

    st.markdown("")
    ov1, ov2 = st.columns(2)
    with ov1:
        section_header("시도별 오염물질 평균")
        sido_avg = filtered.groupby("시도")[pollutants].mean().reset_index()
        sido_melt = sido_avg.melt(id_vars="시도", var_name="오염물질", value_name="평균값")
        # PM10, PM25 스케일이 다르므로 정규화
        for pol in pollutants:
            mask = sido_melt["오염물질"] == pol
            max_val = sido_melt.loc[mask, "평균값"].max()
            if max_val > 0:
                sido_melt.loc[mask, "정규화"] = sido_melt.loc[mask, "평균값"] / max_val
            else:
                sido_melt.loc[mask, "정규화"] = 0

        fig_radar_data = sido_avg.set_index("시도")
        # 정규화해서 레이더 차트
        normalized = fig_radar_data.copy()
        for col in pollutants:
            max_v = normalized[col].max()
            if max_v > 0:
                normalized[col] = normalized[col] / max_v

        fig_radar = go.Figure()
        for sido in normalized.index:
            values = normalized.loc[sido, pollutants].tolist()
            values.append(values[0])  # close the polygon
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=[POLLUTANT_INFO[p]["name"][:5] for p in pollutants] + [POLLUTANT_INFO[pollutants[0]]["name"][:5]],
                name=sido,
                fill="toself",
                opacity=0.6,
            ))
        apply_dark(fig_radar, "시도별 오염 프로필 (정규화)")
        fig_radar.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 1.1], gridcolor="rgba(94,186,213,0.15)"),
                angularaxis=dict(gridcolor="rgba(94,186,213,0.15)"),
            ),
            height=420,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with ov2:
        section_header("오염물질 간 상관관계")
        corr = filtered[pollutants].corr()
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=[POLLUTANT_INFO[p]["name"][:6] for p in pollutants],
            y=[POLLUTANT_INFO[p]["name"][:6] for p in pollutants],
            colorscale=[[0, "#0F1923"], [0.5, "#5EBAD5"], [1, "#FF6B6B"]],
            text=corr.values.round(2),
            texttemplate="%{text}",
            textfont=dict(size=11, color="#E0F0F6"),
            zmin=-1, zmax=1,
            colorbar=dict(title="상관계수"),
        ))
        apply_dark(fig_corr, "오염물질 상관관계 히트맵")
        fig_corr.update_layout(height=420)
        st.plotly_chart(fig_corr, use_container_width=True)

# ──────────────────────────────────────────────
# 탭 2: 시계열 분석
# ──────────────────────────────────────────────
with tab2:
    section_header(f"{p_info['name']} — 시도별 일별 추이")

    daily_sido = filtered.groupby(["날짜", "시도"])[primary_pollutant].mean().reset_index()
    fig_ts = px.line(daily_sido, x="날짜", y=primary_pollutant, color="시도",
                     color_discrete_sequence=COLORS)
    fig_ts.update_traces(line_width=2)
    apply_dark(fig_ts, f"시도별 {p_info['name']} 일별 평균")
    fig_ts.update_layout(height=420, yaxis_title=p_info["unit"])
    st.plotly_chart(fig_ts, use_container_width=True)

    st.markdown("")
    ts1, ts2 = st.columns(2)

    with ts1:
        section_header("일별 6대 오염물질 동시 추이")
        sel_pols = st.multiselect("비교할 오염물질", pollutants, default=["PM10", "PM25"],
                                   format_func=lambda x: POLLUTANT_INFO[x]["name"])
        if sel_pols:
            daily_multi = filtered.groupby("날짜")[sel_pols].mean().reset_index()
            fig_multi = go.Figure()
            for pol in sel_pols:
                fig_multi.add_trace(go.Scatter(
                    x=daily_multi["날짜"], y=daily_multi[pol],
                    name=POLLUTANT_INFO[pol]["name"],
                    line=dict(color=POLLUTANT_COLORS[pol], width=2),
                ))
            apply_dark(fig_multi, "선택 오염물질 비교")
            fig_multi.update_layout(height=380, yaxis_title="농도")
            st.plotly_chart(fig_multi, use_container_width=True)

    with ts2:
        section_header(f"{p_info['name']} 분포 (박스플롯)")
        fig_box = px.box(filtered.dropna(subset=[primary_pollutant]),
                         x="시도", y=primary_pollutant,
                         color="시도", color_discrete_sequence=COLORS)
        apply_dark(fig_box, f"시도별 {p_info['name']} 분포")
        fig_box.update_layout(height=380, showlegend=False, yaxis_title=p_info["unit"])
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("")
    section_header(f"{p_info['name']} — 7일 이동평균")

    daily_ma = filtered.groupby("날짜")[primary_pollutant].mean().reset_index()
    daily_ma.columns = ["날짜", "평균"]
    daily_ma["7일 이동평균"] = daily_ma["평균"].rolling(7, min_periods=1).mean()

    fig_ma = go.Figure()
    fig_ma.add_trace(go.Scatter(x=daily_ma["날짜"], y=daily_ma["평균"], name="일 평균",
                                 line=dict(color=POLLUTANT_COLORS[primary_pollutant], width=1.5),
                                 opacity=0.5))
    fig_ma.add_trace(go.Scatter(x=daily_ma["날짜"], y=daily_ma["7일 이동평균"], name="7일 이동평균",
                                 line=dict(color="#A8E6CF", width=3)))
    apply_dark(fig_ma, f"{p_info['name']} 7일 이동평균")
    fig_ma.update_layout(height=350, yaxis_title=p_info["unit"])
    st.plotly_chart(fig_ma, use_container_width=True)

# ──────────────────────────────────────────────
# 탭 3: 지역 비교
# ──────────────────────────────────────────────
with tab3:
    section_header(f"지역별 {p_info['name']} 평균 랭킹")

    region_avg = filtered.groupby("지역")[primary_pollutant].mean().reset_index()
    region_avg.columns = ["지역", "평균"]
    region_avg = region_avg.sort_values("평균", ascending=True)

    rc1, rc2 = st.columns([3, 2])

    with rc1:
        top_n = st.slider("표시할 지역 수", 10, min(50, len(region_avg)), 20)
        top_regions = region_avg.tail(top_n)
        fig_rank = px.bar(top_regions, x="평균", y="지역", orientation="h",
                          color="평균",
                          color_continuous_scale=[[0, "#6BCB77"], [0.5, "#FFB347"], [1, "#FF6B6B"]])
        fig_rank.update_traces(marker_line_width=0)
        apply_dark(fig_rank, f"{p_info['name']} 상위 {top_n}개 지역 (높을수록 오염)")
        fig_rank.update_layout(height=max(400, top_n * 22), coloraxis_showscale=False)
        st.plotly_chart(fig_rank, use_container_width=True)

    with rc2:
        section_header("시도별 평균 비교")
        sido_bar = filtered.groupby("시도")[primary_pollutant].mean().reset_index()
        sido_bar.columns = ["시도", "평균"]
        sido_bar = sido_bar.sort_values("평균", ascending=True)

        fig_sido = px.bar(sido_bar, x="시도", y="평균",
                          color="평균",
                          color_continuous_scale=[[0, "#6BCB77"], [0.5, "#FFB347"], [1, "#FF6B6B"]])
        fig_sido.update_traces(text=sido_bar["평균"].apply(lambda x: f"{x:.2f}"),
                               textposition="outside", textfont=dict(color="#A8E6CF", size=11))
        apply_dark(fig_sido, f"시도별 {p_info['name']} 평균")
        fig_sido.update_layout(height=400, coloraxis_showscale=False)
        st.plotly_chart(fig_sido, use_container_width=True)

    st.markdown("")
    section_header("시도 × 오염물질 히트맵")

    sido_pol = filtered.groupby("시도")[pollutants].mean()
    # 정규화 (0~1)
    sido_pol_norm = sido_pol.copy()
    for col in pollutants:
        max_v = sido_pol_norm[col].max()
        if max_v > 0:
            sido_pol_norm[col] = sido_pol_norm[col] / max_v

    fig_heat = go.Figure(data=go.Heatmap(
        z=sido_pol_norm.values,
        x=[POLLUTANT_INFO[p]["name"][:6] for p in pollutants],
        y=sido_pol_norm.index.tolist(),
        colorscale=[[0, "#0F1923"], [0.3, "#3D7EA6"], [0.6, "#FFB347"], [1, "#FF4757"]],
        text=sido_pol.values.round(3),
        texttemplate="%{text}",
        textfont=dict(size=10, color="#E0F0F6"),
        colorbar=dict(title="정규화"),
    ))
    apply_dark(fig_heat, "시도별 오염물질 농도 히트맵 (정규화)")
    fig_heat.update_layout(height=350)
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("")
    section_header("측정망별 오염물질 비교")
    mang_avg = filtered.groupby("망")[pollutants].mean().reset_index()
    mang_melt = mang_avg.melt(id_vars="망", var_name="오염물질", value_name="평균값")
    fig_mang = px.bar(mang_melt, x="망", y="평균값", color="오염물질",
                      barmode="group", color_discrete_map=POLLUTANT_COLORS)
    apply_dark(fig_mang, "측정망별 오염물질 평균 농도")
    fig_mang.update_layout(height=380)
    st.plotly_chart(fig_mang, use_container_width=True)

# ──────────────────────────────────────────────
# 탭 4: 시간대·요일 분석
# ──────────────────────────────────────────────
with tab4:
    section_header(f"{p_info['name']} — 시간대별 패턴")

    hour_avg = filtered.groupby("시간")[primary_pollutant].mean().reset_index()
    hour_avg.columns = ["시간", "평균"]

    peak_threshold = hour_avg["평균"].quantile(0.75)
    hour_avg["구분"] = hour_avg["평균"].apply(lambda x: "📈 고농도" if x >= peak_threshold else "일반")

    fig_hour = px.bar(hour_avg, x="시간", y="평균", color="구분",
                      color_discrete_map={"📈 고농도": "#FF6B6B", "일반": "#3D7EA6"},
                      text=hour_avg["평균"].apply(lambda x: f"{x:.2f}"))
    fig_hour.update_traces(textposition="outside", textfont=dict(color="#A8E6CF", size=9))
    fig_hour.update_xaxes(dtick=1)
    apply_dark(fig_hour, f"시간대별 {p_info['name']} 평균 (0~23시)")
    fig_hour.update_layout(height=380, xaxis_title="시간 (시)", yaxis_title=p_info["unit"])
    st.plotly_chart(fig_hour, use_container_width=True)

    st.markdown("")
    td1, td2 = st.columns(2)

    with td1:
        section_header("요일별 패턴")
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_kr = {"Monday": "월", "Tuesday": "화", "Wednesday": "수", "Thursday": "목",
                  "Friday": "금", "Saturday": "토", "Sunday": "일"}
        day_avg = filtered.groupby("요일")[primary_pollutant].mean().reset_index()
        day_avg.columns = ["요일", "평균"]
        day_avg["요일_kr"] = day_avg["요일"].map(day_kr)
        day_avg["order"] = day_avg["요일"].map({d: i for i, d in enumerate(day_order)})
        day_avg = day_avg.sort_values("order")

        fig_day = px.bar(day_avg, x="요일_kr", y="평균", color_discrete_sequence=["#5EBAD5"])
        fig_day.update_traces(text=day_avg["평균"].apply(lambda x: f"{x:.2f}"),
                              textposition="outside", textfont=dict(color="#A8E6CF", size=10))
        apply_dark(fig_day, f"요일별 {p_info['name']} 평균")
        fig_day.update_layout(height=380, xaxis_title="요일")
        st.plotly_chart(fig_day, use_container_width=True)

    with td2:
        section_header("시간대별 6대 오염물질 (정규화)")
        hour_all = filtered.groupby("시간")[pollutants].mean()
        hour_norm = hour_all.copy()
        for col in pollutants:
            max_v = hour_norm[col].max()
            if max_v > 0:
                hour_norm[col] = hour_norm[col] / max_v

        fig_hourall = go.Figure()
        for pol in pollutants:
            fig_hourall.add_trace(go.Scatter(
                x=hour_norm.index, y=hour_norm[pol],
                name=POLLUTANT_INFO[pol]["name"][:6],
                line=dict(color=POLLUTANT_COLORS[pol], width=2),
            ))
        apply_dark(fig_hourall, "시간대별 오염물질 패턴 비교 (정규화)")
        fig_hourall.update_layout(height=380, xaxis_title="시간", yaxis_title="정규화 값")
        fig_hourall.update_xaxes(dtick=2)
        st.plotly_chart(fig_hourall, use_container_width=True)

    st.markdown("")
    section_header("요일 × 시간대 히트맵")

    day_hour = filtered.groupby(["요일", "시간"])[primary_pollutant].mean().reset_index()
    day_hour["요일_kr"] = day_hour["요일"].map(day_kr)
    day_hour["order"] = day_hour["요일"].map({d: i for i, d in enumerate(day_order)})
    day_hour = day_hour.sort_values("order")

    pivot_dh = day_hour.pivot_table(index="요일_kr", columns="시간", values=primary_pollutant, sort=False)

    fig_dh = go.Figure(data=go.Heatmap(
        z=pivot_dh.values,
        x=[f"{h}시" for h in pivot_dh.columns],
        y=pivot_dh.index.tolist(),
        colorscale=[[0, "#0F1923"], [0.3, "#3D7EA6"], [0.6, "#FFB347"], [1, "#FF4757"]],
        colorbar=dict(title=p_info["unit"]),
    ))
    apply_dark(fig_dh, f"요일 × 시간대 {p_info['name']} 분포")
    fig_dh.update_layout(height=350)
    st.plotly_chart(fig_dh, use_container_width=True)

# ──────────────────────────────────────────────
# 탭 5: 데이터 탐색
# ──────────────────────────────────────────────
with tab5:
    dt1, dt2, dt3 = st.tabs(["🔍 데이터 탐색", "📊 피벗 분석", "⬇️ 다운로드"])

    with dt1:
        section_header("필터링된 데이터")
        show_n = st.slider("표시 행 수", 50, 500, 100, key="data_rows")
        st.caption(f"📌 총 {len(filtered):,}건 중 상위 {show_n}건 표시")

        display_cols = ["지역", "망", "측정소명", "날짜", "시간"] + pollutants
        st.dataframe(
            filtered[display_cols].head(show_n),
            use_container_width=True,
            hide_index=True,
            height=500,
        )

        st.markdown("")
        section_header("기초 통계량")
        stats = filtered[pollutants].describe().round(4)
        stats.index = ["건수", "평균", "표준편차", "최솟값", "25%", "50%", "75%", "최댓값"]
        st.dataframe(stats, use_container_width=True)

    with dt2:
        section_header("피벗 테이블 생성")
        pv1, pv2 = st.columns(2)
        with pv1:
            pivot_rows = st.selectbox("행 기준", ["시도", "구군", "지역", "망", "요일"], key="pvr")
        with pv2:
            pivot_values = st.selectbox("값",
                                         pollutants,
                                         format_func=lambda x: POLLUTANT_INFO[x]["name"],
                                         key="pvv")

        pivot_agg = st.radio("집계 함수", ["평균", "최댓값", "최솟값", "중앙값", "표준편차"],
                              horizontal=True, key="pva")
        agg_map = {"평균": "mean", "최댓값": "max", "최솟값": "min",
                   "중앙값": "median", "표준편차": "std"}

        pivot_result = filtered.pivot_table(
            index=pivot_rows, values=pivot_values,
            aggfunc=agg_map[pivot_agg]
        ).round(4).sort_values(pivot_values, ascending=False)

        st.dataframe(pivot_result, use_container_width=True, height=400)

        # 피벗 결과 시각화
        if len(pivot_result) <= 30:
            pr = pivot_result.reset_index()
            fig_pv = px.bar(pr, x=pivot_rows, y=pivot_values,
                            color=pivot_values,
                            color_continuous_scale=[[0, "#6BCB77"], [0.5, "#FFB347"], [1, "#FF6B6B"]])
            apply_dark(fig_pv, f"{pivot_rows}별 {POLLUTANT_INFO[pivot_values]['name']} ({pivot_agg})")
            fig_pv.update_layout(height=380, coloraxis_showscale=False)
            fig_pv.update_xaxes(tickangle=-45)
            st.plotly_chart(fig_pv, use_container_width=True)

    with dt3:
        section_header("데이터 다운로드")

        csv_data = filtered.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 필터링 데이터 (CSV)",
            data=csv_data,
            file_name="air_quality_filtered.csv",
            mime="text/csv",
        )

        st.markdown("")
        summary = filtered.groupby("지역")[pollutants].agg(["mean", "max", "min"]).round(4)
        summary.columns = [f"{col[0]}_{col[1]}" for col in summary.columns]
        csv_summary = summary.to_csv().encode("utf-8-sig")
        st.download_button(
            label="📥 지역별 요약 통계 (CSV)",
            data=csv_summary,
            file_name="air_quality_summary.csv",
            mime="text/csv",
        )
