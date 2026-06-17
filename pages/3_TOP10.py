import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("🏆 TOP10 혼잡역")

csv_path = Path(__file__).parent.parent / "서울교통공사_지하철혼잡도정보_20260331.csv"

try:
    df = pd.read_csv(csv_path, encoding="cp949")
except Exception:
    df = pd.read_csv(csv_path, encoding="utf-8")

time_cols = list(df.columns[5:])

for col in time_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

selected_time = st.selectbox(
    "시간 선택",
    time_cols
)

rank_df = (
    df.groupby("출발역")[selected_time]
      .mean()
      .reset_index()
      .sort_values(selected_time, ascending=False)
      .head(10)
)

fig = px.bar(
    rank_df,
    x=selected_time,
    y="출발역",
    orientation="h",
    title=f"{selected_time} TOP10 혼잡역"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(rank_df, use_container_width=True)
