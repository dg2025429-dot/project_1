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

st.title("🚉 역별 혼잡도 조회")

c1,c2,c3,c4 = st.columns(4)

weekday = c1.selectbox(
    "요일",
    sorted(df["요일구분"].unique())
)

line = c2.selectbox(
    "호선",
    sorted(df["호선"].unique())
)

station = c3.selectbox(
    "역",
    sorted(
        df[df["호선"]==line]["출발역"].unique()
    )
)

direction = c4.selectbox(
    "상하구분",
    ["상선","하선"]
)

filtered = df[
    (df["요일구분"]==weekday)&
    (df["호선"]==line)&
    (df["출발역"]==station)&
    (df["상하구분"]==direction)
]

row = filtered.iloc[0]

chart_df = pd.DataFrame({
    "시간":time_cols,
    "혼잡도":row[time_cols].values
})

fig = px.line(
    chart_df,
    x="시간",
    y="혼잡도",
    markers=True
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

max_idx = chart_df["혼잡도"].idxmax()

st.success(
    f"최대 혼잡 시간 : {chart_df.loc[max_idx,'시간']} "
    f"({chart_df.loc[max_idx,'혼잡도']:.1f})"
)
