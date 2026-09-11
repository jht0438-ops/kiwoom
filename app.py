import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="키움증권 재무분석", page_icon="📊", layout="wide")

# ---------------------------------------------------------
# 스타일
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1450px;}
    .section-title {font-size: 1.55rem; font-weight: 800; margin: 0.6rem 0 0.25rem 0;}
    .subtle {color:#6b7280; font-size:0.92rem;}
    .question-box {
        border:1px solid #e5e7eb; border-radius:14px; padding:16px 18px;
        background:#fafafa; margin: 8px 0 18px 0;
    }
    .bridge-box {
        border-left: 5px solid #111827; border-radius:10px; padding:14px 18px;
        background:#f8fafc; margin: 18px 0;
    }
    .conclusion-box {
        border-left: 5px solid #2563eb; border-radius:10px; padding:15px 18px;
        background:#eff6ff; margin: 18px 0 10px 0;
    }
    .conclusion-box b {font-size:1.02rem;}
    .diagnosis-card {
        border:1px solid #e5e7eb; border-radius:14px; padding:18px; min-height:150px;
        background:white;
    }
    .small-note {font-size:0.84rem; color:#6b7280;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 데이터
# 단위: 억원 (실적), 백만원 (건전성 원자료)
# 공개 실적보고서/정기보고서에서 확인되는 수치만 반영
# ---------------------------------------------------------
quarters = [
    "2023Q1","2023Q2","2023Q3","2023Q4",
    "2024Q1","2024Q2","2024Q3","2024Q4",
    "2025Q1","2025Q2","2025Q3","2025Q4",
    "2026Q1","2026Q2"
]

earnings = pd.DataFrame({
    "분기": quarters,
    "순영업수익": [4547,2745,3640,-1730,4312,4057,3979,3698,4549,5372,5188,5275,7325,9830],
    "순수수료수익": [1513,1533,1615,1253,1812,1893,1882,1947,2030,2513,2490,3193,3661,5092],
    "위탁매매 수수료": [1683,1696,1794,1383,1725,1756,1773,1874,1844,2054,2193,2774,3655,5023],
    "IB 수수료": [245,251,246,198,544,567,504,479,570,783,596,821,533,833],
    "이자손익": [1717,1808,1942,1903,1664,1811,1595,1804,1748,1761,2020,2051,2115,2281],
    "S&T/운용손익": [1438,221,161,290,945,579,601,407,980,1216,738,605,1557,2492],
    "기타영업손익": [-120,-817,-77,-5176,-108,-226,-99,-459,-209,-117,-61,-574,-8,-34],
    "판매비와관리비": [1166,1170,1113,1029,1303,1405,1388,1702,1594,1637,1590,2309,1977,2920],
    "영업이익": [3380,1575,2527,-2759,3009,2652,2590,1996,2955,3735,3598,2966,5348,6910],
    "당기순이익": [2712,1044,1900,-2272,2458,2067,2090,1535,2303,3369,2758,2564,4432,6783],
})

# 최근 IR에서 일관되게 비교 가능한 분기 영업지표
market = pd.DataFrame({
    "분기": ["2025Q2","2025Q3","2025Q4","2026Q1","2026Q2"],
    "KRX 일평균 약정(조원)": [7.0, 6.7, 10.5, 16.7, 20.2],
    "NXT 일평균 약정(조원)": [3.7, 4.1, 5.0, 11.1, 16.1],
    "리테일 Market Share(%)": [29.4, 27.0, 26.5, 25.7, 25.0],
    # 최근 Monthly IR의 분기 집계값. 2025~2026 공개자료에는 과거와 달리 해외주식 Market Share가 별도 공시되지 않음.
    "해외주식 일평균 약정(조원)": [1.9, 1.3, 1.4, 1.7, 2.1],
    "해외주식 시장거래대금(조원)": [228.3, 212.0, 218.4, 280.2, 271.0],
})

# 국내·해외 주식 수수료수익: 분기 실적보고서 기준
# 전체 매출 비중이 아니라, 국내주식과 해외주식 수수료수익 합계 내 구성비를 보기 위한 데이터
stock_fee_mix = pd.DataFrame({
    "분기": ["2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2"],
    "국내주식 수수료수익": [908, 1030, 1313, 2311, 3165],
    "해외주식 수수료수익": [716, 822, 993, 804, 1355],
})
stock_fee_mix["합계"] = stock_fee_mix["국내주식 수수료수익"] + stock_fee_mix["해외주식 수수료수익"]
stock_fee_mix["국내 비중(%)"] = stock_fee_mix["국내주식 수수료수익"] / stock_fee_mix["합계"] * 100
stock_fee_mix["해외 비중(%)"] = stock_fee_mix["해외주식 수수료수익"] / stock_fee_mix["합계"] * 100

liquidity = pd.DataFrame({
    "시점": ["2023H1", "2024H1", "2025H1", "2025YE", "2026H1"],
    "3개월 이내 유동성자산": [33742817, 32329033, 40681478, 50637840, 67635179],
    "3개월 이내 유동성부채": [29046630, 26677318, 36141743, 44240496, 57686765],
    "유동성비율(%)": [116, 121, 113, 114, 117],
})

capital = pd.DataFrame({
    "시점": ["2023H1", "2024H1", "2025H1", "2025YE", "2026H1"],
    "영업용순자본": [2715249, 2900664, 3544900, 4349653, 4950589],
    "총위험액": [1343685, 1517141, 2073231, 2568687, 2855969],
    "잉여자본": [1371563, 1383523, 1471669, 1780966, 2094620],
    "필요유지자기자본": [130725, 130725, 131425, 131425, 131425],
    "순자본비율(%)": [1049.20, 1058.35, 1119.78, 1355.12, 1593.78],
})

# ---------------------------------------------------------
# 공통 함수
# ---------------------------------------------------------
def fmt(v):
    return f"{v:,.0f}"

def yoy_pct(series, idx):
    if idx < 4:
        return None
    prev = series.iloc[idx-4]
    cur = series.iloc[idx]
    if prev == 0:
        return None
    return (cur / prev - 1) * 100

def qoq_pct(series, idx):
    if idx < 1:
        return None
    prev = series.iloc[idx-1]
    cur = series.iloc[idx]
    if prev == 0:
        return None
    return (cur / prev - 1) * 100

def direction_text(value):
    if value is None:
        return "비교 불가"
    return f"{value:+.1f}%"

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("키움증권 재무·영업 연계 분석")
st.caption("시장환경 → 거래활동 → 수익구조 → 실적 원인 → 유동성 → 자본적정성 → 종합진단")

# 탭
(tab0, tab1, tab2, tab3, tab4, tab5, tab6) = st.tabs([
    "종합개요",
    "영업환경·거래활동",
    "실적·수익구조",
    "실적 원인분해",
    "유동성·자금여력",
    "자본적정성·재무리스크",
    "최종진단",
])

# ---------------------------------------------------------
# 0. 종합개요
# ---------------------------------------------------------
with tab0:
    st.markdown('<div class="section-title">분석의 출발점</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.expander("왜 분석하나요?", expanded=True):
            st.write(
                "키움증권의 리테일 경쟁력이 실제 수익성으로 어떻게 연결되는지 확인하고, "
                "그 성장을 뒷받침할 유동성과 자본여력이 함께 유지되는지 점검합니다."
            )
    with c2:
        with st.expander("어떤 흐름으로 분석하나요?", expanded=True):
            st.write(
                "시장환경과 거래활동을 먼저 확인한 뒤 수익구조와 실적 원인을 분해합니다. "
                "이후 관점을 재무안정성으로 전환해 유동성과 자본적정성을 확인합니다."
            )
    with c3:
        with st.expander("어떤 결론을 도출하나요?", expanded=True):
            st.write(
                "단순히 '실적이 좋아졌다'는 결론이 아니라, 무엇이 성장을 만들었고 "
                "그 성장을 안정적으로 지속할 재무여력이 있는지를 종합적으로 판단합니다."
            )

    st.markdown("#### 분석 흐름")
    st.info(
        "시장환경 → 고객 거래활동 → 수익구조 → 실적 원인분해 → "
        "단기 유동성 점검 → 위험 대비 자본여력 점검 → 최종진단"
    )

    st.markdown("#### 분석 범위")
    a, b, c = st.columns(3)
    a.metric("분기 실적", "2023Q1 ~ 2026Q2")
    b.metric("영업활동 지표", "최근 비교가능 구간")
    c.metric("재무건전성", "2023H1 ~ 2026H1")
    st.caption("공개된 키움증권 실적보고서·월간 IR·정기보고서에서 확인 가능한 수치만 사용했습니다.")

# ---------------------------------------------------------
# 1. 영업환경·거래활동
# ---------------------------------------------------------
with tab1:
    st.markdown('<div class="question-box"><b>질문</b><br>시장 거래활동이 확대될 때 키움증권의 거래활동과 리테일 Market Share는 어떻게 움직였는가?</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=market["분기"], y=market["KRX 일평균 약정(조원)"], name="KRX 일평균 약정"))
    fig.add_trace(go.Bar(x=market["분기"], y=market["NXT 일평균 약정(조원)"], name="NXT 일평균 약정"))
    fig.add_trace(go.Scatter(x=market["분기"], y=market["리테일 Market Share(%)"], name="리테일 Market Share", yaxis="y2", mode="lines+markers"))
    fig.update_layout(
        title="국내주식 거래활동과 리테일 Market Share",
        barmode="stack",
        yaxis=dict(title="일평균 약정 (조원)"),
        yaxis2=dict(title="Market Share (%)", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h"),
        height=460,
    )
    st.plotly_chart(fig, use_container_width=True)

    # 해외도 국내와 동일하게 한 화면에서 시장환경과 키움의 거래활동을 함께 확인
    # 다만 2025~2026 최근 Monthly IR에는 해외주식 Market Share가 별도 공시되지 않아
    # 시장거래대금(막대) + 키움 해외주식 일평균 약정(선)으로 구성한다.
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=market["분기"],
        y=market["해외주식 시장거래대금(조원)"],
        name="해외주식 시장거래대금",
    ))
    fig2.add_trace(go.Scatter(
        x=market["분기"],
        y=market["해외주식 일평균 약정(조원)"],
        name="키움 해외주식 일평균 약정",
        yaxis="y2",
        mode="lines+markers",
    ))
    fig2.update_layout(
        title="해외주식 시장 거래활동과 키움 해외주식 약정",
        yaxis=dict(title="시장거래대금 (조원)"),
        yaxis2=dict(title="키움 일평균 약정 (조원)", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h"),
        height=460,
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "※ 최근 2025~2026 Monthly IR에서는 과거 자료와 달리 해외주식 Market Share를 별도로 공시하지 않아, "
        "동일 기간에는 해외주식 시장거래대금과 키움의 해외주식 일평균 약정을 함께 비교했습니다."
    )

    st.markdown("#### 국내·해외 주식 수수료수익 구성")
    fee_long = stock_fee_mix.melt(
        id_vars=["분기", "합계"],
        value_vars=["국내주식 수수료수익", "해외주식 수수료수익"],
        var_name="구분",
        value_name="수수료수익",
    )
    fee_long["비중(%)"] = fee_long["수수료수익"] / fee_long["합계"] * 100

    fig3 = px.bar(
        fee_long,
        x="분기",
        y="비중(%)",
        color="구분",
        text=fee_long["비중(%)"].map(lambda x: f"{x:.1f}%"),
        hover_data={"수수료수익": ":,.0f", "합계": ":,.0f", "비중(%)": ":.1f"},
        title="국내·해외 주식 수수료수익 비중",
    )
    fig3.update_layout(
        barmode="stack",
        yaxis=dict(title="구성비 (%)", range=[0, 100]),
        xaxis_title="",
        legend=dict(orientation="h"),
        height=430,
    )
    fig3.update_traces(textposition="inside")
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        "※ 전체 매출 또는 전체 순영업수익의 국내·해외 비중이 아닙니다. "
        "분기 실적보고서에서 별도로 확인 가능한 국내주식·해외주식 수수료수익 합계 안에서의 구성비입니다."
    )

    latest_fee = stock_fee_mix.iloc[-1]
    st.markdown(
        f'<div class="subtle">2026Q2 국내주식 수수료수익 <b>{latest_fee["국내주식 수수료수익"]:,.0f}억원</b> '
        f'({latest_fee["국내 비중(%)"]:.1f}%) · 해외주식 수수료수익 '
        f'<b>{latest_fee["해외주식 수수료수익"]:,.0f}억원</b> ({latest_fee["해외 비중(%)"]:.1f}%)</div>',
        unsafe_allow_html=True,
    )

    latest_m = market.iloc[-1]
    prev_m = market.iloc[-2]
    total_domestic_latest = latest_m["KRX 일평균 약정(조원)"] + latest_m["NXT 일평균 약정(조원)"]
    total_domestic_prev = prev_m["KRX 일평균 약정(조원)"] + prev_m["NXT 일평균 약정(조원)"]
    domestic_change = (total_domestic_latest / total_domestic_prev - 1) * 100
    ms_change = latest_m["리테일 Market Share(%)"] - prev_m["리테일 Market Share(%)"]
    overseas_contract_change = (latest_m["해외주식 일평균 약정(조원)"] / prev_m["해외주식 일평균 약정(조원)"] - 1) * 100
    overseas_market_change = (latest_m["해외주식 시장거래대금(조원)"] / prev_m["해외주식 시장거래대금(조원)"] - 1) * 100

    st.markdown(
        f'<div class="conclusion-box"><b>이 탭에서 얻을 수 있는 결론</b><br>'
        f'최근 비교구간인 {latest_m["분기"]}의 국내주식 일평균 약정은 KRX와 NXT 합산 약 '
        f'<b>{total_domestic_latest:.1f}조원</b>으로 직전 분기 대비 <b>{domestic_change:+.1f}%</b> 변했습니다. '
        f'같은 기간 리테일 Market Share는 <b>{latest_m["리테일 Market Share(%)"]:.1f}%</b>로 '
        f'직전 분기 대비 <b>{ms_change:+.1f}%p</b> 변했습니다.<br>'
        f'해외주식 시장거래대금은 직전 분기 대비 <b>{overseas_market_change:+.1f}%</b>, '
        f'키움의 해외주식 일평균 약정은 <b>{overseas_contract_change:+.1f}%</b> 변했습니다. '
        f'국내는 거래규모와 Market Share를 함께 보고, 해외는 최근 공개자료 범위에서 시장 거래규모와 키움 약정의 방향을 비교해 '
        f'시장 확대 효과와 키움의 거래활동 변화를 구분해 확인합니다.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="bridge-box"><b>다음 질문</b><br>거래활동의 변화가 실제 키움증권의 수수료수익과 영업이익으로 이어졌는지 확인합니다.</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. 실적·수익구조
# ---------------------------------------------------------
with tab2:
    st.markdown('<div class="question-box"><b>질문</b><br>영업환경 변화가 실제 손익에 어떻게 반영됐는가?</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("2026Q2 순영업수익", f"{earnings.iloc[-1]['순영업수익']:,.0f}억원")
    c2.metric("2026Q2 영업이익", f"{earnings.iloc[-1]['영업이익']:,.0f}억원")
    c3.metric("2026Q2 당기순이익", f"{earnings.iloc[-1]['당기순이익']:,.0f}억원")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=earnings["분기"], y=earnings["순영업수익"], mode="lines+markers", name="순영업수익"))
    fig.add_trace(go.Scatter(x=earnings["분기"], y=earnings["영업이익"], mode="lines+markers", name="영업이익"))
    fig.update_layout(title="순영업수익·영업이익 추이", yaxis_title="억원", height=450, legend=dict(orientation="h"))
    st.plotly_chart(fig, use_container_width=True)

    components = ["위탁매매 수수료", "IB 수수료", "이자손익", "S&T/운용손익"]
    long = earnings.melt(id_vars="분기", value_vars=components, var_name="수익원", value_name="금액")
    fig = px.bar(long, x="분기", y="금액", color="수익원", title="주요 수익원별 추이", barmode="group")
    fig.update_layout(yaxis_title="억원", height=480)
    st.plotly_chart(fig, use_container_width=True)

    latest_e = earnings.iloc[-1]
    prev_q = earnings.iloc[-2]
    yoy_e = earnings.iloc[-5]

    revenue_qoq = (latest_e["순영업수익"] / prev_q["순영업수익"] - 1) * 100
    op_qoq = (latest_e["영업이익"] / prev_q["영업이익"] - 1) * 100
    ni_qoq = (latest_e["당기순이익"] / prev_q["당기순이익"] - 1) * 100
    revenue_yoy = (latest_e["순영업수익"] / yoy_e["순영업수익"] - 1) * 100
    op_yoy2 = (latest_e["영업이익"] / yoy_e["영업이익"] - 1) * 100
    ni_yoy = (latest_e["당기순이익"] / yoy_e["당기순이익"] - 1) * 100

    st.markdown(
        f'<div class="conclusion-box"><b>이 탭에서 얻을 수 있는 결론</b><br>'
        f'최근 흐름을 보기 위해 전분기와 먼저 비교하면, 2026Q2 순영업수익은 <b>{latest_e["순영업수익"]:,.0f}억원</b>으로 '
        f'2026Q1 대비 <b>{revenue_qoq:+.1f}%</b>, 영업이익은 <b>{latest_e["영업이익"]:,.0f}억원</b>으로 '
        f'<b>{op_qoq:+.1f}%</b>, 당기순이익은 <b>{latest_e["당기순이익"]:,.0f}억원</b>으로 <b>{ni_qoq:+.1f}%</b> 변했습니다.<br>'
        f'전년동기와 비교해도 순영업수익 <b>{revenue_yoy:+.1f}%</b>, 영업이익 <b>{op_yoy2:+.1f}%</b>, '
        f'당기순이익 <b>{ni_yoy:+.1f}%</b>로 모두 증가했습니다. '
        f'즉 QoQ로 최근 실적 모멘텀을 확인하고, YoY로 분기별 시장환경 차이에도 개선이 유지되는지를 보조적으로 검증할 수 있습니다.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="bridge-box"><b>다음 질문</b><br>실적이 변했다면, 어떤 수익원이 그 변화를 만들었는지 항목별로 분해합니다.</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. 실적 원인분해
# ---------------------------------------------------------
with tab3:
    st.markdown('<div class="question-box"><b>질문</b><br>선택한 분기의 실적 변화를 만든 핵심 원인은 무엇인가?</div>', unsafe_allow_html=True)

    selected = st.selectbox("분석 분기", earnings["분기"].tolist(), index=len(earnings)-1)
    idx = earnings.index[earnings["분기"] == selected][0]

    compare_mode = st.radio("비교 기준", ["전분기 대비", "전년동기 대비"], horizontal=True)
    lag = 1 if compare_mode == "전분기 대비" else 4

    if idx < lag:
        st.warning("선택한 분기는 해당 비교기준의 이전 데이터가 없습니다.")
    else:
        current = earnings.iloc[idx]
        prior = earnings.iloc[idx-lag]
        drivers = ["위탁매매 수수료", "IB 수수료", "이자손익", "S&T/운용손익", "기타영업손익", "판매비와관리비"]

        rows = []
        for d in drivers:
            # 판관비 증가는 영업이익에 부정적이므로 기여도 부호 반전
            diff = current[d] - prior[d]
            impact = -diff if d == "판매비와관리비" else diff
            rows.append({"항목": d, "증감": diff, "영업이익 방향 기여": impact})
        bridge = pd.DataFrame(rows).sort_values("영업이익 방향 기여", ascending=False)

        c1, c2, c3 = st.columns(3)
        op_change = current["영업이익"] - prior["영업이익"]
        c1.metric("선택 분기", selected)
        c2.metric("영업이익", f"{current['영업이익']:,.0f}억원", f"{op_change:+,.0f}억원")
        c3.metric("비교 분기", prior["분기"])

        # 항목 자체의 증감과 영업이익에 미친 방향을 분리해 표시
        bridge["표시항목"] = bridge.apply(
            lambda r: f"{r['항목']}<br>({r['증감']:+,.0f}억원 {'증가' if r['증감'] > 0 else '감소' if r['증감'] < 0 else '변동 없음'})",
            axis=1,
        )
        fig = px.bar(
            bridge,
            x="표시항목",
            y="영업이익 방향 기여",
            hover_data={"항목": True, "증감": ":+,.0f", "영업이익 방향 기여": ":+,.0f", "표시항목": False},
            title=f"{prior['분기']} → {selected} 영업이익 변동 요인 ({compare_mode})",
        )
        fig.update_layout(yaxis_title="영업이익 영향(억원)", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("막대의 +/−는 각 항목 금액의 증감이 아니라, 해당 변화가 영업이익에 미친 방향을 뜻합니다. 판관비는 비용이므로 증가할수록 영업이익에는 음(-)의 영향을 줍니다.")

        top_pos = bridge.iloc[0]
        top_neg = bridge.iloc[-1]

        def impact_sentence(row):
            change_word = "증가" if row["증감"] > 0 else "감소" if row["증감"] < 0 else "변동 없음"
            return (
                f"{row['항목']} {abs(row['증감']):,.0f}억원 {change_word} "
                f"→ 영업이익에 {row['영업이익 방향 기여']:+,.0f}억원 영향"
            )

        st.success(f"가장 큰 긍정 요인: {impact_sentence(top_pos)}")
        st.warning(f"가장 큰 부담 요인: {impact_sentence(top_neg)}")

        positive = bridge[bridge["영업이익 방향 기여"] > 0]
        negative = bridge[bridge["영업이익 방향 기여"] < 0]
        pos_names = ", ".join(positive["항목"].tolist()[:3]) if not positive.empty else "뚜렷한 긍정 요인 없음"
        neg_names = ", ".join(negative["항목"].tolist()[:3]) if not negative.empty else "뚜렷한 부담 요인 없음"

        st.markdown(
            f'<div class="conclusion-box"><b>이 탭에서 얻을 수 있는 결론</b><br>'
            f'{selected} 영업이익은 {prior["분기"]} 대비 <b>{op_change:+,.0f}억원</b> 변했습니다. '
            f'가장 큰 긍정 요인은 <b>{top_pos["항목"]}</b>, 가장 큰 부담 요인은 <b>{top_neg["항목"]}</b>으로 나타났습니다. '
            f'긍정 방향 요인은 {pos_names}, 부담 방향 요인은 {neg_names}입니다. '
            f'이를 통해 단순히 “영업이익이 증가했다/감소했다”가 아니라, 그 변화가 특정 수익원에 집중됐는지 '
            f'여러 수익원이 함께 움직였는지를 확인할 수 있습니다.</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="bridge-box"><b>관점 전환</b><br>'
        '여기까지는 <b>얼마나 잘 벌었고 왜 벌었는가</b>를 확인했습니다. '
        '하지만 높은 수익성이 곧 안정적인 경영을 의미하지는 않습니다. '
        '이제 단기 지급의무에 대응할 충분한 자금여력이 있는지 확인합니다.</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# 4. 유동성·자금여력
# ---------------------------------------------------------
with tab4:
    st.markdown('<div class="question-box"><b>질문</b><br>단기적으로 지급해야 할 자금에 대응할 충분한 유동성자산을 확보하고 있는가?</div>', unsafe_allow_html=True)

    latest_l = liquidity.iloc[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("3개월 이내 유동성자산", f"{latest_l['3개월 이내 유동성자산']/1_000_000:.1f}조원")
    c2.metric("3개월 이내 유동성부채", f"{latest_l['3개월 이내 유동성부채']/1_000_000:.1f}조원")
    c3.metric("유동성비율", f"{latest_l['유동성비율(%)']:.0f}%")

    with st.popover("유동성비율 계산식·해석 보기"):
        st.markdown("**유동성비율 계산식**")
        st.code("유동성비율 = 3개월 이내 유동성자산 ÷ 3개월 이내 유동성부채 × 100")
        calc_ratio = latest_l["3개월 이내 유동성자산"] / latest_l["3개월 이내 유동성부채"] * 100
        st.markdown(
            f"**2026H1 실제 계산**  \n"
            f"{latest_l['3개월 이내 유동성자산']/1_000_000:.1f}조원 ÷ "
            f"{latest_l['3개월 이내 유동성부채']/1_000_000:.1f}조원 × 100 "
            f"≈ **{calc_ratio:.1f}%**"
        )
        st.caption(
            "향후 3개월 이내 지급해야 할 유동성부채 대비 같은 기간 내 현금화 가능한 유동성자산을 "
            "얼마나 확보하고 있는지를 보는 지표입니다. 공개 보고서의 표시값은 반올림 때문에 직접 계산값과 소폭 차이날 수 있습니다."
        )

    plot_l = liquidity.copy()
    plot_l["유동성자산(조원)"] = plot_l["3개월 이내 유동성자산"] / 1_000_000
    plot_l["유동성부채(조원)"] = plot_l["3개월 이내 유동성부채"] / 1_000_000

    fig = go.Figure()
    fig.add_trace(go.Bar(x=plot_l["시점"], y=plot_l["유동성자산(조원)"], name="3개월 이내 유동성자산"))
    fig.add_trace(go.Bar(x=plot_l["시점"], y=plot_l["유동성부채(조원)"], name="3개월 이내 유동성부채"))
    fig.update_layout(title="단기 유동성자산·부채", barmode="group", yaxis_title="조원", height=430)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(plot_l, x="시점", y="유동성비율(%)", markers=True, title="유동성비율 추이")
    fig.update_layout(yaxis_title="%", height=390)
    st.plotly_chart(fig, use_container_width=True)

    prev_l = liquidity.iloc[-2]
    asset_change = (latest_l["3개월 이내 유동성자산"] / prev_l["3개월 이내 유동성자산"] - 1) * 100
    liability_change = (latest_l["3개월 이내 유동성부채"] / prev_l["3개월 이내 유동성부채"] - 1) * 100
    ratio_delta = latest_l["유동성비율(%)"] - prev_l["유동성비율(%)"]
    gap_latest = latest_l["3개월 이내 유동성자산"] - latest_l["3개월 이내 유동성부채"]

    st.markdown(
        f'<div class="conclusion-box"><b>이 탭에서 얻을 수 있는 결론</b><br>'
        f'2026H1 기준 3개월 이내 유동성자산은 약 <b>{latest_l["3개월 이내 유동성자산"]/1_000_000:.1f}조원</b>, '
        f'유동성부채는 약 <b>{latest_l["3개월 이내 유동성부채"]/1_000_000:.1f}조원</b>으로 '
        f'유동성자산이 약 <b>{gap_latest/1_000_000:.1f}조원</b> 더 많습니다. '
        f'유동성비율은 <b>{latest_l["유동성비율(%)"]:.0f}%</b>로 전년말 대비 <b>{ratio_delta:+.0f}%p</b> 변했습니다. '
        f'같은 기간 유동성자산은 <b>{asset_change:+.1f}%</b>, 유동성부채는 <b>{liability_change:+.1f}%</b> 증가했습니다. '
        f'따라서 단기 지급의무에 대응할 자산 우위는 유지되고 있지만, 자산과 부채가 동시에 빠르게 확대되고 있어 '
        f'비율뿐 아니라 양쪽의 증가 속도를 함께 보는 것이 중요합니다.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="bridge-box"><b>다음 질문</b><br>'
        '단기 자금 대응능력을 확인했다고 해서 회사가 부담하는 전체 위험까지 충분히 흡수할 수 있다는 뜻은 아닙니다. '
        '따라서 다음 단계에서는 <b>영업 과정의 위험 대비 자본여력</b>을 확인합니다.</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# 5. 자본적정성·재무리스크
# ---------------------------------------------------------
with tab5:
    st.markdown('<div class="question-box"><b>질문</b><br>영업 과정에서 부담하는 위험을 감당할 충분한 자본여력을 확보하고 있는가?</div>', unsafe_allow_html=True)

    latest_c = capital.iloc[-1]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("영업용순자본", f"{latest_c['영업용순자본']/1_000_000:.2f}조원")
    c2.metric("총위험액", f"{latest_c['총위험액']/1_000_000:.2f}조원")
    c3.metric("잉여자본", f"{latest_c['잉여자본']/1_000_000:.2f}조원")
    c4.metric("순자본비율", f"{latest_c['순자본비율(%)']:,.2f}%")

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        with st.popover("영업용순자본 설명"):
            st.markdown("**무엇을 뜻하나요?**")
            st.write(
                "증권사가 보유한 자본 가운데 영업 과정에서 발생할 수 있는 손실을 흡수하는 데 "
                "사용할 수 있다고 금융투자업 감독규정상 인정되는 금액입니다. "
                "일반적인 회계상 자기자본을 그대로 쓰는 개념이 아니라, 순재산액을 출발점으로 "
                "규정상 가산항목과 차감항목을 반영해 계산합니다."
            )
            st.markdown("**왜 가산·차감하나요?**")
            st.write(
                "회계상 자기자본에 포함되어 있더라도 실제 위기 상황에서 손실을 흡수하는 데 바로 활용하기 어려운 항목은 "
                "자본여력에서 제외할 필요가 있습니다. 반대로 회계상 부채로 분류되더라도 일정 조건을 충족해 "
                "손실을 흡수하는 성격이 강한 항목은 일부 자본처럼 인정할 수 있습니다."
            )
            st.markdown("**대표적인 가산항목 예시**")
            st.write(
                "정상·요주의 자산에 설정된 일부 대손충당금, 일정 요건을 충족하는 후순위차입금, "
                "규정상 인정되는 일부 자산평가이익 등이 대표적인 예입니다."
            )
            st.markdown("**차감항목은?**")
            st.write(
                "감독규정은 영업용순자본 계산 시 별도의 차감항목을 두고 있습니다. "
                "핵심 취지는 회계상 순자산에 포함되어 있어도 손실흡수 재원으로 보기 어렵거나 즉시 활용하기 어려운 부분을 제외하는 것입니다. "
                "이 프로그램에서는 키움증권 공시자료에 개별 차감항목의 세부 내역이 제시되지 않아 회사별 세부 금액은 임의 추정하지 않습니다."
            )
            st.code("개념적 구조: 순재산액 - 차감항목 + 가산항목")
            st.caption("일반 재무회계 지표라기보다 금융투자업자의 재무건전성을 보기 위한 감독상 자본 개념입니다.")

    with p2:
        with st.popover("총위험액 설명"):
            st.markdown("**무엇을 뜻하나요?**")
            st.write(
                "증권사가 영업하면서 부담하는 서로 다른 위험을 금융투자업 감독기준에 따른 산식으로 금액화한 뒤 "
                "합산한 규제상 위험 규모입니다."
            )
            st.code("총위험액 = 시장위험액 + 신용위험액 + 운영위험액")
            st.markdown("**시장위험**")
            st.write(
                "주가·금리·환율 등 시장가격이 불리하게 움직여 보유 주식, 채권, 외환, 파생상품 등에서 "
                "손실이 발생할 위험입니다."
            )
            st.markdown("**신용위험**")
            st.write(
                "거래상대방이나 채무자가 약속한 금액을 지급하지 못해 손실이 발생할 위험입니다. "
                "신용공여, 채권·파생상품 거래상대방 노출 등이 대표적인 예입니다."
            )
            st.markdown("**운영위험**")
            st.write(
                "시장가격이나 거래상대방의 부실이 아니라 시스템 장애, 업무처리 오류, 내부통제 실패, "
                "외부사건 등 영업 과정 자체에서 손실이 발생할 위험입니다."
            )
            st.markdown("**'감독규정 방식으로 금액화'한다는 뜻**")
            st.write(
                "각 위험을 실제 예상손실액으로 단순 추정하는 것이 아니라, 자산·거래 유형과 위험 특성에 따라 "
                "감독기준에서 정한 산식과 위험값을 적용해 공통된 '위험액' 단위로 환산한다는 뜻입니다."
            )
            st.caption(
                "따라서 총위험액 2.86조원은 실제로 2.86조원을 잃을 것이라는 예상손실이 아니라, "
                "감독기준상 측정된 위험 규모입니다."
            )

    with p3:
        with st.popover("잉여자본 설명"):
            st.markdown("**무엇을 뜻하나요?**")
            st.write(
                "키움증권 공식 공시에서 사용하는 명칭입니다. 영업용순자본에서 총위험액을 차감하고도 남아 있는 "
                "자본여력을 의미합니다. 즉 현재 측정된 시장·신용·운영위험을 감안한 뒤에도 추가 손실을 흡수할 수 있는 "
                "여유가 얼마나 남아 있는지를 보여줍니다."
            )
            st.markdown("**계산식**")
            st.code("잉여자본 = 영업용순자본 - 총위험액")
            st.markdown(
                f"**2026H1 실제 계산**  \n"
                f"{latest_c['영업용순자본']/1_000_000:.2f}조원 - "
                f"{latest_c['총위험액']/1_000_000:.2f}조원 ≈ **{latest_c['잉여자본']/1_000_000:.2f}조원**"
            )
            st.write(
                "여기서 '자본완충'은 별도의 회계 계정과목이 아니라 해석을 돕기 위한 표현입니다. "
                "예상하지 못한 시장충격이나 거래상대방 부실 등이 발생할 때 이를 흡수할 여유가 있다는 의미로 이해하면 됩니다."
            )

    with p4:
        with st.popover("순자본비율 설명"):
            st.markdown("**무엇을 뜻하나요?**")
            st.write(
                "위험을 차감하고 남은 잉여자본이, 회사가 영위하는 금융투자업에 대해 감독상 요구되는 "
                "필요유지자기자본보다 얼마나 충분한지를 나타내는 재무건전성 지표입니다."
            )
            st.markdown("**계산식**")
            st.code("순자본비율 = (영업용순자본 - 총위험액) ÷ 필요유지자기자본 × 100")
            calc_ncr = latest_c["잉여자본"] / latest_c["필요유지자기자본"] * 100
            st.markdown(
                f"**2026H1 실제 계산**  \n"
                f"{latest_c['잉여자본']/100:,.2f}억원 ÷ "
                f"{latest_c['필요유지자기자본']/100:,.2f}억원 × 100 = **{calc_ncr:,.2f}%**"
            )
            st.markdown("**필요유지자기자본이란?**")
            st.write(
                "증권사가 인가·등록받아 영위하는 금융투자업의 종류와 규모 등에 따라 감독기준상 유지하도록 요구되는 "
                "최소 자기자본 기준입니다."
            )
            st.caption(
                "순자본비율 1,593.78%는 자산이 부채보다 15.9배 많다는 뜻이 아니라, "
                "위험을 차감하고 남은 잉여자본이 필요유지자기자본의 약 15.9배라는 뜻입니다."
            )

    fig = go.Figure()
    fig.add_trace(go.Bar(x=capital["시점"], y=capital["영업용순자본"]/1_000_000, name="영업용순자본"))
    fig.add_trace(go.Bar(x=capital["시점"], y=capital["총위험액"]/1_000_000, name="총위험액"))
    fig.update_layout(title="영업용순자본과 총위험액", barmode="group", yaxis_title="조원", height=430)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(capital, x="시점", y="순자본비율(%)", markers=True, title="순자본비율 추이")
    fig.update_layout(yaxis_title="%", height=390)
    st.plotly_chart(fig, use_container_width=True)

    # 원인분해
    prev_c = capital.iloc[-2]
    net_cap_change = latest_c["영업용순자본"] - prev_c["영업용순자본"]
    risk_change = latest_c["총위험액"] - prev_c["총위험액"]
    surplus_change = latest_c["잉여자본"] - prev_c["잉여자본"]
    ratio_change = latest_c["순자본비율(%)"] - prev_c["순자본비율(%)"]

    st.markdown("#### 최근 변화 원인")
    a, b, c, d = st.columns(4)
    a.metric("영업용순자본 변화", f"{net_cap_change/1_000_000:+.2f}조원")
    b.metric("총위험액 변화", f"{risk_change/1_000_000:+.2f}조원")
    c.metric("잉여자본 변화", f"{surplus_change/1_000_000:+.2f}조원")
    d.metric("순자본비율 변화", f"{ratio_change:+.2f}%p")

    net_cap_pct = (latest_c["영업용순자본"] / prev_c["영업용순자본"] - 1) * 100
    risk_pct = (latest_c["총위험액"] / prev_c["총위험액"] - 1) * 100
    surplus_pct = (latest_c["잉여자본"] / prev_c["잉여자본"] - 1) * 100

    st.markdown(
        f'<div class="conclusion-box"><b>이 탭에서 얻을 수 있는 결론</b><br>'
        f'2026H1 지배회사 기준 영업용순자본은 약 <b>{latest_c["영업용순자본"]/1_000_000:.2f}조원</b>, '
        f'총위험액은 약 <b>{latest_c["총위험액"]/1_000_000:.2f}조원</b>입니다. '
        f'전년말 대비 영업용순자본은 <b>{net_cap_pct:+.1f}%</b>, 총위험액은 <b>{risk_pct:+.1f}%</b> 증가했지만 '
        f'잉여자본도 <b>{surplus_pct:+.1f}%</b> 늘었고 순자본비율은 '
        f'<b>{prev_c["순자본비율(%)"]:,.2f}% → {latest_c["순자본비율(%)"]:,.2f}%</b>로 상승했습니다. '
        f'즉 위험액이 증가하는 가운데 이를 흡수할 수 있는 자본여력이 더 크게 확대되면서 '
        f'공개지표상 현재 부담하는 위험을 감안하고도 남는 자본여력이 확대된 흐름으로 해석할 수 있습니다.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="bridge-box"><b>마지막 질문</b><br>'
        '수익성, 단기 유동성, 위험 대비 자본여력을 모두 확인했습니다. '
        '이 세 축을 함께 놓고 키움증권의 성장과 재무안정성을 종합적으로 판단합니다.</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# 6. 최종진단
# ---------------------------------------------------------
with tab6:
    st.markdown('<div class="question-box"><b>최종 질문</b><br>수익성과 재무안정성을 함께 고려했을 때, 키움증권의 성장에는 충분한 재무적 뒷받침이 있는가?</div>', unsafe_allow_html=True)

    # 최근 수익성
    op_yoy = (earnings.iloc[-1]["영업이익"] / earnings.iloc[-5]["영업이익"] - 1) * 100
    liquidity_change = liquidity.iloc[-1]["유동성비율(%)"] - liquidity.iloc[-2]["유동성비율(%)"]
    capital_change = capital.iloc[-1]["순자본비율(%)"] - capital.iloc[-2]["순자본비율(%)"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="diagnosis-card">', unsafe_allow_html=True)
        st.subheader("수익성")
        st.metric("2026Q2 영업이익 YoY", f"{op_yoy:+.1f}%")
        st.write("위탁매매 수수료와 S&T/운용손익 확대가 최근 실적 개선의 핵심 축입니다.")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="diagnosis-card">', unsafe_allow_html=True)
        st.subheader("유동성")
        st.metric("최근 유동성비율 변화", f"{liquidity_change:+.0f}%p")
        st.write("유동성자산이 유동성부채를 상회하는 가운데, 비율의 방향과 자산·부채의 증가 속도를 함께 봅니다.")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="diagnosis-card">', unsafe_allow_html=True)
        st.subheader("자본적정성")
        st.metric("최근 순자본비율 변화", f"{capital_change:+.2f}%p")
        st.write("총위험액 증가에도 잉여자본과 순자본비율이 함께 확대되는지 확인합니다.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### 종합 해석")

    latest_e = earnings.iloc[-1]
    prior_yoy = earnings.iloc[-5]
    brokerage_yoy = (latest_e["위탁매매 수수료"] / prior_yoy["위탁매매 수수료"] - 1) * 100
    ib_yoy = (latest_e["IB 수수료"] / prior_yoy["IB 수수료"] - 1) * 100
    interest_yoy = (latest_e["이자손익"] / prior_yoy["이자손익"] - 1) * 100
    st_yoy = (latest_e["S&T/운용손익"] / prior_yoy["S&T/운용손익"] - 1) * 100
    sgna_yoy = (latest_e["판매비와관리비"] / prior_yoy["판매비와관리비"] - 1) * 100

    latest_l = liquidity.iloc[-1]
    prev_l = liquidity.iloc[-2]
    l_gap = latest_l["3개월 이내 유동성자산"] - latest_l["3개월 이내 유동성부채"]

    latest_c = capital.iloc[-1]
    prev_c = capital.iloc[-2]

    st.markdown("##### 1. 수익성 진단")
    st.write(
        f"2026Q2 순영업수익은 {latest_e['순영업수익']:,.0f}억원, 영업이익은 {latest_e['영업이익']:,.0f}억원으로 "
        f"전년동기 대비 각각 {(latest_e['순영업수익']/prior_yoy['순영업수익']-1)*100:+.1f}%, "
        f"{(latest_e['영업이익']/prior_yoy['영업이익']-1)*100:+.1f}% 증가했습니다. "
        "따라서 최근 실적은 외형뿐 아니라 이익 수준에서도 뚜렷한 개선 흐름을 보입니다."
    )

    st.markdown("##### 2. 수익구조 진단")
    st.write(
        f"전년동기 대비 위탁매매 수수료는 {brokerage_yoy:+.1f}%, S&T/운용손익은 {st_yoy:+.1f}%, "
        f"이자손익은 {interest_yoy:+.1f}% 증가했고 IB 수수료는 {ib_yoy:+.1f}% 변했습니다. "
        "최근 성장의 가장 강한 축은 위탁매매와 S&T/운용이지만, 이자손익도 함께 개선돼 "
        "실적 증가가 하나의 수익원에만 의존했다고 보기는 어렵습니다. "
        f"다만 판매비와관리비도 전년동기 대비 {sgna_yoy:+.1f}% 증가했기 때문에 "
        "향후에는 수익 성장 속도와 비용 증가 속도의 차이를 함께 점검할 필요가 있습니다."
    )

    st.markdown("##### 3. 유동성 진단")
    st.write(
        f"2026H1 기준 3개월 이내 유동성자산은 약 {latest_l['3개월 이내 유동성자산']/1_000_000:.1f}조원, "
        f"유동성부채는 약 {latest_l['3개월 이내 유동성부채']/1_000_000:.1f}조원으로 "
        f"유동성자산이 약 {l_gap/1_000_000:.1f}조원 더 많습니다. "
        f"유동성비율은 전년말 {prev_l['유동성비율(%)']:.0f}%에서 {latest_l['유동성비율(%)']:.0f}%로 상승했습니다. "
        "즉 공개지표상 단기 지급의무에 대응할 자산 우위가 유지되고 있습니다. "
        "다만 유동성자산과 부채가 모두 큰 폭으로 늘고 있으므로 단순 비율 수준만이 아니라 "
        "자산·부채의 동반 확대 속도도 계속 확인해야 합니다."
    )

    st.markdown("##### 4. 자본적정성 진단")
    st.write(
        f"2026H1 지배회사 기준 영업용순자본은 약 {latest_c['영업용순자본']/1_000_000:.2f}조원, "
        f"총위험액은 약 {latest_c['총위험액']/1_000_000:.2f}조원, 잉여자본은 약 {latest_c['잉여자본']/1_000_000:.2f}조원입니다. "
        f"순자본비율은 전년말 {prev_c['순자본비율(%)']:,.2f}%에서 {latest_c['순자본비율(%)']:,.2f}%로 상승했습니다. "
        "총위험액이 증가했음에도 잉여자본과 순자본비율이 함께 개선됐다는 점에서, "
        "위험 증가를 흡수할 수 있는 자본여력 역시 확대된 흐름으로 볼 수 있습니다."
    )

    st.markdown("##### 5. 그래서 어떻게 해석할 수 있나?")
    st.success(
        "최근 키움증권의 실적 개선은 단순히 한 수익원의 일시적 증가로 설명되기보다 "
        "위탁매매, S&T/운용, 이자손익 등 복수의 수익원이 함께 개선된 결과로 해석할 수 있습니다. "
        "동시에 실적 확대 과정에서 단기 유동성자산이 유동성부채를 상회하고 있고, "
        "위험액 증가에도 순자본비율과 잉여자본이 함께 확대되고 있습니다. "
        "따라서 공개자료 기준으로는 수익성 개선이 유동성이나 자본적정성을 희생하면서 이루어졌다고 보기 어렵고, "
        "현재까지는 성장과 재무안정성이 함께 유지되는 흐름으로 판단할 수 있습니다."
    )

    st.markdown("##### 6. 추가로 점검해야 할 포인트")
    st.info(
        "① 최근 위탁매매 수수료의 높은 성장기여가 시장 거래활동 둔화 국면에서도 유지되는지, "
        "② S&T/운용손익의 변동성이 확대될 경우 전체 이익 안정성이 어떻게 달라지는지, "
        "③ 판매비와관리비 증가 속도가 수익 성장 속도를 지속적으로 하회하는지, "
        "④ 유동성자산·부채의 동반 확대 과정에서도 유동성비율이 안정적으로 유지되는지, "
        "⑤ 총위험액 증가보다 영업용순자본과 잉여자본의 증가가 계속 우위를 유지하는지를 추가로 확인할 필요가 있습니다."
    )

    st.caption(
        "※ 본 프로그램은 공개 공시자료를 기반으로 한 분석 도구입니다. "
        "내부 자금계획, 개별 통제활동의 효과성, 내부 리스크 한도 등 비공개 정보는 분석 범위에서 제외합니다."
    )

# ---------------------------------------------------------
# 데이터 출처 안내
# ---------------------------------------------------------
st.divider()
with st.expander("데이터 기준 및 해석 유의사항"):
    st.write("- 실적 데이터: 키움증권 분기 실적보고서의 별도기준 수치")
    st.write("- 시장/영업 데이터: 키움증권 월간 IR 자료에서 확인 가능한 비교가능 구간")
    st.write("- 유동성·자본적정성: 키움증권 정기보고서의 지배회사 기준 재무건전성 지표")
    st.write("- 금액 단위가 서로 다른 원자료는 화면 목적에 맞게 억원·조원으로 환산")
    st.write("- 공개자료만으로 확인할 수 없는 내부 자금운용계획이나 내부회계 통제의 세부 효과성은 추정하지 않음")
