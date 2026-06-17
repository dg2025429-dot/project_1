import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("🤖 AI 혼잡도 분석")

csv_file = Path(**file**).parent.parent / "서울교통공사_지하철혼잡도정보_20260331.csv"

try:
df = pd.read_csv(csv_file, encoding="cp949")
except:
df = pd.read_csv(csv_file, encoding="utf-8")

time_cols = df.columns[5:]

for col in time_cols:
df[col] = pd.to_numeric(df[col], errors="coerce")

# 전체 평균 혼잡도

avg_by_time = df[time_cols].mean()

peak_time = avg_by_time.idxmax()
peak_value = round(avg_by_time.max(), 1)

lowest_time = avg_by_time.idxmin()
lowest_value = round(avg_by_time.min(), 1)

st.subheader("📊 혼잡도 핵심 분석")

col1, col2 = st.columns(2)

with col1:
st.metric(
"가장 붐비는 시간",
peak_time,
peak_value
)

with col2:
st.metric(
"가장 한산한 시간",
lowest_time,
lowest_value
)

# 시간대 그래프

chart_df = pd.DataFrame({
"시간": avg_by_time.index,
"평균혼잡도": avg_by_time.values
})

fig = px.line(
chart_df,
x="시간",
y="평균혼잡도",
markers=True,
title="서울 지하철 평균 혼잡도 추이"
)

st.plotly_chart(
fig,
use_container_width=True
)

# 역별 평균

station_df = (
df.groupby("출발역")[time_cols]
.mean()
.mean(axis=1)
.reset_index()
)

station_df.columns = [
"출발역",
"평균혼잡도"
]

top_station = station_df.sort_values(
"평균혼잡도",
ascending=False
).iloc[0]

st.subheader("🏆 가장 혼잡한 역")

st.success(
f"{top_station['출발역']} (평균 혼잡도 {top_station['평균혼잡도']:.1f})"
)

# TOP10 역

top10 = station_df.sort_values(
"평균혼잡도",
ascending=False
).head(10)

fig2 = px.bar(
top10,
x="평균혼잡도",
y="출발역",
orientation="h",
title="평균 혼잡도 TOP10 역"
)

st.plotly_chart(
fig2,
use_container_width=True
)

# AI 분석 문장

st.subheader("💡 AI 인사이트")

st.info(
f"""
• 가장 붐비는 시간은 {peak_time} 입니다.

• 가장 한산한 시간은 {lowest_time} 입니다.

• 가장 혼잡한 역은 {top_station['출발역']} 입니다.

• 출퇴근 시간대에 이용객이 집중되는 경향을 확인할 수 있습니다.
"""
)
