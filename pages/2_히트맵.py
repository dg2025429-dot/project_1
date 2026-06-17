import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/서울교통공사_지하철혼잡도정보_20260331.csv",
        encoding="cp949"
    )

df = load_data()

time_cols = df.columns[5:]

st.title("🔥 혼잡도 히트맵")

line = st.selectbox(
    "호선 선택",
    sorted(df["호선"].unique())
)

subset = df[
    (df["호선"]==line) &
    (df["요일구분"]=="평일")
]

heat_df = (
    subset.groupby("출발역")[time_cols]
    .mean()
)

fig = px.imshow(
    heat_df,
    aspect="auto",
    labels=dict(
        x="시간",
        y="역",
        color="혼잡도"
    )
)

fig.update_layout(height=900)

st.plotly_chart(
    fig,
    use_container_width=True
)
