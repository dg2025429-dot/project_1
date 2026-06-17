import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():

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

    return df

df = load_data()

time_cols = df.columns[5:]

st.title("🚉 역별 혼잡도 분석")

weekday = st.selectbox(
    "요일",
    sorted(df["요일구분"].unique())
)

line = st.selectbox(
    "호선",
    sorted(df["호선"].unique())
)

stations = sorted(
    df[df["호선"]==line]["출발역"].unique()
)

station = st.selectbox(
    "역 선택",
    stations
)

direction = st.selectbox(
    "상하구분",
    sorted(df["상하구분"].unique())
)

filtered = df[
    (df["요일구분"]==weekday)&
    (df["호선"]==line)&
    (df["출발역"]==station)&
    (df["상하구분"]==direction)
]

if len(filtered)==0:

    st.warning(
        "선택한 조건의 데이터가 없습니다."
    )

else:

    row = filtered.iloc[0]

    chart_df = pd.DataFrame({
        "시간": time_cols,
        "혼잡도": row[time_cols].values
    })

    fig = px.line(
        chart_df,
        x="시간",
        y="혼잡도",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    max_time = chart_df.loc[
        chart_df["혼잡도"].idxmax()
    ]

    min_time = chart_df.loc[
        chart_df["혼잡도"].idxmin()
    ]

    c1,c2 = st.columns(2)

    c1.metric(
        "최대 혼잡 시간",
        max_time["시간"],
        round(max_time["혼잡도"],1)
    )

    c2.metric(
        "최소 혼잡 시간",
        min_time["시간"],
        round(min_time["혼잡도"],1)
    )
