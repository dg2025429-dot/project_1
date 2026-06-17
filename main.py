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
return pd.read_csv(
"data/서울교통공사_지하철혼잡도정보_20260331.csv",
encoding="cp949"
)

df = load_data()

st.title("🚇 서울 지하철 혼잡도 분석 대시보드")

st.markdown("""
서울교통공사 혼잡도 데이터를 기반으로
시간대별·역별 혼잡도를 분석할 수 있습니다.
""")

col1, col2, col3 = st.columns(3)

time_cols = df.columns[5:]

avg_crowd = round(df[time_cols].mean().mean(), 1)

station_mean = (
df.groupby("출발역")[time_cols]
.mean()
.mean(axis=1)
)

most_station = station_mean.idxmax()
least_station = station_mean.idxmin()

with col1:
st.metric("평균 혼잡도", avg_crowd)

with col2:
st.metric("가장 혼잡한 역", most_station)

with col3:
st.metric("가장 여유로운 역", least_station)

st.divider()

st.subheader("호선별 평균 혼잡도")

line_df = (
df.groupby("호선")[time_cols]
.mean()
.mean(axis=1)
.reset_index()
)

line_df.columns = ["호선", "평균혼잡도"]

fig = px.bar(
line_df,
x="호선",
y="평균혼잡도",
text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

st.info(
"왼쪽 사이드바에서 상세 분석 페이지를 선택하세요."
)
