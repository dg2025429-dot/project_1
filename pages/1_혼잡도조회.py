import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="역별 혼잡도 분석",
    layout="wide"
)

# -----------------------------
# 데이터 로드
# -----------------------------
@st.cache_data
def load_data():

    csv_path = (
        Path(__file__).parent.parent
        / "서울교통공사_지하철혼잡도정보_20260331.csv"
    )

    try:
        df = pd.read_csv(
            csv_path,
            encoding="cp949"
        )
    except:
        df = pd.read_csv(
            csv_path,
            encoding="utf-8"
        )

    time_cols = list(df.columns[5:])

    for col in time_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df, time_cols


df, time_cols = load_data()

st.title("🚉 역별 혼잡도 분석")

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("조회 조건")

weekday = st.sidebar.selectbox(
    "요일",
    sorted(df["요일구분"].unique())
)

line = st.sidebar.selectbox(
    "호선",
    sorted(df["호선"].unique())
)

line_df = df[df["호선"] == line]

station = st.sidebar.selectbox(
    "역",
    sorted(line_df["출발역"].unique())
)

direction = st.sidebar.selectbox(
    "상하구분",
    sorted(
        line_df["상하구분"].unique()
    )
)

# -----------------------------
# 필터
# -----------------------------
filtered = df[
    (df["요일구분"] == weekday)
    & (df["호선"] == line)
    & (df["출발역"] == station)
    & (df["상하구분"] == direction)
]

if filtered.empty:
    st.error("조건에 맞는 데이터가 없습니다.")
    st.stop()

# -----------------------------
# 선택 데이터 표시
# -----------------------------
st.success(
    f"{weekday} | {line} | {station} | {direction}"
)

row = filtered.iloc[0]

chart_df = pd.DataFrame({
    "시간": time_cols,
    "혼잡도": row[time_cols].values
})

# -----------------------------
# KPI
# -----------------------------
col1, col2, col3 = st.columns(3)

peak_idx = chart_df["혼잡도"].idxmax()

col1.metric(
    "최대 혼잡도",
    round(
        chart_df["혼잡도"].max(),
        1
    )
)

col2.metric(
    "최대 혼잡 시간",
    chart_df.loc[
        peak_idx,
        "시간"
    ]
)

col3.metric(
    "평균 혼잡도",
    round(
        chart_df["혼잡도"].mean(),
        1
    )
)

# -----------------------------
# 라인 그래프
# -----------------------------
fig = px.line(
    chart_df,
    x="시간",
    y="혼잡도",
    markers=True,
    title=f"{line} {station} 시간대별 혼잡도"
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# 막대 그래프
# -----------------------------
fig2 = px.bar(
    chart_df,
    x="시간",
    y="혼잡도",
    title="시간대별 혼잡도 막대그래프"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------
# 데이터 확인
# -----------------------------
with st.expander("선택된 원본 데이터"):

    st.dataframe(
        filtered[
            [
                "요일구분",
                "호선",
                "출발역",
                "상하구분"
            ]
        ],
        use_container_width=True
    )

with st.expander("시간대별 데이터"):

    st.dataframe(
        chart_df,
        use_container_width=True
    )
