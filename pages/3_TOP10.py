import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("🏆 시간대별 TOP10 혼잡역")

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
text_auto=".1f",
title=f"{selected_time} 기준 TOP10 혼잡역"
)

fig.update_layout(
height=600,
yaxis={"categoryorder":"total ascending"}
)

st.plotly_chart(
fig,
use_container_width=True
)

st.dataframe(
rank_df,
use_container_width=True
)
