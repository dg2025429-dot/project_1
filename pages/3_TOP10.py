import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv(
    "data/서울교통공사_지하철혼잡도정보_20260331.csv",
    encoding="cp949"
)

time_cols = df.columns[5:]

st.title("🏆 시간대별 TOP10 혼잡역")

selected_time = st.selectbox(
    "시간 선택",
    time_cols
)

rank_df = (
    df.groupby("출발역")[selected_time]
    .mean()
    .reset_index()
)

rank_df = rank_df.sort_values(
    selected_time,
    ascending=False
).head(10)

fig = px.bar(
    rank_df,
    x=selected_time,
    y="출발역",
    orientation="h",
    text_auto=".1f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
