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
    "해외주식 일평균 약정(십억달러)": [1.9, 1.3, 1.4, 1.7, 2.1],
    "해외주식 거래대금(십억달러)": [228.3, 212.0, 218.4, 280.2, 271.0],
})

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

    c1, c2 = st.columns(2)
    with c1:
        fig2 = px.line(market, x="분기", y="해외주식 일평균 약정(십억달러)", markers=True, title="해외주식 일평균 약정")
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        fig3 = px.line(market, x="분기", y="해외주식 거래대금(십억달러)", markers=True, title="해외주식 거래대금")
        st.plotly_chart(fig3, use_container_width=True)

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

        fig = px.bar(
            bridge,
            x="항목",
            y="영업이익 방향 기여",
            title=f"{selected} 실적 변동 요인 ({compare_mode})",
        )
        fig.update_layout(yaxis_title="영업이익 방향 기준 증감(억원)", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

        top_pos = bridge.iloc[0]
        top_neg = bridge.iloc[-1]
        st.success(f"가장 큰 긍정 요인: {top_pos['항목']} ({top_pos['영업이익 방향 기여']:+,.0f}억원)")
        st.warning(f"가장 큰 부담 요인: {top_neg['항목']} ({top_neg['영업이익 방향 기여']:+,.0f}억원)")

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
    h1, h2 = st.columns([4,1])
    with h1:
        st.markdown('<div class="question-box"><b>질문</b><br>영업 과정에서 부담하는 위험을 감당할 충분한 자본여력을 확보하고 있는가?</div>', unsafe_allow_html=True)
    with h2:
        with st.popover("순자본비율이란?"):
            st.markdown("**순자본비율 계산식**")
            st.code("순자본비율 = (영업용순자본 - 총위험액) ÷ 필요유지자기자본 × 100")
            st.caption("영업용순자본에서 총위험액을 차감한 잉여자본을 필요유지자기자본과 비교한 비율입니다.")

    latest_c = capital.iloc[-1]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("영업용순자본", f"{latest_c['영업용순자본']/1_000_000:.2f}조원")
    c2.metric("총위험액", f"{latest_c['총위험액']/1_000_000:.2f}조원")
    c3.metric("잉여자본", f"{latest_c['잉여자본']/1_000_000:.2f}조원")
    c4.metric("순자본비율", f"{latest_c['순자본비율(%)']:,.2f}%")

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
    st.success(
        "최근 키움증권은 위탁매매와 운용손익을 중심으로 수익성이 크게 개선되었습니다. "
        "동시에 공개자료상 단기 유동성자산이 유동성부채를 상회하고 있으며, "
        "순자본비율도 최근 비교시점에서 상승했습니다. 따라서 실적 성장의 원인과 함께 "
        "유동성·자본여력을 연계해 지속가능성을 점검하는 것이 핵심입니다."
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
