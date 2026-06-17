import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="서울 지하철 혼잡도 분석",
    page_icon="🚇",
    layout="wide"
)

# --------------------------
# 데이터 로드
# --------------------------

@st.cache_data
def load_data():

    file_path = Path(
        "서울교통공사_지하철혼잡도정보_20260331.csv"
    )

    df = pd.read_csv(
        file_path,
        encoding="cp949"
    )

    time_cols = df.columns[5:]

    for col in time_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df

df = load_data()

time_cols = df.columns[5:]

# --------------------------
# KPI
# --------------------------

st.title("🚇 서울 지하철 혼잡도 분석")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "역 수",
    df["출발역"].nunique()
)

c2.metric(
    "호선 수",
    df["호선"].nunique()
)

c3.metric(
    "시간대",
    len(time_cols)
)

c4.metric(
    "데이터 행 수",
    f"{len(df):,}"
)

st.divider()

# --------------------------
# TOP10
# --------------------------

station_mean = (
    df.groupby("출발역")[time_cols]
      .mean()
      .mean(axis=1)
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

station_mean.columns = [
    "출발역",
    "평균혼잡도"
]

fig = px.bar(
    station_mean,
    x="평균혼잡도",
    y="출발역",
    orientation="h",
    title="혼잡도 TOP10"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------
# 전체 평균 추세
# --------------------------

avg_time = df[time_cols].mean()

chart_df = pd.DataFrame({
    "시간": avg_time.index,
    "혼잡도": avg_time.values
})

fig2 = px.line(
    chart_df,
    x="시간",
    y="혼잡도",
    markers=True,
    title="서울 전체 평균 혼잡도"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)
