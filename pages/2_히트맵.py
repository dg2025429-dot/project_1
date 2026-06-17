import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv(
    "서울교통공사_지하철혼잡도정보_20260331.csv",
    encoding="cp949"
)

time_cols = df.columns[5:]

for col in time_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

st.title("🔥 혼잡도 히트맵")

line = st.selectbox(
    "호선 선택",
    sorted(df["호선"].unique())
)

heat_df = (
    df[df["호선"]==line]
    .groupby("출발역")[time_cols]
    .mean()
)

fig = px.imshow(
    heat_df,
    aspect="auto",
    color_continuous_scale="Reds"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
