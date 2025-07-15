# democracy_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="민주주의 지수 분석",
    page_icon="🗳️",
    layout="wide"
)

# 색상 매핑
color_map = {
    'Full Democracy': '#2E8B57',
    'Flawed Democracy': '#FFD700',
    'Hybrid Regime': '#FF8C00',
    'Authoritarian': '#DC143C'
}

# 데이터 불러오기
@st.cache_data
def load_data():
    data = {
        'country': ['Norway', 'South Korea', 'India', 'Brazil', 'Russia', 'China', 'Iran', 'North Korea'],
        'democracy_index': [9.81, 8.09, 7.04, 6.86, 2.28, 2.21, 2.20, 1.08],
        'latitude': [60.472, 35.907, 20.593, -14.235, 61.524, 35.861, 32.427, 40.339],
        'longitude': [8.468, 127.766, 78.962, -51.925, 105.318, 104.195, 53.688, 127.510]
    }

    df = pd.DataFrame(data)

    # 민주주의 유형 분류 함수
    def classify_democracy(score):
        if score >= 8.0:
            return 'Full Democracy'
        elif score >= 6.0:
            return 'Flawed Democracy'
        elif score >= 4.0:
            return 'Hybrid Regime'
        else:
            return 'Authoritarian'

    df['democracy_type'] = df['democracy_index'].apply(classify_democracy)

    return df

# 메인 함수
def main():
    st.title("🗳️ 민주주의 지수 분석 대시보드")

    df = load_data()

    # 필터
    st.sidebar.header("필터")
    selected_types = st.sidebar.multiselect(
        "민주주의 유형 선택",
        options=df['democracy_type'].unique(),
        default=df['democracy_type'].unique()
    )

    filtered_df = df[df['democracy_type'].isin(selected_types)]

    st.subheader("🌍 국가별 민주주의 지수 지도")

    fig = px.scatter_geo(
        filtered_df,
        lat='latitude',
        lon='longitude',
        color='democracy_type',
        color_discrete_map=color_map,
        hover_name='country',
        hover_data=['democracy_index'],
        size='democracy_index',
        title="민주주의 지수 세계 지도"
    )

    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📏 거리 기반 비교")

    reference_country = st.selectbox("기준 국가 선택", df['country'])

    ref_row = df[df['country'] == reference_country].iloc[0]

    # 거리 계산
    def distance(row):
        return ((row['latitude'] - ref_row['latitude'])**2 + (row['longitude'] - ref_row['longitude'])**2)**0.5

    df['distance'] = df.apply(distance, axis=1)
    nearby = df[df['country'] != reference_country].nsmallest(5, 'distance')

    st.markdown(f"**{reference_country}와 가장 가까운 5개국:**")
    for _, row in nearby.iterrows():
        st.write(f"• {row['country']} (지수: {row['democracy_index']})")

    fig2 = px.scatter_geo(
        pd.concat([df[df['country'] == reference_country], nearby]),
        lat='latitude',
        lon='longitude',
        color='democracy_type',
        size='democracy_index',
