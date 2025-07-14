import streamlit as st
import plotly.graph_objects as go

# 세계 인구 상위 10개국 데이터 (2024 기준, 단위: 백만)
countries = [
    "인도", "중국", "미국", "인도네시아", "파키스탄",
    "나이지리아", "브라질", "방글라데시", "러시아", "멕시코"
]
populations = [1420, 1410, 339, 277, 240, 223, 216, 172, 144, 129]

# Plotly 막대 그래프 생성
fig = go.Figure(
    data=[
        go.Bar(
            x=countries,
            y=populations,
            marker_color='skyblue'
        )
    ]
)

# 레이아웃 설정
fig.update_layout(
    title="🌍 세계 인구 순위 TOP 10 (2024)",
    xaxis_title="국가",
    yaxis_title="인구 (백만 명)",
    template="simple_white"
)

# Streamlit 앱 제목 및 출력
st.title("🌏 세계 인구 TOP 10 시각화 (Plotly)")
st.plotly_chart(fig, use_container_width=True)
