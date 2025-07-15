# democracy_analysis.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.patches import Rectangle
import io

# 페이지 설정
st.set_page_config(
    page_title="민주주의 지수 분석",
    page_icon="🗳️",
    layout="wide"
)

# 데이터 로드 함수
@st.cache_data
def load_data():
    democracy_data = {
        'country': [...],  # 생략: 기존 데이터 그대로 유지
        'democracy_index': [...],
        'latitude': [...],
        'longitude': [...]
    }

    df = pd.DataFrame(democracy_data)

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

    def classify_region(lat):
        if lat > 50:
            return 'Northern Europe/North America'
        elif lat > 25:
            return 'Europe/North America/Asia'
        elif lat > -25:
            return 'Africa/Asia/Central America'
        else:
            return 'Southern Africa/Oceania'

    df['region'] = df['latitude'].apply(classify_region)
    return df

color_map = {
    'Full Democracy': '#2E8B57',
    'Flawed Democracy': '#FFD700',
    'Hybrid Regime': '#FF8C00',
    'Authoritarian': '#DC143C'
}

def main():
    st.title("🗳️ 민주주의 지수 지리적 분석")
    st.markdown("---")
    df = load_data()
    st.sidebar.header("🔧 설정")
    page = st.sidebar.selectbox("분석 페이지 선택", [...])  # 생략 가능
    # 페이지 라우팅 생략

    # 필터링 및 비교 섹션 예시
    st.subheader("🔍 필터링 및 비교")
    col1, col2 = st.columns(2)

    with col1:
        selected_types = st.multiselect(
            "민주주의 유형 선택",
            df['democracy_type'].unique(),
            default=df['democracy_type'].unique()
        )

    with col2:
        min_score, max_score = st.slider(
            "민주주의 지수 범위",
            min_value=float(df['democracy_index'].min()),
            max_value=float(df['democracy_index'].max()),
            value=(float(df['democracy_index'].min()), float(df['democracy_index'].max()))
        )

    filtered_df = df[
        (df['democracy_type'].isin(selected_types)) &
        (df['democracy_index'] >= min_score) &
        (df['democracy_index'] <= max_score)
    ]

    if not filtered_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig_all = px.scatter_geo(
                df,
                lat='latitude',
                lon='longitude',
                hover_name='country',
                hover_data=['democracy_index', 'democracy_type'],
                color='democracy_type',
                color_discrete_map=color_map,
                size='democracy_index',
                size_max=15,
                title="전체 데이터"
            )
            fig_all.update_layout(height=400)
            st.plotly_chart(fig_all, use_container_width=True)

        with col2:
            fig_filtered = px.scatter_geo(
                filtered_df,
                lat='latitude',
                lon='longitude',
                hover_name='country',
                hover_data=['democracy_index', 'democracy_type'],
                color='democracy_type',
                color_discrete_map=color_map,
                size='democracy_index',
                size_max=15,
                title=f"필터된 데이터 ({len(filtered_df)}개국)"
            )
            fig_filtered.update_layout(height=400)
            st.plotly_chart(fig_filtered, use_container_width=True)
    else:
        st.warning("선택한 조건에 맞는 국가가 없습니다.")

    # 거리 기반 분석
    st.subheader("📏 거리 기반 분석")
    reference_country = st.selectbox("기준 국가 선택", df['country'].tolist())

    if reference_country:
        ref_row = df[df['country'] == reference_country].iloc[0]

        def calculate_distance(row):
            return ((row['latitude'] - ref_row['latitude'])**2 + (row['longitude'] - ref_row['longitude'])**2)**0.5

        df['distance_from_ref'] = df.apply(calculate_distance, axis=1)
        nearest_countries = df[df['country'] != reference_country].nsmallest(5, 'distance_from_ref')

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**{reference_country}와 가장 가까운 5개국:**")
            for _, row in nearest_countries.iterrows():
                st.write(f"• {row['country']} (지수: {row['democracy_index']})")

        with col2:
            nearby_df = pd.concat([df[df['country'] == reference_country], nearest_countries])
            fig_nearby = px.scatter_geo(
                nearby_df,
                lat='latitude',
                lon='longitude',
                hover_name='country',
                hover_data=['democracy_index', 'democracy_type'],
                color='democracy_type',
                color_discrete_map=color_map,
                size='democracy_index',
                size_max=20,
                title=f"{reference_country} 주변 국가들"
            )

            fig_nearby.add_trace(
                go.Scattergeo(
                    lon=[ref_row['longitude']],
                    lat=[ref_row['latitude']],
                    marker=dict(size=25, color='red', symbol='star'),
                    name=f"{reference_country} (기준)",
                    hoverinfo='text',
                    hovertext=f"{reference_country}<br>민주주의 지수: {ref_row['democracy_index']}"
                )
            )

            fig_nearby.update_layout(height=400)
            st.plotly_chart(fig_nearby, use_container_width=True)

if __name__ == "__main__":
    main()
