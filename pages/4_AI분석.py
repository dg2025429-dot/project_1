import streamlit as st
import pandas as pd

df = pd.read_csv(
    "data/서울교통공사_지하철혼잡도정보_20260331.csv",
    encoding="cp949"
)

time_cols = df.columns[5:]

st.title("🤖 AI 혼잡도 분석")

mean_time = df[time_cols].mean()

peak_time = mean_time.idxmax()

peak_station = (
    df.groupby("출발역")[time_cols]
    .mean()
    .mean(axis=1)
    .idxmax()
)

st.success(
    f"""
    📌 가장 붐비는 시간

    {peak_time}

    📌 평균적으로 가장 붐비는 역

    {peak_station}
    """
)

morning = [
    "7시00분",
    "7시30분",
    "8시00분",
    "8시30분"
]

evening = [
    "18시00분",
    "18시30분",
    "19시00분"
]

m_avg = df[morning].mean().mean()
e_avg = df[evening].mean().mean()

st.metric(
    "출근시간 평균 혼잡도",
    round(m_avg,1)
)

st.metric(
    "퇴근시간 평균 혼잡도",
    round(e_avg,1)
)
