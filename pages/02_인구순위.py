import streamlit as st
import plotly.graph_objects as go

# 2024년 기준 세계 인구 상위 10개국 (단위: 백만 명)
countries = [
    "인도", "중국", "미국", "인도네시아", "파키스탄",
    "나이지리아", "브라질", "방글라데시", "러시아", "멕시코"
]
populations = [1420, 1410, 339, 277, 240, 223, 216, 172, 144, 129]

# Plotly 그래프
fig = go.Figure(
    data=[
        go.Bar(
            x=countries,
            y=populations,
            marker_color='lightseagreen'
        )
    ]
)

fig.update_layout(
    title="🌍 2024년 세계 인구 TOP 10",
    xaxis_title="국가",
    yaxis_title="인구 (백만 명)",
    template="plotly_white"
)

# Streamlit 출력
st.title("🌏 세계 인구 순위 (Plotly 시각화)")
st.plotly_chart(fig, use_container_width=True)
