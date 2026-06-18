import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(layout="wide")

# ------------------
# 데이터 로드
# ------------------
@st.cache_data
def load_data():

    csv_path = (
        Path(__file__).parent.parent
        / "서울교통공사_지하철혼잡도정보_20260331.csv"
    )

    df = pd.read_csv(
        csv_path,
        encoding="cp949"
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

# ------------------
# 필터 영역
# ------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    weekday = st.selectbox(
        "요일",
        sorted(df["요일구분"].unique())
    )

with col2:
    line = st.selectbox(
        "호선",
        sorted(df["호선"].unique())
    )

with col3:

    station_list = sorted(
        df[df["호선"] == line]["출발역"].unique()
    )

    station = st.selectbox(
        "역 선택",
        station_list
    )

with col4:
    direction = st.selectbox(
        "상하구분",
        sorted(df["상하구분"].unique())
    )

# ------------------
# 데이터 필터링
# ------------------

filtered = df[
    (df["요일구분"] == weekday)
    & (df["호선"] == line)
    & (df["출발역"] == station)
    & (df["상하구분"] == direction)
]

if filtered.empty:

    st.error("선택한 조건의 데이터가 없습니다.")
    st.stop()

row = filtered.iloc[0]

chart_df = pd.DataFrame(
    {
        "시간": time_cols,
        "혼잡도": row[time_cols].values
    }
)

# ------------------
# KPI
# ------------------

max_idx = chart_df["혼잡도"].idxmax()
min_idx = chart_df["혼잡도"].idxmin()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "최대 혼잡도",
        f"{chart_df.loc[max_idx,'혼잡도']:.1f}"
    )

with col2:
    st.metric(
        "최대 혼잡 시간",
        chart_df.loc[max_idx,"시간"]
    )

with col3:
    st.metric(
        "평균 혼잡도",
        f"{chart_df['혼잡도'].mean():.1f}"
    )

# ------------------
# 그래프
# ------------------

fig = px.line(
    chart_df,
    x="시간",
    y="혼잡도",
    markers=True,
    title=f"{line} {station} ({direction}) 시간대별 혼잡도"
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------
# 원본 데이터
# ------------------

with st.expander("데이터 보기"):
    st.dataframe(
        chart_df,
        use_container_width=True
    )
