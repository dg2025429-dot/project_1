import streamlit as st
import pandas as pd
from pathlib import Path

st.title("🤖 AI 혼잡도 분석")

@st.cache_data
def load_data():

```
csv_path = Path(__file__).parent.parent / "서울교통공사_지하철혼잡도정보_20260331.csv"

try:
    df = pd.read_csv(
        csv_path,
        encoding="cp949"
    )
except:
    df = pd.read_csv(
        csv_path,
        encoding="utf-8"
    )

time_cols = df.columns[5:]

for col in time_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

return df
```

df = load_data()

time_cols = df.columns[5:]

# 전체 평균 시간대

mean_time = df[time_cols].mean()

peak_time = mean_time.idxmax()
peak_value = round(mean_time.max(), 1)

# 가장 혼잡한 역

station_mean = (
df.groupby("출발역")[time_cols]
.mean()
.mean(axis=1)
)

peak_station = station_mean.idxmax()
peak_station_value = round(station_mean.max(), 1)

st.subheader("📊 핵심 분석 결과")

col1, col2 = st.columns(2)

with col1:
st.metric(
"가장 붐비는 시간",
peak_time,
peak_value
)

with col2:
st.metric(
"가장 붐비는 역",
peak_station,
peak_station_value
)

# 출근시간

morning_cols = [
c for c in time_cols
if "7시" in c or "8시" in c
]

# 퇴근시간

evening_cols = [
c for c in time_cols
if "18시" in c or "19시" in c
]

morning_avg = round(
df[morning_cols].mean().mean(),
1
)

evening_avg = round(
df[evening_cols].mean().mean(),
1
)

st.subheader("🚇 출퇴근 혼잡도 비교")

c1, c2 = st.columns(2)

c1.metric(
"출근시간 평균",
morning_avg
)

c2.metric(
"퇴근시간 평균",
evening_avg
)

if morning_avg > evening_avg:
st.success(
"서울 지하철은 출근시간 혼잡도가 더 높습니다."
)
else:
st.success(
"서울 지하철은 퇴근시간 혼잡도가 더 높습니다."
)

st.subheader("💡 AI 인사이트")

st.info(
f"""
• 전체 평균 기준 가장 붐비는 시간은 {peak_time}입니다.

```
• 가장 혼잡한 역은 {peak_station}입니다.

• 출근시간 평균 혼잡도는 {morning_avg}입니다.

• 퇴근시간 평균 혼잡도는 {evening_avg}입니다.

• 해당 역과 시간대를 중심으로 추가적인 운영 정책 수립이 가능합니다.
"""
```

)
