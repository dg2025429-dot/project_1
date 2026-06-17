import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="서울 지하철 혼잡도 분석",
    page_icon="🚇",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/서울교통공사_지하철혼잡도정보_20260331.csv",
        encoding="cp949"
    )
    return df

df = load_data()

time_cols = df.columns[5:]

st.title("🚇 서울 지하철 혼잡도 분석 플랫폼")

# KPI
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("역 수", df["출발역"].nunique())

with col2:
    st.metric("노선 수", df["호선"].nunique())

with col3:
    st.metric("시간대", len(time_cols))

with col4:
    st.metric("총 데이터", f"{len(df):,}")

st.divider()

# 혼잡도 TOP10
st.subheader("🔥 평균 혼잡도 TOP10 역")

avg_df = (
    df.groupby("출발역")[time_cols]
    .mean()
    .mean(axis=1)
    .reset_index()
)

avg_df.columns = ["출발역","평균혼잡도"]
avg_df = avg_df.sort_values(
    "평균혼잡도",
    ascending=False
).head(10)

fig = px.bar(
    avg_df,
    x="평균혼잡도",
    y="출발역",
    orientation="h",
    text_auto=".1f",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info("좌측 메뉴에서 상세 분석을 선택하세요.")
