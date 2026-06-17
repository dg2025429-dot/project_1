import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울 지하철 혼잡도 분석",
    page_icon="🚇",
    layout="wide"
)

# -------------------
# HEADER
# -------------------
st.title("🚇 서울 지하철 혼잡도 분석 대시보드")

st.markdown("""
서울교통공사 혼잡도 데이터를 활용하여

- 시간대별 혼잡도 조회
- 지도 기반 혼잡도 시각화
- 역별 비교 분석
- TOP10 혼잡역 분석
- AI 인사이트 제공

기능을 제공합니다.
""")

# -------------------
# SIDEBAR
# -------------------
st.sidebar.title("📌 서비스 메뉴")

st.sidebar.success("""
1. 혼잡도 조회
2. 혼잡도 지도
3. 히트맵
4. TOP10
5. 시간대 분석
6. 데이터 다운로드
""")

# -------------------
# KPI
# -------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "총 역 수",
        "286"
    )

with col2:
    st.metric(
        "분석 노선",
        "1~8호선"
    )

with col3:
    st.metric(
        "시간대",
        "39개"
    )

with col4:
    st.metric(
        "데이터 기준",
        "2026.03"
    )

st.divider()

# -------------------
# 서비스 카드
# -------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("🗺️ 지도 기반 혼잡도 분석")

    st.info("""
    서울 전체 역의 혼잡도를 지도에서 확인할 수 있습니다.

    • 원 크기 = 혼잡도
    • 원 색상 = 혼잡도 수준
    """)

with col2:

    st.subheader("📊 데이터 분석")

    st.info("""
    • 시간대별 추이

    • 출퇴근 비교

    • TOP10 혼잡역

    • AI 인사이트
    """)

st.divider()

# -------------------
# QUICK START
# -------------------
st.subheader("🚀 빠른 시작")

st.markdown("""
좌측 메뉴에서 원하는 기능을 선택하세요.

### 추천 순서

1. 혼잡도 지도
2. 시간대별 조회
3. TOP10 분석
4. 히트맵
5. 데이터 다운로드
""")

# -------------------
# AI INSIGHT
# -------------------
st.subheader("🤖 오늘의 인사이트")

st.success("""
평일 오전 출근시간(08:00~09:00)에는
2호선 및 주요 환승역에서 높은 혼잡도가 나타나는 경향이 있습니다.

'시간대 분석' 페이지에서 자세히 확인해보세요.
""")

# -------------------
# FOOTER
# -------------------
st.divider()

st.caption(
    "Data Source : 서울교통공사 지하철 혼잡도 정보"
)
